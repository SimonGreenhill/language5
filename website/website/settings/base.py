# Django settings for website project.
import os

SITE_ROOT = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

DEBUG = False

ADMINS = (
    ('Simon J. Greenhill', 'test@example.com'),
)

INTERNAL_IPS = ('127.0.0.1',)

# Set in local.py
# ALLOWED_HOSTS = ['.transnewguinea.org', 'www.transnewguinea.org']

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'database.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST': {
            'NAME': None,  # SQLite in-memory test database
        },
    },

}

# Site details
SITE_ID = 1
SITE_NAME = SITE_DOMAIN = 'language5'
SITE_DESCRIPTION = "Language5"

# test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/?logged-in"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.abspath(
    os.path.join(os.path.split(SITE_ROOT)[0], 'media')
)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '../static_root/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(os.path.split(SITE_ROOT)[0], 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=_1)@n652y5qic+)1sj)7!#p##kn0#!k2@yr&amp;e)!019$0tynt2'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
             os.path.join(SITE_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'website.apps.core.context_processors.InjectSettings',
                'website.apps.olac.context_processors.InjectOLACSettings',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    'django.contrib.redirects',

    # Admin site
    'django.contrib.admin',
    'django.contrib.admindocs',

    # website
    'website.apps.core',                 # core functionality
    'website.apps.statistics',           # statistics
    'website.apps.lexicon',              # lexicon
    'website.apps.cognacy',              # lexicon -- cognacy
    'website.apps.olac',                 # OLAC
    'website.apps.entry',                # Data Entry
    'website.apps.pronouns',             # pronoun paradigm project
    'website.apps.maps',                 # maps

    # third-party
    'reversion',                         # reversion: object version control.
    'django_tables2',                    # django-tables2: tables helper
    'watson',                            # search
    'dbbackup',                          # backup
    'static_sitemaps',                   # static sitemaps.
    'compressor',                        # django-compressor
    'twitter_tag',                       # twitter tag
    'tastypie',                          # API
    'django_nvd3',                       # for graphing statistics

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file_logging': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 0,
            'maxBytes': 5000000,
            'filename': 'django.log',
            'filters': ['require_debug_false'],
        },
        'db_logging': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 0,
            'maxBytes': 5000000,
            'filename': 'django-db.log',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file_logging'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db': {
            'handlers': ['db_logging'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# maximum age of persistent database connection
CONN_MAX_AGE = 64

# THIRD-PARTY SETTINGS ==========================================

# Static Sitemaps
STATICSITEMAPS_ROOT_SITEMAP = 'website.sitemap.sitemaps'

OLAC_SETTINGS = {
    'sitename': SITE_NAME,
    'repositoryName': SITE_NAME,
    'sitedomain': SITE_DOMAIN,
    'description': SITE_DESCRIPTION,
    'adminEmail': ADMINS,
    'admins': ADMINS,
    'deletedRecord': 'no',
    'protocolVersion': '2.0',
    'depositor': ADMINS,
    'institution': '',
    'institutionURL': '',
    'shortLocation': '',
}

# override in local.py
TWITTER_OAUTH_TOKEN = None
TWITTER_OAUTH_SECRET = None
TWITTER_CONSUMER_KEY = None
TWITTER_CONSUMER_SECRET = None

