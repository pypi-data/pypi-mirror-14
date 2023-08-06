# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('identificacao.views',
                       (r'escolhe_entidade$', 'ajax_escolhe_entidade'),
                       (r'escolhe_endereco$', 'ajax_escolhe_endereco'),
                       (r'escolhe_entidade_filhos$', 'ajax_escolhe_entidade_filhos'),
                       (r'relatorios/arquivos$', 'arquivos_entidade'),
                       (r'agenda/(?P<pdf>[a-z]+)/(?P<tipo>\d+)$', 'agenda'),
                       (r'agenda/(?P<pdf>[a-z]+)$', 'agenda'),
                       (r'agenda/(?P<tipo>\d+)/$', 'agenda'),
                       (r'agenda$', 'agenda'),
                       (r'acessos/terremark$', 'acessos_terremark'),
                       (r'ecossistema/(?P<tipo>[a-z]+)$', 'planilha_ecossistema'),
                       )
