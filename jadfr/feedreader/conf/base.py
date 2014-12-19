import os

from configurations import Configuration
import environment

location = lambda x: os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../', x))


def always_show_debug_toolbar(request):
    return True


def never_show_debug_toolbar(request):
    return False


class Base(Configuration):

    ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT') or environment.PRODUCTION
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '=2j_rpzp0#03(pv19-xefur2-pn0_f3&4klli%ng&__mnthyco'

    ADMINS = (
        ('Webmaster', 'webmaster@example.com'),
    )

    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'jadfr.db', # Or path to database file if using sqlite3.
            'USER': '', # Not used with sqlite3.
            'PASSWORD': '', # Not used with sqlite3.
            'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '', # Set to empty string for default. Not used with sqlite3.
        }
    }

    SITE_ID = 1

    # Hosts/domain names that are valid for this site; required if DEBUG is False
    # See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = []

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/var/www/example.com/media/"
    MEDIA_ROOT = location('user_uploads')

    # URL that handles the media served from MEDIA_ROOT. Make sure to use a
    # trailing slash.
    # Examples: "http://example.com/media/", "http://media.example.com/"
    MEDIA_URL = ''

    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/var/www/example.com/static/"
    STATIC_ROOT = location('static')

    # URL prefix for static files.
    # Example: "http://example.com/static/", "http://static.example.com/"
    STATIC_URL = '/static/'

    # Additional locations of static files
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        location('assets/build'),
        location('assets/static'),
    )

    # List of finder classes that know how to find static files in
    # various locations.
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    )

    # List of callables that know how to import templates from various sources.
    TEMPLATE_LOADERS = (
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.filesystem.Loader',
        # 'django.template.loaders.eggs.Loader',
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        # Uncomment the next line for simple clickjacking protection:
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    )

    ROOT_URLCONF = 'feedreader.urls'

    WSGI_APPLICATION = 'feedreader.wsgi.application'

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.request",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
    )

    TEMPLATE_DIRS = (
        # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        (os.path.join(BASE_DIR, '../../templates'),)
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

    # Hawk-Authentication for the API calls
    HAWK_MESSAGE_EXPIRATION = 20
    USE_CACHE_FOR_HAWK_NONCE = False  # re-write would do no harm to us

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'djangofeeds',
        'mptt',
        'apps.usercategories',
        'apps.userfeeds'
    ]

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            # 'sentry': {
            #                'level': 'WARNING',
            #                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            #            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
            },
            'apps': {
                'level': 'WARNING',
                'handlers': ['console'],
            },
        }
    }


    BASE_URL = 'http://example.com'

    BASE_URL_HTTPS = 'https://example.com'

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake'
        }
    }

    BROKER_URL = 'Add some broker here'
    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    CELERY_DISABLE_RATE_LIMITS = True

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    REST_FRAMEWORK = {
        # Use hyperlinked styles by default.
        # Only used if the `serializer_class` attribute is not set on a view.
        'DEFAULT_MODEL_SERIALIZER_CLASS':
            'rest_framework.serializers.HyperlinkedModelSerializer',

        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.

        # todo use hawk hre
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ]
    }


class Dev(Base):
    """Settings for development."""
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT') or environment.DEVELOPMENT
    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'debug_toolbar',
    ]
    MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ) + Base.MIDDLEWARE_CLASSES
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'jadfr.conf.base.never_show_debug_toolbar',
    }


class Test(Base):
    """Settings for testing."""
    ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT') or environment.TESTING


class Staging(Base):
    """Settings for a staging system."""
    ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT') or environment.STAGING


class Production(Base):
    """Settings for the production system."""
    ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT') or environment.PRODUCTION
