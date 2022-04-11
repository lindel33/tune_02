# -*- coding: utf-8 -*-
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ljw@!#$uwio5u43u45u35u@#q4utiuopi34io5uodas231123@!#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tune_admin',
    'bot_telegram',
    'price',
    'provider',
    'cost_models',
    'corsheaders',
]

MIDDLEWARE = [
    '**corsheaders.middleware.CorsMiddleware**',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tune.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tune.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'TuneApple$TuneProd',
        'USER': 'TuneApple',
        'PASSWORD': 'tune',
        'OPTIONS': {'charset': 'utf8mb4', },
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/apple/code/project1/tune/static/'
STATIC_URL = '/static/'
#CSRF_COOKIE_SECURE = False
#SESSION_COOKIE_SECURE = False
#STATICFILES_DIRS = [
#    '/home/apple/code/project1/tune/static/',
#    '/home/apple/code/project1/env/lib/python3.8/site-packages/django/contrib/admin/static/',
#]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#SRF_TRUSTED_ORIGINS = ["https://tuneapple.xyz/", "https://www.tuneapple.xyz/"]
#CSRF_TRUSTED_ORIGINS = ["https://tuneapple.xyz/", "https://www.tuneapple.xyz/", "http://tuneapple.xyz/"]
#CORS_ORIGIN_ALLOW_ALL = True
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#USE_X_FORWARDED_HOST = True
#USE_X_FORWARDED_PORT = True
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'TuneApple_cache')
    }
}
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_TRUSTED_ORIGINS = ['https://tuneapple.xyz']
CORS_REPLACE_HTTPS_REFERER = True
CSRF_COOKIE_DOMAIN = 'tuneapple.xyz'
CORS_ORIGIN_WHITELIST = [
        'https://tuneaplle.xyz/',
        'www.tuneapple.xyz',
        'tuneapple.xyz',
]
