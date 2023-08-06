# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from import_export import fields
from import_export import resources
from patrimonio.models import Patrimonio


class PatrimonioResource(resources.ModelResource):
    """
    Definição de ModelResource utilizados no import_export para fazer a exportação de dados para CSV, XSL, etc.
    """
    pagamento__protocolo__termo = fields.Field(column_name='termo')
    equipamento__part_number = fields.Field(column_name='part number', attribute='equipamento__part_number')
    equipamento__modelo = fields.Field(column_name='modelo', attribute='equipamento__modelo')
    equipamento__entidade_fabricante__sigla = fields.Field(column_name='fabricante',
                                                           attribute='equipamento__entidade_fabricante__sigla')
    ns = fields.Field(column_name='serial number', attribute='ns')
    tipo__nome = fields.Field(column_name='tipo', attribute='tipo__nome')
    numero_fmusp = fields.Field(column_name='num fmusp', attribute='numero_fmusp')
    entidade_procedencia__sigla = fields.Field(column_name='procedencia', attribute='entidade_procedencia__sigla')
    garantia_termino = fields.Field(column_name='termino de garantia', attribute='garantia_termino')

    class Meta:
        model = Patrimonio
        fields = ('id',
                  'pagamento__protocolo__termo',
                  'apelido',
                  'equipamento__part_number',
                  'equipamento__modelo',
                  'equipamento__entidade_fabricante__sigla',
                  'ns',
                  'tipo__nome',
                  'numero_fmusp',
                  'entidade_procedencia__sigla',
                  'tamanho',
                  'garantia_termino',
                  'revision',
                  'version',
                  'complemento',
                  'descricao',
                  'descricao_tecnica',
                  'obs',
                  'checado',
                  )
        export_order = ('id',
                        'pagamento__protocolo__termo',
                        'apelido',
                        'equipamento__part_number',
                        'equipamento__modelo',
                        'equipamento__entidade_fabricante__sigla',
                        'ns',
                        'tipo__nome',
                        'numero_fmusp',
                        'entidade_procedencia__sigla',
                        'tamanho',
                        'garantia_termino',
                        'revision',
                        'version',
                        'complemento',
                        'descricao',
                        'descricao_tecnica',
                        'obs',
                        'checado',
                        )

    def dehydrate_pagamento__protocolo__termo(self, p):
        if p.pagamento_id and p.pagamento.protocolo_id and p.pagamento.protocolo.termo_id:
            return '%s' % p.pagamento.protocolo.termo
        return ''


class RelatorioPorTipoResource(resources.ModelResource):
    checado = fields.Field(column_name='Checado', attribute='checado')
    id = fields.Field(column_name='ID', attribute='id')
    procedencia = fields.Field(column_name='Procedência', attribute='entidade_procedencia')
    fabricante = fields.Field(column_name='Marca', attribute='equipamento__entidade_fabricante__sigla')
    modelo = fields.Field(column_name='Modelo', attribute='equipamento__modelo')
    part_number = fields.Field(column_name='Part number', attribute='equipamento__part_number')
    descricao = fields.Field(column_name='Descrição', attribute='descricao')
    ns = fields.Field(column_name='NS', attribute='ns')
    local = fields.Field(column_name='Local')
    posicao = fields.Field(column_name='Posição')
    estado = fields.Field(column_name='Estado')
    nf = fields.Field(column_name='NF')

    class Meta:
        model = Patrimonio
        fields = ('checado',
                  'id',
                  'procedencia',
                  'fabricante',
                  'modelo',
                  'part_number',
                  'descricao',
                  'ns',
                  'local',
                  'posicao',
                  'estado',
                  'nf',
                  )
        export_order = ('checado',
                        'id',
                        'procedencia',
                        'fabricante',
                        'modelo',
                        'part_number',
                        'descricao',
                        'ns',
                        'local',
                        'posicao',
                        'estado',
                        'nf',
                        )

    def dehydrate_local(self, p):
        try:
            return '%s' % p.historico_atual.endereco.end or ''
        except AttributeError:
            return ''

    def dehydrate_posicao(self, p):
        try:
            return '%s' % (p.historico_atual.endereco.complemento or '')
        except AttributeError:
            return ''

    def dehydrate_estado(self, p):
        try:
            return '%s' % (p.historico_atual.estado or '')
        except AttributeError:
            return ''

    def dehydrate_nf(self, p):
        try:
            return '%s' % (p.pagamento.protocolo.num_documento or '')
        except AttributeError:
            return ''
