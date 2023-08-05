# -*- coding: utf-8 -*-
import logging

logging.basicConfig()
LOG = logging.getLogger("AclHelpers")
LOG.setLevel(logging.DEBUG)


def build_data_default_options_dict(action, bind_address, database_name,
                                    database_environment):

    description = "{} {} access for database {} in {}".format(
        action, bind_address, database_name, database_environment)

    data = {"kind": "object#acl", "rules": []}
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


def iter_on_acl_query_results(acl_client, rule):
    query_results = acl_client.query_acls(rule)
    for environment in query_results.get('envs', []):
        for vlan in environment.get('vlans', []):
            environment_id = vlan['environment']
            vlan_id = vlan['num_vlan']
            for rule in vlan.get('rules', []):
                rule_id = rule['id']
                yield environment_id, vlan_id, rule_id


def get_user(request, user, action):
    if not user:
        user = request.args[-1]

    LOG.info("User: {}, action: {}".format(user, action))
    return user
