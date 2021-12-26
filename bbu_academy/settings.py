"""
Django settings for bbu_academy project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from easy_thumbnails.conf import Settings as thumbnailSettings  # Image cropping
from os import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from tools.payme_merchant import get_model

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nnb87jc!tv3a$hw=#pfkb+5y2v=65=on1^2%as@ejl8&zb$^n1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
LOCAL = not bool(environ.get("LOCAL", False))


ALLOWED_HOSTS = ["127.0.0.1", 'tcatb.uz']

# Application definition

INSTALLED_APPS = [
    # Package apps
    'modeltranslation',
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # User apps
    'settings.apps.SettingsConfig',
    'certificates.apps.CertificatesConfig',
    'news.apps.NewsConfig',
    'courses.apps.CoursesConfig',
    'trainings.apps.TrainingsConfig',
    'main_page.apps.MainPageConfig',
    'purchase.apps.PurchaseConfig',
    'payme_billing.apps.PaymeBillingConfig',
    'services.apps.ServicesConfig',
    'small_purchase.apps.SmallPurchaseConfig',
    # Package apps
    'front',  # Edit page text in frontend
    'adminsortable2',  # Drag-n-drop admin sorting
    'ckeditor',  # Text editor
    'image_cropping',  # Crop images
    'easy_thumbnails',  # Create thumbnails
    'django_unused_media',  # Manually deletion unused media
    'django_cleanup.apps.CleanupConfig',  # Auto deletion of unused media
    'formadmin',  # Render forms as in django admin
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'bbu_academy.middleware.LanguageBasedOnUrlMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'bbu_academy.middleware.ProtectPersonalFilesMiddleware',
]

ROOT_URLCONF = 'bbu_academy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'settings.context_processors.page_menu',
                'settings.context_processors.index_link',
                'settings.context_processors.static_information',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'bbu_academy.wsgi.application'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # MySQL
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': str(environ.get("DB_NAME")),
    #         'USER': str(environ.get("DB_USER")),
    #         'PASSWORD': str(environ.get("DB_PASSWORD")),
    #         'HOST': 'localhost',
    #         'PORT': '',
    #         'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    #     }
    # }
    # PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': str(environ.get("DB_NAME")),
            'USER': str(environ.get("DB_USER")),
            'PASSWORD': str(environ.get("DB_PASSWORD")),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ("ru", "Russian"),
    ("uz", "Uzbek"),
)

LOCALE_PATHS = (
    BASE_DIR / "locale",
)

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECURE_SSL_REDIRECT = not LOCAL

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = "/home/wwwtcatb/public_html/media"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = "/home/wwwtcatb/public_html/static"

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Email sending
if LOCAL:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'emails'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = False
EMAIL_HOST = str(environ.get("EMAIL_HOST"))
EMAIL_PORT = 587
EMAIL_HOST_USER = str(environ.get("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(environ.get("EMAIL_HOST_PASSWORD"))
EMAIL_PAYMENT_NOTIFICATION_USER = str(environ.get("EMAIL_PAYMENT_NOTIFICATION_USER"))
# EMAIL_PAYMENT_NOTIFICATION_PASSWORD = str(environ.get("EMAIL_PAYMENT_NOTIFICATION_PASSWORD"))
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = str(environ.get("ADMIN_EMAIL"))
STAFF_MAILS = ["bydev2001@gmail.com", "atb_staff_notifications@tcatb.uz"]


# Packages' settings

# Modeltranslation
MODELTRANSLATION_FALLBACK_LANGUAGES = ('ru', 'uz')

# Image cropping
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnailSettings.THUMBNAIL_PROCESSORS
IMAGE_CROPPING_SIZE_WARNING = True

# Django front
DJANGO_FRONT_EDIT_MODE = "inline"
DJANGO_FRONT_EDITOR_OPTIONS = {
    "toolbar": "Basic",
}

# wkhtmltopdf
PATH_WKHTMLTOPDF = r'static\wkhtmltox\bin\wkhtmltopdf.exe' if LOCAL else r'static/wkhtmltox_linux/usr/local/bin/wkhtmltopdf'

# Payme Billing
PAYME_BILLING_SETTINGS = {
    "test": False,
    "admin": False,  # Display transactions in Django admin
    "web_cash_id": str(environ.get("PAYME_WEB_CASH_ID")),
    "web_cash_key": str(environ.get("PAYME_WEB_CASH_KEY")),
    "test_web_cash_key": str(environ.get("PAYME_WEB_CASH_TEST_KEY")),
    # Function, that receives purchase_id as first positional argument and returns subclass of PaymeMerchantMixin (queryset with a single instance) or None (if not found)
    "billing_models": get_model,
    "callback_time": 4000,  # Time to wait before redirecting to merchant page (in milliseconds)
}
