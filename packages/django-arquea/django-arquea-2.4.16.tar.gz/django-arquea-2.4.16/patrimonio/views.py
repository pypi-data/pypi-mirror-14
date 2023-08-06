# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from operator import itemgetter
from django.contrib.auth.decorators import permission_required, login_required
from utils.decorators import login_required_or_403
from django.core.urlresolvers import reverse
from django.db.models import Q, Prefetch
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe

from utils.functions import render_to_pdf_weasy
import json
import itertools
import datetime
import logging
from decimal import Decimal

from configuracao.models import Variavel
from modelsResource import RelatorioPorTipoResource
from identificacao.models import Entidade, EnderecoDetalhe, Endereco
from outorga.models import Termo, Natureza_gasto, Item
from financeiro.models import Pagamento
from patrimonio.models import Equipamento, Patrimonio, HistoricoLocal, Estado,\
    Tipo, TipoEquipamento, PatrimonioRack, PlantaBaixaDataCenter,\
    PlantaBaixaObjeto, PlantaBaixaPosicao

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Gera uma lista dos protocolos conforme o termo selecionado.
# @login_required
# @require_safe
# def ajax_escolhe_termo(request):
#     retorno = []
#
#     t = request.GET.get('id')
#     if t:
#         termo = Termo.objects.get(pk=int(t))
#         protocolos = Protocolo.objects.filter(termo=termo)
#
#         for p in protocolos:
#             descricao = '%s: %s - %s' % (p.doc_num(), p.descricao2.__unicode__(), p.mostra_valor())
#             retorno.append({'pk':p.pk, 'valor':descricao})
#
#     if not retorno:
#         retorno = [{"pk":"0", "valor":"Nenhum registro"}]
#
#     retorno_json = json.dumps(retorno)
#     return HttpResponse(retorno_json, content_type="application/json")

# Gera uma lista dos itens do protocolo conforme protocolo selecionado.
# @login_required
# @require_safe
# def ajax_escolhe_protocolo(request):
#     retorno = []
#     id = request.GET.get('id')
#     previous = request.GET.get('previous')
#
#     if id and previous:
#         t = Termo.objects.get(pk=int(previous))
#         itens = ItemProtocolo.objects.filter(protocolo__id=int(id), protocolo__termo=t)
#
#         for i in itens:
#             descricao = '%s - %s (%s)' % (i.quantidade, i.descricao, i.mostra_valor())
#             retorno.append({'pk':i.pk, 'valor': descricao})
#
#         if not retorno:
#             retorno = [{"pk":"0", "valor":"Nenhum registro"}]
#
#     retorno_json = json.dumps(retorno)
#     return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_escolhe_pagamento(request):
    """
    Retorna os dados de pagamento, filtrado por termo e número de documento.

    Utilizado no PatrimonioAdminForm, ou seja, no form do admin - patrimonio,
    para preencher os valores do combo do campo de Pagamento.
    """
    retorno = []
    termo = request.GET.get('termo')
    numero = request.GET.get('numero')

    if termo and numero:
        pgt = Pagamento.objects.filter(protocolo__termo__id=termo)
        for p in pgt.filter(Q(conta_corrente__cod_oper__icontains=numero) |
                            Q(protocolo__num_documento__icontains=numero)):
            if p.conta_corrente:
                descricao = 'Doc. %s, cheque %s, valor %s' % (p.protocolo.num_documento, p.conta_corrente.cod_oper,
                                                              p.valor_fapesp)
            else:
                descricao = 'Doc. %s, valor %s' % (p.protocolo.num_documento, p.valor_patrocinio)

            retorno.append({'pk': p.pk, 'valor': descricao})

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


# @login_required
# @require_safe
# def ajax_escolhe_detalhe(request):
#     ed_id = request.GET.get('detalhe')
#     detalhe = get_object_or_404(EnderecoDetalhe, pk=ed_id)
#
#     retorno = []
#     for ed in EnderecoDetalhe.objects.filter(detalhe=detalhe):
#         retorno.append({'pk':ed.pk, 'valor':ed.__unicode__()})
#
#     retorno_json = json.dumps(retorno)
#     return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_escolhe_entidade(request):
    """
    Disparadao do atributo de entidade em PatrimonioHistoricoLocalAdminForm.

    Utilizado para buscar dados de endereço a partir da escolha de uma entidade.
    """
    ent_id = request.GET.get('entidade')
    entidade = get_object_or_404(Entidade, pk=ent_id)

    retorno = []
    for ed in EnderecoDetalhe.objects.all().order_by('endereco', 'detalhe__complemento', 'complemento'):
        if ed.end.entidade == entidade:
            descricao = ed.__unicode__()

            retorno.append({'pk': ed.pk, 'valor': descricao})

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_escolhe_equipamento(request):
    """
    Faz a busca de equipamentos por diversos atributos.
    Utilizado para fazer o filtro de "Equipamentos" durante a tela de cadastro/modificação de patrimonio.
    """
    filtro = request.GET.get('num_doc')
    id_equipamento = request.GET.get('id_equipamento')

    if filtro:
        retorno = [{'pk': p.pk, 'valor': p.__unicode__(), 'selected': (str(p.pk) == id_equipamento)}
                   for p in Equipamento.objects.filter(
                       Q(tipo__nome__icontains=filtro) |
                       Q(descricao__icontains=filtro) |
                       Q(part_number__icontains=filtro) |
                       Q(entidade_fabricante__sigla__icontains=filtro) |
                       Q(entidade_fabricante__nome__icontains=filtro) |
                       Q(modelo__icontains=filtro) |
                       Q(titulo_autor__icontains=filtro) |
                       Q(isbn__icontains=filtro))]
    else:
        retorno = [{'pk': p.pk, 'valor': p.__unicode__(), 'selected': (str(p.pk) == id_equipamento)}
                   for p in Equipamento.objects.all()]

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_get_marcas_por_termo(request):
    """
    Utilizado para montar dados de "Equipamentos" durante a tela de cadastro/modificação de patrimonio.
    """
    termo_id = request.GET.get('termo')

    if termo_id is not None and (termo_id == '0' or termo_id == ''):
        patrimonios = Patrimonio.objects.filter(equipamento__entidade_fabricante__isnull=False)\
            .order_by('equipamento__entidade_fabricante__sigla').distinct('equipamento__entidade_fabricante__sigla')
    else:
        patrimonios = Patrimonio.objects.filter(pagamento__protocolo__termo_id=termo_id,
                                                equipamento__entidade_fabricante__isnull=False)\
            .order_by('equipamento__entidade_fabricante__sigla').distinct('equipamento__entidade_fabricante__sigla')

    retorno = [{'pk': p.equipamento.entidade_fabricante.pk, 'valor': p.equipamento.entidade_fabricante.__unicode__()}
               for p in patrimonios]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_get_equipamento(request):
    """
    Faz a busca de equipamentos
    Utilizado para montar dados de "Equipamentos" durante a tela de cadastro/modificação de patrimonio.
    """
    id_equipamento = request.GET.get('id_equipamento')
    p = Equipamento.objects.get(id=id_equipamento)

    marca = ''
    if p.entidade_fabricante:
        marca = p.entidade_fabricante.sigla

    retorno = {'pk': p.pk, 'valor': p.__unicode__(), 'modelo': p.modelo, 'part_number': p.part_number, 'marca': marca}

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_get_procedencia_filter_tipo(request):
    """
    AJAX para buscar procedencias de patrimonio filtrados por tipo
    """
    id_tipo = request.GET.get('id_tipo')
    entidades_ids = Patrimonio.objects.filter(tipo=id_tipo).order_by('tipo')\
        .values_list('entidade_procedencia', flat=True).distinct()

    procedencias = Entidade.objects.filter(id__in=entidades_ids)

    retorno = [{'pk': p.pk, 'valor': p.__unicode__()}
               for p in procedencias]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_escolhe_patrimonio(request):
    """
    Faz a busca de patrimonios que estao relacionados a NFs.
    Utilizado para fazer o filtro de "Patrimonios Contidos em" durante a tela de cadastro/modificação de patrimonio.
    """
    retorno = []
    num_doc = request.GET.get('num_doc')

    if num_doc:
        retorno = ([{'pk': p.pk, 'valor': p.__unicode__()}
                    for p in Patrimonio.objects.filter(Q(pagamento__protocolo__num_documento__icontains=num_doc) | Q(ns__icontains=num_doc))]) \
                or [{"pk": "0", "valor": "Nenhum registro"}]

    if not retorno or len(retorno) == 0:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type="application/json")


# @login_required
# @require_safe
# def ajax_patrimonio_existente(request):
#     retorno = {'marca':'', 'modelo':'', 'descricao':'', 'procedencia':''}
#     part_number = request.GET.get('part_number')
#
#     existentes = Patrimonio.objects.filter(equipamento__part_number__iexact=part_number)
#
#     if part_number and existentes.count():
#         p = existentes[0]
#
#         retorno = {'marca':p.marca, 'modelo':p.modelo, 'descricao':p.descricao, 'procedencia':p.procedencia}
#
#     retorno_json = json.dumps(retorno)
#     return HttpResponse(retorno_json, content_type='application/json')


@login_required
@permission_required('patrimonio.rel_tec_por_estado', raise_exception=True)
@require_safe
def por_estado(request):
    """
     Relatório Técnico - Relatório de Patrimônio por estado do item.

    """

    patrimonio_queryset = Patrimonio.objects.prefetch_related(
                                                      Prefetch('historicolocal_set',
                                                               queryset=HistoricoLocal.objects.all().select_related(
                                                                                    'estado', 'endereco',
                                                                                    'endereco__detalhe',
                                                                                    'endereco__detalhe__endereco__entidade',
                                                                                    'endereco__endereco__entidade'))) \
                                            .select_related('entidade_procedencia', 'equipamento__entidade_fabricante') \
                                            .order_by('ns')

    filtro_estados = []

    entidades = []
    for p in patrimonio_queryset:
        ht = p.historico_atual_prefetched

        # Montando o filtro de estados
        if ht:
            achou_estado = False
            for e in filtro_estados:
                if e['estado'].id == ht.estado.id:
                    e['count'] = e['count'] + 1
                    achou_estado = True
                    break
            if not achou_estado:
                filtro_estados.append({'estado': ht.estado, 'count': 1})

    if request.method == 'GET' and request.GET.get('estado'):

        estado_id = request.GET.get('estado')

        entidades = []
        estado = ''

        if Estado.objects.filter(pk=estado_id).exists():
            estado = get_object_or_404(Estado, pk=estado_id)

            for p in patrimonio_queryset:
                ht = p.historico_atual_prefetched

                if ht and ht.estado_id == estado.id:
                    # patrimonios_obj.append({'patrimonio':p, 'endereco':ht.endereco, 'entidade':ht.endereco.end.entidade})
                    endereco = ht.endereco
                    patrimonio = p
                    entidade = ht.endereco.end.entidade

                    # Montando o objeto contento entidades > enderecos > patrionios

                    detalhe = {'detalhe': endereco, 'patrimonios': [patrimonio]}
                    achou_entidade = False
                    for e in entidades:
                        # agrupando entidades
                        if e['entidade'].id == entidade.id:
                            achou_entidade = True
                            achou_detalhe = False

                            # agrupando enderecos
                            for d in e['detalhes']:
                                if d and d['detalhe'] and endereco and d['detalhe'].id == endereco.id:
                                    achou_detalhe = True

                                    # agrupando patrimonios
                                    d['patrimonios'].append(patrimonio)

                            if not achou_detalhe:
                                e['detalhes'].append(detalhe)

                    if not achou_entidade:
                        entidades.append({'entidade': entidade, 'detalhes': [detalhe]})

            entidades.sort(key=lambda x: x['entidade'].sigla, reverse=False)
            filtro_estados.sort(key=lambda x: x['estado'].nome, reverse=False)

        return TemplateResponse(request, 'patrimonio/por_estado.html',
                                {'estado_id': estado_id, 'estado': estado, 'entidades': entidades, 'estados': filtro_estados})
    else:
        return TemplateResponse(request, 'patrimonio/por_estado.html', {'estados': filtro_estados})


@login_required
@permission_required('patrimonio.rel_tec_por_tipo', raise_exception=True)
@require_safe
def por_tipo_consignado(request):
    """
     Relatório Técnico - Relatório de Patrimônio por tipo - Filtro por tipo Consignado.

    """
    return por_tipo(request, Tipo.CONSIGNADO)


@login_required
@permission_required('patrimonio.rel_tec_por_tipo', raise_exception=True)
@require_safe
def por_tipo(request, param_tipo_id=None):
    """
     Relatório Técnico - Relatório de Patrimônio por tipo.

    """
    if param_tipo_id or (request.method == 'GET' and request.GET.get('tipo')):
        if param_tipo_id:
            tipo_id = param_tipo_id
        else:
            tipo_id = request.GET.get('tipo')

        tipo = get_object_or_404(Tipo, pk=tipo_id)

        procedencia = ''
        patrimonios = Patrimonio.objects.filter(tipo_id=tipo_id)\
            .order_by('entidade_procedencia', 'equipamento__entidade_fabricante', 'ns')
        if request.GET.get('procedencia') and request.GET.get('procedencia') != '':
            procedencia_id = request.GET.get('procedencia')
            patrimonios = patrimonios.filter(entidade_procedencia=procedencia_id)
            procedencia = Entidade.objects.get(id=procedencia_id)

        patrimonios = patrimonios.select_related('entidade_procedencia', 'equipamento', 'pagamento',
                                                 'equipamento__entidade_fabricante', 'pagamento__protocolo')

        pdf = request.GET.get('acao') == '1'
        xls = request.GET.get('acao') == '2'
        if pdf:
            return render_to_pdf_weasy('patrimonio/por_tipo_weasy.pdf',
                                       {'tipo': tipo, 'procedencia': procedencia, 'patrimonios': patrimonios},
                                       request=request, filename="inventario_por_tipo.pdf")
        elif xls:
            # Export para Excel/XLS
            dataset = RelatorioPorTipoResource().export(queryset=patrimonios)

            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = "attachment; filename=relatorio_patrimonio_por_tipo.xls"

            return response
        else:
            # Listas para remontar o filtro de Tipos e o filtro e Procedencias
            if param_tipo_id:
                # Se receber o tipo como parametro, não enviar a lista de filtro de tipos.
                tipos = []
            else:
                tipos = Tipo.objects.all()

            entidades_ids = Patrimonio.objects.filter(tipo=tipo_id).order_by('tipo')\
                .values_list('entidade_procedencia', flat=True).distinct()
            procedencias = Entidade.objects.filter(id__in=entidades_ids)

            return TemplateResponse(request, 'patrimonio/por_tipo.html',
                                    {'tipos': tipos, 'procedencias': procedencias, 'tipo': tipo,
                                     'procedencia': procedencia, 'patrimonios': patrimonios})
    else:
        tipos = Tipo.objects.all()
        return TemplateResponse(request, 'patrimonio/sel_tipo.html', {'tipos': tipos})


@login_required
@permission_required('patrimonio.rel_tec_por_marca', raise_exception=True)
@require_safe
def por_marca(request, pdf=0):
    """
     Relatório Técnico - Relatório de Patrimônio por marca.

    """
    if request.method == 'GET' and request.GET.get('marca'):
        marca = request.GET.get('marca')

        patrimonios = Patrimonio.objects.filter(equipamento__entidade_fabricante__sigla=marca) \
                                .select_related('tipo', 'equipamento', 'pagamento__protocolo', 'entidade_procedencia') \
                                .prefetch_related(
            Prefetch('historicolocal_set',
                     queryset=HistoricoLocal
                     .objects.select_related('estado', 'endereco__detalhe__endereco__entidade',
                                             'endereco__endereco__entidade')))

        if pdf:
            return render_to_pdf_weasy('patrimonio/por_marca.pdf', {'marca': marca, 'patrimonios': patrimonios},
                                       request=request, filename='inventario_por_marca.pdf')
        return TemplateResponse(request, 'patrimonio/por_marca.html', {'marca': marca, 'patrimonios': patrimonios})
    else:
        eefs = 'equipamento__entidade_fabricante__sigla'
        return TemplateResponse(request, 'patrimonio/sel_marca.html',
                                {'marcas': Patrimonio.objects.values_list(eefs, flat=True).order_by(eefs).distinct()})


@login_required
@permission_required('patrimonio.rel_tec_por_local', raise_exception=True)
@require_safe
def por_local(request, pdf=0):
    """
     Relatório Técnico - Relatório de Patrimônio por localização.

    """
    if request.GET.get('entidade') and request.GET.get('endereco'):
        atuais = []
        detalhes = []

        endereco_id = request.GET.get('endereco')
        detalhe_id = request.GET.get('detalhe2')

        if not detalhe_id:
            detalhe_id = request.GET.get('detalhe1')
        if not detalhe_id:
            detalhe_id = request.GET.get('detalhe')

        for p in Patrimonio.objects.filter(patrimonio__isnull=True)\
                .prefetch_related(Prefetch('historicolocal_set', queryset=HistoricoLocal.objects.all())):
            ht = p.historico_atual_prefetched
            if ht:
                atuais.append(ht.id)

        # Listamos os patrimonios candidatos, a partir do filtro de endereços
        if detalhe_id:
            detalhe = get_object_or_404(EnderecoDetalhe, pk=detalhe_id)

            detalhes = []
            i = 0
            for ed in EnderecoDetalhe.objects.filter(pk=detalhe_id):
                detalhes.append(ed)

            while i < len(detalhes):
                for ed in detalhes[i].enderecodetalhe_set.all():
                    detalhes.append(ed)
                i += 1

            patrimonio_ids = HistoricoLocal.objects.filter(patrimonio__patrimonio__isnull=True, endereco__in=detalhes)\
                .values_list('patrimonio', flat=True).order_by('id')
        else:
            # Se não tiver filtro de detalhe, temos que buscar em todos os enderecos possiveis
            endereco = get_object_or_404(Endereco, pk=endereco_id)

            patrimonio_ids = HistoricoLocal.objects.filter(
                patrimonio__patrimonio__isnull=True, endereco__endereco=endereco)\
                .values_list('patrimonio', flat=True).order_by('id') | HistoricoLocal.objects.filter(
                patrimonio__patrimonio__isnull=True, endereco__detalhe__endereco=endereco)\
                .values_list('patrimonio', flat=True).order_by('id') | HistoricoLocal.objects.filter(
                patrimonio__patrimonio__isnull=True, endereco__detalhe__detalhe__endereco=endereco)\
                .values_list('patrimonio', flat=True).order_by('id')

        # Com os patrimonios candidatos, buscamos somente endereços que possuem
        # históricos atuais nos patrimonios
        atuais = []
        for p in Patrimonio.objects.filter(patrimonio__isnull=True, id__in=patrimonio_ids)\
                .prefetch_related('historicolocal_set'):
            ht = p.historico_atual_prefetched
            if ht:
                atuais.append(ht.id)

        # Aqui listamos os Patrimonios que possuem Historico Atual no endereço selecionado
        if detalhe_id:
            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__in=detalhes)
            context = {'detalhe': detalhe,
                       'det': detalhe_id,
                       'detalhes': [{'patrimonio': Patrimonio.objects.filter(historicolocal__in=historicos)
                                    .select_related('equipamento__entidade_fabricante', 'entidade_procedencia',
                                                    'pagamento__protocolo')
                                    .prefetch_related(Prefetch('historicolocal_set',
                                                               queryset=HistoricoLocal.objects
                                                               .select_related('estado')))
                                    .prefetch_related(Prefetch('contido',
                                                               queryset=Patrimonio.objects
                                                               .select_related('entidade_procedencia',
                                                                               'pagamento__protocolo',
                                                                               'equipamento__entidade_fabricante')))
                                    .prefetch_related(Prefetch('contido__historicolocal_set',
                                                               queryset=HistoricoLocal.objects
                                                               .select_related('estado')))
                                    .prefetch_related(Prefetch('contido__contido',
                                                               queryset=Patrimonio.objects
                                                               .select_related('entidade_procedencia',
                                                                               'pagamento__protocolo',
                                                                               'equipamento__entidade_fabricante')))
                                    .prefetch_related(Prefetch('contido__contido__historicolocal_set',
                                                               queryset=HistoricoLocal.objects
                                                               .select_related('estado')))
                                    .prefetch_related(Prefetch('contido__contido__contido',
                                                               queryset=Patrimonio.objects
                                                               .select_related('entidade_procedencia',
                                                                               'pagamento__protocolo',
                                                                               'equipamento__entidade_fabricante')))
                                    .prefetch_related(Prefetch('contido__contido__contido__historicolocal_set',
                                                               queryset=HistoricoLocal.objects
                                                               .select_related('estado')))
                                    .order_by('descricao', 'complemento')}]}
        else:
            endereco = get_object_or_404(Endereco, pk=endereco_id)

            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__endereco=endereco) \
                | HistoricoLocal.objects.filter(id__in=atuais, endereco__detalhe__endereco=endereco)\
                | HistoricoLocal.objects.filter(id__in=atuais, endereco__detalhe__detalhe__endereco=endereco)
            detalhes = []
            detalhes_ids = historicos.values_list('endereco', flat=True)
            for d in EnderecoDetalhe.objects.filter(id__in=detalhes_ids):
                detalhes.append({'detalhe': d,
                                 'patrimonio': Patrimonio.objects.filter(
                                     historicolocal__in=historicos.filter(endereco=d))
                                 .select_related('equipamento__entidade_fabricante', 'entidade_procedencia',
                                                 'pagamento__protocolo')
                                 .prefetch_related(Prefetch('historicolocal_set',
                                                            queryset=HistoricoLocal.objects.select_related('estado')))
                                 .order_by('descricao', 'complemento')
                                 })
            context = {'endereco': endereco, 'end': endereco_id, 'detalhes': detalhes, 'detalhe': '', 'det': ''}

        if pdf:
            return render_to_pdf_weasy('patrimonio/por_local_weasy.pdf', context, request=request,
                                       filename='inventario_por_local.pdf')
        return render_to_response('patrimonio/por_local.html', context, context_instance=RequestContext(request))
    else:
        entidades = _find_entidades_filhas(None)
        msg = "A seleção da Entidade, Endereço e Localização são obrigatórios."
        return render_to_response('patrimonio/sel_local.html', {'entidades': entidades, 'msg': msg},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('patrimonio.rel_tec_por_local_rack', raise_exception=True)
@require_safe
def por_local_rack(request, pdf=0):
    """
     Relatório Técnico - Relatório de Patrimônio por local e rack.

    """
    entidade = request.GET.get('entidade')
    endereco_id = request.GET.get('endereco')
    detalhe_id = request.GET.get('detalhe')

    if entidade and detalhe_id and endereco_id:
        atuais = []
        # Buscando os históricos atuais de patrimonios de primeiro nível
        for p in Patrimonio.objects.filter(patrimonio__isnull=True).prefetch_related('historicolocal_set'):
            ht = p.historico_atual_prefetched
            if ht:
                atuais.append(ht.id)

        if detalhe_id:
            detalhe = get_object_or_404(EnderecoDetalhe, pk=detalhe_id)
            detalhes = [detalhe]

            i = 0
            while i < len(detalhes):
                for ed in detalhes[i].enderecodetalhe_set.all():
                    detalhes.append(ed)
                i += 1

            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__in=detalhes)

            ps = Patrimonio.objects.filter(historicolocal__in=historicos) \
                .select_related('equipamento', 'equipamento__tipo', 'entidade_procedencia', 'pagamento__protocolo',
                                'pagamento__protocolo__termo',)\
                .prefetch_related(Prefetch('historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido__contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))
            ps = list(ps)
            # Ordena os racks pela posição. Ex: R042 - ordena pela fila 042 e depois pela posição R
#             patrimonio_racks.sort(key=lambda x: x.historico_atual.posicao_rack_letra, reverse=False)
#             patrimonio_racks.sort(key=lambda x: x.historico_atual.posicao_rack_numero, reverse=True)

            endereco = get_object_or_404(Endereco, pk=endereco_id)
            enderecos = []
            enderecos.append({'endereco': endereco, 'end': endereco_id,
                              'detalhes': [{'detalhe': detalhe, 'det': detalhe_id,
                                            'patrimonio': _iterate_patrimonio(ps, 0, False, False, False, 2)}]})
            context = {'detalhe': detalhe, 'det': detalhe_id, 'enderecos': enderecos}

        if pdf:
            return render_to_pdf_weasy('patrimonio/por_local_rack_weasy.pdf', context, request=request,
                                       filename='inventario_por_local_rack.pdf')
        else:
            return render_to_response('patrimonio/por_local_rack.html', context, RequestContext(request, context))
    else:
        # Cria a lista para o SELECT de filtro de Entidades, buscando as Entidades que possuem EnderecoDetalhe
        entidades = _find_entidades_filhas(None)
        msg = "A seleção da Entidade, Endereço e Localização são obrigatórios."
        return render_to_response('patrimonio/sel_local_rack.html', {'entidades': entidades, 'msg': msg},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('patrimonio.rel_tec_por_local_termo', raise_exception=True)
@require_safe
def por_local_termo(request, pdf=0):
    """
     Relatório Técnico - Relatório de Patrimônio por localização (com Termo).

    """
    if request.GET.get('entidade'):
        atuais = []
        # Buscando os históricos atuais de patrimonios de primeiro nível
        for p in Patrimonio.objects.filter(patrimonio__isnull=True).prefetch_related('historicolocal_set'):
            ht = p.historico_atual_prefetched
            if ht:
                atuais.append(ht.id)

        detalhe_id = request.GET.get('detalhe2')
        if not detalhe_id:
            detalhe_id = request.GET.get('detalhe1')
        if not detalhe_id:
            detalhe_id = request.GET.get('detalhe')

        nivel1 = request.GET.get('nivel1')
        nivel2 = request.GET.get('nivel2')
        nivel3 = request.GET.get('nivel3')

        endereco_id = request.GET.get('endereco')
        filtro_com_fmusp = request.GET.get('com_fmusp') or False

        if detalhe_id:
            detalhe = get_object_or_404(EnderecoDetalhe, pk=detalhe_id)
            detalhes = [detalhe]

            i = 0
            while i < len(detalhes):
                for ed in detalhes[i].enderecodetalhe_set.all():
                    detalhes.append(ed)
                i += 1

            historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__in=detalhes)

            ps = Patrimonio.objects.filter(historicolocal__in=historicos)\
                .select_related('equipamento', 'equipamento__tipo', 'entidade_procedencia', 'pagamento__protocolo',
                                'pagamento__protocolo__termo',)\
                .prefetch_related(Prefetch('historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido__contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido__contido__contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__contido__contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))\
                .prefetch_related(Prefetch('contido__contido__contido__contido',
                                           queryset=Patrimonio.objects
                                           .select_related('pagamento__protocolo', 'pagamento__protocolo__termo',
                                                           'equipamento', 'equipamento__tipo', )))\
                .prefetch_related(Prefetch('contido__contido__contido__contido__historicolocal_set',
                                           queryset=HistoricoLocal.objects.select_related('estado')))

            if filtro_com_fmusp:
                ps = ps.filter(numero_fmusp__isnull=False)

            endereco = get_object_or_404(Endereco, pk=endereco_id)
            enderecos = []
            enderecos.append({'endereco': endereco, 'end': endereco_id,
                              'detalhes': [{'detalhe': detalhe, 'det': detalhe_id,
                                            'patrimonio': _iterate_patrimonio(ps, 0, filtro_com_fmusp)}]})
            context = {'nivel1': nivel1, 'nivel2': nivel2, 'nivel3': nivel3, 'detalhe': detalhe, 'det': detalhe_id,
                       'enderecos': enderecos}

        elif endereco_id and endereco_id != "":
            endereco_id = request.GET.get('endereco')

            enderecos = []
            endereco = _find_endereco(atuais, endereco_id, filtro_com_fmusp)
            enderecos.append(endereco)
            context = {'nivel1': nivel1, 'nivel2': nivel2, 'nivel3': nivel3, 'enderecos': enderecos}

        else:
            entidade_id = request.GET.get('entidade')
            entidade_filha_id = request.GET.get('entidade1')

            if entidade_filha_id:
                # Se for selecionada a entidade de segundo nível, podemos utiliza-la como filtro
                entidade = Entidade.objects.filter(pk=entidade_filha_id)
            else:
                # Se for selecionada a entidade de primeiro nível, devemos fazer a busca incluindo todas as
                # suas entidades de segundo nível
                entidade = Entidade.objects.filter(pk=entidade_id) | Entidade.objects.filter(entidade=entidade_id)
            enderecos = []
            for endereco in Endereco.objects.filter(entidade__in=entidade):
                endereco = _find_endereco(atuais, endereco.id, filtro_com_fmusp)
                if endereco:
                    enderecos.append(endereco)
            context = {'nivel1': nivel1, 'nivel2': nivel2, 'nivel3': nivel3, 'entidade': entidade, 'ent': entidade_id,
                       'enderecos': enderecos}

        if pdf == "1":
            return render_to_pdf_weasy('patrimonio/por_local_termo_weasy.pdf', context, request=request,
                                       filename='inventario_por_local_termo.pdf')
        elif pdf == "2":
            return render_to_response('patrimonio/por_local_termo_weasy.pdf', context, RequestContext(request, context))
        else:
            return render_to_response('patrimonio/por_local_termo.html', context, RequestContext(request, context))
    else:
        # Cria a lista para o SELECT de filtro de Entidades, buscando as Entidades que possuem EnderecoDetalhe
        entidades = _find_entidades_filhas(None)
        msg = "A seleção da Entidade é obrigatória."
        return render_to_response('patrimonio/sel_local_termo.html', {'entidades': entidades, 'msg': msg},
                                  context_instance=RequestContext(request))


def _find_entidades_filhas(entidade_id):
    """
    Usado para criar o filtro de entidades.
    Caso o parametro seja None, busca todas as entidades de primeiro nível, seguidas pela busca de todas
    as entidades abaixo.
    Somente são consideradas Entidades válidas para a exibição no filtro as que possuirem EnderecoDetalhe,
    de qualquer nível de Entidade
    """
    if entidade_id:
        entidades = Entidade.objects.filter(entidade=entidade_id)
    else:
        entidades = Entidade.objects.filter(entidade__isnull=True)

    entidades_retorno = []
    for entidade in entidades:
        entidades_filhas = _find_entidades_filhas(entidade.id)
        entidade_valida = Entidade.objects.filter(id=entidade.id, endereco__isnull=False,
                                                  endereco__enderecodetalhe__isnull=False).exists()

        if len(entidades_filhas) > 0 or entidade_valida:
            entidades_retorno.append({"entidade": entidade, "filhas": entidades_filhas})

    return entidades_retorno


def _find_endereco(atuais, endereco_id, filtro_com_fmusp=False):
    """
    Usado no disparo da view por_local_termo
    Busca patrimonios de um endereco
    """
    endereco = get_object_or_404(Endereco, pk=endereco_id)

    # busca os historicos de localizacao de patrimonio baseado no endereco
    # busca os que estiverem no endereço, ou localidades abaixo deste endereco
    historicos = HistoricoLocal.objects.filter(id__in=atuais, endereco__endereco=endereco)\
        | HistoricoLocal.objects.filter(id__in=atuais, endereco__detalhe__endereco=endereco)\
        | HistoricoLocal.objects.filter(id__in=atuais, endereco__detalhe__detalhe__endereco=endereco)
    detalhes = []
    detalhes_ids = historicos.values_list('endereco', flat=True)
    enderecoDetalhes = EnderecoDetalhe.objects.filter(id__in=detalhes_ids)
    for d in enderecoDetalhes:
        ps = Patrimonio.objects.filter(historicolocal__in=historicos.filter(endereco=d))
        if filtro_com_fmusp:
            ps = ps.filter(numero_fmusp__isnull=False)
        detalhes.append({'detalhe': d, 'patrimonio': _iterate_patrimonio(ps, 0, filtro_com_fmusp)})

    context = None
    if len(detalhes) > 0:
        context = {'endereco': endereco, 'end': endereco_id, 'detalhes': detalhes}
    return context


def _iterate_patrimonio(p_pts, nivel=0, filtro_com_fmusp=False, order_fmusp=True, order_termo=True, nivel_maximo=4):
    if nivel == nivel_maximo:  # or len(p_pts) == 0:
        return

    patrimonios = []

    pts = p_pts
    if filtro_com_fmusp:
        pts = pts.filter(numero_fmusp__isnull=False)

    for p in pts:
        patrimonio = {}
        patrimonio.update({'id': p.id, 'termo': '', 'fmusp': p.numero_fmusp, 'num_documento': '',
                           'apelido': p.apelido, 'modelo': p.modelo, 'part_number': p.part_number, 'tipo': '',
                           'descricao': p.descricao, 'ns': p.ns, 'estado': '', 'posicao': '', 'contido': []})
        if p.pagamento and p.pagamento.protocolo:
            patrimonio.update({'termo': str(p.pagamento.protocolo.termo)})
            patrimonio.update({'num_documento': p.pagamento.protocolo.num_documento})

        if p.historico_atual_prefetched:
            patrimonio.update({'estado': p.historico_atual_prefetched.estado})
            if p.historico_atual_prefetched.posicao:
                patrimonio.update({'posicao': p.historico_atual_prefetched.posicao.upper().ljust(15, ' ')})
            else:
                patrimonio.update({'posicao': ''})

        if p.equipamento_id and p.equipamento.tipo_id:
            patrimonio.update({'tipo': p.equipamento.tipo.nome})

        contido = _iterate_patrimonio(p.contido.all(), nivel + 1, filtro_com_fmusp, order_fmusp, order_termo,
                                      nivel_maximo)
        patrimonio.update({'contido': contido})

        patrimonios.append(patrimonio)

    patrimonios.sort(key=itemgetter('posicao'), reverse=True)
    if order_fmusp is True:
        patrimonios.sort(key=lambda p: p['fmusp'], reverse=True)
    if order_termo is True:
        patrimonios.sort(key=lambda p: p['termo'], reverse=True)

    return patrimonios


@login_required
@permission_required('patrimonio.rel_tec_por_tipo_equipamento', raise_exception=True)
@require_safe
def por_tipo_equipamento(request, pdf=0):
    """
     Relatório Técnico - Relatório de Busca por tipo de equipamento.

    """

    if len(request.GET) < 1:
        return TemplateResponse(request, 'patrimonio/sel_tipo_equip.html',
                                {'tipos': TipoEquipamento.objects.all(), 'estados': Estado.objects.all(),
                                 'pns': Equipamento.objects.values_list('part_number', flat=True)
                                 .order_by('part_number').distinct()})

    tipo_id = request.GET.get('tipo')
    entidades = []
    if tipo_id == '0':
        patrimonios_tipo = Patrimonio.objects.all()
        tipo = 'todos'
    else:
        patrimonios_tipo = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)
        tipo = TipoEquipamento.objects.get(id=tipo_id)

    part_number = request.GET.get('partnumber')
    if part_number != '0':
        patrimonios_tipo = patrimonios_tipo.filter(equipamento__part_number=part_number)

    estado_id = request.GET.get('estado')
    for p in patrimonios_tipo.select_related('equipamento__entidade_fabricante')\
            .prefetch_related(Prefetch('historicolocal_set',
                                       queryset=HistoricoLocal.objects
                                       .select_related('estado', 'endereco__detalhe', 'endereco__detalhe__endereco',
                                                       'endereco', 'endereco__endereco__entidade'))):
        if p.historico_atual_prefetched:
            if estado_id != '0':
                if p.historico_atual_prefetched.estado.id != int(estado_id):
                    continue

            ht = p.historico_atual_prefetched
            entidades.append({'entidade': ht.endereco.end.entidade, 'local': ht.endereco.complemento, 'patrimonio': p,
                              'posicao': ht.posicao})

    entidades.sort(key=lambda x: x['posicao'])
    entidades.sort(key=lambda x: x['local'])
    entidades.sort(key=lambda x: x['entidade'].sigla)

    entidade = ''
    local = ''
    for i in range(len(entidades)):
        if entidades[i]['entidade'] != entidade:
            entidade = entidades[i]['entidade']
            local = entidades[i]['local']
            continue
        if entidades[i]['local'] != local:
            local = entidades[i]['local']
            entidades[i]['entidade'] = ''
            continue

        entidades[i]['entidade'] = ''
        entidades[i]['local'] = ''

    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento.html', {'entidades': entidades, 'tipo': tipo})


@login_required
@require_safe
def por_tipo_equipamento_old(request, pdf=0):
    if len(request.GET) < 1:
        return TemplateResponse(request, 'patrimonio/sel_tipo_equip.html',
                                {'tipos': TipoEquipamento.objects.all(), 'estados': Estado.objects.all(),
                                 'pns': Equipamento.objects.values_list('part_number', flat=True)
                                 .order_by('part_number').distinct()})

    tipo_id = request.GET.get('tipo')
    entidades = []
    if tipo_id == '0':
        patrimonios_tipo = Patrimonio.objects.all()
        tipo = 'todos'
    else:
        patrimonios_tipo = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)
        tipo = TipoEquipamento.objects.get(id=tipo_id)

    estado_id = request.GET.get('estado')
    if estado_id != '0':
        for p in patrimonios_tipo:
            if p.historico_atual is None:
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)
            elif p.historico_atual.estado.id != int(estado_id):
                patrimonios_tipo = patrimonios_tipo.exclude(id=p.id)

    part_number = request.GET.get('partnumber')
    if part_number != '0':
        patrimonios_tipo = patrimonios_tipo.filter(equipamento__part_number=part_number)

    for e in Entidade.objects.all():
        patrimonios_entidade = patrimonios_tipo.all()

        for p in patrimonios_entidade:
            if p.historico_atual is None:
                patrimonios_entidade = patrimonios_entidade.exclude(id=p.id)
            elif p.historico_atual.endereco.end.entidade != e:
                patrimonios_entidade = patrimonios_entidade.exclude(id=p.id)
        if patrimonios_entidade.count() > 0:
            entidade = {'entidade': e}
            locais = []
            for l in sorted(set([p.historico_atual.endereco.complemento for p in patrimonios_entidade])):
                patrimonios_local = patrimonios_entidade.all()
                for p in patrimonios_local:
                    if p.historico_atual is None:
                        patrimonios_local = patrimonios_local.exclude(id=p.id)
                    elif p.historico_atual.endereco.complemento != l:
                        patrimonios_local = patrimonios_local.exclude(id=p.id)
                local = {'local': l, 'patrimonios': patrimonios_local}
                locais.append(local)
            entidade['locais'] = locais
            entidades.append(entidade)

    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento.html', {'entidades': entidades, 'tipo': tipo})


@login_required_or_403
@require_safe
def ajax_filtra_pn_estado(request):
    tipo_id = request.GET.get('id')
    if tipo_id == '0':
        part_numbers = Equipamento.objects.values_list('part_number', flat=True).order_by('part_number').distinct()
        patrimonios = Patrimonio.objects.all()
    else:
        part_numbers = Equipamento.objects.filter(tipo__id=tipo_id).values_list('part_number', flat=True)\
            .order_by('part_number').distinct()
        patrimonios = Patrimonio.objects.filter(equipamento__tipo__id=tipo_id)

    pns = []
    for p in part_numbers:
        pns.append({'pk': p, 'value': '%s (%s)' % (p, patrimonios.filter(equipamento__part_number=p)
                                                   .order_by('id').distinct().count())})

    estados = []
    for e in Estado.objects.all():
        patrimonios_estado = patrimonios.all().prefetch_related(
            Prefetch('historicolocal_set', queryset=HistoricoLocal.objects.select_related('estado')))
        for p in patrimonios_estado:
            if not p.historico_atual_prefetched:
                patrimonios_estado = patrimonios_estado.exclude(id=p.id)
            elif p.historico_atual_prefetched.estado != e:
                patrimonios_estado = patrimonios_estado.exclude(id=p.id)

        estados.append({'pk': e.id, 'value': '%s (%s)' % (e, patrimonios_estado.order_by('id').distinct().count())})

    retorno = {'estados': estados, 'pns': pns}
    retorno_json = json.dumps(retorno)

    return HttpResponse(retorno_json, content_type="application/json")


@login_required
@permission_required('patrimonio.rel_adm_por_termo', raise_exception=True)
@require_safe
def por_termo(request, pdf=0):
    """
     Relatório Administrativo - Relatório de Patrimônio por termo de outorga.

    """
    termo_id = request.GET.get('termo') or request.POST.get('termo')
    modalidade = request.GET.get('modalidade') or request.POST.get('modalidade')
    agilis = request.GET.get('agilis') or request.POST.get('agilis')
    doado = request.GET.get('doado') or request.POST.get('doado')
    localizado = request.GET.get('localizado') or request.POST.get('localizado')
    numero_fmusp = request.GET.get('numero_fmusp') or request.POST.get('numero_fmusp')
    ver_numero_fmusp = request.GET.get('ver_numero_fmusp') or request.POST.get('ver_numero_fmusp')
    marcas = request.GET.getlist('marca') or request.POST.getlist('marca')

    template_name = 'por_termo'

    # Se não tiver Termo selecionado, volta para a tela de seleção de filtros.
    ids_fabricantes_de_patrimonios = Patrimonio.objects.filter(
        pagamento__protocolo__termo_id=termo_id, equipamento__entidade_fabricante__isnull=False)\
        .select_related('equipamento__entidade_fabricante')\
        .values_list('equipamento__entidade_fabricante__id')\
        .order_by('equipamento__entidade_fabricante__sigla')

    filtro_marcas = Entidade.objects.filter(id__in=ids_fabricantes_de_patrimonios)

    filtro_termos = Termo.objects.all()
    if termo_id is None:
        return TemplateResponse(request, 'patrimonio/escolhe_termo.html',
                                {'filtro_termos': filtro_termos, 'filtro_marcas': filtro_marcas})

    if termo_id != '0':
        qs = Termo.objects.filter(id=termo_id)
    else:
        if Variavel.objects.filter(nome=Variavel.TERMO_EXCLUIDO_IDS).exists():
            termos_excluidos = Variavel.objects.get(nome=Variavel.TERMO_EXCLUIDO_IDS).valor
            if termos_excluidos:
                termo_excluido_ids = map(int, termos_excluidos.split(','))
                qs = Termo.objects.exclude(id__in=termo_excluido_ids)

            else:
                qs = Termo.objects.all()
        else:
            qs = Termo.objects.all()

    termo_filtro = None
    if qs.exists():
        termo_filtro = qs[0]

    termos = []

    if agilis == '0':
        patrimonios = Patrimonio.objects.filter(agilis=False)
    elif agilis == '1':
        patrimonios = Patrimonio.objects.filter(agilis=True)
    else:
        patrimonios = Patrimonio.objects.all()

    if doado == '0':
        patrimonios = patrimonios.exclude(historicolocal__endereco__endereco__entidade__recebe_doacao=True,
                                          historicolocal__estado__id=1)
    elif doado == '1':
        patrimonios = patrimonios.filter(historicolocal__endereco__endereco__entidade__recebe_doacao=True)

    if localizado == '1':
        patrimonios = patrimonios.exclude(historicolocal__endereco__complemento__icontains='Localizado')
    elif localizado == '0':
        patrimonios = patrimonios.filter(historicolocal__endereco__complemento__icontains='Localizado')

    if modalidade == '1':
        patrimonios = patrimonios.filter(
            pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla__in=['MPN', 'MPI'])
    elif modalidade == '2':
        patrimonios = patrimonios.filter(
            pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla__in=['MCN', 'MCI'])

    if numero_fmusp == '1':
        patrimonios = patrimonios.filter(numero_fmusp__isnull=False)
    elif numero_fmusp == '0':
        patrimonios = patrimonios.filter(numero_fmusp__isnull=True)

    if marcas and len(marcas) > 0:
        filter_marcas = []
        for m in marcas:
            if m and m != '0':
                filter_marcas.append(m)
        if len(filter_marcas) > 0:
            patrimonios = patrimonios.filter(equipamento__entidade_fabricante__id__in=filter_marcas)

    patrimonios = patrimonios.select_related('equipamento__entidade_fabricante', 'equipamento__tipo')

    for t in qs:
        termo = {'termo': t}
        tps = []
        pat_termo = patrimonios.filter(pagamento__protocolo__termo=t)
        if numero_fmusp == '1':
            termo.update({'patrimonios': pat_termo.order_by('numero_fmusp', 'descricao', 'complemento')})
            termos.append(termo)
            # continue

        tipos = pat_termo.values_list('tipo', flat=True).order_by('tipo').distinct()
        for tipo in Tipo.objects.filter(id__in=tipos):
            tp = {'tipo': tipo}
            pgtos = []
            pt = pat_termo.filter(tipo=tipo)
            pagtos = pt.values_list('pagamento', flat=True).order_by('numero_fmusp').distinct()
            for pg in Pagamento.objects.filter(id__in=pagtos).select_related('protocolo'):
                pgto = {'pg': pg,
                        'patrimonios': pt.filter(pagamento=pg).order_by('numero_fmusp', 'descricao', 'complemento')}
                pgtos.append(pgto)
            tp.update({'pagamentos': pgtos})
            tps.append(tp)
        termo.update({'tipos': tps})
        termos.append(termo)

    if pdf:
        context_dict = {'termo': termo_filtro, 'termos': termos, 'i': itertools.count(1), 'numero_fmusp': numero_fmusp,
                        'ver_numero_fmusp': ver_numero_fmusp, }
        if termo_id != 0 and len(qs) > 0:
            context_dict.update({'t': termo_filtro})
        return render_to_pdf_weasy('patrimonio/%s.pdf' % template_name, context_dict, request=request,
                                   filename='inventario_por_termo.pdf')
    else:
        return TemplateResponse(request, 'patrimonio/%s.html' % template_name,
                                {'termos': termos, 'i': itertools.count(1), 'termo': termo_filtro, 'marca': marcas,
                                 'modalidade': modalidade, 'agilis': agilis, 'doado': doado, 'localizado': localizado,
                                 'numero_fmusp': numero_fmusp, 'ver_numero_fmusp': ver_numero_fmusp,
                                 'filtro_marcas': filtro_marcas, 'filtro_termos': filtro_termos,
                                 })


@login_required
@permission_required('patrimonio.rel_tec_racks', raise_exception=True)
@require_safe
def racks(request):
    """
     Relatório Técnico - Relatório de racks (bayface).

    """
    # Busca os endereços que possuem Racks no estadoAtivos
    locais = EnderecoDetalhe.objects.filter(historicolocal__estado__id=Estado.PATRIMONIO_ATIVO,
                                            historicolocal__patrimonio__equipamento__tipo__nome='Rack',
                                            mostra_bayface=True,)\
        .select_related('endereco__entidade').order_by('id').distinct()

    # Buscando os datacenters, com Entidade e Nome do endereçco
    todos_dcs = []
    for local in locais:
        nome = local.complemento

        entidade = local.entidade()
        if entidade:
            nome = "%s - %s" % (entidade, nome)

        dc = {'nome': nome, 'id': local.id}
        todos_dcs.append(dc)
    # Fazendo a ordenação pelo nome do Datacenter
    todos_dcs.sort(key=lambda c: c['nome'].upper(), reverse=False)

    p_dc = request.GET.get('dc_id')
    p_rack = request.GET.get('rack_id')

    dcs = _rack_data(p_dc, p_rack)

    chk_stencil = request.GET.get('chk_stencil') if request.GET.get('chk_stencil') else 1
    chk_legenda = request.GET.get('chk_legenda') if request.GET.get('chk_legenda') else 1
    chk_legenda_desc = request.GET.get('chk_legenda_desc') if request.GET.get('chk_legenda_desc') else 0
    chk_outros = request.GET.get('chk_outros') if request.GET.get('chk_outros') else 1
    chk_avisos = request.GET.get('chk_avisos') if request.GET.get('chk_avisos') else 1
    chk_traseira = request.GET.get('chk_traseira') if request.GET.get('chk_traseira') else 0

    context = {'dcs': dcs, 'todos_dcs': todos_dcs, 'chk_legenda': chk_legenda, 'chk_legenda_desc': chk_legenda_desc,
               'chk_stencil': chk_stencil, 'chk_outros': chk_outros, 'chk_avisos': chk_avisos,
               'chk_traseira': chk_traseira}
    if request.GET.get('pdf') == "2":
        return render_to_pdf_weasy('patrimonio/racks-wk.pdf', context, request=request,
                                   filename='diagrama_de_racks.pdf', zoom=1)
    elif request.GET.get('pdf'):
        return TemplateResponse(request, 'patrimonio/racks-wk.pdf', context)
    else:
        return TemplateResponse(request, 'patrimonio/racks.html', context)


def _rack_data(datacenter_id, rack_id):
    dcs = []
    if datacenter_id is not None and int(datacenter_id) > 0:
        locais = EnderecoDetalhe.objects.filter(id=datacenter_id)

        for local in locais:
            racks = []

            if rack_id:
                patrimonio_racks = PatrimonioRack.objects.filter(id=rack_id, historicolocal__endereco__id=local.id)
            else:
                patrimonio_racks = PatrimonioRack.get_racks_as_list(local.id)

            fileiras = []
            rack_anterior = None
            for rack in patrimonio_racks:
                if rack.historico_atual_prefetched.estado.id == Estado.PATRIMONIO_ATIVO:
                    posicao_atual = rack.historico_atual_prefetched.posicao_rack_numero
                    if not rack_anterior \
                            or posicao_atual != rack_anterior.historico_atual_prefetched.posicao_rack_numero:
                        racks = []
                        fileiras.append({'racks': racks})
                        rack_anterior = rack

                    equipamentos = []
                    equipamentos_fora_visao = []
                    equipamentos_pdu = []
                    conflitos = []

                    eixoY = 0
                    if not rack.tamanho:
                        rack.tamanho = 42
                        conflitos.append({'obs': u'Rack não possui tamanho.'})

                    # recupera os equipamentos do rack ordenados pela posição no rack
                    pts = rack.get_patrimonios()

                    ptAnterior = None
                    for pt in pts:
                        tamanho = 0
                        if pt.tamanho:
                            tamanho = pt.tamanho
                        # calculando a altura em furos
                        tam = int(round(tamanho * 3))

                        # Setando Imagem do equipamento
                        imagem = None
                        imagem_traseira = None
                        if pt.equipamento and pt.equipamento.imagem:
                            imagem = pt.equipamento.imagem.url
                        if pt.equipamento and pt.equipamento.imagem_traseira:
                            imagem_traseira = pt.equipamento.imagem_traseira.url

                        # Verificando profundidade
                        # Assinala somente se ocupa a profundidade toda, ou somente metade
                        # da profundidade do rack
                        profundidade = 1.0
                        if rack.equipamento.dimensao_id and pt.equipamento.dimensao_id:
                            if pt.equipamento.dimensao.profundidade < (rack.equipamento.dimensao.profundidade / 2):
                                profundidade = 0.5

                        pos = pt.historico_atual_prefetched.posicao_furo - 1

                        eixoY = pt.eixoy_em_px()

                        last_equipamento = {'id': pt.id, 'tam': tam, 'eixoY': pt.eixoy_em_px(),
                                            'eixoY_pt': pt.eixoy_em_pt(), 'tam_u': tamanho, 'altura': pt.altura_em_px(),
                                            'altura_pt': pt.altura_em_pt(), 'profundidade': profundidade,
                                            'pos_original': pt.historico_atual_prefetched.posicao_furo,
                                            'pos_col': pt.historico_atual_prefetched.posicao_colocacao,
                                            'imagem': imagem, 'imagem_traseira': imagem_traseira, 'sn': pt.ns,
                                            'pn': pt.part_number, 'modelo': pt.modelo, 'nome': pt.apelido,
                                            'descricao': pt.descricao or u'Sem descrição', 'conflito': False,
                                            'flag_traseiro': pt.is_posicao_traseira()}

                        if pt.is_pdu():
                            # Guardando as calhas de tomadas para apresentar nas laterais do Rack
                            equipamentos_pdu.append(last_equipamento)
                        elif pos < 0 or pt.historico_atual_prefetched.posicao_colocacao in \
                                ('TD', 'TE', 'piso', 'lD', 'lE'):
                            # Verifica equipamentos posicionados de forma errada no rack
                            if pos < 0:
                                pos = '-'
                                last_equipamento['pos'] = pos
                            equipamentos_fora_visao.append(last_equipamento)
                            continue
                        else:
                            # x a partir do topo do container
                            # Adiciona os equipamentos frontais e traseiros.
                            # O layout deve ser tratado no template
                            equipamentos.append(last_equipamento)

                        # CHECAGEM DE PROBLEMAS
                        if pt.tamanho is None:
                            obs = u'Equip. com tamanho ZERO.'
                            conflitos.append({'obs': obs, 'eq1': last_equipamento})
                            last_equipamento['conflito'] = True
                        elif pos + tam > rack.altura_furos:
                            # Ocorre quando um equipamento está passando do limite máximo do rack
                            # obs = '{!s} + {!s} > {!s}'.format(pos, (tam), 126)
                            obs = u'Equip. acima do limite do rack.'
                            conflitos.append({'obs': obs, 'eq1': last_equipamento})
                            last_equipamento['conflito'] = True

                        elif len(equipamentos) >= 2 and eixoY:
                            # Ocorre quando um equipamento sobrepoe o outro
                            # Caso estejam na mesma posição 01 ou 02, ou então, haja um equipamento que ocupe toda
                            # largura do rack
                            # Não ocorre quando os equipamentos estiverem lado a lado (marcados no attr pos_col,
                            # por exemplo, 01 com 02)

                            if ptAnterior and ptAnterior['profundidade'] + last_equipamento['profundidade'] <= 1.0 and \
                                    ptAnterior['eixoY'] + ptAnterior['tam'] > eixoY and \
                                    (ptAnterior['pos_col'] == last_equipamento['pos_col'] or
                                        not ptAnterior['pos_col'] or not last_equipamento['pos_col']):

                                obs = u'Equipamentos sobrepostos.'
                                conflitos.append({'obs': obs, 'eq1': ptAnterior, 'eq2': last_equipamento})
                                last_equipamento['conflito'] = True
                                equipamentos[-2]['conflito'] = True
                        elif pos == -2:
                            # Posição -2 significa que o patrimonio não possui furo.
                            obs = u'Equip. sem posição definida.'
                            conflitos.append({'obs': obs, 'eq1': last_equipamento})
                            last_equipamento['conflito'] = True
                        elif pos < 0:
                            # Posição negativa
                            # Ocorre quando o equipamento não tem uma posição válida
                            obs = u'Equip. abaixo do limite do rack.'
                            conflitos.append({'obs': obs, 'eq1': last_equipamento})
                            last_equipamento['conflito'] = True
                        elif len(equipamentos) > 0 and last_equipamento['pos_col'] and last_equipamento['pos_col']\
                                not in ('01', '02', 'T', 'TD', 'TE', 'T01', 'T02', 'piso', 'lD', 'lE', 'LD', 'LE'):
                            obs = u'Posicao inválida %s' % pt.historico_atual_prefetched.posicao_colocacao
                            conflitos.append({'obs': obs, 'eq1': last_equipamento},)
                            last_equipamento['conflito'] = True

                        ptAnterior = last_equipamento

                    rack = {'id': rack.id, 'altura': int(rack.tamanho) * 3.0, 'nome': rack.apelido,
                            'altura_pts': int(rack.tamanho) * Patrimonio.U_TO_PT, 'marca': rack.marca,
                            'altura_pxs': int(rack.tamanho) * Patrimonio.U_TO_PX,
                            'altura_count': range(1, rack.tamanho + 1), 'equipamentos': equipamentos,
                            'equipamentos_fora_visao': equipamentos_fora_visao, 'equipamentos_pdu': equipamentos_pdu,
                            'conflitos': conflitos
                            }

                    espaco_ocupado = calcula_ocupacao(equipamentos)

                    # Calculo de uso do rack
                    rack['vazio'] = '%.2f%%' % ((espaco_ocupado * 100.0) / (rack['altura']))
                    racks.append(rack)

            dcEntidade = Entidade.objects.filter(endereco__enderecodetalhe=local)

            dc = {'id': local.id, 'nome': local.complemento, 'fileiras': fileiras, 'entidade': dcEntidade[0].sigla}
            dcs.append(dc)
    return dcs


def calcula_ocupacao(pts):
    """
    Calculo de ocupação do rack
    """
    tamanhos = []

    for pt in pts:
        atualizou = False
        for tm in tamanhos:
            if pt['eixoY'] <= tm['eixoYMin'] <= pt['eixoY'] + pt['tam']:
                # O ponto inferior está dentro do intervalo de tamanho do equipamento?

                tm['eixoYMin'] = min(tm['eixoYMin'], pt['eixoY'])
                tm['eixoYMax'] = max(tm['eixoYMax'], pt['eixoY'] + pt['tam'])
                atualizou = True

            elif pt['eixoY'] <= tm['eixoYMax'] <= pt['eixoY'] + pt['tam']:
                # O ponto inferior está dentro do intervalo de tamanho do equipamento?
                tm['eixoYMin'] = min(tm['eixoYMin'], pt['eixoY'])
                tm['eixoYMax'] = max(tm['eixoYMax'], pt['eixoY'] + pt['tam'])
                atualizou = True

        if not atualizou:
            item = {'eixoYMin': pt['eixoY'], 'eixoYMax': pt['eixoY'] + pt['tam']}
            tamanhos.append(item)

    ocupacao = 0
    for tm in tamanhos:
        ocupacao += tm['eixoYMax'] - tm['eixoYMin']

    return ocupacao


@login_required
@permission_required('patrimonio.rel_tec_relatorio_rack', raise_exception=True)
def relatorio_rack(request):
    """
     Relatório Técnico - Relatório por rack.

     Relatório de patrimônio separados por rack.
     Exibe o bayface de visão frontal e traseira, além de uma lista dos equipamentos que estão
     localizados no rack e que não são exibidos no bayface.

    """
    p_dc = request.GET.get('dc')
    p_rack = request.GET.get('rack')

    # Busca os endereços que possuem Racks no estadoAtivos
    locais = EnderecoDetalhe.objects.filter(historicolocal__estado__id=Estado.PATRIMONIO_ATIVO,
                                            historicolocal__patrimonio__equipamento__tipo__nome='Rack',
                                            mostra_bayface=True).order_by('id').distinct()

    todos_dcs = []
    for local in locais:
        nome = local.complemento

        entidade = local.entidade()
        if entidade:
            nome = "%s - %s" % (entidade, nome)

        dc = {'nome': nome, 'id': local.id}
        todos_dcs.append(dc)
    # Fazendo a ordenação pelo nome do Datacenter
    todos_dcs.sort(key=lambda c: c['nome'].upper(), reverse=False)

    patrimonio_racks = []
    dcs = []
    if p_dc:
        patrimonio_racks = PatrimonioRack.get_racks_as_list(p_dc)
    if p_rack:
        dcs = _rack_data(p_dc, p_rack)

    context = {'dcs': dcs, 'todos_dcs': todos_dcs, 'patrimonio_racks': patrimonio_racks}

    if request.GET.get('pdf') == "2":
        return render_to_pdf_weasy('patrimonio/relatorio-racks-wk.pdf', context, request=request,
                                   filename='relatorio_de_racks.pdf', zoom=0.66)
    elif request.GET.get('pdf'):
        return TemplateResponse(request, 'patrimonio/relatorio-racks-wk.pdf', context)
    else:
        return TemplateResponse(request, 'patrimonio/relatorio-racks.html', context)

    #    context = {'dcs':dcs, 'todos_dcs':todos_dcs, 'chk_legenda':chk_legenda, 'chk_legenda_desc':chk_legenda_desc,
    #  'chk_stencil':chk_stencil, 'chk_outros':chk_outros, 'chk_avisos':chk_avisos, 'chk_traseira':chk_traseira}
    #    if request.GET.get('pdf') == "2":
    #        return render_to_pdf_weasy('patrimonio/racks-wk.pdf', context, request=request,
    # filename='diagrama_de_racks.pdf', zoom=1)


@login_required
@permission_required('patrimonio.rel_adm_presta_contas', raise_exception=True)
def presta_contas(request):
    """
     Relatório Administrativo - Relatório de Prestação de contas patrimonial.

    """
    termos = []
    for t in Termo.objects.all():
        termo = {'termo': t}
        termos.append(termo)

    return TemplateResponse(request, 'patrimonio/presta_contas.html', {'termos': termos})


@login_required_or_403
@require_safe
def ajax_abre_arvore(request):
    ret = []
    if request.GET.get('id'):
        termo_id = request.GET.get('id')
        model = request.GET.get('model')
        if model == 'termo':
            for n in Termo.objects.get(id=termo_id).natureza_gasto_set\
                    .filter(item__origemfapesp__pagamento__patrimonio__isnull=False).distinct():
                ret.append({'data': n.modalidade.sigla,
                            'attr': {'style': 'padding-top:4px;', 'o_id': n.id, 'o_model': n._meta.model_name}})
        elif model == 'natureza_gasto':
            for i in Natureza_gasto.objects.get(id=termo_id).item_set\
                    .filter(origemfapesp__pagamento__patrimonio__isnull=False).distinct():
                ret.append({'data': i.__unicode__(),
                            'attr': {'style': 'padding-top:4px;', 'o_id': i.id, 'o_model': i._meta.model_name}})
        elif model == 'item':
            for o in Item.objects.get(id=termo_id).origemfapesp_set.filter(pagamento__patrimonio__isnull=False).distinct():
                for p in o.pagamento_set.filter(patrimonio__isnull=False).distinct():
                    ret.append({'data': '%s %s' % (p.protocolo.tipo_documento.sigla or '', p.protocolo.num_documento),
                                'attr': {'style': 'padding-top:4px;', 'o_id': p.id, 'o_model': p._meta.model_name}})
        elif model == 'pagamento':
            for pt in Pagamento.objects.get(id=termo_id).patrimonio_set.all():
                ret.append({'data': '<div><div class="col1"></div><div class="col2"><div class="menor">%s</div>'
                                    '<div class="maior">%s</div><div class="maior">%s - %s</div>'
                                    '<div class="medio">%s</div><div class="menor">%s</div><div class="menor">%s</div>'
                                    '<div class="menor">%s</div></div><div style="clear:both;"></div></div>' %
                                    (pt.tipo, pt.ns, pt.descricao, pt.complemento, pt.equipamento.tipo, pt.valor,
                                     'Sim' if pt.agilis else u'Não', 'Sim' if pt.checado else u'Não'),
                            'attr': {'style': 'height:130px;'}})
    else:
        for t in Termo.objects.all():
            ret.append({'data': t.__unicode__(),
                        'attr': {'style': 'padding-top:6px;', 'o_id': t.id, 'o_model': t._meta.model_name}})
    retorno_json = json.dumps(ret)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required
@permission_required('patrimonio.rel_tec_patr_tipo_equipamento', raise_exception=True)
def por_tipo_equipamento2(request):
    """
     Relatório Técnico - Relatório de Patrimônio por tipo de equipamento.

    """
    return TemplateResponse(request, 'patrimonio/por_tipo_equipamento2.html')


@login_required_or_403
@require_safe
def ajax_abre_arvore_tipo(request):
    ret = []
    if request.GET.get('id'):
        tipo_id = request.GET.get('id')
        model = request.GET.get('model')
        if model == 'tipoequipamento':
            for e in TipoEquipamento.objects.get(id=tipo_id).equipamento_set.all():
                ret.append({'data': e.descricao,
                            'attr': {'style': 'padding-top:4px;', 'o_id': e.id, 'o_model': e._meta.model_name}})
        elif model == 'equipamento':
            patrimonios = list(Equipamento.objects.get(id=tipo_id).patrimonio_set.all())
            try:
                patrimonios.sort(key=lambda x: x.historico_atual.endereco.end.entidade.sigla)
            except:
                pass

            if patrimonios and len(patrimonios):
                retPatrimonio = u'<div><div class="col1"></div><div class="col2">'
                retPatrimonio += u'<table><tr class="col2"><th class="th_1"><div>Entidade</div></th>' \
                                 u'<th class="th_2"><div>Local</div></th>'
                retPatrimonio += u'<th class="th_3"><div>Posição</div></th><th class="th_4"><div>Marca</div></th>'
                retPatrimonio += u'<th class="th_5"><div>Modelo</div></th><th class="th_6"><div>Part number</div></th>'
                retPatrimonio += u'<th class="th_7"><div>NS</div></th><th class="th_8"><div>Estado</div></th></tr>'
                for p in patrimonios:
                    ha = p.historico_atual
                    pUrl = reverse('admin:patrimonio_patrimonio_change', args=(p.id,))
                    r = u'<tr class=""><td class="td_1"><div><a href="%s" target="_blank">%s</a></div></td>' % \
                        (pUrl, ha.endereco.end.entidade if ha else 'ND')
                    r += u'<td class="td_2"><a href="%s" target="_blank"><div>%s</a></div></td>' %\
                         (pUrl, ha.endereco.complemento if ha else 'ND')
                    r += u'<td class="td_3"><a href="%s" target="_blank"><div>%s</a></div></td>' % \
                         (pUrl, ha.posicao if ha and ha.posicao else 'ND')

                    eq_fabricante = ''
                    eq_modelo = ''
                    eq_part_number = ''
                    if p.equipamento:
                        if p.equipamento.entidade_fabricante:
                            eq_fabricante = p.equipamento.entidade_fabricante.sigla
                        if p.equipamento.modelo:
                            eq_modelo = p.equipamento.modelo
                        if p.equipamento.part_number:
                            eq_part_number = p.equipamento.part_number

                    r += u'<td class="td_4"><a href="%s" target="_blank"><div>%s</a></div></td>' % (pUrl, eq_fabricante)
                    r += u'<td class="td_5"><a href="%s" target="_blank"><div>%s</a></div></td>' % (pUrl, eq_modelo)
                    r += u'<td class="td_6"><a href="%s" target="_blank"><div>%s</a></div></td>' % \
                         (pUrl, eq_part_number)
                    r += u'<td class="td_7"><a href="%s" target="_blank"><div>%s</a></div></td>' % (pUrl, p.ns)
                    r += u'<td class="td_8"><a href="%s" target="_blank"><div>%s</a></div></td>' % \
                         (pUrl, ha.estado if ha else 'ND')
                    retPatrimonio = '%s %s' % (retPatrimonio, r)
                retPatrimonio += '</table></div><div style="clear:both;"></div></div>'
                ret.append({'data': retPatrimonio,
                            'attr': {'style': 'padding-top:4px; height:%spx' % ((1 + len(patrimonios)) * 20)}})
    else:
        for tp in TipoEquipamento.objects.all():
            # ret.append({'data':'%s <a onclick="$(\'#blocos\').jstree(\'open_all\', \'#%s-%s\')"
            # style="color:#0000aa;">Abrir tudo</a>' % (tp.__unicode__(), tp._meta.model_name, tp.id),
            # 'attr':{'id':'%s-%s'% (tp._meta.model_name, tp.id), 'style':'padding-top:6px;', 'o_id':tp.id,
            # 'o_model': tp._meta.model_name}})
            ret.append({'data': '%s <a onclick="abre_fecha(\'%s-%s\', \'blocos\'); return false;" '
                                'id="a-%s-%s" style="color:#0000aa;">Abrir tudo</a>' %
                                (tp.__unicode__(), tp._meta.model_name, tp.id, tp._meta.model_name, tp.id),
                        'attr': {'id': '%s-%s' % (tp._meta.model_name, tp.id), 'style': 'padding-top:6px;',
                                 'o_id': tp.id, 'o_model': tp._meta.model_name}})

    retorno_json = json.dumps(ret)
    return HttpResponse(retorno_json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_patrimonio_historico(request):
    """
    Retorna os dados de um Historico Atual dado o ID de um patrimonio.

    Utilizado no PatrimonioAdminForm, ou seja, no form do admin - patrimonio.
    """
    patr_id = request.GET.get('id')
    patr = Patrimonio.objects.get(id=patr_id)
    historico = patr.historico_atual

    retorno = {'entidade_id': historico.endereco.endereco.entidade_id if historico.endereco.endereco_id else '',
               'entidade_desc': historico.endereco.endereco.entidade.__unicode__()
               if historico.endereco.endereco_id and historico.endereco.endereco.entidade_id else '',
               'localizacao_id': historico.endereco_id,
               'localizacao_desc': historico.endereco.__unicode__(),
               'posicao': historico.posicao,
               'descricao': historico.descricao,
               'data': str(datetime.date.today()),
               'estado_id': historico.estado_id,
               'estado_desc': historico.estado.__unicode__(),
               'memorando_id': historico.memorando_id,
               'memorando_desc': historico.memorando.__unicode__() if historico.memorando_id else '',
               }

    retorno_json = json.dumps(retorno)
    return HttpResponse(retorno_json, content_type='application/json')


@login_required
@permission_required('patrimonio.rel_tec_planta_baixa_edit', raise_exception=True)
def planta_baixa_edit(request):
    """
     Relatório Técnico - Relatório de Planta baixa - racks.

     Página para configurar o design de Planta baixa dos cages

    """
    # Busca os endereços que possuem Racks no estadoAtivos
    locais = PlantaBaixaDataCenter.objects.all()

    todos_dcs = []
    for local in locais:
        dc = {'nome': local.endereco.complemento, 'id': local.id}
        todos_dcs.append(dc)

    # Se for um POST, executar a funcionalidade de salvar os dados
    if request.POST:
        with transaction.atomic():
            dc_id = request.POST.get('dc_id')
            dc = PlantaBaixaDataCenter.objects.get(id=dc_id)

            dc.w = request.POST.get('dc_w') or 0
            dc.h = request.POST.get('dc_h') or 0
            # salvando parametros de datacenter
            dc.save()

            length = request.POST.get('obj_length')
            for index in xrange(int(length)):
                post_patrimonio_id = request.POST.get('obj_patrimonio_id_%s' % index)
                post_objeto_id = request.POST.get('obj_objeto_id_%s' % index)
                post_posicao_id = request.POST.get('obj_posicao_id_%s' % index)
                post_x = request.POST.get('obj_x_id_%s' % index) or ''
                post_y = request.POST.get('obj_y_id_%s' % index) or ''
                post_h = request.POST.get('obj_h_id_%s' % index) or ''
                post_w = request.POST.get('obj_w_id_%s' % index) or ''
                post_cor = request.POST.get('obj_cor_id_%s' % index)
                post_desc = request.POST.get('obj_desc_%s' % index)

                objeto = None
                posicao = None

                if post_posicao_id:
                    # recuperando uma posição de objeto
                    posicao = PlantaBaixaPosicao.objects.get(id=post_posicao_id)
                    objeto = posicao.objeto
                elif post_objeto_id:
                    # recuperando um objeto e buscando sua posição
                    objeto = PlantaBaixaObjeto.objects.get(id=post_objeto_id)
                    posicao = PlantaBaixaPosicao(objeto=objeto)
                elif post_patrimonio_id:
                    if post_patrimonio_id and PlantaBaixaObjeto.objects.filter(patrimonio=post_patrimonio_id).exists():
                        # recuperando um objeto a partir do patrimonio e buscando sua posição
                        objeto = PlantaBaixaObjeto.objects.get(patrimonio=post_patrimonio_id)
                        posicao = PlantaBaixaPosicao(objeto=objeto)
                    else:
                        # Criando um objeto novo a partir de um patrimonio (ex: racks novos)
                        patrimonio = Patrimonio.objects.get(id=post_patrimonio_id)
                        objeto = PlantaBaixaObjeto(data_center=dc, patrimonio=patrimonio)
                        objeto.titulo = patrimonio.apelido

                if not posicao:
                    # se não foi recuperada uma posição, cria um objeto novo
                    posicao = PlantaBaixaPosicao(objeto=objeto)

                # se não for definido as coordenadas de posição, o objeto de posição deve ser removido
                if post_x != '' and post_y != '':
                    posicao.x = Decimal(post_x)
                    posicao.y = Decimal(post_y)
                    posicao.h = Decimal(post_h)
                    posicao.w = Decimal(post_w)
                    posicao.cor = post_cor
                    posicao.descricao = post_desc

                    if objeto:
                        objeto.save()
                    if posicao:
                        posicao.objeto = objeto
                        posicao.save()
                elif posicao.id is not None:
                    posicao.delete()

    # Independente de salvar, devemos carregar os dados de exibição.
    p_dc = request.GET.get('dc')

    dc = {}
    objetos = []
    if p_dc is not None and p_dc != 0:
        planta_datacenter = PlantaBaixaDataCenter.objects.get(id=p_dc)
        # Recuperando lista de racks que estão no datacenter
        patrimonio_racks = Patrimonio.objects.filter(
            equipamento__tipo__nome='Rack', historicolocal__endereco__id=planta_datacenter.endereco_id)\
            .select_related('equipamento')

        patrimonio_racks = list(patrimonio_racks)
        # Ordena os racks pela posição. Ex: R042 - ordena pela fila 042 e depois pela posição R
        patrimonio_racks.sort(key=lambda x: x.historico_atual_prefetched.posicao_rack_letra, reverse=False)
        patrimonio_racks.sort(key=lambda x: x.historico_atual_prefetched.posicao_rack_numero, reverse=True)

        for rack in patrimonio_racks:
            posicao = ''
            objeto = ''
            cor = ''
            desc = ''

            # Verifica se o rack já tem uma posição na planta baixa
            if PlantaBaixaPosicao.objects.filter(objeto__patrimonio=rack.id).exists():
                posicao = PlantaBaixaPosicao.objects.get(objeto__patrimonio=rack.id)
                objeto = posicao.objeto
                cor = posicao.cor
                desc = posicao.descricao

            rack = {'patrimonio_id': rack.id, 'nome': rack.apelido, 'objeto': objeto, 'posicao': posicao, 'cor': cor,
                    'desc': desc}
            # Adicionando patrimonios do tipo rack
            objetos.append(rack)

        dc = {'id': planta_datacenter.id, 'nome': planta_datacenter.endereco.complemento, 'w': planta_datacenter.w,
              'h': planta_datacenter.h}

        # Adicionando outros objetos que não estão com posição definida
        for outro in PlantaBaixaObjeto.objects.filter(patrimonio__isnull=True, data_center=planta_datacenter.id):
            posicao = ''
            cor = ''
            desc = ''
            if PlantaBaixaPosicao.objects.filter(objeto=outro).exists():
                posicao = PlantaBaixaPosicao.objects.get(objeto=outro)
                cor = posicao.cor
                desc = posicao.descricao
            outro = {'patrimonio_id': '', 'nome': outro.titulo, 'objeto': outro, 'posicao': posicao, 'cor': cor,
                     'desc': desc}
            objetos.append(outro)

    context = {'dc': dc, 'todos_dcs': todos_dcs, 'objetos': objetos}

    if request.GET.get('pdf') == "2":
        return render_to_pdf_weasy('patrimonio/planta_baixa_racks.pdf', context, request=request,
                                   filename='diagrama_de_planta_baixa.pdf')
    else:
        return render_to_response('patrimonio/planta_baixa_racks.html', context, RequestContext(request, context))
