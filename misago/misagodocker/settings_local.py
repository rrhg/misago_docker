"""
Django settings for misagodocker project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

from misago import load_plugin_list_if_exists

from .utils import strtobool, strtolist


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Define placeholder gettext function
# This function will mark strings in settings visible to makemessages
# without need for Django's i18n features be initialized first.
_ = lambda s: s


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MISAGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get('MISAGO_DEBUG'))


# A list of strings representing the host/domain names that this Django site can serve.
# If you are unsure, just enter here your domain name, eg. ['mysite.com', 'www.mysite.com']

# ALLOWED_HOSTS = strtolist(os.environ.get('VIRTUAL_HOST'))
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # Misago requires PostgreSQL to run
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_USER'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': 5432,
    }
}


# Caching
# https://docs.djangoproject.com/en/1.11/topics/cache/#setting-up-the-cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        'OPTIONS': {
            'user_attributes': ['username', 'email'],
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = os.environ.get('MISAGO_LANGUAGE_CODE', 'en-us')

TIME_ZONE = os.environ.get('MISAGO_TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# User uploads (Avatars, Attachments, files uploaded in other Django apps, ect.)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

MEDIA_URL = '/media/'


# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/1.11/ref/settings/#static-root

STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Absolute filesystem path to the directory that will hold user-uploaded files.
# https://docs.djangoproject.com/en/1.11/ref/settings/#media-root

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# https://docs.djangoproject.com/en/1.10/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'theme', 'static'),
]


# Fingerprint static files
# Includes small version checksum at end of every static file,
# forcing browser to download new version when file contents change.

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


# Email configuration
# https://docs.djangoproject.com/en/1.11/ref/settings/#email-backend

# Misago Docker autoconfigures the email provider based on user preferences

if os.environ.get('MISAGO_EMAIL_PROVIDER') == "smtp":
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_SSL = strtobool(os.environ['MISAGO_EMAIL_USE_SSL'])
    EMAIL_USE_TLS = strtobool(os.environ['MISAGO_EMAIL_USE_TLS'])
    EMAIL_HOST = os.environ['MISAGO_EMAIL_HOST']
    EMAIL_HOST_PASSWORD = os.environ['MISAGO_EMAIL_PASSWORD']
    EMAIL_HOST_USER = os.environ['MISAGO_EMAIL_USER']
    EMAIL_PORT =  os.environ['MISAGO_EMAIL_PORT']
elif os.environ.get('MISAGO_EMAIL_PROVIDER') == "gmail":
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_PASSWORD = os.environ['MISAGO_GMAIL_PASSWORD']
    EMAIL_HOST_USER = os.environ['MISAGO_GMAIL_USER']
    EMAIL_PORT = 587
elif os.environ.get('MISAGO_EMAIL_PROVIDER') == "mailjet":
    EMAIL_BACKEND = 'anymail.backends.mailjet.EmailBackend'
    ANYMAIL = {
        'MAILJET_API_KEY': os.environ['MISAGO_MAILJET_API_KEY_PUBLIC'],
        'MAILJET_SECRET_KEY': os.environ['MISAGO_MAILJET_API_KEY_PRIVATE'],
    }
elif os.environ.get('MISAGO_EMAIL_PROVIDER') == "sendinblue":
    EMAIL_BACKEND = 'anymail.backends.sendinblue.EmailBackend'
    ANYMAIL = {
        'SENDINBLUE_API_KEY': os.environ['MISAGO_SENDINBLUE_API_KEY'],
    }
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Default email address to use for various automated correspondence from the site manager(s).

DEFAULT_FROM_EMAIL = os.environ.get('MISAGO_DEFAULT_FROM_EMAIL', '')


# Application definition

AUTH_USER_MODEL = 'misago_users.User'

AUTHENTICATION_BACKENDS = [
    'misago.users.authbackends.MisagoBackend',
]

CSRF_COOKIE_NAME = 'misagocsrftoken'
CSRF_COOKIE_SECURE = True

CSRF_FAILURE_VIEW = 'misago.core.errorpages.csrf_failure'

PLUGINS_LIST_PATH = os.path.join(BASE_DIR, "plugins.txt")

INSTALLED_PLUGINS = load_plugin_list_if_exists(PLUGINS_LIST_PATH) or []

INSTALLED_APPS = INSTALLED_PLUGINS + [
    # Misago overrides for Django core feature
    'misago',
    'misago.users',

    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.postgres",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd party apps used by Misago
    "ariadne.contrib.django",
    "celery",
    "debug_toolbar",
    "mptt",
    "rest_framework",
    "social_django",

    # Misago apps
    "misago.admin",
    "misago.acl",
    "misago.analytics",
    "misago.cache",
    "misago.core",
    "misago.conf",
    "misago.icons",
    "misago.themes",
    "misago.markup",
    "misago.legal",
    "misago.categories",
    "misago.threads",
    "misago.readtracker",
    "misago.search",
    "misago.socialauth",
    "misago.graphql",
    "misago.faker",
    "misago.menus",
    "misago.sso",
    "misago.plugins",
]

INTERNAL_IPS = [
    '127.0.0.1'
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGIN_REDIRECT_URL = 'misago:index'

LOGIN_URL = 'misago:login'

LOGOUT_URL = 'misago:logout'

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    "misago.users.middleware.RealIPMiddleware",
    "misago.core.middleware.FrontendContextMiddleware",

    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "misago.cache.middleware.cache_versions_middleware",
    "misago.conf.middleware.dynamic_settings_middleware",
    "misago.socialauth.middleware.socialauth_providers_middleware",
    "misago.users.middleware.UserMiddleware",
    "misago.acl.middleware.user_acl_middleware",
    "misago.core.middleware.ExceptionHandlerMiddleware",
    "misago.users.middleware.OnlineTrackerMiddleware",
    "misago.admin.middleware.AdminAuthMiddleware",
    "misago.threads.middleware.UnreadThreadsCountMiddleware",
]

ROOT_URLCONF = 'misagodocker.urls'

SESSION_COOKIE_NAME = 'misagosessionid'
SESSION_COOKIE_SECURE = True

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

SOCIAL_AUTH_STRATEGY = "misago.socialauth.strategy.MisagoStrategy"

SOCIAL_AUTH_PIPELINE = (
    # Steps required by social pipeline to work - don't delete those!
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',

    # If enabled in admin panel, lets your users to associate their old forum account
    # with social one, if both have same e-mail address.
    "misago.socialauth.pipeline.associate_by_email",

    # Those steps make sure banned users may not join your site or use banned name or email.
    'misago.socialauth.pipeline.validate_ip_not_banned',
    'misago.socialauth.pipeline.validate_user_not_banned',

    # Reads user data received from social site and tries to create valid and available username
    # Required if you want automatic account creation to work. Otherwhise optional.
    'misago.socialauth.pipeline.get_username',

    # Uncomment next line to enable automatic account creation if data from social site is valid
    # and get_username found valid name for new user account:
    # 'misago.socialauth.pipeline.create_user',

    # This step asks user to complete simple, pre filled registration form containing username,
    # email, legal note if you remove it without adding custom one, users will have no fallback
    # for joining your site using their social account.
    'misago.socialauth.pipeline.create_user_with_form',

    # Steps finalizing social authentication flow - don't delete those!
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'misago.socialauth.pipeline.require_activation',
)

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'theme', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                "misago.acl.context_processors.user_acl",
                "misago.conf.context_processors.conf",
                "misago.conf.context_processors.og_image",
                "misago.core.context_processors.misago_version",
                "misago.core.context_processors.request_path",
                "misago.core.context_processors.momentjs_locale",
                "misago.icons.context_processors.icons",
                "misago.search.context_processors.search_providers",
                "misago.themes.context_processors.theme",
                "misago.legal.context_processors.legal_links",
                "misago.menus.context_processors.menus",
                "misago.users.context_processors.user_links",
                "misago.core.context_processors.hooks",

                # Data preloaders
                "misago.conf.context_processors.preload_settings_json",
                "misago.core.context_processors.current_link",
                "misago.markup.context_processors.preload_api_url",
                "misago.threads.context_processors.preload_threads_urls",
                "misago.users.context_processors.preload_user_json",
                "misago.socialauth.context_processors.preload_socialauth_json",

                # Note: keep frontend_context processor last for previous processors
                # to be able to expose data UI app via request.frontend_context
                'misago.core.context_processors.frontend_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'misagodocker.wsgi.application'


# Django Debug Toolbar
# http://django-debug-toolbar.readthedocs.io/en/stable/configuration.html

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',

    'misago.acl.panels.MisagoACLPanel',

    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
]


# Django Rest Framework
# http://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'misago.core.rest_permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'misago.core.exceptionhandler.handle_api_exception',
    'UNAUTHENTICATED_USER': 'misago.users.models.AnonymousUser',
    'URL_FORMAT_OVERRIDE': None,
}


# Celery - Distributed Task Queue
# http://docs.celeryproject.org/en/latest/userguide/configuration.html

# Configure Celery to use Redis as message broker.

CELERY_BROKER_URL = "redis://redis/0"

# Celery workers may leak the memory, eventually depriving the instance of resources.
# This setting forces celery to stop worker, clean after it and create new one
# after worker has processed 10 tasks.

CELERY_WORKER_MAX_TASKS_PER_CHILD = 10


# Default logging configuration
# Logs errors to /logs/misago.log, rotates them every week

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process} {thread} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime}] {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'logs', 'misago.log'),
            'when': 'W0', # Rotate logs on mondays
        },
        'celery': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'logs', 'celery.log'),
            'when': 'W0', # Rotate logs on mondays
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['celery'],
            'level': 'INFO',
        },
    },
}


# Enable sentry for logging, if Sentry DNS is specified
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=os.environ['SENTRY_DSN'],
        integrations=[DjangoIntegration()]
    )


# Misago specific settings
# https://misago.readthedocs.io/en/latest/developers/settings.html


# PostgreSQL text search configuration to use in searches
# Defaults to "simple", for list of installed configurations run "\dF" in "psql".
# Standard configs as of PostgreSQL 9.5 are: dutch, english, finnish, french,
# german, hungarian, italian, norwegian, portuguese, romanian, russian, simple,
# spanish, swedish and turkish
# Example on adding custom language can be found here: https://github.com/lemonskyjwt/plpstgrssearch

MISAGO_SEARCH_CONFIG = os.environ.get('MISAGO_SEARCH_CONFIG', 'simple')


# Path to the directory that Misago should use to prepare user data downloads.
# Should not be accessible from internet.

MISAGO_USER_DATA_DOWNLOADS_WORKING_DIR = os.path.join(BASE_DIR, 'userdata')


# Path to directory containing avatar galleries
# Those galleries can be loaded by running loadavatargallery command

MISAGO_AVATAR_GALLERY = os.path.join(BASE_DIR, 'avatargallery')


# Profile fields

MISAGO_PROFILE_FIELDS = [
    {
        'name': _("Personal"),
        'fields': [
            'misago.users.profilefields.default.RealNameField',
            'misago.users.profilefields.default.GenderField',
            'misago.users.profilefields.default.BioField',
            'misago.users.profilefields.default.LocationField',
        ],
    },
    {
        'name': _("Contact"),
        'fields': [
            'misago.users.profilefields.default.TwitterHandleField',
            'misago.users.profilefields.default.SkypeIdField',
            'misago.users.profilefields.default.WebsiteField',
        ],
    },
    {
        'name': _("IP address"),
        'fields': [
            'misago.users.profilefields.default.JoinIpField',
        ],
    },
]


# Display threads instead of categories on forum index?

MISAGO_THREADS_ON_INDEX = os.environ.get('MISAGO_INDEX', "threads") == "threads"


# Import settings override
try:
    from .settings_override import *
except ImportError:
    pass