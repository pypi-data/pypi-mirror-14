# -*- coding: utf-8 -*-
import copy
import logging
from celery import shared_task
from notification.models import TaskHistory
from simple_audit.models import AuditRequest
from dbaas_aclapi.helpers import (get_user, bind_address, unbind_address)
from dbaas_aclapi.acl_base_client import get_acl_client
from dbaas_aclapi.models import (ERROR, DatabaseBind, DatabaseInfraInstanceBind)
from dbaas_aclapi.exceptions import ACL_API_EXCEPTION


logging.basicConfig()
LOG = logging.getLogger("AclTask")
LOG.setLevel(logging.DEBUG)


@shared_task(bind=True)
def bind_address_on_database(self, database_bind, user=None):
    user = get_user(self.request, user, "permit")

    AuditRequest.new_request("create_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.databaseinfra

    try:
        task_history.update_details(
            persist=True, details="Creating binds...")

        acl_client = get_acl_client(database.environment)

        if bind_address(database_bind, acl_client):
            task_history.update_status_for(
                TaskHistory.STATUS_SUCCESS, details='Bind succesfully created')
            return True

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
    action = "permit"
    user = get_user(self.request, user, action)

    AuditRequest.new_request("destroy_databasebind", user, "localhost")

    task_history = register_task(self.request, user)
    database = database_bind.database
    databaseinfra = database.infra

    try:
        acl_client = get_acl_client(database.environment)
        task_history.update_details(persist=True, details="Removing binds...")

        infra_instances_binds = DatabaseInfraInstanceBind.objects.filter(
            databaseinfra=databaseinfra, bind_address=database_bind.bind_address)

        if unbind_address(database_bind, acl_client, infra_instances_binds):
            task_history.update_status_for(TaskHistory.STATUS_SUCCESS,
                                           details='Bind succesfully destroyed')
            return True
    except Exception as e:
        LOG.info("Database unbind ERROR: {}".format(e))
        task_history.update_status_for(TaskHistory.STATUS_ERROR,
                                       details='Bind could not be removed')
        return False
    finally:
        AuditRequest.cleanup_request()


@shared_task(bind=True)
def monitor_aclapi_jobs(self,):
    from dbaas_aclapi.models import (
        AclApiJob, ERROR, PENDING, RUNNING, JOB_STATUS)

    status_dict = {_tuple[1]: _tuple[0] for _tuple in JOB_STATUS}
    user = get_user(action='monitor job')

    AuditRequest.new_request("monitor_aclapi_jobs", user, "localhost")
    task_history = register_task(self.request, user)

    try:
        task_history.update_details(persist=True, details="Monitoring binds...")

        for job in AclApiJob.objects.filter(job_status__in=[PENDING, RUNNING, ERROR]):
            acl_client = get_acl_client(job.environment)

            try:
                response = acl_client.get_job(job_id=job.job_id)
            except Exception as e:
                LOG.warn(e)

            if 'jobs' in response:
                status = response["jobs"]["status"]
                if status in ["PENDING", "ERROR"]:
                    try:
                        response = acl_client.run_job(job_id=job.job_id)
                    except Exception as e:
                        LOG.warn(e)

                job_status = status_dict.get(status, PENDING)
                job.job_status = job_status
                job.save(update_fields=['job_status', 'updated_at'])

        task_history.update_status_for(
            TaskHistory.STATUS_SUCCESS, details='Monitoring finished')
    except Exception as e:
        LOG.info("Database unbind ERROR: {}".format(e))
        task_history.update_status_for(
            TaskHistory.STATUS_ERROR, details='Erro while monitoring Jobs: {}'.format(e))
    finally:
        AuditRequest.cleanup_request()


def replicate_acl_for(database, old_ip, new_ip):
    acl_client = get_acl_client(database.environment)
    acls = acl_client.query_acls(payload={"destination": old_ip})
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
    acls = acl_client.query_acls(payload={"destination": ip})
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


def register_task(request, user):
    LOG.info("id: {} | task: {} | kwargs: {} | args: {}".format(request.id,
             request.task,
             request.kwargs,
             str(request.args)))
    task_history = TaskHistory.register(request=request, user=user,
                                        worker_name=get_worker_name())
    task_history.update_details(persist=True, details="Loading Process...")

    return task_history


def get_worker_name():
    from billiard import current_process
    p = current_process()
    return p.initargs[1].split('@')[1]
