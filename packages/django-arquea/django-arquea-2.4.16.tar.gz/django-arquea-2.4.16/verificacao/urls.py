# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('verificacao.views',
                       (r'versao$', 'versao'),
                       (r'relatorio/equipamento_consolidado$', 'equipamento_consolidado'),
                       (r'relatorio/equipamento_part_number_modelo_vazio$', 'equipamento_part_number_modelo_vazio'),
                       (r'relatorio/equipamento_part_number_vazio$', 'equipamento_part_number_vazio'),
                       (r'relatorio/equipamento_part_number_modelo_diferente$',
                        'equipamento_part_number_modelo_diferente'),
                       (r'relatorio/equipamento_marca_vazia$', 'equipamento_marca_vazia'),

                       (r'relatorio/patrimonio_consolidado$', 'patrimonio_consolidado'),
                       (r'relatorio/patrimonio_equipamento_vazio$', 'patrimonio_equipamento_vazio'),
                       (r'relatorio/patrimonio_equipamento_descricao_diferente$',
                        'patrimonio_equipamento_descricao_diferente'),
                       (r'relatorio/patrimonio_procedencia_vazia$', 'patrimonio_procedencia_vazia'),
                       (r'relatorio/patrimonio_localidade_diferente', 'patrimonio_localidade_diferente'),

                       (r'relatorio/check_patrimonio_equipamento$', 'check_patrimonio_equipamento'),

                       (r'relatorio/patrimonio_equipamento_marca_diferente$', 'patrimonio_equipamento_marca_diferente'),
                       (r'relatorio/patrimonio_equipamento_tamanho_diferente$',
                        'patrimonio_equipamento_tamanho_diferente'),
                       (r'verificacao/copy_attribute_to_patrimonio$', 'copy_attribute_to_patrimonio'),
                       )
