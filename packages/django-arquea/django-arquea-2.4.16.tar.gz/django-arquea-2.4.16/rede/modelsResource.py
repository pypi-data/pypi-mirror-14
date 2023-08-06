# -*- encoding:utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from import_export import fields
from import_export import resources
from rede.models import Recurso, BlocoIP, Beneficiado, CrossConnection


class CustoTerremarkRecursoResource(resources.ModelResource):
    """
    Modelo do model Recurso para a geração do XLS para o relatório Custo Terremark
    """
    total_sem_imposto = fields.Field(column_name='Total sem imposto')
    total_geral = fields.Field(column_name='Total com imposto')
    planejamento__valor_unitario = fields.Field(column_name='Preço unitário')
    planejamento__os__contrato__numero = fields.Field(column_name='Contrato')
    planejamento__os = fields.Field(column_name='OS')
    planejamento__os__data_inicio = fields.Field(column_name='Data Ini')
    planejamento__os__data_rescisao = fields.Field(column_name='Data Fim')
    planejamento__projeto = fields.Field(column_name='Projeto')
    planejamento__tipo = fields.Field(column_name='Descrição')
    planejamento__referente = fields.Field(column_name='Referente')
    planejamento__unidade = fields.Field(column_name='Unidade')
    planejamento__quantidade = fields.Field(column_name='Qtd')
    valor_mensal_sem_imposto = fields.Field(column_name='Custo mensal sem imposto')
    valor_imposto_mensal = fields.Field(column_name='Custo mensal com imposto')
    quantidade = fields.Field(column_name='Meses pagos')
    pagamento__protocolo__num_documento = fields.Field(column_name='Nota fiscal')

    class Meta:
        model = Recurso
        fields = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__os__data_inicio',
                  'planejamento__os__data_rescisao',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__unidade',
                  'planejamento__valor_unitario',
                  'planejamento__quantidade',
                  'valor_mensal_sem_imposto',
                  'valor_imposto_mensal',
                  'quantidade',
                  'total_sem_imposto',
                  'total_geral',
                  'pagamento__protocolo__num_documento'
                  )
        export_order = ('planejamento__os__contrato__numero',
                        'planejamento__os',
                        'planejamento__os__data_inicio',
                        'planejamento__os__data_rescisao',
                        'planejamento__projeto',
                        'planejamento__tipo',
                        'planejamento__referente',
                        'planejamento__unidade',
                        'planejamento__valor_unitario',
                        'planejamento__quantidade',
                        'valor_mensal_sem_imposto',
                        'valor_imposto_mensal',
                        'quantidade',
                        'total_sem_imposto',
                        'total_geral',
                        'pagamento__protocolo__num_documento'
                        )

    def dehydrate_total_sem_imposto(self, recurso):
        return recurso.total_sem_imposto()

    def dehydrate_total_geral(self, recurso):
        return recurso.total_geral()

    def dehydrate_planejamento__valor_unitario(self, recurso):
        return recurso.planejamento.valor_unitario

    def dehydrate_planejamento__os__contrato__numero(self, recurso):
        return '%s' % recurso.planejamento.os.contrato.numero

    def dehydrate_planejamento__os(self, recurso):
        return '%s' % recurso.planejamento.os

    def dehydrate_planejamento__os__data_inicio(self, recurso):
        if recurso.planejamento.os.data_inicio:
            return '%s' % recurso.planejamento.os.data_inicio.strftime('%d/%m/%Y')
        else:
            return ''

    def dehydrate_planejamento__os__data_rescisao(self, recurso):
        if recurso.planejamento.os.data_rescisao:
            return '%s' % recurso.planejamento.os.data_rescisao.strftime('%d/%m/%Y')
        else:
            return ''

    def dehydrate_planejamento__projeto(self, recurso):
        return '%s' % recurso.planejamento.projeto

    def dehydrate_planejamento__tipo(self, recurso):
        return '%s' % recurso.planejamento.tipo

    def dehydrate_planejamento__referente(self, recurso):
        return '%s' % recurso.planejamento.referente

    def dehydrate_planejamento__unidade(self, recurso):
        return '%s' % recurso.planejamento.unidade

    def dehydrate_planejamento__quantidade(self, recurso):
        return recurso.planejamento.quantidade

    def dehydrate_valor_mensal_sem_imposto(self, recurso):
        return recurso.valor_mensal_sem_imposto

    def dehydrate_valor_imposto_mensal(self, recurso):
        return recurso.valor_imposto_mensal

    def dehydrate_quantidade(self, recurso):
        return recurso.quantidade

    def dehydrate_pagamento__protocolo__num_documento(self, recurso):
        return '%s' % recurso.pagamento.protocolo.num_documento


class BlocosIPResource(resources.ModelResource):
    """
    Utilizado na exportação para a lista de Bloco IP.
    """
    usuario = fields.Field(column_name='Usado por')
    cidr = fields.Field(column_name='Bloco IP')
    asn = fields.Field(column_name='AS Anunciante')
    proprietario = fields.Field(column_name='AS Proprietário')
    designado = fields.Field(column_name='Designado para')
    rir = fields.Field(column_name='RIR')
    obs = fields.Field(column_name='Observacao')
    superbloco = fields.Field(column_name='Superbloco')
    superbloco_mask = fields.Field(column_name='Superbloco Másc.')
    mask = fields.Field(column_name='Máscara IP')
    ipv = fields.Field(column_name='IPv4_6')

    class Meta:
        model = BlocoIP
        fields = ('id',
                  'usuario',
                  'superbloco',
                  'superbloco_mask',
                  'cidr',
                  'mask',
                  'asn',
                  'proprietario',
                  'designado',
                  'rir',
                  'obs',
                  'ipv'
                  )
        export_order = ('id',
                        'usuario',
                        'superbloco',
                        'superbloco_mask',
                        'cidr',
                        'mask',
                        'asn',
                        'proprietario',
                        'designado',
                        'rir',
                        'obs',
                        'ipv'
                        )

    def dehydrate_usuario(self, bloco):
        return '%s' % (bloco.usuario or '')

    def dehydrate_superbloco(self, bloco):
        return '%s' % (bloco.superbloco or '')

    def dehydrate_cidr(self, bloco):
        return '%s' % bloco.cidr()

    def dehydrate_asn(self, bloco):
        return '%s' % (bloco.asn or '')

    def dehydrate_proprietario(self, bloco):
        return '%s' % (bloco.proprietario or '')

    def dehydrate_designado(self, bloco):
        return '%s' % bloco.designado

    def dehydrate_rir(self, bloco):
        return '%s' % bloco.rir

    def dehydrate_obs(self, bloco):
        return '%s' % bloco.obs

    def dehydrate_mask(self, bloco):
        return '%s' % bloco.netmask()

    def dehydrate_superbloco_mask(self, bloco):
        if bloco.superbloco:
            return '%s' % bloco.superbloco.netmask()
        else:
            return ''

    def dehydrate_ipv(self, bloco):
        if bloco.is_IPV4():
            return 'IPv4'
        elif bloco.is_IPV6():
            return 'IPv6'
        else:
            return ''


class BlocosIP_Rel_Lista_Inst_BlocoIP_Resource(resources.ModelResource):
    """
    Utilizado na exportação para o relatório de Lista de Blocos IP por instituição
    """

    usuario = fields.Field(column_name='Usado por')
    cidr = fields.Field(column_name='Bloco IP')
    asn = fields.Field(column_name='AS Anunciante')
    proprietario = fields.Field(column_name='AS Proprietário')
    designado = fields.Field(column_name='Designado para')
    rir = fields.Field(column_name='RIR')
    obs = fields.Field(column_name='Observacao')
    superbloco = fields.Field(column_name='Superbloco')
    superbloco_mask = fields.Field(column_name='Superbloco Másc.')
    mask = fields.Field(column_name='Máscara IP')
    ipv = fields.Field(column_name='IPv4_6')

    class Meta:
        model = BlocoIP
        fields = ('id',
                  'usuario',
                  'superbloco',
                  'superbloco_mask',
                  'cidr',
                  'mask',
                  'asn',
                  'proprietario',
                  'designado',
                  'rir',
                  'obs',
                  'ipv'
                  )
        export_order = ('id',
                        'usuario',
                        'superbloco',
                        'superbloco_mask',
                        'cidr',
                        'mask',
                        'asn',
                        'proprietario',
                        'designado',
                        'rir',
                        'obs',
                        'ipv'
                        )

    def dehydrate_usuario(self, bloco):
        return '%s' % (bloco.usuario or '')

    def dehydrate_superbloco(self, bloco):
        return '%s' % (bloco.superbloco or '')

    def dehydrate_cidr(self, bloco):
        return '%s' % bloco.cidr()

    def dehydrate_asn(self, bloco):
        return '%s' % (bloco.asn or '')

    def dehydrate_proprietario(self, bloco):
        return '%s' % (bloco.proprietario or '')

    def dehydrate_designado(self, bloco):
        return '%s' % bloco.designado

    def dehydrate_rir(self, bloco):
        return '%s' % bloco.rir

    def dehydrate_obs(self, bloco):
        return '%s' % bloco.obs

    def dehydrate_mask(self, bloco):
        return '%s' % bloco.netmask()

    def dehydrate_superbloco_mask(self, bloco):
        if bloco.superbloco:
            return '%s' % bloco.superbloco.netmask()
        else:
            return ''

    def dehydrate_ipv(self, bloco):
        if bloco.is_IPV4():
            return 'IPv4'
        elif bloco.is_IPV6():
            return 'IPv6'
        else:
            return ''


class BlocosIP_Rel_Lista_BlocoIP_Resource(resources.ModelResource):
    """
    Utilizado na exportação para o relatório de Lista de Blocos IP
    """

    usuario = fields.Field(column_name='Usado por')
    cidr = fields.Field(column_name='Bloco IP')
    asn = fields.Field(column_name='AS Anunciante')
    proprietario = fields.Field(column_name='AS Proprietário')
    designado = fields.Field(column_name='Designado para')
    rir = fields.Field(column_name='RIR')
    obs = fields.Field(column_name='Observacao')
    superbloco = fields.Field(column_name='Superbloco')
    superbloco_mask = fields.Field(column_name='Superbloco Másc.')
    mask = fields.Field(column_name='Máscara IP')
    ipv = fields.Field(column_name='IPv4_6')

    class Meta:
        model = BlocoIP
        fields = ('superbloco',
                  'cidr',
                  'mask',
                  'asn',
                  'proprietario',
                  'usuario',
                  'designado',
                  'rir',
                  'obs',
                  'ipv'
                  )
        export_order = ('superbloco',
                        'cidr',
                        'mask',
                        'asn',
                        'proprietario',
                        'usuario',
                        'designado',
                        'rir',
                        'obs',
                        'ipv'
                        )

    def dehydrate_superbloco(self, bloco):
        return '%s' % (bloco.superbloco or '')

    def dehydrate_cidr(self, bloco):
        return '%s' % bloco.cidr()

    def dehydrate_mask(self, bloco):
        return '%s' % bloco.netmask()

    def dehydrate_asn(self, bloco):
        return '%s' % (bloco.asn or '')

    def dehydrate_proprietario(self, bloco):
        return '%s' % (bloco.proprietario or '')

    def dehydrate_usuario(self, bloco):
        return '%s' % (bloco.usuario or '')

    def dehydrate_designado(self, bloco):
        return '%s' % bloco.designado

    def dehydrate_rir(self, bloco):
        return '%s' % bloco.rir

    def dehydrate_obs(self, bloco):
        return '%s' % bloco.obs

    def dehydrate_ipv(self, bloco):
        if bloco.is_IPV4():
            return 'IPv4'
        elif bloco.is_IPV6():
            return 'IPv6'
        else:
            return ''


class RecursoOperacionalResource(resources.ModelResource):
    """
    Modelo do model Recurso para a geração do XLS para o relatório Custo Terremark
    """
    planejamento__os__contrato__numero = fields.Field(column_name='Contrato')
    planejamento__os = fields.Field(column_name='OS')
    planejamento__projeto = fields.Field(column_name='Projeto')
    planejamento__tipo = fields.Field(column_name='Descrição')
    planejamento__referente = fields.Field(column_name='Referente')
    planejamento__quantidade = fields.Field(column_name='Qtd. Total')
    entidade = fields.Field(column_name='Beneficiado')
    estado = fields.Field(column_name='Ben. Estado')
    quantidade = fields.Field(column_name='Ben. Qtd')

    class Meta:
        model = Beneficiado
        fields = ('planejamento__os__contrato__numero',
                  'planejamento__os',
                  'planejamento__projeto',
                  'planejamento__tipo',
                  'planejamento__referente',
                  'planejamento__quantidade',
                  'entidade',
                  'estado',
                  'quantidade',
                  )
        export_order = ('planejamento__os__contrato__numero',
                        'planejamento__os',
                        'planejamento__projeto',
                        'planejamento__tipo',
                        'planejamento__referente',
                        'planejamento__quantidade',
                        'entidade',
                        'estado',
                        'quantidade',
                        )

    def dehydrate_planejamento__os__contrato__numero(self, beneficiado):
        if beneficiado.planejamento.os_id and beneficiado.planejamento.os.contrato_id:
            return '%s' % beneficiado.planejamento.os.contrato.numero
        return ''

    def dehydrate_planejamento__os(self, beneficiado):
        return '%s' % beneficiado.planejamento.os

    def dehydrate_planejamento__projeto(self, beneficiado):
        return '%s' % beneficiado.planejamento.projeto

    def dehydrate_planejamento__tipo(self, beneficiado):
        return '%s' % beneficiado.planejamento.tipo

    def dehydrate_planejamento__referente(self, beneficiado):
        return '%s' % beneficiado.planejamento.referente

    def dehydrate_planejamento__quantidade(self, beneficiado):
        return beneficiado.planejamento.quantidade

    def dehydrate_entidade(self, beneficiado):
        if beneficiado.entidade_id:
            return beneficiado.entidade.nome
        return ''

    def dehydrate_estado(self, beneficiado):
        if beneficiado.estado_id:
            return beneficiado.estado.nome
        return ''

    def dehydrate_quantidade(self, beneficiado):
        return beneficiado.quantidade


class CrossConnectionResource(resources.ModelResource):
    """
    Modelo do model CrossConnection para a geração do XLS para a lista de registros de Cross Connection
    """
    origem__rack__complemento = fields.Field(column_name='Rack 1')
    origem__shelf = fields.Field(column_name='Shelf')
    origem__porta = fields.Field(column_name='Porta')
    origem__tipoConector__sigla = fields.Field(column_name='Conector')

    destino__rack__complemento = fields.Field(column_name='Rack 2')
    destino__shelf = fields.Field(column_name='Shelf')
    destino__porta = fields.Field(column_name='Porta')
    destino__tipoConector__sigla = fields.Field(column_name='Conector')

    ordemDeServico = fields.Field(column_name='OS/Projeto')
    circuito = fields.Field(column_name='Circuito')

    obs = fields.Field(column_name='Observação')

    class Meta:
        model = CrossConnection
        fields = ('origem__rack__complemento',
                  'origem__shelf',
                  'origem__porta',
                  'origem__tipoConector__sigla',
                  'destino__rack__complemento',
                  'destino__shelf',
                  'destino__porta',
                  'destino__tipoConector__sigla',
                  'ordemDeServico',
                  'circuito',
                  'obs',
                  )
        export_order = ('origem__rack__complemento',
                        'origem__shelf',
                        'origem__porta',
                        'origem__tipoConector__sigla',
                        'destino__rack__complemento',
                        'destino__shelf',
                        'destino__porta',
                        'destino__tipoConector__sigla',
                        'ordemDeServico',
                        'circuito',
                        'obs',
                        )

    def dehydrate_origem__rack__complemento(self, obj):
        return obj.origem.rack.complemento

    def dehydrate_origem__shelf(self, obj):
        return obj.origem.shelf

    def dehydrate_origem__porta(self, obj):
        return obj.origem.porta

    def dehydrate_origem__tipoConector__sigla(self, obj):
        return obj.origem.tipoConector.sigla

    def dehydrate_destino__rack__complemento(self, obj):
        return obj.destino.rack.complemento

    def dehydrate_destino__shelf(self, obj):
        return obj.destino.shelf

    def dehydrate_destino__porta(self, obj):
        return obj.destino.porta

    def dehydrate_destino__tipoConector__sigla(self, obj):
        return obj.destino.tipoConector.sigla

    def dehydrate_ordemDeServico(self, obj):
        return obj.ordemDeServico

    def dehydrate_circuito(self, obj):
        return obj.circuito

    def dehydrate_obs(self, obj):
        return obj.obs
