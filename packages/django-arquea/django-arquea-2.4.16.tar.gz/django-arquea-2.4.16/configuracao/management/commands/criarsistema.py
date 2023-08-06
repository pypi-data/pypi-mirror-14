# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = (u"Modifica um projeto Django para rodar o Sistema, com as configurações "
            u"padrão já criadas.")

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='projeto', nargs=1)

    def handle(self, *args, **options):
        if len(args) < 1:
            self.stdout.write('Projeto faltando')
            return

        project_name = args[0]

        urls = open('%s/urls.py' % project_name, 'w')
        settings = open('%s/settings.py' % project_name, 'w')

        urls.write("""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

try:
    import ckeditor.urls
    ck = ''
except ImportError:
    ck = '_uploader'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^files/(?P<filename>.*)', 'utils.views.serve_files'),
    url(r'^protocolo/', include('protocolo.urls')),
    url(r'^patrimonio/', include('patrimonio.urls')),
    url(r'^financeiro/', include('financeiro.urls')),
    url(r'^outorga/', include('outorga.urls')),
    url(r'^memorando/', include('memorando.urls')),
    url(r'^identificacao/', include('identificacao.urls')),
    url(r'^membro/', include('membro.urls')),
    url(r'^rede/', include('rede.urls')),
    url(r'^processo/', include('processo.urls')),
    url(r'^verificacao/', include('verificacao.urls')),
    url(r'^repositorio/', include('repositorio.urls')),
    url(r'^carga/', include('carga.urls')),
    url(r'^configuracao/', include('configuracao.urls')),
    url(r'^verifica$', 'utils.views.verifica'),
    url(r'^sempermissao$', TemplateView.as_view(template_name="401.html")),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^ckeditor/', include('ckeditor%s.urls' % ck)),
    url(r'^', include(admin.site.urls)),
)
        """)

        # Create a random SECRET_KEY to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)

        settings.write("""
\"\"\"
Django settings for %s project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
\"\"\"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
        'configuracao',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'carga',
        'evento',
        'financeiro',
        'identificacao',
        'membro',
        'memorando',
        'outorga',
        'patrimonio',
        'processo',
        'protocolo',
        'rede',
        'verificacao',
        'repositorio',
        'utils',
        'ckeditor',
        'tinymce',
        'import_export',
        'treemenus',
        'menuextension',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.request_cache.RequestCacheMiddleware',
)

ROOT_URLCONF = '%s.urls'

WSGI_APPLICATION = '%s.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static/'


TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
        'utils.context_processors.debug',
        'utils.context_processors.sistema',
    )

CKEDITOR_UPLOAD_PATH = 'ckeditor/'

MEDIA_ROOT = '/var/www/files'
MEDIA_URL = '/files/'
        """ % (project_name, secret_key, project_name, project_name))
