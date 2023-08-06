# -*- coding: utf-8 -*-

import unittest


class NormalizeConfigTestCase(unittest.TestCase):

    def test_int(self):
        from .. import normalize_config
        config = {'botocore.metadata_service_num_attempts': '33',
                  'botocore.metadata_service_timeout': '25',
                  'botocore.profile': 'someprofile'}
        self.assertDictEqual(normalize_config(config), {
            'metadata_service_num_attempts': 33,
            'metadata_service_timeout': 25,
            'profile': 'someprofile',
        })


class SessionFromConfigTestCase(unittest.TestCase):

    def test_functional_1(self):
        import os
        from ..import session_from_config
        d = os.path.dirname(__file__)
        config = {
            'aaa.profile': 'testing',
            'aaa.config_file': os.path.join(d, 'config_1.ini'),
            'aaa.credentials_file': os.path.join(d, 'credentials_1.ini'),
        }
        session = session_from_config(config, prefix='aaa.')
        self.assertEquals(session.profile, 'testing')
        self.assertEquals(session.get_config_variable('region'),
                          'ap-northeast-1')
        cred = session.get_credentials()
        self.assertEquals(cred.access_key, 'DUMMY_TESTING_KEY')
        self.assertEquals(cred.secret_key, 'DUMMY_TESTING_SECRET')
