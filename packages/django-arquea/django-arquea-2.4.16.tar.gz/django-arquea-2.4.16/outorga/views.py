# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db.models import Sum, Prefetch
from django.contrib.auth.decorators import permission_required, login_required
from utils.decorators import login_required_or_403
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_safe
from django.db.models import Min, Max

from decimal import Decimal
import json as simplejson

from patrimonio.models import Patrimonio, Equipamento
from financeiro.models import Pagamento, Auditoria
from outorga.models import Termo, Modalidade, Item, Acordo, Contrato, EstadoOS, OrdemDeServico
from utils.functions import render_to_pdf_weasy, render_to_pdfxhtml2pdf, month_range

import logging
from identificacao.models import Entidade

# Get an instance of a logger
logger = logging.getLogger(__name__)

# def termo(request, termo_id):
#
#     """
#
#     """
#
#     u = request.user
#     if not u.is_authenticated():
#         return admin.site.login(request)
#
#     #if not u.has_perm('outorga.change_termo'):
#      #   raise PermissionDenied
#
#     t = get_object_or_404(Termo, pk=termo_id)
#
#     r = []
#     for p in t.outorga_set.all():
#         r.append(p)
#
#     return render_to_response('outorga/termo.html',
#                               {'termo' : t,
#                                'pedido' : r})
#
# def pedido(request, pedido_id):
#
#     """
#
#     """
#
#     u = request.user
#     if not u.is_authenticated():
#         return admin.site.login(request)
#
#     #if not u.has_perm('outorga.change_termo'):
#     #    raise PermissionDenied
#
#     p = get_object_or_404(Outorga, pk=pedido_id)
#
#     return render_to_response('outorga/pedido.html',
#                               {'pedido' : p})

# Gera uma lista com as modalidades do termo selecionado.
# def escolhe_termo(request):
#     if request.method == 'POST':
#         termo = int(request.POST.get('id'))
#
#         retorno = {}
#
#         if termo:
# 	    retorno['modalidade'] = []
#             retorno['item'] = []
#
#  	    t = Termo.objects.get(pk=termo)
#             modalidades = Modalidade.modalidades_termo(t)
#             itens = Item.objects.filter(natureza_gasto__termo=t, item=None)

#             for m in modalidades:
#                 retorno['modalidade'].append({'pk':m.pk, 'valor':m.__unicode__()})
#             for i in itens:
#                 retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})
#
#             if not retorno['modalidade']:
#                 retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
#             if not retorno['item']:
#                 retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
# 	else:
#             retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
#             retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
#
#         json = simplejson.dumps(retorno)
#     return HttpResponse(json,content_type="application/json")

# Gera uma lista dos itens de outorga conforme a modalidade selecionada.
# def escolhe_modalidade(request):
#     if request.method == 'POST':
#         retorno = []
#         id = request.POST.get('id')
#         previous = request.POST.get('previous')
#
#         if id and previous:
#             t = Termo.objects.get(pk=int(previous))
#             itens = Item.objects.filter(natureza_gasto__termo=t, natureza_gasto__modalidade=id, item=None)
#
#             for i in itens:
#                 retorno.append({'pk':i.pk, 'valor':i.__unicode__()})
#
#             if not retorno:
#                 retorno = [{"pk":"0","valor":"Nenhum registro"}]
#         else:
#             retorno = [{"pk":"0","valor":"Nenhum registro"}]
#
#         json = simplejson.dumps(retorno)
#     return HttpResponse(json,content_type="application/json")

# def seleciona_termo_natureza(request):
#     if request.method == 'POST':
#         termo = int(request.POST.get('id'))
#
#         retorno = []
#
#         if termo:
#
#             t = Termo.objects.get(pk=termo)
#
#             naturezas = Natureza_gasto.objects.filter(termo=t)
#
#             for n in naturezas:
#                 retorno.append({'pk':n.pk, 'valor':n.modalidade.sigla})
#             if not retorno:
#                 retorno = [{"pk":"0","valor":"Nenhum registro"}]
#         else:
#             retorno = [{"pk":"0","valor":"Nenhum registro"}]
#
#         json = simplejson.dumps(retorno)
#     return HttpResponse(json,content_type="application/json")
#
#
# # Gera listas modalidade, item e natureza conforme termo selecionado.
# def seleciona_mod_item_natureza(request):
#     if request.method == 'POST':
#         termo = int(request.POST.get('id'))
#
#         retorno = {}
#
#         if termo:
#             retorno['modalidade'] = []
#             retorno['item'] = []
#             retorno['natureza'] = []
#
#             t = Termo.objects.get(pk=termo)
#
#             modalidade = Modalidade.modalidades_termo(t)
#             itens = Item.objects.filter(natureza_gasto__termo=t, item=None)
#             naturezas = Natureza_gasto.objects.filter(termo=t)
#
#             for m in modalidade:
#                 retorno['modalidade'].append({'pk':m.pk, 'valor':m.__unicode__()})
#             for i in itens:
#                 retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})
#             for n in naturezas:
#                 retorno['natureza'].append({'pk':n.pk, 'valor':n.__unicode__()})
#
#             if not retorno['modalidade']:
#                 retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
#             if not retorno['item']:
#                 retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
#             if not retorno['natureza']:
#                 retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
#         else:
#             retorno['modalidade'] = [{"pk":"0","valor":"Nenhum registro"}]
#             retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
#             retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
#
#         json = simplejson.dumps(retorno)
#     return HttpResponse(json,content_type="application/json")
#
#
# # Gera uma lista dos itens de outorga conforme a modalidade selecionada.
# def seleciona_item_natureza(request):
#     if request.method == 'POST':
#         retorno = {}
#
#         id = request.POST.get('id')
#         previous = request.POST.get('previous')
#
#         if id and previous:
#             retorno['item'] = []
#             retorno['natureza'] = []
#
#             t = Termo.objects.get(pk=int(previous))
#             itens = Item.objects.filter(natureza_gasto__termo=t, natureza_gasto__modalidade=id, item=None)
#             naturezas = Natureza_gasto.objects.filter(termo=t, modalidade=id)
#
#             for i in itens:
#                 retorno['item'].append({'pk':i.pk, 'valor':i.__unicode__()})
#             for n in naturezas:
#                 retorno['natureza'].append({'pk':n.pk, 'valor':n.__unicode__()})
#
#             if not retorno['item']:
#                 retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
#             if not retorno['natureza']:
#                 retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
#         else:
#             retorno['item'] = [{"pk":"0","valor":"Nenhum registro"}]
#             retorno['natureza'] = [{"pk":"0","valor":"Nenhum registro"}]
#
#         json = simplejson.dumps(retorno)
#     return HttpResponse(json,content_type="application/json")

# ROGERIO: VERIFICAR SE EXISTE ALGUMA CHAMADA PARA ESTA VIEW
#         PARA A SUA REMOÇÃO DO SISTEMA
# def gastos_acordos(request):
#     acordos = []
#     acordo = ['']
#     for t in Termo.objects.filter(ano__gte=2005).order_by('ano'):
#         acordo.append('%s (%s)' % (t.__unicode__(), t.duracao_meses()))
#
#     acordos.append(acordo)
#     for a in Acordo.objects.all():
#
#         acordo = [a.descricao]
#         for t in Termo.objects.filter(ano__gte=2005).order_by('ano'):
#             total = Decimal('0.0')
#             for o in a.origemfapesp_set.filter(item_outorga__natureza_gasto__termo=t):
#                 total += o.gasto()
#             acordo.append(total)
#         acordos.append(acordo)
#
#     return render_to_pdf('outorga/acordos.pdf', {'acordos':acordos}, request=request)


@login_required
@permission_required('outorga.rel_ger_contratos', raise_exception=True)
@require_safe
def contratos(request, pdf=False):
    """
     Relatório Gerencial - Relatório de Contratos por Entidade.

    """
    # Filtrando as entidades pelo parametro de filtro 'entidade'
    entidade_id = request.GET.get('entidade')
    # Filtrando as entidades pelo parametro de filtro 'estadoos'
    estadoos_id = request.GET.get('estadoos')

    # Obj da Entidade escolhida para o filtro
    param_entidade = None
    # Obj da Entidade escolhida para o filtro
    param_estadoos = None

    entidades = Entidade.objects.prefetch_related(
        Prefetch('contrato_set', queryset=Contrato.objects.order_by('-data_inicio'))).order_by('sigla')

    # Filtrando as entidades
    if entidade_id and entidade_id != '0' and entidade_id.isdigit():
        entidades = entidades.filter(id=int(entidade_id))
        param_entidade = Entidade.objects.get(id=int(entidade_id))

    if estadoos_id and estadoos_id != '0' and estadoos_id.isdigit():
        param_estadoos = EstadoOS.objects.get(id=int(estadoos_id))

    retorno_entidades = []
    for e in entidades:

        cts = e.contrato_set.all()

        entidade = {'entidade': e.sigla}
        contratos = []
        for c in cts:
            contrato = {'id': c.id, 'inicio': c.data_inicio, 'termino': c.limite_rescisao, 'numero': c.numero,
                        'arquivo': c.arquivo, 'auto': c.auto_renova, 'os': []}
            ordens = []
            oss = c.ordemdeservico_set.select_related('tipo', 'estado')\
                .prefetch_related('arquivos').order_by('-data_inicio')

            for os in oss:
                if param_estadoos:
                    # Se tiver filtro de EstadoOS, somente adicionamos as OS filtradas
                    if param_estadoos.id == os.estado.id:
                        ordens.append(os)
                else:
                    ordens.append(os)

            if len(ordens) > 0:
                contrato.update({'os': ordens})

            if param_estadoos:
                # Se tiver filtro de EstadoOS, somente adicionamos os contratos com alguma OS
                if len(contrato['os']) > 0:
                    contratos.append(contrato)
            else:
                contratos.append(contrato)

        # Somente adicionamos as entidades com algum contrato válido
        if len(contratos) > 0:
            entidade.update({'contratos': contratos})
            retorno_entidades.append(entidade)

    if pdf == '2':
        return render(request, 'outorga/contratos.pdf', {'entidades': retorno_entidades,
                                                         'entidade': param_entidade, 'estadoos': param_estadoos})
    elif pdf:
        return render_to_pdf_weasy('outorga/contratos.pdf', {'entidades': retorno_entidades,
                                                             'entidade': param_entidade, 'estadoos': param_estadoos},
                                   request=request, filename="relatorio_contratos.pdf")
    else:
        # Selecionando os valores de Entidades para serem exibidas no filtro
        contrato_entidades = Contrato.objects.values_list('entidade__id')
        filtro_entidades = Entidade.objects.filter(id__in=contrato_entidades)

        # Selecionando os valores de Entidades para serem exibidas no filtro
        os_estadoos = OrdemDeServico.objects.values_list('estado__id')
        filtro_estadoos = EstadoOS.objects.filter(id__in=os_estadoos)

        return render(request, 'outorga/contratos.html',
                      {'entidades': retorno_entidades, 'filtro_entidades': filtro_entidades,
                       'filtro_estadoos': filtro_estadoos, 'entidade': param_entidade, 'estadoos': param_estadoos})


# ROGERIO: VERIFICAR SE EXISTE ALGUMA CHAMADA PARA ESTA VIEW
#         PARA A SUA REMOÇÃO DO SISTEMA
@login_required
@require_safe
def por_item(request):
    termo = request.GET.get('termo')
    entidade = request.GET.get('entidade')

    retorno = {'itens': ''}

    itens = Item.objects.filter(natureza_gasto__termo__id=termo)
    if entidade:
        itens = itens.filter(entidade__id=entidade)

    its = []
    for i in itens:
        it = {'item': i}
        pgs = []
        for p in Pagamento.objects.filter(origem_fapesp__item_outorga=i):
            pgs.append(p)
        it.update({'pgtos': pgs})
        its.append(it)

    retorno.update({'itens': its})
    return render(request, 'outorga/por_item.html', retorno)


@login_required
@require_safe
def relatorio_termos(request):
    termos = Termo.objects.order_by('-ano')
    return render(request, 'outorga/termos.html', {'termos': termos})


@login_required
@permission_required('outorga.rel_ger_lista_acordos', raise_exception=True)
@require_safe
def lista_acordos(request, pdf=False):
    """
     Relatório Gerencial - Relatório de Concessões por Acordo.

     Distribuição das concessões por acordo nos processos a partir de 2005.
     Exibe os acordos de todos os processos.

    """
    processos = []
    for t in Termo.objects.filter(ano__gte=2004).order_by('-ano'):
        processo = {'processo': t}
        acordos = []
        for a in Acordo.objects.filter(origemfapesp__item_outorga__natureza_gasto__termo=t).distinct():
            acordo = {'acordo': a}
            itens = []
            for it in Item.objects.filter(origemfapesp__acordo=a, natureza_gasto__termo=t)\
                    .order_by('natureza_gasto__modalidade__sigla', 'entidade'):
                itens.append({'modalidade': it.natureza_gasto.modalidade.sigla, 'entidade': it.entidade,
                              'descricao': it.descricao})
            acordo.update({'itens': itens})
            acordos.append(acordo)
        processo.update({'acordos': acordos})
        processos.append(processo)

    if pdf:
        return render_to_pdf_weasy('outorga/acordos.pdf', {'processos': processos}, request=request,
                                   filename="distribuicao_das_concessoes_por_acordo.pdf")
    else:
        return render(request, 'outorga/acordos.html', {'processos': processos})


@login_required
@permission_required('outorga.rel_adm_item_modalidade', raise_exception=True)
@require_safe
def item_modalidade(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Itens do orçamento por modalidade.

    """
    if request.GET.get('termo') and request.GET.get('termo') != '0' and \
       request.GET.get('modalidade') and request.GET.get('modalidade') != '0':

        termo_id = request.GET.get('termo')
        termo = get_object_or_404(Termo, id=termo_id)
        mod_id = request.GET.get('modalidade')
        mod = get_object_or_404(Modalidade, id=mod_id)
        itens = []
        it_objs = Item.objects.filter(natureza_gasto__termo=termo, natureza_gasto__modalidade=mod)
        entidade_id = request.GET.get('entidade')
        marca_id = request.GET.get('marca')
        procedencia_id = request.GET.get('procedencia')

        if entidade_id > '0':
            it_objs = it_objs.filter(origemfapesp__item_outorga__entidade__id=entidade_id)
        for item in it_objs:
            pags = []
            total = Decimal('0.0')

            pagamentos_qs = Pagamento.objects.filter(origem_fapesp__item_outorga=item)\
                .select_related('conta_corrente', 'protocolo', 'protocolo__descricao2',
                                'protocolo__descricao2__entidade', 'protocolo__tipo_documento')\
                .prefetch_related(Prefetch('auditoria_set', queryset=Auditoria.objects.select_related('tipo')))
            for p in pagamentos_qs:
                patrimonios = []
                pag = {'p': p, 'docs': p.auditoria_set.all(), 'patrimonios': ''}
                if marca_id > '0':
                    if p.patrimonio_set.filter(equipamento__entidade_fabricante_id=marca_id).exists():
                        patrimonios = p.patrimonio_set.filter(equipamento__entidade_fabricante_id=marca_id)
                        total += p.valor_fapesp
                elif procedencia_id > '0':
                    if p.patrimonio_set.filter(entidade_procedencia_id=procedencia_id).exists():
                        patrimonios = p.patrimonio_set.filter(entidade_procedencia_id=procedencia_id)
                        total += p.valor_fapesp
                else:
                    patrimonios = p.patrimonio_set.all()
                    total += p.valor_fapesp

                patrimonios = patrimonios.select_related('equipamento__entidade_fabricante')
                pag.update({'patrimonios': patrimonios})
                pags.append(pag)

            # se for especificado o filtro de marca ou procedencia, somente
            # adiciona o item de outorga se tiver patrimonios com estes dados.
            if (marca_id == '0' and procedencia_id == '0') or len(pags) > 0:
                itens.append({'item': item, 'total': total, 'pagtos': pags})

        if pdf:
            return render_to_pdf_weasy('outorga/por_item_modalidade.pdf',
                                       {'termo': termo, 'modalidade': mod, 'itens': itens},
                                       request=request, filename='%s-%s.pdf' % (termo, mod.sigla))
        else:
            return render(request, 'outorga/por_item_modalidade.html',
                          {'termo': termo, 'modalidade': mod, 'itens': itens, 'entidade': entidade_id,
                           'marca': marca_id, 'procedencia': procedencia_id})
    else:
        termos = Termo.objects.all()
        termo = request.GET.get('termo')
        modalidades = Modalidade.objects.all()
        modalidade = request.GET.get('modalidade')
        entidade = request.GET.get('entidade')

        entidadesProcedencia = Patrimonio.objects.all().values('entidade_procedencia')
        entidadesFabricante = Equipamento.objects.all().values('entidade_fabricante')
        entidadesItemOutorga = Item.objects.all().values('entidade')

        return render(request,
                      'outorga/termo_mod.html',
                      {'termos': termos, 'termo': termo, 'modalidades': modalidades, 'modalidade': modalidade,
                       'entidadesProcedencia': Entidade.objects.filter(id__in=entidadesProcedencia),
                       'entidadesFabricante': Entidade.objects.filter(id__in=entidadesFabricante),
                       'entidadesItemOutorga': Entidade.objects.filter(id__in=entidadesItemOutorga),
                       'entidade': entidade})


@login_required
@permission_required('outorga.rel_ger_acordo_progressivo', raise_exception=True)
@require_safe
def acordo_progressivo(request, pdf=False):
    """
     Relatório Gerencial - Relatório gerencial progressivo

    """
    acordos = []
    termos = []

    for a in Acordo.objects.all():
        acordo = {'nome': a.descricao}
        termos = []

        totalTermoRealizadoReal = Decimal('0.0')
        totalTermoConcedidoReal = Decimal('0.0')
        totalTermoSaldoReal = Decimal('0.0')
        totalTermoRealizadoDolar = Decimal('0.0')
        totalTermoConcedidoDolar = Decimal('0.0')
        totalTermoSaldoDolar = Decimal('0.0')

        for t in Termo.objects.filter(exibe_rel_ger_progressivo=True)\
                .order_by('inicio').only('ano', 'processo', 'digito'):
            concedido = a.itens_outorga.filter(natureza_gasto__termo=t)\
                .values('natureza_gasto__modalidade__moeda_nacional').annotate(soma=Sum('valor')).order_by()

            concedido_real = Decimal('0.0')
            concedido_dolar = Decimal('0.0')

            for c in concedido:
                if c['soma']:
                    if c['natureza_gasto__modalidade__moeda_nacional']:
                        concedido_real = c['soma']
                    else:
                        concedido_dolar = c['soma']

            realizado_real = Decimal('0.0')
            realizado_dolar = Decimal('0.0')

            realizado = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t,
                                                 origem_fapesp__acordo=a) \
                .values('origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional')\
                .annotate(soma=Sum('valor_fapesp')).order_by()
            for r in realizado:
                if r['soma']:
                    if r['origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional']:
                        realizado_real = r['soma']
                    else:
                        realizado_dolar = r['soma']

            saldo_real = concedido_real - realizado_real
            saldo_dolar = concedido_dolar - realizado_dolar

            if concedido_real and concedido_real != 0:
                porcentagem_real = str(round(Decimal('100.0') * realizado_real / concedido_real, 2)) + '%'
            else:
                porcentagem_real = "==="

            if concedido_dolar and concedido_dolar != 0:
                porcentagem_dolar = str(round(Decimal('100.0') * realizado_dolar / concedido_dolar, 2)) + '%'
            else:
                porcentagem_dolar = "==="

            tem_real = concedido_real or realizado_real
            tem_dolar = concedido_dolar or realizado_dolar
            itens = []

            if a.itens_outorga.filter(natureza_gasto__termo=t).exists():
                itensOutorga = a.itens_outorga.filter(natureza_gasto__termo=t)\
                    .select_related('natureza_gasto__modalidade', 'entidade').defer('justificativa', 'obs')
                for item in itensOutorga:
                    realiz = Pagamento.objects.filter(origem_fapesp__item_outorga=item, origem_fapesp__acordo=a)\
                        .aggregate(Sum('valor_fapesp'))
                    realiz = realiz['valor_fapesp__sum'] or Decimal('0.0')
                    concede = item.valor or Decimal('0.0')

                    excedido = realiz.compare(concede) == Decimal('1')
                    if concede and concede != 0:
                        porcentagem = str(round(Decimal('100.0') * realiz / concede, 2)) + '%'
                    else:
                        porcentagem = "==="

                    itens.append({'item': item, 'concedido': concede, 'realizado': realiz, 'saldo': concede-realiz,
                                  'porcentagem': porcentagem, 'excedido': excedido})

            if tem_real:
                valores_real = {'tem_real': 1, 'concedido_real': concedido_real, 'realizado_real': realizado_real,
                                'saldo_real': saldo_real, 'porcentagem_real': porcentagem_real}
                totalTermoRealizadoReal += realizado_real
                totalTermoConcedidoReal += concedido_real
                totalTermoSaldoReal += saldo_real
            else:
                valores_real = {'tem_real': 0}

            if tem_dolar:
                valores_dolar = {'tem_dolar': 1, 'concedido_dolar': concedido_dolar, 'realizado_dolar': realizado_dolar,
                                 'saldo_dolar': saldo_dolar, 'porcentagem_dolar': porcentagem_dolar}
                totalTermoRealizadoDolar += realizado_dolar
                totalTermoConcedidoDolar += concedido_dolar
                totalTermoSaldoDolar += saldo_dolar
            else:
                valores_dolar = {'tem_dolar': 0}

            valores = valores_real
            valores.update(valores_dolar)

            valores.update({'termo': t, 'itens': itens})
            termos.append(valores)

        tem_real = (totalTermoConcedidoReal and totalTermoConcedidoReal != 0.0) or \
                   (totalTermoRealizadoReal and totalTermoRealizadoReal != 0.0)
        tem_dolar = (totalTermoConcedidoDolar and totalTermoConcedidoDolar != 0.0) or \
                    (totalTermoRealizadoDolar and totalTermoRealizadoDolar != 0.0)
        acordo.update({'termos': termos, 'tem_real': tem_real, 'tem_dolar': tem_dolar,
                       'totalTermoRealizadoReal': totalTermoRealizadoReal,
                       'totalTermoConcedidoReal': totalTermoConcedidoReal,
                       'totalTermoSaldoReal': totalTermoSaldoReal,
                       'totalTermoRealizadoDolar': totalTermoRealizadoDolar,
                       'totalTermoConcedidoDolar': totalTermoConcedidoDolar,
                       'totalTermoSaldoDolar': totalTermoSaldoDolar})
        acordos.append(acordo)

        termos = Termo.objects.filter(exibe_rel_ger_progressivo=True).order_by('inicio')
    if pdf:
        return render_to_pdfxhtml2pdf('outorga/acordo_progressivo.pdf', {'acordos': acordos, 'termos': termos},
                                      request=request, filename='acordo_progressivo.pdf')
    else:
        return render(request, 'outorga/acordo_progressivo.html', {'acordos': acordos, 'termos': termos})


@login_required_or_403
@require_safe
def ajax_termo_datas(request):
    """
     Ajax utilizado para retornar os dados de mês/ano de início e término de um dado termo.
     Utilizado em diversos relatórios para fazer o filtro inicial antes de gerar os dados de relatório.

     Ex: Relatório Gerencial, Relatório de Acordos, etc.
    """
    # if not request.GET.has_key('termo'):
    #     raise Http404
    termo_id = request.GET.get('termo')
    parcial = request.GET.get('parcial')
    try:
        termo = Termo.objects.get(pk=termo_id)
    except (Termo.DoesNotExist, ValueError):
        termo = None
    pagamentos = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=termo)
    if parcial:
        pagamentos = pagamentos.filter(auditoria__parcial=parcial)

    datas = pagamentos.aggregate(min=Min('conta_corrente__data_oper'))
    datas.update(pagamentos.aggregate(max=Max('conta_corrente__data_oper')))

    meses = []
    if datas['min'] and datas['max']:
        for m in month_range(datas['min'], datas['max']):
            meses.append({'value': '%s-%s' % (m.year, m.month), 'display': '%02d/%s' % (m.month, m.year)})
    return HttpResponse(simplejson.dumps(meses), content_type='application/json')


@login_required_or_403
@require_safe
def ajax_termo_parciais(request):
    """
    Ajax utilizado para retornar as parciais abertas de um termo.
    """

    # if not request.GET.has_key('termo'):
    #     raise Http404

    termo_id = request.GET.get('termo')
    try:
        termo = Termo.objects.get(pk=termo_id)
    except (Termo.DoesNotExist, ValueError):
        termo = None

    parciais = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=termo)\
        .values_list('auditoria__parcial', flat=True).order_by('auditoria__parcial').distinct()
    return HttpResponse(simplejson.dumps(list(parciais)), content_type='application/json')
