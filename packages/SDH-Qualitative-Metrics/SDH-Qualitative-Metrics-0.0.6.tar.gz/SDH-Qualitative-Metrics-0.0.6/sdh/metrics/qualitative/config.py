"""
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  This file is part of the Smart Developer Hub Project:
    http://www.smartdeveloperhub.org

  Center for Open Middleware
        http://www.centeropenmiddleware.com/
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Copyright (C) 2015 Center for Open Middleware.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

            http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
"""

import logging
import os

__author__ = 'Fernando Serena'


def _api_port():
    return int(os.environ.get('API_PORT', 5004))


def _redis_conf(def_host, def_db, def_port):
    return {'host': os.environ.get('DB_HOST', def_host),
            'db': int(os.environ.get('DB_DB', def_db)),
            'port': int(os.environ.get('DB_PORT', def_port))}


def _agora_conf(def_host, def_port):
    return {'agora_host': os.environ.get('AGORA_HOST', def_host),
            'agora_port': int(os.environ.get('AGORA_PORT', def_port))}


def _broker_conf(def_host, def_port):
    return {'broker_host': os.environ.get('BROKER_HOST', def_host),
            'broker_port': int(os.environ.get('BROKER_PORT', def_port))}


def _stoa_conf(def_exchange, def_topic_pattern, def_response_prefix):
    return {
        'exchange': os.environ.get('EXCHANGE', def_exchange),
        'topic_pattern': os.environ.get('TOPIC_PATTERN', def_topic_pattern),
        'response_prefix': os.environ.get('RESPONSE_PREFIX', def_response_prefix)
    }


class Config(object):
    PORT = _api_port()


class DevelopmentConfig(Config):
    DEBUG = True
    LOG = logging.DEBUG
    PROVIDER = _broker_conf('localhost', 5672)
    PROVIDER.update(_agora_conf('localhost', 9009))
    PROVIDER.update(_stoa_conf('sdh', 'scholar.request', 'scholar.response'))
    REDIS = _redis_conf('localhost', 5, 6379)


class ProductionConfig(Config):
    DEBUG = False
    LOG = logging.INFO
    PROVIDER = _broker_conf('localhost', 5672)
    PROVIDER.update(_agora_conf('localhost', 9009))
    PROVIDER.update(_stoa_conf('sdh', 'scholar.request', 'scholar.response'))
    REDIS = _redis_conf('redis', 5, 6379)
