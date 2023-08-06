# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns


urlpatterns = patterns('protocolo.views',
                       (r'^(?P<prot_id>\d+)/cotacoes/$', 'cotacoes', None, 'cotacoes'),
                       (r'escolhe_termo$', 'escolhe_termo'),
                       # (r'listagem/(?P<t_id>\d+)$', 'lista_protocolos'),
                       (r'descricao$', 'protocolos_descricao'),
                       (r'descricao/(?P<pdf>\d)$', 'protocolos_descricao'),
                       )