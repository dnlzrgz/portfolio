"""
Django settings for portfolio project.
"""

from datetime import timedelta
from pathlib import Path
from environs import Env

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = Env()
env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY",
    "django-insecure-&r9rcqb*2b-pxu)j!q+$e!(#&t=5^v=l3tivxte28cvd^9^w8q",
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    ["*"],
)

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
    "base",
    "home",
    "blog",
    "projects",
    "search",
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
    "modelcluster",
    "taggit",
    "axes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "axes.middleware.AxesMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]


if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
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
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.str("POSTGRES_PORT", 5432),
        "ATOMIC_REQUESTS": env.bool("DATABASE_ATOMIC_REQUESTS", True),
        "CONN_MAX_AGE": env.int("DATABASE_CONN_MAX_AGE", default=60),
    },
}


# Cache
# https://docs.djangoproject.com/en/5.0/topics/cache/

if env.bool("USE_CACHE", False):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": env.str("CACHE_TABLE", "cache_table"),
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

CACHE_TIMEOUT_SECONDS = env.int("CACHE_TIMEOUT_SECONDS", 0)


# Authentication backends
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#specifying-authentication-backends

AUTHENTICATION_BACKENDS = (
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
)


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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

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
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if env.bool("USE_S3_STORAGE", False):
    INSTALLED_APPS += ["storages"]

    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME")
    AWS_DEFAULT_ACL = env.str("AWS_DEFAULT_ACL", "public-read")
    AWS_QUERYSTRING_AUTH = False

    _AWS_EXPIRY = env.int("AWS_EXPIRY", 60 * 60 * 24 * 7)
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": f"max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate",
    }

    AWS_S3_MAX_MEMORY_SIZE = env.int(
        "AWS_S3_MAX_MEMORY_SIZE",
        5_000_000,  # 5MB
    )

    AWS_LOCATION = "static"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "media",
            "file_overwrite": False,
        },
    }


WHITENOISE_MAX_AGE = env.int("WHITENOISE_MAX_AGE", 0)


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

WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "subscript",
                "link",
            ],
        },
    },
    "minimal": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "strikethrough",
                "link",
            ],
        },
    },
    "full": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "h2",
                "h3",
                "h4",
                "bold",
                "italic",
                "strikethrough",
                "ol",
                "ul",
                "link",
                "hr",
                "image",
                "embed",
                "code",
                "document-link",
                "blockquote",
            ],
        },
    },
}

WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
    },
]

# Images
WAGTAILIMAGES_AVIF_QUALITY = env.int("WAGTAILIMAGES_AVIF_QUALITY", 50)
WAGTAILIMAGES_JPEG_QUALITY = env.int("WAGTAILIMAGES_JPEG_QUALITY", 40)
WAGTAILIMAGES_WEBP_QUALITY = env.int("WAGTAILIMAGES_WEBP_QUALITY", 45)

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


# CSRF
# https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    [],
)

CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", False)


# Security related settings
# https://docs.djangoproject.com/en/5.0/topics/security/

SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", False)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", False)

if env.bool("SECURE_PROXY_SSL_HEADER", False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", False)

SECURE_CONTENT_TYPE_NOSNIFF = env.bool("SECURE_CONTENT_TYPE_NOSNIFF", False)


# Axes
# https://django-axes.readthedocs.io/en/latest/4_configuration.html

AXES_ENABLED = env.bool("AXES_ENABLED", True)
AXES_FAILURE_LIMIT = env.int("AXES_FAILURE_LIMIT", 3)
AXES_LOCK_OUT_AT_FAILURE = env.bool("AXES_LOCK_OUT_AT_FAILURE", True)
AXES_COOLOFF_TIME = lambda request: timedelta(hours=env.int("AXES_COOLOFF_TIME", 24))

AXES_IPWARE_META_PRECEDENCE_ORDER = [
    "HTTP_CF_CONNECTING_IP",
    "HTTP_X_FORWARDED_FOR",
    "REMOTE_ADDR",
]


# Logging
# https://docs.djangoproject.com/en/5.0/topics/logging/

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}
