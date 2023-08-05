# -*- coding: utf-8 -*-
import json
import urllib3
import logging
from util import get_credentials_for
from networkapiclient import (Ip, Network)

logging.basicConfig()
LOG = logging.getLogger("AclBaseClient")
LOG.setLevel(logging.DEBUG)


def get_acl_client(database_environment):
    from dbaas_credentials.models import CredentialType
    acl_credential = get_credentials_for(database_environment,
                                         CredentialType.ACLAPI)
    return AclClient(acl_credential.endpoint, acl_credential.user, acl_credential.password,
                     database_environment)


class AclClient(object):

    def __init__(self, base_url, username, password, database_environment,
                 ip_version=4):
        LOG.info("Initializing new acl base client.")
        self.kind = ""
        self.acls = []
        self.headers = {}
        self.base_url = base_url
        self.username = username
        self.password = password
        self.ip_version = ip_version
        self.database_environment = database_environment
        self._add_basic_athentication()

    def _add_basic_athentication(self):
        LOG.info("Setting up authentication.")
        basic_auth = '{}:{}'.format(self.username, self.password)
        self.headers.update(urllib3.util.make_headers(basic_auth=basic_auth))

    def _add_content_type_json(self,):
        LOG.info("Setting up \"Content-Type\".")
        self.headers.update({'Content-Type': 'application/json'})

    def _make_request(self, http_verb, endpoint, payload=None):
        endpoint = self.base_url + endpoint
        http = urllib3.PoolManager()
        LOG.debug("Requesting {} on {}".format(http_verb, endpoint))

        if http_verb == 'GET':
            response = http.request(method=http_verb, url=endpoint,
                                    headers=self.headers)
        else:
            self._add_content_type_json()

            if type(payload) is not str:
                payload = json.dumps(payload)

            LOG.info("JSON PAYLOAD: {}".format(payload))

            response = http.urlopen(method=http_verb, body=payload,
                                    url=endpoint, headers=self.headers)

        LOG.debug("Response {}".format(response.data))

        return response

    def _get_network_from_networkapi(self, ip, database_environment):
        from dbaas_credentials.models import CredentialType
        net_api_credentials = get_credentials_for(environment=database_environment,
                                                  credential_type=CredentialType.NETWORKAPI)

        ip_client = Ip.Ip(net_api_credentials.endpoint,
                          net_api_credentials.user,
                          net_api_credentials.password)

        ips = ip_client.get_ipv4_or_ipv6(ip)
        ips = ips['ips']
        if type(ips) != list:
            ips = [ips]

        net_ip = ips[0]
        network_client = Network.Network(net_api_credentials.endpoint,
                                         net_api_credentials.user,
                                         net_api_credentials.password)

        network = network_client.get_network_ipv4(net_ip['networkipv4'])
        network = network['network']

        return network['oct1'] + '.' + network['oct2'] + '.' + network['oct3'] + '.' + network['oct4'] + '/' + network['block']

    def register_acl(self, payload):
        LOG.info("Registering new ACL.")
        endpoint = "api/ipv{}/acl".format(self.ip_version)
        response = self._make_request(http_verb="POST", endpoint=endpoint,
                                      payload=payload)

        return json.loads(response.data)

    def destroy_acl(self, payload):
        LOG.info("Destroying ACL.")

        endpoint = "api/ipv{}/acl".format(self.ip_version)
        response = self._make_request(http_verb="DELETE", endpoint=endpoint,
                                      payload=payload)

        return json.loads(response.data)

    def delete_acl(self, environment_id, vlan, acl_id):
        LOG.info("Deleting ACL.")
        endpoint = "api/ipv{}/acl/{}/{}/{}".format(
            self.ip_version, environment_id, vlan, acl_id)
        response = self._make_request(http_verb="DELETE", endpoint=endpoint)

        return json.loads(response.data)

    def list_acls_for(self, environment, vlan):
        LOG.info("Retrieving ACLs for {} on {}".format(vlan, environment))
        endpoint = "api/ipv{}/acl/{}/{}".format(self.ip_version, environment,
                                                vlan)
        response = self._make_request(http_verb="GET", endpoint=endpoint,)

        return json.loads(response.data)

    def grant_acl_for(self, environment, vlan, payload):
        LOG.info("GRANT ACLs for {} on {}".format(vlan, environment))
        LOG.debug("Payload: {}".format(payload))
        network = self._get_network_from_networkapi(environment,
                                                    self.database_environment)
        endpoint = "api/ipv{}/acl/{}".format(self.ip_version, network)
        response = self._make_request(http_verb="PUT", endpoint=endpoint,
                                      payload=json.dumps(payload))

        json_data = json.loads(response.data)
        LOG.debug("JSON request.DATA decoded: {}".format(json_data))

        return json_data

    def revoke_acl_for(self, environment, vlan, payload):
        LOG.info("REVOKE ACLs for {} on {}".format(vlan, environment))
        network = self._get_network_from_networkapi(environment,
                                                    self.database_environment)
        endpoint = "api/ipv{}/acl/{}".format(self.ip_version, network)
        response = self._make_request(http_verb="PURGE", endpoint=endpoint,
                                      payload=payload)

        json_data = json.loads(response.data)
        LOG.debug("JSON request.DATA decoded: {}".format(json_data))

        return json_data

    def list_jobs(self):
        LOG.info("Retrieving Jobs list.")
        endpoint = "api/jobs"
        response = self._make_request(http_verb="GET", endpoint=endpoint,)

        return json.loads(response.data)

    def get_job(self, job_id):
        LOG.info("Retrieving job {}".format(job_id))
        endpoint = "api/jobs/{}".format(job_id)
        response = self._make_request(http_verb="GET", endpoint=endpoint,)

        return json.loads(response.data)

    def run_job(self, job_id):
        LOG.info("Run job {}".format(job_id))
        endpoint = "api/jobs/{}/run".format(job_id)
        response = self._make_request(http_verb="GET", endpoint=endpoint,)

        return json.loads(response.data)

    def get_next_job(self):
        LOG.info("Getting next job")
        endpoint = "api/jobs/next"
        response = self._make_request(http_verb="GET", endpoint=endpoint,)

        return json.loads(response.data)

    def get_ip_vlan(self, ip):
        return "{}.0".format(ip[:ip.rindex('.')])

    def search_acl_for(self, destination):
        LOG.info("Retrieving acls for: {}".format(destination))
        endpoint = 'api/ipv{}/acl/search'.format(self.ip_version)
        payload = json.dumps({'destination': destination})
        response = self._make_request(http_verb="POST", endpoint=endpoint,
                                      payload=payload)

        return json.loads(response.data)

    def query_acls(self, payload):
        endpoint = 'api/ipv{}/acl/search'.format(self.ip_version)
        response = self._make_request(http_verb="POST", endpoint=endpoint,
                                      payload=payload)

        return json.loads(response.data)
