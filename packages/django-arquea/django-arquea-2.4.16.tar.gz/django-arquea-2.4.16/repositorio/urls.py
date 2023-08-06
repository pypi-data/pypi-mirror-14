# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns


urlpatterns = patterns('repositorio.views',
                       (r'seleciona_patrimonios$', 'ajax_seleciona_patrimonios'),
                       (r'ajax_repositorio_tipo_nomes$', 'ajax_repositorio_tipo_nomes'),
                       (r'relatorio/repositorio$', 'relatorio_repositorio'),
                       (r'relatorio/repositorio/(?P<pdf>\d)$', 'relatorio_repositorio'),
                       )
