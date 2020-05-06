"""
Django settings for django_minio_storage_tests project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from tests.test_app.tests.utils import bucket_name

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "fbkujk%qi0!g$xcz#jah-@#(m%yen^z0dpdatz7hw*=k+&ezgj"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DEFAULT_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"

MINIO_STORAGE_ENDPOINT = os.getenv("MINIO_STORAGE_ENDPOINT", "minio:9000")
MINIO_STORAGE_ACCESS_KEY = "weak_access_key"
MINIO_STORAGE_SECRET_KEY = "weak_secret_key"
MINIO_STORAGE_MEDIA_BUCKET_NAME = bucket_name("tests-media")
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = bucket_name("tests-static")
MINIO_STORAGE_USE_HTTPS = False

MINIO_STORAGE_MEDIA_URL = "http://{}/{}".format(
    MINIO_STORAGE_ENDPOINT, bucket_name("tests-media")
)
# MINIO_STATIC_URL = 'http://localhost:9000/{}'.format(
#     bucket_name("tests-static"))

# MINIO_STORAGE_MEDIA_USE_PRESIGNED = True
# MINIO_STORAGE_STATIC_USE_PRESIGNED = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "minio_storage",
    "test_app",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_minio_storage_tests.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "django_minio_storage_tests.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation" ".MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation" ".CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation" ".NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"
