# -*- coding: utf-8 -*-

import boto3.session
import botocore_paste


__version__ = '0.1'

def normalize_config(config, prefix='boto3.', **kwargs):
    """
    :type config: dict
    :type prefix: str
    :rtype: dict
    """
    prefix_len = len(prefix)
    normalized = dict([(k[prefix_len:], v) for k, v in config.items()
                       if k.startswith(prefix) and v])
    normalized.update(kwargs)
    core_prefix = 'botocore.'
    core_prefix_len = len(core_prefix)
    core = dict([(k[core_prefix_len:], v) for k, v in normalized.items()
                 if k.startswith(core_prefix)])
    if core:
        for k in core:
            del normalized[core_prefix + k]
        normalized['botocore'] = core
    return normalized


def session_from_config(config, prefix='boto3.', **kwargs):
    """
    :type config: dict
    :type prefix: str
    :rtype: boto3.session.Session
    """
    normalized = normalize_config(config, prefix, **kwargs)
    botocore_config = normalized.pop('botocore', {})
    botocore_session = normalized.get('botocore_session', None)
    if botocore_session is None and botocore_config:
        normalized['botocore_session'] = botocore_paste.session_from_config(
            botocore_config, prefix=''
        )
    session = boto3.session.Session(**normalized)
    return session
