"""
Django settings

"""
import ast
import os
from typing import Any, Optional

from django.core.exceptions import ImproperlyConfigured

import structlog


def get_env_variable(var_name: str, default: Optional[str] = None) -> Any:
    if default:
        value = os.environ.get(var_name, default)
    else:
        value = os.environ[var_name]
    return ast.literal_eval(value)


ENV = os.environ["ENV"]

if ENV not in ("dev", "prod", "staging", "test"):
    raise ImproperlyConfigured("Unknown environment for settings: " + ENV)

DEBUG = get_env_variable("DEBUG", "False")

if ENV == "prod" and DEBUG:
    raise ImproperlyConfigured("DEBUG = True is not allowed in production")


# #########
#   PATHS
# #########

CONF_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CONF_DIR)
ROOT_DIR = os.path.dirname(PROJECT_DIR)

if ENV in ("prod", "staging"):
    MEDIA_ROOT = os.environ["MEDIA_ROOT"]
    STATIC_ROOT = os.environ["STATIC_ROOT"]
else:
    # No need for static root in development
    MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
    if not os.path.exists(MEDIA_ROOT):
        os.mkdir(MEDIA_ROOT)

# #####################
#   APPS & MIDDLEWARE
# #####################

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
    "django_celery_beat",
    "django_extensions",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "django_structlog.middlewares.CeleryMiddleware",
]

if ENV == "dev" and DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

# ##############
#   WEB SERVER
# ##############

ROOT_URLCONF = "project.conf.urls"

WSGI_APPLICATION = "project.conf.wsgi.application"

if ENV == "dev":
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

# ############
#   DATABASE
# ############

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}

# ###########
#   CACHING
# ###########

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# ############
#   SECURITY
# ############

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Basic security settings. We're not going to deal with HSTS settings, at least
# for now since there is nothing that specifically needs protecting.

# Redirect HTTP requests to HTTPS, but only in production
SECURE_SSL_REDIRECT = ENV == "prod"
# Set the "X-Content-Type-Options: nosniff" header if it is not set already.
SECURE_CONTENT_TYPE_NOSNIFF = True
# Don't send the session cookie unless the connection is secure.
SESSION_COOKIE_SECURE = True
# Tell the browser not to allow access to the cookie via javascript.
SESSION_COOKIE_HTTPONLY = True
# Don't send the CSRF cookie unless the connection is secure.
CSRF_COOKIE_SECURE = True

# #############
#   TEMPLATES
# #############

# The configuration will use the filesystem and app_directories loaders
# by default and enable the caching loader in production.

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(ROOT_DIR, "templates"),
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

if ENV in ("prod", "staging"):
    TEMPLATES[0]["APP_DIRS"] = False
    TEMPLATES[0]["OPTIONS"]["loaders"] = [  # type: ignore
        (
            "django.template.loaders.cached.Loader",
            [
                "django_spaceless_templates.loaders.filesystem.Loader",
                "django_spaceless_templates.loaders.app_directories.Loader",
            ],
        )
    ]


# ########################
#   INTERNATIONALIZATION
# ########################

LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(ROOT_DIR, "locale"),
]

# ################
#   STATIC FILES
# ################

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, "static"),
    os.path.join(PROJECT_DIR, "static"),
]

if ENV in ("prod", "staging"):
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# ###########
#   LOGGING
# ###########

# In general (production, staging, test) log everything to the console and
# leave the decision on where to store the messages to the environment in
# which Django is running, see https://12factor.net/logs.
#
# For development, log messages are also written to a file, so you can see
# whether the information being logged is actually useful, and you can act
# on it. A RotatingFileHandler is used so the log files don't get too big,
# and they don't need to be cleaned out all the time.
#
# Log messages from requests, celery and the site are generated by structlog.
# while Django and third-party apps generally use standard python logging.
# Django's logging configuration is used to define the handlers and
# formatters for processing log messages. However, it does not seem possible
# to mix the two types of log records since structlog formatters often use
# attributes that are not available on standard python records. Fortunately
# the "propagate" attribute makes it easy to maintain separation between
# the two pipelines until they are written to either the console or a file.
#
# The logging configuration also include overrides for the default loggers
# created by Django, for example, 'django.server' which is added for the
# runserver management command. This was done so the logger could be turned
# off to keep the console output equivalent to what would be seen in the
# production environment.

LOG_LEVEL = os.environ.get("LOG_LEVEL", "ERROR")

if LOG_LEVEL not in ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"):
    raise ImproperlyConfigured("Unknown level for logging: " + LOG_LEVEL)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} [{levelname}] {message}",
            "style": "{",
        },
        "structlog.json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "structlog.key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=["timestamp", "level", "event", "logger"]
            ),
        },
        "structlog.console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "structlog.console": {
            "class": "logging.StreamHandler",
            "formatter": "structlog.console",
        },
    },
    "loggers": {
        "root": {
            "handlers": ["structlog.console"],
            "level": LOG_LEVEL,
        },
    },
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,  # noqa
    cache_logger_on_first_use=not DEBUG,
)

# ##########
#   SENTRY
# ##########

if get_env_variable("SENTRY_ENABLED", "False"):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(  # type: ignore
        os.environ["SENTRY_DSN"],
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
        ],
    )

# #########
#   EMAIL
# #########

EMAIL_ENABLED = get_env_variable("EMAIL_ENABLED", "False")

if EMAIL_ENABLED:
    DEFAULT_FROM_EMAIL = os.environ["DEFAULT_FROM_EMAIL"]
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = os.environ["EMAIL_PORT"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_USE_SSL = get_env_variable("EMAIL_USE_SSL")
    SERVER_EMAIL = os.environ["SERVER_EMAIL"]
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ########
#   SITE
# ########

SITE_SCHEME = os.environ.get("SITE_SCHEME", "http")
SITE_ID = int(os.environ["DJANGO_SITE_ID"])
SITE_ADMIN_PATH = os.environ.get("SITE_ADMIN_PATH", "admin")

# ##########
#   PEOPLE
# ##########

ADMINS = get_env_variable("ADMINS")
MANAGERS = get_env_variable("MANAGERS")
