# -*- coding: utf-8 -*-

import botocore.session


__version__ = '0.2'


def normalize_config(config, prefix='botocore.', **kwargs):
    """
    :type config: dict
    :type prefix: str
    :rtype: dict
    """
    config = dict((k[len(prefix):], config[k]) for k in config
                  if k.startswith(prefix) and len(config[k]) > 0)
    config.update(kwargs)
    for logical, v in botocore.session.Session.SESSION_VARIABLES.items():
        (config_file_key, env_key, default, conversion) = v
        if conversion and logical in config:
            config[logical] = conversion(config[logical])
    return config


def session_from_config(config, prefix='botocore.', **kwargs):
    """
    :type config: dict
    :type prefix: str
    :rtype: botocore.session.Session
    """
    config = normalize_config(config, prefix, **kwargs)
    session = botocore.session.Session()
    for k, v in config.items():
        session.set_config_variable(k, v)
    return session
