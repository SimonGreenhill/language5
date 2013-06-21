# Django settings for website project.
import os

SITE_ROOT = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('Simon J. Greenhill', 'simon@simon.net.nz'),
)

INTERNAL_IPS = ('127.0.0.1',)

# Set in local.py
# ALLOWED_HOSTS = ['.transnewguinea.org', 'www.transnewguinea.org']


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(SITE_ROOT, 'database.db'),
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_NAME': None,               # use SQLite in-memory for testing
    }
}

# Site details
SITE_ID = 1
SITE_NAME = SITE_DOMAIN = 'TransNewGuinea.org'
SITE_DESCRIPTION = "Trans-New Guinea Language Database"

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
LOGIN_REDIRECT_URL = "/"

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
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.split(SITE_ROOT)[0], 'media'))

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

# Replace Test Runner with the auto-discover one (django-discover-runner)
TEST_RUNNER = 'discover_runner.DiscoverRunner'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]    

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "website.apps.core.context_processors.InjectSettings",
    "website.apps.olac.context_processors.InjectOLACSettings",
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
    
    # third-party
    'south',                             # south: database migrations
    'reversion',                         # reversion: object version control.
    'robots',                            # django-robots: robots.txt handling
    'djangosecure',                      # django-secure: Security helper
    'django_tables2',                    # django-tables2: tables helper
    'watson',                            # search
    'dbbackup',                          # backup
    'static_sitemaps',                   # static sitemaps.
    'compressor',                        # django-compressor for asset compression and versioning.
    
    # website
    'website.apps.core',                 # core functionality
    'website.apps.statistics',           # statistics
    'django_nvd3',                       # for graphing statistics
    
    # NOTE: all other apps should be added to local.py
    # INSTALLED_APPS.append('website.apps.lexicon')   # Lexicon
    # INSTALLED_APPS.append('website.apps.olac')      # OLAC utils
    # INSTALLED_APPS.append('website.apps.entry')     # Data Entry
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
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'backupCount' : 0,
            'maxBytes': 5000000,
            'filename': 'django.log',
            'filters': ['require_debug_false'],
        },
        'db_logging': {
            'level' : 'DEBUG',
            'class' : 'logging.handlers.RotatingFileHandler',
            'backupCount' : 0,
            'maxBytes': 5000000,
            'filename': 'django-db.log',
            'filters': ['require_debug_false'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
        
    'loggers': {
        'django' : {
            'handlers': ['file_logging'],
            'level' : 'DEBUG',
            'propagate' : False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db' : {
            'handlers' : ['db_logging'],
            'level' : 'DEBUG',
            'propagate': False,
        },
    }
}

# Caching:
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
        'KEY_PREFIX': SITE_NAME,
    }
}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# maximum age of persistent database connection
CONN_MAX_AGE = 64 

# THIRD-PARTY SETTINGS ==========================================

# Django-Security settings
SECURE_FRAME_DENY = True         # prevent framing of pages.
SECURE_BROWSER_XSS_FILTER = True # enable XSS protection
SESSION_COOKIE_SECURE = False    # can't login with True? 
SESSION_COOKIE_HTTPONLY = False  # can't login with True?
SECURE_CONTENT_TYPE_NOSNIFF = True

# South
SOUTH_TESTS_MIGRATE = False # just use syncdb

# Static Sitemaps
STATICSITEMAPS_ROOT_SITEMAP = 'website.sitemap.sitemaps'


# OLAC
OLAC_SETTINGS = {
    'sitename': SITE_NAME,
    'repositoryName': SITE_NAME,
    'sitedomain': SITE_DOMAIN,
    'description': SITE_DESCRIPTION,
    'adminEmail': ADMINS, 
    'admins': ADMINS,
    'deletedRecord': 'no', # deletedRecord policy
    'protocolVersion': '2.0', # the version of the OAI-PMH supported by the repository;
    'depositor': ADMINS,
    'institution': 'Australian National University',
    'institutionURL': 'http://anu.edu.au',
    'shortLocation': 'Canberra, Australia',
}


# cache the ``robots.txt`` for 24 hours (86400 seconds).
ROBOTS_CACHE_TIMEOUT = 60*60*24

# Set PIWIK ID
PIWIK_ID = 1

# Backup 
DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
DBBACKUP_S3_BUCKET = 'sjg-transnewguinea.org'
DBBACKUP_S3_ACCESS_KEY = 'AKIAI5L4FEQGKHXLZIEQ'
DBBACKUP_S3_SECRET_KEY = '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'
# no schema and use extended insert format
DBBACKUP_POSTGRES_BACKUP_COMMANDS = "pg_dump --username={adminuser} --host={host} --port={port} --data-only --inserts {databasename}" 
DBBACKUP_MEDIA_PATH = MEDIA_ROOT # see https://bitbucket.org/mjs7231/django-dbbackup/pull-request/13/multiple-big-fixes/