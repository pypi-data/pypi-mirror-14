# -*- coding: utf-8 -*-
# Copyright (c) Polyconseil SAS. All rights reserved.
# This code is distributed under the two-clause BSD License.
from __future__ import absolute_import, unicode_literals
import base64
import logging

from getconf import ConfigGetter

# Import Sentry's DEFAULT_SETTINGS_MODULE
from sentry.conf.server import *

from autoguard.config_helpers import (
    database_from_url, get_hostname, mail_from_url, sentry_caches_from_url,
    ldapized_middleware_classes, ldapized_authentication_backends
)


PROJECT_NAME = 'autoguard'

# Load configuration from INI files in /etc/autoguard/settings, along with default configuration dictionary
CONFIG = ConfigGetter(
    PROJECT_NAME,
    ['/etc/%s/settings/' % PROJECT_NAME, ],
    {
        'DEFAULT': {
            'host': '127.0.0.1',
            'port': 9000,
        },
        'dev': {
            'debug': False,
            'template_debug': False,
            'maintenance': False,
        },
        'django': {
            'broker_url': None,
            'db_uri': 'sqlite:///autoguard.sqlite',
            'language_code': 'fr-fr',
            'mail_uri': 'console://?sender=no-reply@localhost',
            'site_url': 'http://localhost:9000',
            'secret_key': base64.b64encode(os.urandom(40)),
            'time_zone': 'UTC',
        },
        'ldap': {
            'uri': None,
            'user_tpl': 'uid={username}',
            'user_key': 'uniqueMember',
            'groups': '',
        },
        'sentry': {
            'cache_url': 'redis://127.0.0.1:6379/',
            'web_workers': 5,
            'disallowed_ips': SENTRY_DISALLOWED_IPS,
        }
    }
)

# Locale Setup
# ############

TIME_ZONE = CONFIG.getstr('django.time_zone')
LANGUAGE_CODE = CONFIG.getstr('django.language_code')

# Database and Caches Setup
# #########################

DATABASES = {
    'default': database_from_url(CONFIG.getstr('django.db_uri'))
}

_parsed_sentry_caches = sentry_caches_from_url(CONFIG.getstr('sentry.cache_url'))
CACHES = _parsed_sentry_caches['django_caches']

SENTRY_REDIS_OPTIONS = _parsed_sentry_caches['redis_options']

SENTRY_CACHE = _parsed_sentry_caches['sentry']
SENTRY_BUFFER = _parsed_sentry_caches['buffer']
SENTRY_TSDB = _parsed_sentry_caches['tsdb']
SENTRY_RATELIMITER = _parsed_sentry_caches['rate_limits']
SENTRY_DIGESTS = _parsed_sentry_caches['digest']
SENTRY_QUOTAS = _parsed_sentry_caches['quota']


# Email setup
# ###########

_parsed_email_url = mail_from_url(CONFIG.getstr('django.mail_uri'))
EMAIL_SUBJECT_PREFIX = _parsed_email_url['prefix']
EMAIL_BACKEND = _parsed_email_url['backend']
EMAIL_HOST = _parsed_email_url['host']
EMAIL_PORT = _parsed_email_url['port']
EMAIL_HOST_USER = _parsed_email_url['user']
EMAIL_HOST_PASSWORD = _parsed_email_url['password']
EMAIL_USE_TLS = _parsed_email_url['use_tls']
SERVER_EMAIL = _parsed_email_url['sender']


# Async Setup
# ###########

BROKER_URL = CONFIG.getstr('django.broker_url')
CELERY_ALWAYS_EAGER = CONFIG.getbool('django.celery_always_eager', BROKER_URL is None)


# Web Server Setup
# ################

SENTRY_URL_PREFIX = CONFIG.getstr('django.site_url')

extra_allowed_hosts = CONFIG.getlist('sentry.extra_allowed_hosts', [])
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", get_hostname(SENTRY_URL_PREFIX)] + extra_allowed_hosts

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SENTRY_WEB_HOST = CONFIG.getstr('host', '0.0.0.0')
SENTRY_WEB_PORT = CONFIG.getint('port', 9000)
SENTRY_WEB_OPTIONS = {
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'workers': CONFIG.getint('sentry.web_workers', 4),
}

SENTRY_DISALLOWED_IPS = CONFIG.getlist('sentry.disallowed_ips', [])

SECRET_KEY = CONFIG.getstr('django.secret_key')


# Sentry Setup
# ############

SENTRY_USE_BIG_INTS = True
SENTRY_BEACON = True
SENTRY_SINGLE_ORGANIZATION = True
SENTRY_FEATURES = {
    'auth:register': False,  # no auto-registration
    'organizations:create': True,
    'organizations:sso': True,
    'projects:global-events': False,
    'projects:quotas': True,
    'projects:user-reports': False,
    'projects:plugins': True,
}


# LDAP Setup
# ##########

LDAP = {
    'uri': CONFIG.getstr('ldap.uri'),
    'user_tpl': CONFIG.getstr('ldap.user_tpl'),
    'member_key': CONFIG.getstr('ldap.member_key'),
    'groups': [x.strip() for x in CONFIG.getstr('ldap.groups').split(':')],
}

REMOTE_USER_HTTP_HEADER = CONFIG.getstr('django.remote_user_http_header', 'HTTP_X_REMOTE_USER')

if LDAP['uri']:
    MIDDLEWARE_CLASSES = ldapized_middleware_classes(MIDDLEWARE_CLASSES)
    AUTHENTICATION_BACKENDS = ldapized_authentication_backends(AUTHENTICATION_BACKENDS)

# Dev Setup
# #########

DEBUG = CONFIG.getbool('dev.debug', False)
TEMPLATE_DEBUG = CONFIG.getbool('dev.template_debug', False)
MAINTENANCE = CONFIG.getbool('dev.maintenance', False)

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
