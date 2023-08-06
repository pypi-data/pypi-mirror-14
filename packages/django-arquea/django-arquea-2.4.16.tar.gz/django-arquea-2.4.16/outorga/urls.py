# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns


urlpatterns = patterns('outorga.views',
                       # (r'^termo/(?P<termo_id>\d+)/$', 'termo'),
                       # (r'^pedido/(?P<pedido_id>\d+)/$', 'pedido'),
                       # (r'escolhe_termo$', 'escolhe_termo'),
                       # (r'escolhe_modalidade$', 'escolhe_modalidade'),
                       # (r'seleciona_termo_natureza$', 'seleciona_termo_natureza'),
                       # (r'seleciona_mod_item_natureza$', 'seleciona_mod_item_natureza'),
                       # (r'seleciona_item_natureza$', 'seleciona_item_natureza'),
                       # (r'relatorios/acordos$', 'gastos_acordos'),
                       # (r'relatorios/acordos/$', 'gastos_acordos'),
                       (r'relatorios/contratos$', 'contratos'),
                       (r'relatorios/contratos/$', 'contratos'),
                       (r'relatorios/contratos/(?P<pdf>\d)$', 'contratos'),

                       (r'relatorios/por_item$', 'por_item'),
                       (r'relatorios/por_item/$', 'por_item'),

                       (r'relatorios/termos$', 'relatorio_termos'),
                       (r'relatorios/termos/$', 'relatorio_termos'),

                       (r'relatorios/lista_acordos$', 'lista_acordos'),
                       (r'relatorios/lista_acordos/$', 'lista_acordos'),
                       (r'relatorios/lista_acordos/(?P<pdf>\d)$', 'lista_acordos'),

                       (r'relatorios/item_modalidade$', 'item_modalidade'),
                       (r'relatorios/item_modalidade/$', 'item_modalidade'),
                       (r'relatorios/item_modalidade/(?P<pdf>\d)$', 'item_modalidade'),

                       (r'relatorios/acordo_progressivo$', 'acordo_progressivo'),
                       (r'relatorios/acordo_progressivo/$', 'acordo_progressivo'),
                       (r'relatorios/acordo_progressivo/(?P<pdf>\d)$', 'acordo_progressivo'),

                       (r'json/termo_datas$', 'ajax_termo_datas'),
                       (r'json/termo_parciais$', 'ajax_termo_parciais'),
                       )
