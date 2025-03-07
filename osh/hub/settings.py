# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: Copyright contributors to the OpenScanHub project.

# Django global settings for OpenScanHub

# DEBUG = True


import os

import kobo

from osh.hub.other.settings_util import get_secret

# Definition of PROJECT_DIR, just for convenience:
# you can use it instead of specifying the full path
PROJECT_DIR = os.path.dirname(__file__)

URL_PREFIX = "/osh"

# directory to read the real SECRET_KEY from
SECRET_KEY_DIR = "/var/lib/osh/hub/"

# where to read API keys from
SECRETS_DIR = "/etc/osh/hub/secrets"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the assets served from STATIC_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
STATIC_URL = URL_PREFIX + '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static-assets'),
)

# Default field type for primary keys
# TODO: By default, Django 3 uses BigAutoField but we must remain compatible
# with Kobo which still supports Django 2.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # `/etc/osh/hub/templates` overrides `index-content.html`
            "/etc/osh/hub/templates",
            os.path.join(PROJECT_DIR, "templates"),
            os.path.join(os.path.dirname(kobo.__file__), "hub", "templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "kobo.django.menu.context_processors.menu_context_processor",
                "django.template.context_processors.static",
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

ROOT_URLCONF = 'osh.hub.urls'
ROOT_MENUCONF = 'osh.hub.menu'


AUTHENTICATION_BACKENDS = (
    'kobo.django.auth.krb5.Krb5RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'kobo_auth.User'

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'kobo.django.auth.middleware.LimitedRemoteUserMiddleware',
    'kobo.hub.middleware.WorkerMiddleware',
    'kobo.django.menu.middleware.MenuMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'kobo.django.auth.apps.AuthConfig',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',

    # nice numbers and dates
    'django.contrib.humanize',

    # kobo apps:
    'kobo.django.upload',
    'kobo.django.xmlrpc',
    'kobo.hub',

    # OpenScanHub
    'osh.hub.scan',
    'osh.hub.waiving',
    'osh.hub.stats',

    # better ./manage.py shell
    # 'django_extensions',
)

# pagination by default was removed in kobo-0.4.2~9 (use this to re-enable it)
PAGINATE_BY = 50

###############################################################################
# OpenScanHub SPECIFIC
###############################################################################

# kobo XML-RPC API calls
# If you define additional methods, you have to list them there.
XMLRPC_METHODS = {
    # 'handler': (/xmlrpc/<handler>)
    'client': (
        # module with rpc methods     prefix which is added to all methods from
        #                             the module
        ('kobo.hub.xmlrpc.auth', 'auth'),
        ('kobo.hub.xmlrpc.client', 'client'),
        ('kobo.hub.xmlrpc.system', 'system'),
        ('kobo.django.upload.xmlrpc', 'upload'),
        ('osh.hub.osh_xmlrpc.client', 'client'),
        ('osh.hub.osh_xmlrpc.mock_config', 'mock_config'),
        ('osh.hub.osh_xmlrpc.scan', 'scan'),
    ),
    'worker': (
        ('kobo.hub.xmlrpc.auth', 'auth'),
        ('kobo.hub.xmlrpc.system', 'system'),
        ('kobo.hub.xmlrpc.worker', 'worker'),
        ('kobo.django.upload.xmlrpc', 'upload'),
        ('kobo.hub.xmlrpc.client', 'client'),
        ('osh.hub.osh_xmlrpc.worker', 'worker'),
    ),
    'kerbauth': (
        ('kobo.hub.xmlrpc.auth', 'auth'),
        ('osh.hub.osh_xmlrpc.errata', 'errata'),
    ),

}

LOGIN_URL_NAME = 'auth/krb5login'
LOGIN_EXEMPT_URLS = ['.*xmlrpc/.*']

# Default redirect targets for unsafe or invalid ?next URLs
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# Denote whether the access to user list/detail view is restricted
# Possible values:
# "" (empty string) = Anonymous access (default)
# "authenticated" = Authenticated users
# "staff" = Staff (admin) users only
USERS_ACL_PERMISSION = "staff"

VALID_TASK_LOG_EXTENSIONS = ['.log', '.ini', '.err', '.out', '.js', '.txt', '.cfg']

# Log file extensions to be viewed unrendered even when `?format=raw` is not used
VIEW_RAW_LOG_EXTENSIONS = [".html", ".js", ".json"]

# This is kept here for backward compatibility.
# https://github.com/openscanhub/openscanhub/pull/256#pullrequestreview-2001187953
DEFAULT_EMAIL_DOMAIN = "redhat.com"

NOTIFICATION_EMAIL_FOOTER = ""

# If this setting is enabled, a worker is only used to perform a single task.
ENABLE_SINGLE_USE_WORKERS = False

# Disable sending messages to Fedora rabbitmq
# Enabling this option requires `fedora-messaging` package
ENABLE_FEDORA_MESSAGING = False

# override default values with custom ones from local settings
try:
    from .settings_local import *  # noqa
except ImportError:
    pass


###############################################################################
# Secrets
###############################################################################

# Issue trackers
BZ_API_KEY = get_secret('bugzilla_secret', SECRETS_DIR)
JIRA_API_KEY = get_secret('jira_secret', SECRETS_DIR)

# Secret key (will be overridden by the content of SECRET_KEY_FILE if available)
SECRET_KEY = get_secret('secret_key', SECRET_KEY_DIR) or 'x' * 50
