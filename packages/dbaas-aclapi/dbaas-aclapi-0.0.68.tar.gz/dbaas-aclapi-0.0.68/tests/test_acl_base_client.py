#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from dbaas_aclapi.acl_base_client import AclClient


class AclApiTest(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://acl_api.mock.test.globoi.globo.com'
        self.username = 'dbaas'
        self.password = 'dbaas'
        self.database_environment = 'dev'
        self.ip_version = 4

    def test_assert_acl_api_init(self):
        acl_api_client = AclClient(self.base_url, self.username, self.password,
                                   self.database_environment, self.ip_version)

        self.assertIsInstance(acl_api_client, AclClient)

    def tearDown(self):
        pass
