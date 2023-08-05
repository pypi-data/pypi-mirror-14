# -*- coding: utf-8 -*-
"""
    matterllo.utils
    ~~~~~~~~~~~~~~~

    The utils parts.

    :copyright: (c) 2016 by Lujeni.
    :license: BSD, see LICENSE for more details.
"""
import os
import sys
import logging

from yaml import load

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')


def config():
    """
    TODO:
        - change the way to manage the settings.
        - add a cache layer.
    """
    config_file = os.environ.get('MATTERLLO_CONFIG_FILE')
    if not config_file:
        logging.error('Make sure the following environment variables are set: MATTERLLO_CONFIG_FILE')
        sys.exit(0)

    with open(config_file, 'r') as f:
        return load(f)

def logger():
    """
    """
    logging.basicConfig(
        level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    return logging
