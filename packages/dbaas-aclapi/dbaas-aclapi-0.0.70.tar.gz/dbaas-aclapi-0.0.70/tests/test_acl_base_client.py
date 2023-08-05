#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from dbaas_aclapi import acl_base_client
from tests.factory import AclApiTestCase


class AclApiTest(AclApiTestCase):

    def test_assert_acl_api_init(self):
        acl_api_client = acl_base_client.AclClient(
            self.base_url, self.username, self.password, self.database_environment,
            self.ip_version)

        self.assertIsInstance(acl_api_client, acl_base_client.AclClient)

    def test_grant_acl_for(self):
        s_payload = {"new_access": "129.12.12.4/32"}
        self.acl_api_client.grant_acl_for('32', 8, s_payload)
        method, route, payload = self.acl_api_client.last_request

        self.assertEqual(method, 'PUT')
        self.assertEqual(route, 'api/ipv4/acl/32')
        self.assertEqual(payload, json.dumps(s_payload))

    def test_delete_acl(self):
        environment_id = 32
        vlan = 8
        acl_id = 321
        self.acl_api_client.delete_acl(environment_id, vlan, acl_id)

        method, route, _ = self.acl_api_client.last_request
        self.assertEqual(method, 'DELETE')
        self.assertEqual(route, 'api/ipv4/acl/32/8/321')

    def test_list_jobs(self):
        self.acl_api_client.list_jobs()
        method, route, _ = self.acl_api_client.last_request
        self.assertEqual(method, 'GET')
        self.assertEqual(route, 'api/jobs')

    def test_get_job(self):
        job_id = 171
        self.acl_api_client.get_job(job_id)
        method, route, _ = self.acl_api_client.last_request
        self.assertEqual(method, 'GET')
        self.assertEqual(route, 'api/jobs/171')

    def test_run_job(self):
        job_id = 172
        self.acl_api_client.run_job(job_id)
        method, route, _ = self.acl_api_client.last_request
        self.assertEqual(method, 'GET')
        self.assertEqual(route, 'api/jobs/172/run')

    def test_get_next_job(self):
        self.acl_api_client.get_next_job()
        method, route, _ = self.acl_api_client.last_request
        self.assertEqual(method, 'GET')
        self.assertEqual(route, 'api/jobs/next')

    def test_query_acls(self):
        search_payload = {"protocol": "tcp",
                          "source": "192.168.1.10",
                          "destination": "192.168.10.2",
                          "description": "test",
                          "action": "permit",
                          "l4-options": {"dest-port-start": "3306",
                                         "dest-port-op": "eq"}
                          }
        self.acl_api_client.query_acls(search_payload)
        method, route, payload = self.acl_api_client.last_request

        self.assertEqual(method, 'POST')
        self.assertEqual(route, 'api/ipv4/acl/search')
        self.assertEqual(payload, search_payload)

    def tearDown(self):
        pass
