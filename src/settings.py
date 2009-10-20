# Django settings for skram-si project.

import os
ROOT_PATH = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Administrator', 'admin@skram.si'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'appengine'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ABS_ROOT_PATH = os.path.abspath(ROOT_PATH)
LOCALE_PATHS = (
    os.path.join(ABS_ROOT_PATH, 'lib', 'locale'),
)


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bsjm7+n#u_lc9*cgijl*1&@l37ax=p(n)+y6a(66r%oeierdr$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'openidgae.middleware.OpenIDMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".  Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT_PATH + '/skram/templates',
)

INSTALLED_APPS = (
    'skram.poll',
    'skram',
    'openidgae',
    'appengine_django',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Latest tweet
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    "skram.context_processors.latest_tweets",
)

TWITTER_USER = 'skramsi'
TWITTER_SKRAMSI_KEY = '80389756-5nE1HMPGvA8tiIcuTmDc0xkLpRiM3hBb6iKRSF3U0'
TWITTER_SKRAMSI_SECRET = '6ZVlpo5Q6lnIkwdjU9HcBiZ7js5riVluVlUbRnsL0'
TWITTER_SKRAMSI_CONSUMER_KEY = 'G136lSFtGh1krLy8whH6A'
TWITTER_SKRAMSI_CONSUMER_SECRET = 'R04q5Cga56ppxCH7PlNhO3CuHb4PhLUcdKKuY3Sdg'
TWITTER_TIMEOUT = 1
TWITTER_TWEETS_SHOWN = 6
