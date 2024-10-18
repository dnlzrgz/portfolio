"""
Django settings for portfolio project.
"""

from pathlib import Path
from environs import Env

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

WAGTAIL_ADMIN_URL = env.str("WAGTAIL_ADMIN_URL", "admin/")

DJANGO_ADMIN_URL = env.str("DJANGO_ADMIN_URL", "django-admin/")

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Application definition

INSTALLED_APPS = [
    # local
    "base",
    "blog",
    "projects",
    "search",
    # Wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.frontend_cache",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "portfolio.apps.CustomImagesAppConfig",
    # "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    # 3rd party
    "modelcluster",
    "taggit",
    "bakery",
    "wagtailbakery",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


ROOT_URLCONF = "portfolio.urls"

APPEND_SLASH = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "init_command": (
                "PRAGMA foreign_keys = ON;"
                "PRAGMA journal_mode = WAL;"
                "PRAGMA synchronous = NORMAL;"
                "PRAGMA busy_timeout = 5000;"
                "PRAGMA temp_store = MEMORY;"
                "PRAGMA mmap_size = 134217728;"
                "PRAGMA journal_size_limit = 67108864;"
                "PRAGMA cache_size = 2000;"
            ),
            "transaction_mode": "IMMEDIATE",
        },
    }
}

# Authentication backends
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#specifying-authentication-backends

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en-us")

TIME_ZONE = env.str("TIME_ZONE", "UTC")

USE_I18N = env.bool("USE_I18N", True)

USE_TZ = env.bool("USE_TZ", True)

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Wagtail settings

WAGTAIL_SITE_NAME = env.str("WAGTAIL_SITE_NAME", "portfolio")

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", "http://example.com")

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
    },
]

# Images
WAGTAILIMAGES_AVIF_QUALITY = env.int("WAGTAIL_IMAGES_AVIF_QUALITY", 50)
WAGTAILIMAGES_JPEG_QUALITY = env.int("WAGTAIL_IMAGES_JPEG_QUALITY", 40)
WAGTAILIMAGES_WEBP_QUALITY = env.int("WAGTAIL_IMAGES_WEBP_QUALITY", 45)

# Private pages
WAGTAIL_PRIVATE_PAGE_OPTIONS = {"SHARED_PASSWORD": True}


# Frontend cache invalidator
# https://docs.wagtail.org/en/stable/reference/contrib/frontendcache.html

if env.bool("USE_CLOUDFARE_CACHE", False):
    WAGTAILFRONTENDCACHE = {
        "cloudflare": {
            "BACKEND": "wagtail.contrib.frontend_cache.backends.CloudflareBackend",
            "BEARER_TOKEN": env.str("CLOUDFARE_BEARER_TOKEN"),
            "ZONEID": env.str("CLOUDFARE_ZONE_ID"),
        },
    }


# Bakery
# https://github.com/wagtail-nest/wagtail-bakery

BAKERY_MULTISITE = env.bool("WAGTAIL_BAKERY_MULTISITE", False)

BUILD_DIR = env.str("WAGTAIL_BAKERY_BUILD_DIR", "/tmp/build/")

BAKERY_VIEWS = ("wagtailbakery.views.AllPublishedPagesView",)


# Logging
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env.str("DJANGO_LOG_LEVEL", "INFO"),
        },
    },
}
