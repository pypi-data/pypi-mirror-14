import copy
import logging
from time import sleep
from celery import shared_task
from notification.models import TaskHistory
from simple_audit.models import AuditRequest
from dbaas_aclapi.acl_base_client import get_acl_client
from dbaas_cloudstack.models import DatabaseInfraAttr
from dbaas_aclapi.models import (ERROR, CREATED, DatabaseBind,
                                 DatabaseInfraInstanceBind)


logging.basicConfig()
LOG = logging.getLogger("AclTask")
LOG.setLevel(logging.DEBUG)

ACL_API_EXCEPTION = Exception('ACL API error, please check the logs!')
ACL_API_JOB_MISSING_EXCEPTION = Exception("The AclApi is not working properly: ['job'] key is missing on response")


@shared_task(bind=True)
def bind_address_on_database(self, database_bind, user=None):
    action = "permit"
    user = get_user(self.request, user, action)

    AuditRequest.new_request("create_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.databaseinfra

    try:
        acl_environment, acl_vlan = get_bind_env_and_vlan(database_bind)

        data, default_options = build_data_default_options_dict(
            action, database_bind.bind_address, database.name,
            database.environment.name)

        instances = databaseinfra.instances.all()
        port = instances[0].port

        task_history.update_details(
            persist=True, details="Creating binds...")

        for instance in instances:
            custom_options = copy.deepcopy(default_options)
            custom_options['source'] = database_bind.bind_address
            custom_options['destination'] = instance.address + '/32'
            custom_options['l4-options']['dest-port-start'] = instance.port
            data['rules'].append(custom_options)

            LOG.debug("Creating bind for instance: {}".format(instance))

            instance_bind = DatabaseInfraInstanceBind(
                instance=instance.address, databaseinfra=databaseinfra,
                bind_address=database_bind.bind_address, instance_port=instance.port)
            instance_bind.save()

            LOG.debug("InstanceBind: {}".format(instance_bind))

        LOG.debug("Instance binds created!")

        for instance in DatabaseInfraAttr.objects.filter(databaseinfra=databaseinfra):
            custom_options = copy.deepcopy(default_options)
            custom_options['source'] = database_bind.bind_address
            custom_options['destination'] = instance.ip + '/32'
            custom_options['l4-options']['dest-port-start'] = port
            data['rules'].append(custom_options)

            LOG.debug("Creating bind for instance: {}".format(instance))

            instance_bind = DatabaseInfraInstanceBind(
                instance=instance.ip, databaseinfra=databaseinfra,
                bind_address=database_bind.bind_address, instance_port=port)
            instance_bind.save()

            LOG.debug("DatabaseInraAttrInstanceBind: {}".format(instance_bind))

        acl_client = get_acl_client(database.environment)
        response = acl_client.grant_acl_for(
            environment=acl_environment, vlan=acl_vlan, payload=data)

        if 'job' in response:
            if monitor_acl_job(job_id=response['job'], database_bind=database_bind):
                DatabaseBind.objects.filter(
                    id=database_bind.id).update(bind_status=CREATED)

                DatabaseInfraInstanceBind.objects.filter(
                    databaseinfra=database.databaseinfra, bind_address=database_bind.bind_address
                ).update(bind_status=CREATED)

                task_history.update_status_for(
                    TaskHistory.STATUS_SUCCESS, details='Bind succesfully created')

                return True
        else:
            raise ACL_API_JOB_MISSING_EXCEPTION

    except Exception as e:
        LOG.info("Database bind ERROR: {}".format(e))
        task_history.update_status_for(TaskHistory.STATUS_ERROR,
                                       details='Bind could not be created')

        DatabaseBind.objects.filter(
            id=database_bind.id).update(bind_status=ERROR)

        DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=databaseinfra, bind_address=database_bind.bind_address,
        ).update(bind_status=ERROR)

        return False
    finally:
        AuditRequest.cleanup_request()


@shared_task(bind=True)
def unbind_address_on_database(self, database_bind, user=None):
    action = "deny"
    user = get_user(self.request, user, action)

    AuditRequest.new_request("destroy_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.infra

    try:
        acl_environment, acl_vlan = get_bind_env_and_vlan(database_bind)

        data, default_options = build_data_default_options_dict(
            action, database_bind.bind_address, database.name,
            database.environment.name)

        infra_instances_binds = DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=databaseinfra,
            bind_address=database_bind.bind_address)

        task_history.update_details(
            persist=True, details="Removing binds...")

        for infra_instance_bind in infra_instances_binds:
            custom_options = copy.deepcopy(default_options)
            custom_options['source'] = database_bind.bind_address
            custom_options[
                'destination'] = infra_instance_bind.instance + '/32'
            custom_options[
                'l4-options']['dest-port-start'] = infra_instance_bind.instance_port
            data['rules'].append(custom_options)

        acl_client = get_acl_client(database.environment)

        response = acl_client.revoke_acl_for(
            environment=acl_environment, vlan=acl_vlan, payload=data)

        if 'job' in response:
            if monitor_acl_job(job_id=response['job'], database_bind=database_bind):
                infra_instances_binds.delete()
                database_bind.delete()

                task_history.update_status_for(TaskHistory.STATUS_SUCCESS,
                                               details='Bind succesfully destroyed')
                return True

        else:
            raise ACL_API_JOB_MISSING_EXCEPTION

    except Exception as e:
        LOG.info("Database unbind ERROR: {}".format(e))
        task_history.update_status_for(TaskHistory.STATUS_ERROR,
                                       details='Bind could not be removed')
        return False
    finally:
        AuditRequest.cleanup_request()


def monitor_acl_job(job_id, database_bind, retries=100, interval=10):
    database = database_bind.database
    LOG.debug("Monitoring job_id: {} for bind_address: {}".format(
        job_id, database_bind))
    acl_client = get_acl_client(database.environment)

    for attempt in range(retries):
        if job_has_finished(acl_client, job_id):
            return True

        if attempt == retries - 1:
            raise Exception("Maximum number of monitoring attempts.")

        LOG.info("Wating {} seconds to try again...".format(interval))
        sleep(interval)


def job_has_finished(acl_client, job_id):
    exception = Exception("AclAPI job {} execution failed!".format(job_id))
    response = acl_client.get_job(job_id=job_id)
    if 'jobs' in response:
        status = response["jobs"]["status"]
        if status == "PENDING":
            response = acl_client.run_job(job_id=job_id)
            if response["result"] == "success":
                return True
        elif status == "SUCCESS":
            return True
        elif status == "RUNNING":
            pass
        else:
            raise exception
    else:
        raise exception


def replicate_acl_for(database, old_ip, new_ip):
    acl_client = get_acl_client(database.environment)
    acls = acl_client.search_acl_for(destination=old_ip)
    if 'envs' not in acls:
        return
    for environment in acls['envs']:
        if 'vlans' not in environment:
            continue
        for vlan in environment['vlans']:
            if 'rules' not in vlan:
                continue
            for rule in vlan['rules']:
                if not copy_acl_rule(rule, new_ip, acl_client):
                    raise ACL_API_EXCEPTION


def destroy_acl_for(database, ip):
    acl_client = get_acl_client(database.environment)
    acls = acl_client.search_acl_for(destination=ip)
    if 'envs' not in acls:
        return
    for environment in acls['envs']:
        if 'vlans' not in environment:
            continue
        for vlan in environment['vlans']:
            if 'rules' not in vlan:
                continue
            for rule in vlan['rules']:
                if not destroy_acl_rule(rule, acl_client):
                    raise ACL_API_EXCEPTION


def destroy_acl_rule(rule, acl_client):
    acl_id = rule['id']
    acl_environment, vlan = rule['source'].split('/')
    response = acl_client.delete_acl(acl_environment, vlan, acl_id)

    if 'jobs' not in response:
        return False

    return True


def copy_acl_rule(rule, new_ip, acl_client):
    data = {"kind": "object#acl", "rules": []}

    new_rule = copy.deepcopy(rule)
    new_rule['destination'] = '{}/32'.format(new_ip)
    data['rules'].append(new_rule)

    acl_environment, vlan = new_rule['source'].split('/')
    response = acl_client.grant_acl_for(environment=acl_environment,
                                        vlan=vlan, payload=data)
    if 'jobs' not in response:
        return False

    return True


def build_data_default_options_dict(action, bind_address, database_name,
                                    database_environment):

    description = "{} {} access for database {} in {}".format(
        action, bind_address, database_name, database_environment)

    data = {"kind": "object#acl", "rules": []},
    dafault_options = {"protocol": "tcp",
                       "source": "",
                       "destination": "",
                       "description": description,
                       "action": action,
                       "l4-options": {"dest-port-start": "",
                                      "dest-port-op": "eq"}
                       }
    LOG.info("Default options: {}".format(dafault_options))
    return data, dafault_options


def register_task(request, user):
    LOG.info("id: {} | task: {} | kwargs: {} | args: {}".format(request.id,
             request.task,
             request.kwargs,
             str(request.args)))
    task_history = TaskHistory.register(request=request, user=user,
                                        worker_name=get_worker_name())
    task_history.update_details(persist=True, details="Loading Process...")

    return task_history


def get_user(request, user, action):
    if not user:
        user = request.args[-1]

    LOG.info("User: {}, action: {}".format(user, action))
    return user


def get_bind_env_and_vlan(database_bind):
    return database_bind.bind_address.split('/')


def get_worker_name():
    from billiard import current_process
    p = current_process()
    return p.initargs[1].split('@')[1]
