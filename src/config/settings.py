import pymysql
import os
pymysql.install_as_MySQLdb()

from pathlib import Path
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_KEY = 'django-insecure-7f#^w@b*kf5qvty(k@*(w)^s5rnt%09ija9$%2j7l_%b@#d@$$'
DEBUG = True
ALLOWED_HOSTS = []
DJANGO_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_filters',
    'corsheaders',
]

LOCAL_APP = [
    'manage_users',
    'master_data',
    'pasien',
    'surat',
] 

INSTALLED_APPS = DJANGO_APPS + LOCAL_APP 


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates') 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'breadcrumb_tags': 'config.templatetags.breadcrumb_tags',
                'custom_tags': 'config.templatetags.tags'
            }
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'    : config("DB_CONNECTION", default='django.db.backends.mysql'),
        'USER'      : config('DB_USER', default='root'),
        'NAME'      : config('DB_NAME'),
        'PASSWORD'  : config('DB_PASSWORD', default=''),
        'HOST'      : config('DB_HOST', default='localhost'),
        'PORT'      : config('DB_PORT', default='3306'),
    },
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static') 
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'manage_users.AccountUser'

JAZZMIN_SETTINGS = {
    "site_title": "Admin Klinik",
    "site_header": "Admin Klinik",
    "copyright": "Admin Klinik",
    # icon

    # custom list sidebar
    "order_with_respect_to": ["auth"],
    "navigation_expanded": False,
}


GOOGLE_CREDENTIALS = config("GOOGLE_CREDENTIALS", "./credentials.json")