# -*- coding: utf-8 -*-

import unittest


class NormalizeConfigTestCase(unittest.TestCase):

    def test(self):
        from .. import normalize_config
        config = {
            'aaa.aws_access_key_id': '__some_key__',
            'aaa.botocore.config_file': '__some_path__',
            'aaa.botocore.credentials_file': '__some_path__',
        }
        kwargs = {
            'botocore.credentials_file': '__some_path_2__',
        }
        ret = normalize_config(config, 'aaa.', **kwargs)
        self.assertDictEqual(ret, {
            'aws_access_key_id': '__some_key__',
            'botocore': {
                'config_file': '__some_path__',
                'credentials_file': '__some_path_2__',
            }
        })


class SessionFromConfigTestCase(unittest.TestCase):

    def test_minimum(self):
        from .. import session_from_config
        from boto3.session import Session
        config = {}
        ret = session_from_config(config)
        self.assertIsInstance(ret, Session)

    def test_cred(self):
        from .. import session_from_config
        config = {
            'boto3.aws_access_key_id': '__test_key__',
            'boto3.aws_secret_access_key': '__test_secret__',
            'boto3.region_name': '__test_region__',
        }
        ret = session_from_config(config)
        self.assertEqual(ret.region_name, '__test_region__')
        cred = ret._session.get_credentials()
        self.assertEqual(cred.access_key, '__test_key__')
        self.assertEqual(cred.secret_key, '__test_secret__')

    def test_profile(self):
        import os
        from .. import session_from_config
        d = os.path.dirname(__file__)
        config = {
            'boto3.botocore.config_file': os.path.join(d, 'config_1.ini'),
            'boto3.botocore.credentials_file': os.path.join(d, 'cred_1.ini'),
            'boto3.botocore.profile': 'testing',
        }
        ret = session_from_config(config)
        self.assertEqual(ret.region_name, 'ap-northeast-1')
        cred = ret._session.get_credentials()
        self.assertEqual(cred.access_key, 'DUMMY_TESTING_KEY')
        self.assertEqual(cred.secret_key, 'DUMMY_TESTING_SECRET')

    def test_coresession(self):
        import mock
        from .. import session_from_config
        marker = mock.Mock()
        config = {
            'boto3.botocore_session': marker,
        }
        ret = session_from_config(config)
        self.assertIs(ret._session, marker)
