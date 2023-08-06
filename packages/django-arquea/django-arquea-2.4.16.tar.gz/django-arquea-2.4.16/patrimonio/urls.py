# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns


urlpatterns = patterns('patrimonio.views',
                       #     (r'escolhe_termo$', 'ajax_escolhe_termo'),
                       #    (r'escolhe_protocolo$', 'ajax_escolhe_protocolo'),
                       (r'escolhe_pagamento$', 'ajax_escolhe_pagamento'),
                       (r'escolhe_entidade$', 'ajax_escolhe_entidade'),
                       (r'escolhe_patrimonio$', 'ajax_escolhe_patrimonio'),
                       (r'escolhe_equipamento$', 'ajax_escolhe_equipamento'),
                       #    (r'escolhe_detalhe$', 'ajax_escolhe_detalhe'),
                       (r'filtra_pn_estado$', 'ajax_filtra_pn_estado'),
                       #    (r'patrimonio_existente$', 'ajax_patrimonio_existente'),
                       (r'relatorio/por_estado$', 'por_estado'),

                       (r'relatorio/por_tipo$', 'por_tipo'),
                       (r'relatorio/por_tipo/$', 'por_tipo'),

                       (r'relatorio/por_tipo_consignado$', 'por_tipo_consignado'),
                       (r'relatorio/por_tipo_consignado/$', 'por_tipo_consignado'),

                       (r'relatorio/por_marca$', 'por_marca'),
                       (r'relatorio/por_marca/(?P<pdf>\d)$', 'por_marca'),
                       (r'relatorio/por_local$', 'por_local'),
                       (r'relatorio/por_local/(?P<pdf>\d)$', 'por_local'),
                       (r'relatorio/por_local_termo$', 'por_local_termo'),
                       (r'relatorio/por_local_termo/(?P<pdf>\d)$', 'por_local_termo'),
                       (r'relatorio/por_local_rack$', 'por_local_rack'),
                       (r'relatorio/por_local_rack/(?P<pdf>\d)$', 'por_local_rack'),
                       (r'relatorio/por_termo$', 'por_termo'),
                       (r'relatorio/por_termo/(?P<pdf>\d)$', 'por_termo'),
                       (r'relatorio/por_tipo_equipamento$', 'por_tipo_equipamento'),
                       (r'relatorio/por_tipo_equipamento2$', 'por_tipo_equipamento2'),
                       (r'relatorio/presta_contas$', 'presta_contas'),
                       (r'abre_arvore$', 'ajax_abre_arvore'),
                       (r'abre_arvore_tipo$', 'ajax_abre_arvore_tipo'),
                       (r'racks$', 'racks'),
                       (r'relatorio_rack$', 'relatorio_rack'),
                       (r'patrimonio_historico$', 'ajax_patrimonio_historico'),
                       (r'ajax_get_equipamento$', 'ajax_get_equipamento'),
                       (r'ajax_get_procedencia_filter_tipo$', 'ajax_get_procedencia_filter_tipo'),
                       (r'ajax_get_marcas_por_termo$', 'ajax_get_marcas_por_termo'),
                       (r'planta_baixa_edit$', 'planta_baixa_edit'),
                       )
