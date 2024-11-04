# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import django.contrib.auth
from pathlib import Path

# te da la ruta de donde parte el directorio inicial ej: c:\vportfolio\pportfolio\appportfolio, llevaría a vportfolio, porque el parent.parent
#                                   da dos saltos para atrás
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-x)9e4m28q3j!ce0%b2)nnzx2-r&&*5qnv86o4$9wy-jt#v43&d'

# true: en desarrollo | false: en nube
DEBUG = True

#los host permitidos
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appportfolio',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pportfolio.urls'
WSGI_APPLICATION = 'pportfolio.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

#donde se le dice la base de datos
if DEBUG == True:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if DEBUG == False:
    print("**************************DESARROLLO EN LOCAL")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'vportfolio',
            'USER': 'postgres',
            'PASSWORD': 'Adivinala1.',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

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

SITE_ID = 1
SITE_NAME = "Portfolio"
LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'djblets.siteconfig.context_processors.siteconfig',
    'djblets.util.context_processors.settingsVars',
    'djblets.util.context_processors.siteRoot',
    'djblets.util.context_processors.ajaxSerial',
    'djblets.util.context_processors.mediaSerial',
	'django.template.context_processors.request',)

#la parte estática es obligatoria para Heroku y para nuestra máquina
STATIC_URL = '/static/'    #js, css3, ..
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'  #videos, imágenes
STATIC_ROOT= os.path.join(BASE_DIR, 'static')

# declara la ruta donde se enlazará el contenido estático
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
	('css', os.path.join(STATIC_ROOT, 'css')),
	('js', os.path.join(STATIC_ROOT, 'js')),
	('images', os.path.join(STATIC_ROOT, 'images')),
	('img', os.path.join(STATIC_ROOT, 'img')),
)
# List of finder classes that know how to find static files in | se encarga de buscar los ficheros en ejecución del proyecto
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
)
