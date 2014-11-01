from __future__ import absolute_import

"""
Django settings for Pythonidae project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import djcelery

djcelery.setup_loader()
BROKER_URL = 'django://'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a8xgv6jns!70xp1+zsbfakg95b1_^l(d9-dzwu+%vzqa8d5t2u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# For production
# ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'rest_framework',
    'rest_framework.authtoken',
    'django_cron',
    'djcelery',
    'kombu.transport.django',
    'autofixture',
    'yaas',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'Pythonidae.urls'

WSGI_APPLICATION = 'Pythonidae.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'yaas.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR + '/yaas/emails/messages/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = ('/static/')

LOCALE_PATHS = ('locale',)

ugettext = lambda s: s
LANGUAGES = (
    ('en', ugettext('English')),
    ('fi', ugettext('Suomi')),
    ('sv', ugettext('Svenska')),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Static directory definition
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '/static/'),
)


# Data fixtures directory definition
FIXTURES_DIRS = (
    os.path.join(BASE_DIR, '/fixtures/'),
)

# Security
#SESSION_COOKIE_SECURE = True

# csfr Security
# CSRF_COOKIE_SECURE = True
# Clear session when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Session Expire in 3600 seconds and require re-login by the member user
SESSION_COOKIE_AGE = 3600

# crontabs for banning auction and handling bids on a schedule manner
CRON_CLASSES = [
    "yaas.crontask.ResolveAuction",
]

'''
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'UTC'
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_RESULT_EXPIRES = 1800
'''
CELERY_IMPORTS = ("yaas.tasks",)
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # for web browsable API
    ),
    'PAGINATE_BY': 20,
    #'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer'),
    #'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONResponse'),

}

ADMINS = (
    ('Dawit Nida', 'dawit.nida@abo.fi'),
    ('Yaas Admin', 'yaas@abo.fi'),
)

MANAGERS = ADMINS

'''
import warnings
warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')
'''
