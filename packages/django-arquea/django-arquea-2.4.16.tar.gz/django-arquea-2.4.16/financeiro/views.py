# -* coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import permission_required, login_required
from utils.decorators import login_required_or_403
from django.db.models import Q, Max, Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe, require_POST

from decimal import Decimal
import json as simplejson
from datetime import datetime as dtime, date
import logging

from outorga.models import Item, Termo, OrigemFapesp, Natureza_gasto, Acordo
from protocolo.models import Protocolo
from configuracao.models import Cheque
from rede.models import PlanejaAquisicaoRecurso
from utils.functions import formata_moeda, render_to_pdf_weasy
from operator import itemgetter
from financeiro.models import ExtratoCC, Auditoria, Pagamento, ExtratoFinanceiro

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required_or_403
@require_safe
def ajax_termo_escolhido(request):
    termo_id = request.GET.get('termo_id')

    try:
        t = Termo.objects.get(id=termo_id)
    except (Termo.DoesNotExist, ValueError):
        t = None

    retorno = {}
    if t:
        protocolos = Protocolo.objects.filter(termo=t).order_by('tipo_documento', 'num_documento', 'data_vencimento')
        origens = OrigemFapesp.objects.filter(item_outorga__natureza_gasto__termo=t)\
            .order_by('acordo', 'item_outorga__natureza_gasto__modalidade', 'item_outorga')
        prot = []
        for p in protocolos:
            prot.append({'pk': p.id, 'valor': p.__unicode__()})
        orig = []
        for o in origens:
            orig.append({'pk': o.id,
                         'valor': u'%s - %s - %s' % (o.acordo, o.item_outorga.natureza_gasto.modalidade.sigla,
                                                     o.item_outorga)})
        retorno = {'protocolos': prot, 'origens': orig}
    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_numero_escolhido(request):
    termo_id = request.GET.get('termo_id')
    numero = request.GET.get('numero')

    try:
        t = Termo.objects.get(id=termo_id)
    except (Termo.DoesNotExist, ValueError):
        t = None

    if t:
        protocolos = Protocolo.objects.filter(termo=t, num_documento__icontains=numero)\
            .order_by('tipo_documento', 'num_documento', 'data_vencimento')
    else:
        protocolos = Protocolo.objects.filter(num_documento__icontains=numero)\
            .order_by('tipo_documento', 'num_documento', 'data_vencimento')
    prot = []
    for p in protocolos:
        prot.append({'pk': p.id, 'valor': p.__unicode__()})
    retorno = {'protocolos': prot}
    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_codigo_escolhido(request):
    codigo = request.GET.get('codigo')

    contas = ExtratoCC.objects.filter(cod_oper__icontains=codigo)
    ccs = []

    for c in contas:
        ccs.append({'pk': c.id, 'valor': c.__unicode__()})

    retorno = {'ccs': ccs}
    json = simplejson.dumps(retorno)

    return HttpResponse(json, content_type="application/json")


def _estrutura_pagamentos(pagamentos):
    """
    Função para montar a estrutura de dados utilizado nos relatórios de pagamentos
    """
    total = pagamentos.aggregate(Sum('valor_fapesp'))
    por_modalidade = pagamentos.values('origem_fapesp__item_outorga__natureza_gasto')\
        .order_by('origem_fapesp__item_outorga__natureza_gasto').annotate(Sum('valor_fapesp'))
    pm = []
    for p in por_modalidade:
        pg = {}
        try:
            ng = Natureza_gasto.objects.get(id=p['origem_fapesp__item_outorga__natureza_gasto'])
            pg['modalidade'] = ng.modalidade.nome
            pg['total'] = formata_moeda(p['valor_fapesp__sum'], ',')
            pm.append(pg)
        except Natureza_gasto.DoesNotExist:
            pass

    pg = []
    for p in pagamentos.filter(conta_corrente__isnull=False)\
            .order_by('origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla')\
            .select_related('conta_corrente', 'protocolo', 'protocolo__tipo_documento',
                            'origem_fapesp__item_outorga__natureza_gasto__modalidade'):
        pp = {}
        pp['data'] = p.conta_corrente.data_oper.strftime('%d/%m/%Y')
        pp['termo'] = p.protocolo.termo.__unicode__()
        pp['oper'] = p.conta_corrente.cod_oper

        if p.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
            pp['documento'] = '%s %s' % (p.protocolo.tipo_documento.nome, p.protocolo.num_documento)
        else:
            pp['documento'] = p.protocolo.num_documento
        pp['valor'] = formata_moeda(p.valor_fapesp, ',')

        try:
            pp['modalidade'] = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        except:
            pp['modalidade'] = ''

        pag = 0
        ane = 0
        out = 0
        for a in p.auditoria_set.all().select_related('tipo'):
            if u'Comprovante de pag' in a.tipo.nome:
                pag = a
            elif u'Anexo' in a.tipo.nome:
                ane = a
            else:
                out = a

        if pag:
            pp['parcial'] = pag.parcial
            pp['pagina'] = pag.pagina
        elif ane:
            pp['parcial'] = ane.parcial
            pp['pagina'] = ane.pagina
        elif out:
            pp['parcial'] = out.parcial
            pp['pagina'] = out.pagina
        else:
            pp['parcial'] = ''
            pp['pagina'] = ''

        pg.append(pp)

    return {'pg': sorted(pg, key=itemgetter('modalidade', 'pagina')), 'pm': pm, 'total': total}


@login_required_or_403
@require_safe
def ajax_parcial_pagina(request):
    orig = request.GET.get('orig_id')
    origem = get_object_or_404(OrigemFapesp, pk=orig)
    a = Auditoria.objects.filter(
        pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto)\
        .aggregate(Max('parcial'))
    parcial = a['parcial__max'] or 1
    a = Auditoria.objects.filter(
        pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto, parcial=parcial)\
        .aggregate(Max('pagina'))
    pagina = a['pagina__max'] or 0
    retorno = {'parcial': parcial, 'pagina': pagina+1}
    json = simplejson.dumps(retorno)

    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_nova_pagina(request):
    origem_id = request.GET.get('orig_id')
    parcial = request.GET.get('parcial')

    origem = get_object_or_404(OrigemFapesp, pk=origem_id)
    pagina = Auditoria.objects.filter(
        pagamento__origem_fapesp__item_outorga__natureza_gasto=origem.item_outorga.natureza_gasto, parcial=parcial)\
        .aggregate(Max('pagina'))
    pagina = 0 if pagina['pagina__max'] is None else pagina['pagina__max']

    retorno = pagina+1
    return HttpResponse(simplejson.dumps(retorno), content_type="application/json")


@login_required
@permission_required('financeiro.rel_adm_pagamentos_mes', raise_exception=True)
@require_safe
def pagamentos_mensais(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Pagamentos por mês.

    """
    if request.GET.get('ano'):
        ano = int(request.GET.get('ano'))
        mes = int(request.GET.get('mes'))
        pagamentos = Pagamento.objects.filter(conta_corrente__data_oper__year=ano)
        if mes != 0:
            pagamentos = pagamentos.filter(conta_corrente__data_oper__month=mes)
        dados = _estrutura_pagamentos(pagamentos)

        if pdf:
            return render_to_pdf_weasy(
                'financeiro/pagamentos.pdf',
                {'pagamentos': dados['pg'], 'ano': ano, 'mes': mes,
                 'total': formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm': dados['pm']},
                request=request, filename='pagamentos_mensais.pdf')
        else:
            return render_to_response(
                'financeiro/pagamentos.html',
                {'pagamentos': dados['pg'], 'ano': ano, 'mes': mes,
                 'total': formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm': dados['pm']},
                context_instance=RequestContext(request))
    else:
        meses = range(0, 13)
        anos = range(1990, dtime.now().year+1)
        anos.sort(reverse=True)
        return render_to_response('financeiro/pagamentos_mes.html',
                                  {'meses': meses, 'anos': anos, 'view': 'pagamentos_mensais'},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_pagamentos_parcial', raise_exception=True)
@require_safe
def pagamentos_parciais(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Pagamentos por parcial.

    """
    if request.GET.get('parcial') and request.GET.get('termo'):
        parcial = int(request.GET.get('parcial'))
        termo_id = int(request.GET.get('termo'))
        termo = Termo.objects.get(pk=termo_id)
        ids = [p.id for p in Pagamento.objects.filter(protocolo__termo=termo, auditoria__parcial=parcial).distinct()]
        pagamentos = Pagamento.objects.filter(id__in=ids)
        # for p in pagamentos:
        # if p.auditoria_set.filter(parcial=parcial).count() == 0:
        # pagamentos = pagamentos.exclude(id=p.id)
        dados = _estrutura_pagamentos(pagamentos)

        if pdf:
            return render_to_pdf_weasy(
                'financeiro/pagamentos_parciais.pdf',
                {'pagamentos': dados['pg'], 'parcial': parcial, 'termo': termo,
                 'total': formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm': dados['pm']}, request=request,
                filename='pagamentos_parciais.pdf')
        else:
            return render_to_response(
                'financeiro/pagamentos_parciais.html',
                {'pagamentos': dados['pg'], 'parcial': parcial, 'termo': termo,
                 'total': formata_moeda(dados['total']['valor_fapesp__sum'], ','), 'pm': dados['pm']},
                context_instance=RequestContext(request))
    else:
        parciais = range(1, 21)
        termos = Termo.objects.all()
        return render_to_response('financeiro/pagamentos_parcial.html', {'parciais': parciais, 'termos': termos},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_ger_gerencial', raise_exception=True)
@require_safe
def relatorio_gerencial(request, pdf=False):
    """
     Relatório Gerencial - Relatório financeiro com visão gerencial por processo.

     O relatório está separado em duas partes.
     - uma agregação de pagamentos por modalidade
     - detalhamento dos pagamentos por modalidade

    """
    if request.GET.get('termo'):
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        except Exception:
            print ''

        termo_id = int(request.GET.get('termo'))
        t = get_object_or_404(Termo, id=termo_id)

        try:
            rt = int(request.GET.get('rt'))
        except TypeError:
            rt = 0
        try:
            parcial = int(request.GET.get('parcial'))
        except TypeError:
            parcial = 0

        if 'tamanho' in request.GET:
            tamanho = request.GET.get('tamanho')
        else:
            tamanho = 'a3'

        retorno = []
        meses = []
        totalizador = []

        inicio = request.GET.get('inicio')
        termino = request.GET.get('termino')
        ainicio, minicio = (int(x) for x in inicio.split('-'))
        afinal, mfinal = (int(x) for x in termino.split('-'))

        ultimo = Pagamento.objects.filter(protocolo__termo=t).aggregate(ultimo=Max('conta_corrente__data_oper'))
        ultimo = ultimo['ultimo']

        pagamentos = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__termo=t)
        itens = Item.objects.filter(natureza_gasto__termo=t)
        if rt == 1:
            pagamentos = pagamentos.filter(origem_fapesp__item_outorga__rt=True)
            itens = itens.filter(rt=True)
        elif rt == 2:
            pagamentos = pagamentos.filter(origem_fapesp__item_outorga__rt=False)
            itens = itens.filter(rt=False)

        pag_total_mod = pagamentos
        if parcial > 0:
            pag_ids = [p.id for p in pagamentos.filter(auditoria__parcial=parcial).distinct()]
            pagamentos = pagamentos.filter(id__in=pag_ids)

        ano = ainicio
        mes = minicio
        while ano < afinal or (ano <= afinal and mes <= mfinal):
            dt = date(ano, mes, 1)
            # meses.append(dt.strftime('%B de %Y').decode('latin1'))
            meses.append(dt)
            if ano == t.termino.year and mes == t.termino.month:
                dt2 = date(ano+5, mes, 1)
                total_real = pagamentos\
                    .filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True,
                            conta_corrente__data_oper__range=(dt, dt2)).aggregate(Sum('valor_fapesp'))
                total_dolar = pagamentos\
                    .filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False,
                            protocolo__data_vencimento__range=(dt, dt2)).aggregate(Sum('valor_fapesp'))
            else:
                total_real = pagamentos\
                    .filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True,
                            conta_corrente__data_oper__year=ano, conta_corrente__data_oper__month=mes)\
                    .aggregate(Sum('valor_fapesp'))
                total_dolar = pagamentos\
                    .filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False,
                            protocolo__data_vencimento__year=ano, protocolo__data_vencimento__month=mes)\
                    .aggregate(Sum('valor_fapesp'))

            totalizador.append({'total_real': total_real['valor_fapesp__sum'] or Decimal('0.0'),
                                'total_dolar': total_dolar['valor_fapesp__sum'] or Decimal('0.0'),
                                'ord': dt.strftime('%Y%m')})

            mes += 1
            if mes > 12:
                mes = 1
                ano += 1

        cr = itens.filter(natureza_gasto__modalidade__moeda_nacional=True)\
            .exclude(natureza_gasto__modalidade__sigla='REI').aggregate(Sum('valor'))
        cr = cr['valor__sum'] or Decimal('0.0')

        cd = itens.filter(natureza_gasto__modalidade__moeda_nacional=False)\
            .exclude(natureza_gasto__modalidade__sigla='REI').aggregate(Sum('valor'))
        cd = cd['valor__sum'] or Decimal('0.0')

        dt1 = date(ainicio, minicio, 1)
        if mfinal == 12:
            dt2 = date(afinal+1, 1, 1)
        else:
            dt2 = date(afinal, mfinal+1, 1)
        grp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True,
                                conta_corrente__data_oper__range=(dt1, dt2)).aggregate(Sum('valor_fapesp'))
        grp = grp['valor_fapesp__sum'] or Decimal('0.0')

        gdp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False,
                                protocolo__data_vencimento__range=(dt1, dt2)).aggregate(Sum('valor_fapesp'))
        gdp = gdp['valor_fapesp__sum'] or Decimal('0.0')

        gr = pag_total_mod.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True)\
            .aggregate(Sum('valor_fapesp'))
        gr = gr['valor_fapesp__sum'] or Decimal('0.0')

        gd = pag_total_mod.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=False)\
            .aggregate(Sum('valor_fapesp'))
        gd = gd['valor_fapesp__sum'] or Decimal('0.0')

        gerais = {'concedido_real': cr, 'concedido_dolar': cd, 'gasto_real_parcial': grp, 'gasto_dolar_parcial': gdp,
                  'gasto_real': gr, 'gasto_dolar': gd, 'saldo_real': cr-gr, 'saldo_dolar': cd-gd}

        for ng in Natureza_gasto.objects.filter(termo=t).exclude(modalidade__sigla='REI')\
                .select_related('modalidade__moeda_nacional').order_by('modalidade__sigla'):

            ng_itens = ng.item_set.all()
            if rt == 1:
                ng_itens = ng_itens.filter(rt=True)
                b_rt = True
            elif rt == 2:
                ng_itens = ng_itens.filter(rt=False)
                b_rt = False
            else:
                b_rt = None

            ng_concedido = ng_itens.aggregate(Sum('valor'))['valor__sum'] or Decimal('0.0')
            ng_realizado = ng.total_realizado_rt(rt=b_rt)
            item = {'modalidade': ng.modalidade, 'concedido': ng_concedido, 'realizado': ng_realizado, 'meses': [],
                    'realizado_parcial': ng.total_realizado_parcial(minicio, ainicio, mfinal, afinal, rt=rt,
                                                                    parcial=parcial),
                    'saldo': ng_concedido-ng_realizado, 'itens': {}, 'obs': ng.obs}
            for it in ng_itens:
                item['itens'].update({it: []})

            ano, mes = (int(x) for x in inicio.split('-'))

            while ano < afinal or (ano <= afinal and mes <= mfinal):
                total = Decimal('0.0')

                if ng.modalidade.moeda_nacional:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto=ng,
                                                  conta_corrente__data_oper__year=ano,
                                                  conta_corrente__data_oper__month=mes).aggregate(Sum('valor_fapesp'))
                else:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto=ng,
                                                  protocolo__data_vencimento__year=ano,
                                                  protocolo__data_vencimento__month=mes).aggregate(Sum('valor_fapesp'))

                total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')

                try:
                    dt = date(ano, mes+1, 1)
                except:
                    dt = date(ano+1, 1, 1)
                dt2 = date(ano+5, 1, 1)
                if ano == t.termino.year and mes == t.termino.month:
                    if ng.modalidade.moeda_nacional:
                        sumFapesp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto=ng,
                                                      conta_corrente__data_oper__range=(dt, dt2))\
                            .aggregate(Sum('valor_fapesp'))
                    else:
                        sumFapesp = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto=ng,
                                                      protocolo__data_vencimento__range=(dt, dt2))\
                            .aggregate(Sum('valor_fapesp'))
                    total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')
                dt = date(ano, mes, 1)
                item['meses'].append({'ord': dt.strftime('%Y%m'), 'data': dt.strftime('%B de %Y'), 'valor': total})

                for it in item['itens'].keys():
                    after = False
                    if ano == t.termino.year and mes == t.termino.month:
                        after = True
                    total = it.calcula_realizado_mes(dt, after=after, pagamentos=pagamentos)
                    item['itens'][it].append({'ord': dt.strftime('%Y%m'), 'valor': total})
                mes += 1
                if mes > 12:
                    mes = 1
                    ano += 1

            for it in item['itens'].values():
                total_parcial = Decimal('0.0')
                for mes in it:
                    total_parcial += mes['valor']
                it[-1]['total_parcial'] = total_parcial

            retorno.append(item)

        if pdf:
            return render_to_pdf_weasy('financeiro/gerencial.pdf',
                                       {'atualizado': ultimo, 'termo': t, 'meses': meses, 'modalidades': retorno,
                                        'tamanho': tamanho, 'totais': totalizador, 'gerais': gerais},
                                       request=request, filename='relatorio_gerencial.pdf')
        else:
            return render_to_response('financeiro/gerencial.html',
                                      {'inicio': inicio, 'termino': termino, 'rt': rt, 'parcial': parcial,
                                       'atualizado': ultimo, 'termo': t, 'meses': meses, 'modalidades': retorno,
                                       'totais': totalizador, 'gerais': gerais},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'view': 'relatorio_gerencial'},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_ger_acordos', raise_exception=True)
@require_safe
def relatorio_acordos(request, pdf=False):
    """
     Relatório Gerencial - Relatório de Acordos.

     Deve receber um termo como parametro inicial, senão vai para uma tela para a seleção do termo.

    """
    if request.GET.get('termo'):
        termo_id = int(request.GET.get('termo'))
        t = get_object_or_404(Termo, id=termo_id)
        try:
            rt = int(request.GET.get('rt'))
        except TypeError:
            rt = 0
        try:
            parcial = int(request.GET.get('parcial'))
        except TypeError:
            parcial = 0
        retorno = []

        for a in Acordo.objects.all():
            ac = {'desc': a.__unicode__()}
            totalGeralReal = Decimal('0.0')
            totalGeralDolar = Decimal('0.0')
            itens = []

            if rt == 1:
                rts = [True]
            elif rt == 2:
                rts = [False]
            else:
                rts = [True, False]

            for o in a.origemfapesp_set.filter(item_outorga__natureza_gasto__termo=t, item_outorga__rt__in=rts)\
                    .select_related('item_outorga', 'item_outorga__entidade'):
                it = {'desc': '%s - %s' % (o.item_outorga.entidade, o.item_outorga.descricao), 'id': o.id}
                totalReal = Decimal('0.0')
                totalDolar = Decimal('0.0')
                pg = []
                for p in o.pagamento_set.order_by('conta_corrente__data_oper', 'id') \
                                        .prefetch_related('auditoria_set', 'auditoria_set__tipo') \
                                        .select_related('conta_corrente', 'protocolo', 'protocolo__descricao2',
                                                        'protocolo__tipo_documento', 'protocolo__descricao2__entidade',
                                                        'origem_fapesp__item_outorga__natureza_gasto__modalidade'):
                    if parcial > 0 and p.auditoria_set.filter(parcial=parcial).count() == 0:
                        continue
                    pags = {'p': p, 'docs': p.auditoria_set.all()}
                    pg.append(pags)

                    if p.origem_fapesp and \
                       p.origem_fapesp.item_outorga.natureza_gasto.modalidade.moeda_nacional is False:

                        totalDolar += p.valor_fapesp

                    else:
                        totalReal += p.valor_fapesp

                it.update({'totalReal': totalReal, 'totalDolar': totalDolar, 'pg': pg})

                totalGeralReal += totalReal
                totalGeralDolar += totalDolar
                itens.append(it)

            ac.update({'totalGeralReal': totalGeralReal, 'totalGeralDolar': totalGeralDolar, 'itens': itens})
            retorno.append(ac)

        if pdf:
            return render_to_pdf_weasy(template_src='financeiro/acordos_weasy.pdf',
                                       context_dict={'termo': t, 'acordos': retorno},
                                       request=request, filename='relatorio_de_acordos_da_outorga_%s.pdf' % t,)
        else:
            return render_to_response('financeiro/acordos.html',
                                      {'termo': t, 'acordos': retorno, 'rt': rt, 'parcial': parcial},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'view': 'relatorio_acordos'},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_extrato', raise_exception=True)
@require_safe
def extrato(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Panorama da conta corrente.

    """
    if request.GET.get('ano'):
        ano = int(request.GET.get('ano'))
        retorno = []
        mes = 0
        for e in ExtratoCC.objects.filter(data_oper__year=ano)\
                .select_related('extrato_financeiro', 'extrato_financeiro__termo').order_by('data_oper', 'id'):
            if mes == 0:
                mes = e.data_oper.month
                retorno.append({'saldo_mes_anterior': e.saldo_anterior, 'data': e.data_oper})
            if e.data_oper.month == mes:
                retorno.append(e)
            else:
                if retorno:
                    e1 = retorno[-1]
                    retorno.append({'saldo': e1.saldo, 'data': e1.data_oper})
                retorno.append(e)
                mes = e.data_oper.month
        if retorno:
            e1 = retorno[-1]
            retorno.append({'saldo': e1.saldo, 'data': e1.data_oper})

        if pdf:
            return render_to_pdf_weasy('financeiro/contacorrente.pdf',
                                       {'ano': ano, 'extrato': retorno}, request=request,
                                       filename='panorama_cc_%s.pdf' % ano)
        else:
            return render_to_response('financeiro/contacorrente.html',
                                      {'ano': ano, 'extrato': retorno}, context_instance=RequestContext(request))
    else:
        anos = range(1990, dtime.now().year+1)
        anos.sort(reverse=True)
        return render_to_response('financeiro/sel_contacorrente.html',
                                  {'anos': anos}, context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_extrato_mes', raise_exception=True)
@require_safe
def extrato_mes(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Extrato da conta corrente por mês.

    """
    if request.GET.get('ano'):
        ano = int(request.GET.get('ano'))
        mes = int(request.GET.get('mes'))
        retorno = []
        sa = True
        for e in ExtratoCC.objects.filter(data_oper__year=ano, data_oper__month=mes).order_by('data_oper', 'id'):
            if sa:
                sa = False
                retorno.append(e.saldo_anterior)
            retorno.append(e)
        if retorno:
            e1 = retorno[-1]
            retorno.append(e1.saldo)

        if pdf:
            return render_to_pdf_weasy('financeiro/contacorrente_mes.pdf',
                                       {'ano': ano, 'mes': mes, 'extrato': retorno},
                                       request=request, filename='extrato_cc_%s/%s.pdf' % (mes, ano))
        else:
            return render_to_response('financeiro/contacorrente_mes.html',
                                      {'ano': ano, 'mes': mes, 'extrato': retorno},
                                      context_instance=RequestContext(request))
    else:
        meses = range(1, 13)
        anos = range(1990, dtime.now().year+1)
        anos.sort(reverse=True)
        return render_to_response('financeiro/sel_contacorrente_mes.html',
                                  {'anos': anos, 'meses': meses}, context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_extrato_financeiro', raise_exception=True)
@require_safe
def extrato_financeiro(request, ano=dtime.now().year, pdf=False):
    """
     Relatório Administrativo - Relatório Extrato do financeiro por mês.

    """
    if request.GET.get('termo'):
        codigo = 'MP'

        termo_id = int(request.GET.get('termo'))
        termo = get_object_or_404(Termo, id=termo_id)
        mes = int(request.GET.get('mes'))
        if mes:
            efs = ExtratoFinanceiro.objects.filter(termo=termo, data_libera__month=mes, cod__endswith=codigo)
        else:
            efs = ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo)
        extrato = []
        for ef in efs.order_by('data_libera'):
            ex = {'data': ef.data_libera, 'cod': ef.cod, 'historico': ef.historico, 'valor': ef.valor,
                  'comprovante': ef.comprovante, 'cheques': []}
            total = Decimal('0.0')
            for c in ef.extratocc_set.all():
                valor = c.pagamento_set.aggregate(Sum('valor_fapesp'))
                total += valor['valor_fapesp__sum'] or Decimal('0.0')
                parciais = []
                for p in c.pagamento_set.all():
                    for a in p.auditoria_set.all():
                        if a.parcial not in parciais:
                            parciais.append(a.parcial)

                ch = {'id': c.id, 'valor': c.valor, 'cod': c.cod_oper,
                      'parciais': ', '.join([str(p) for p in parciais])}
                ex['cheques'].append(ch)
            ex['diferenca'] = ef.valor+total
            extrato.append(ex)

        if pdf:
            return render_to_pdf_weasy('financeiro/financeiro.pdf',
                                       {'ano': ano, 'extrato': extrato}, request=request,
                                       filename='financeiro_%s/%s.pdf' % (mes, ano))
        else:
            return render_to_response('financeiro/financeiro.html',
                                      {'termo': termo, 'mes': mes, 'ano': ano, 'extrato': extrato},
                                      context_instance=RequestContext(request))
    else:
        meses = range(0, 13)
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'meses': meses, 'view': 'extrato_financeiro',
                                   'rt': False}, context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_extrato_tarifas', raise_exception=True)
@require_safe
def extrato_tarifas(request):
    """
     Relatório Administrativo - Relatório de Extrato de tarifas por mês.

    """
    if request.GET.get('ano'):
        ano = int(request.GET.get('ano'))
        mes = int(request.GET.get('mes'))
        if mes == 0:
            tars = ExtratoCC.objects.filter(Q(data_oper__year=ano), Q(historico__icontains='tar') |
                                            Q(historico__icontains='crédito aut') |
                                            Q(historico__icontains='juro')).order_by('data_oper')
        else:
            tars = ExtratoCC.objects.filter(Q(data_oper__month=mes), Q(data_oper__year=ano),
                                            Q(historico__icontains='tar') | Q(historico__icontains='créditto aut') |
                                            Q(historico__icontains='juro')).order_by('data_oper')
        total = tars.aggregate(Sum('valor'))

        context = {'total': total['valor__sum'], 'ano': ano, 'tarifas': tars}
        if mes > 0:
            context.update({'mes': mes})

        return render_to_response('financeiro/tarifas.html', context, context_instance=RequestContext(request))
    else:
        meses = range(0, 13)
        anos = range(1990, dtime.now().year+1)
        anos.sort(reverse=True)
        return render_to_response('financeiro/pagamentos_mes.html',
                                  {'anos': anos, 'meses': meses, 'view': 'extrato_tarifas'},
                                  context_instance=RequestContext(request))


@login_required
def cheque(request, cc=1):
    extrato = get_object_or_404(ExtratoCC, id=cc)

    if not extrato.extrato_financeiro:
        termo = None
    else:
        termo = extrato.extrato_financeiro.termo

    parciais = extrato.pagamento_set.all()
    pps = []
    if parciais.count() > 0:
        for p in parciais:
            pp = p.__unicode__()
            name = pp.split(' - ')[-1]
            name = name.split('ID:')[0]
            pps.append(name)
    else:
        name = ''
        pps.append(name)

    assinatura = ""
    assinaturas = Cheque.objects.all()
    for a in assinaturas:
        assinatura = a.nome_assinatura

    return render_to_pdf_weasy('financeiro/cheque.pdf',
                               {'cc': extrato, 'termo': termo, 'pps': pps, 'assinatura': assinatura},
                               request=request, filename='capa_%s.pdf' % extrato.cod_oper)


@login_required
@permission_required('financeiro.rel_adm_extrato_financeiro_parciais', raise_exception=True)
@require_safe
def financeiro_parciais(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Extrato do financeiro por parcial.

    """
    if request.GET.get('termo'):
        termo_id = int(request.GET.get('termo'))

        codigo = 'MP'

        termo = get_object_or_404(Termo, id=termo_id)
        retorno = []
        parciais = ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo).distinct('parcial')\
            .values_list('parcial', flat=True).order_by('parcial')
        totais = {}

        for parcial in parciais:
            extrato = []

            liberado = Decimal('0.0')
            devolvido = Decimal('0.0')
            estornado = Decimal('0.0')
            disponibilizado = Decimal('0.0')
            pagamentos = Decimal('0.0')

            concedido = Decimal('0.0')
            suplementado = Decimal('0.0')
            anulado = Decimal('0.0')
            cancelado = Decimal('0.0')

            liberacoes = ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo, parcial=parcial)\
                .values('cod').annotate(Sum('valor')).order_by()

            for t in liberacoes:
                if t['cod'] == 'PGMP' or t['cod'] == 'PGRP':
                    liberado = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'DVMP' or t['cod'] == 'DVRP':
                    devolvido = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'COMP' or t['cod'] == 'CORP':
                    concedido = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'SUMP' or t['cod'] == 'SURP':
                    suplementado = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'ANMP' or t['cod'] == 'ANRP':
                    anulado = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'ESMP' or t['cod'] == 'ESRP':
                    estornado = t['valor__sum'] or Decimal('0.0')
                elif t['cod'] == 'CAMP' or t['cod'] == 'CARP':
                    cancelado = t['valor__sum'] or Decimal('0.0')

            disponibilizado = - liberado.copy_abs() + devolvido.copy_abs() + estornado.copy_abs()

            concessoes = concedido.copy_abs() + suplementado.copy_abs() - anulado.copy_abs() - cancelado.copy_abs()

            somatoria_diferenca = Decimal('0.0')
            anterior = date(1971, 1, 1)
            tdia = Decimal('0.0')
            exi = {}
            for ef in ExtratoFinanceiro.objects.filter(termo=termo, cod__endswith=codigo, parcial=parcial)\
                    .prefetch_related('extratocc_set').order_by('data_libera', '-historico'):
                if ef.data_libera > anterior:
                    ex = {'data': ef.data_libera}
                    anterior = ef.data_libera
                    if exi:
                        exi.update({'valor_data': tdia})
                    exi = ex
                    tdia = ef.valor
                else:
                    ex = {'data': ''}
                    if ef.cod == 'PGMP':
                        tdia += ef.valor
                    else:
                        ex = {'data': ef.data_libera}
                ex.update({'cod': ef.cod, 'historico': ef.historico, 'valor': ef.valor, 'comprovante': ef.comprovante,
                           'cheques': []})
                total = Decimal('0.0')
                tcheques = Decimal('0.0')
                for c in ef.extratocc_set.all():
                    v_fapesp = Decimal('0.0')
                    # total += c.valor
                    tcheques += c.valor
                    mods = {}
                    for p in c.pagamento_set.all().prefetch_related('auditoria_set') \
                        .select_related('origem_fapesp', 'origem_fapesp__item_outorga__natureza_gasto__modalidade') \
                        .only('origem_fapesp_id', 'valor_fapesp',
                              'origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla', 'conta_corrente'):

                        if not p.origem_fapesp_id:
                            continue

                        v_fapesp += p.valor_fapesp
                        modalidade = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
                        if modalidade not in mods.keys():
                            mods[modalidade] = {}
                        for a in p.auditoria_set.all():
                            if a.parcial not in mods[modalidade].keys():
                                mods[modalidade][a.parcial] = []
                            if a.pagina not in mods[modalidade][a.parcial]:
                                mods[modalidade][a.parcial].append(a.pagina)
                    total -= v_fapesp
                    parc = ''
                    for modalidade in mods.keys():
                        parc += '%s [parcial ' % modalidade
                        pags = []
                        if len(mods[modalidade].keys()) > 0:
                            for p in mods[modalidade].keys():
                                pags = mods[modalidade][p]
                                pags.sort()
                        parc += '%s (%s)' % (p, ','.join([str(k) for k in pags]))
                        parc += ']       '

                    ch = {'id': c.id, 'valor': c.valor, 'cod': c.cod_oper, 'parciais': parc, 'obs': c.obs}

                    if v_fapesp != c.valor:
                        ch.update({'v_fapesp': v_fapesp})
                    ex['cheques'].append(ch)
                if ef.cod == 'PGMP' or ef.cod == 'DVMP' or ef.cod == 'ESMP' or \
                   ef.cod == 'PGRP' or ef.cod == 'DVRP' or ef.cod == 'ESRP':
                    ex['diferenca'] = ef.valor-total
                    somatoria_diferenca += ex['diferenca']
                if total > ef.valor:
                    ex['cor'] = 'red'
                else:
                    ex['cor'] = 'blue'
                if tcheques != ef.valor and ef.cod == 'PGMP':
                    ex['patrocinio'] = tcheques - ef.valor

                pagamentos += total
                extrato.append(ex)
            if exi:
                exi.update({'valor_data': tdia})

            # OBS: os valores de 'liberado' e 'pagamentos' estão com o sinal negativo
            total_processo = - liberado.copy_abs() + devolvido.copy_abs() + estornado.copy_abs() + pagamentos.copy_abs()

            retorno.append({'parcial': str(parcial), 'extrato': extrato, 'liberado': liberado, 'devolvido': devolvido,
                            'disponibilizado': disponibilizado, 'pagamentos': -pagamentos,
                            'somatoria_diferenca': somatoria_diferenca,  'concedido': concedido,
                            'suplementado': suplementado, 'anulado': anulado, 'cancelado': cancelado,
                            'concessoes': concessoes, 'estornado': estornado, 'total_processo': total_processo})

            total_liberado = 0
            total_devolvido = 0
            total_estornado = 0
            total_disponibilizado = 0
            total_pagamentos = 0
            total_somatoria_diferenca = 0

            total_concedido = 0
            total_suplementado = 0
            total_anulado = 0
            total_cancelado = 0
            total_concessoes = 0

            for r in retorno:
                total_liberado += r['liberado']
                total_devolvido += r['devolvido']
                total_estornado += r['estornado']
                total_disponibilizado += r['disponibilizado']
                total_pagamentos += r['pagamentos']

                total_somatoria_diferenca += r['somatoria_diferenca']

                total_concedido += r['concedido']
                total_suplementado += r['suplementado']
                total_anulado += r['anulado']
                total_cancelado += r['cancelado']
                total_concessoes += r['concessoes']
            total_processo = - total_liberado.copy_abs() \
                + total_devolvido.copy_abs() \
                + total_estornado.copy_abs() \
                + total_pagamentos.copy_abs()

            totais = {'total_liberado': total_liberado, 'total_devolvido': total_devolvido,
                      'total_estornado': total_estornado, 'total_pagamentos': total_pagamentos,
                      'total_disponibilizado': total_disponibilizado,
                      'total_somatoria_diferenca': total_somatoria_diferenca, 'total_concedido': total_concedido,
                      'total_suplementado': total_suplementado, 'total_anulado': total_anulado,
                      'total_cancelado': total_cancelado, 'total_concessoes': total_concessoes,
                      'total_processo': total_processo}

        if pdf:
            return render_to_pdf_weasy('financeiro/financeiro_parcial.pdf',
                                       {'size': pdf, 'termo': termo, 'parciais': retorno, 'totais': totais},
                                       request=request,
                                       filename='financeiro_parciais_%s_%s.pdf' % (termo.ano, termo.processo))
        else:
            return render_to_response('financeiro/financeiro_parcial.html',
                                      {'termo': termo, 'parciais': retorno, 'totais': totais},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'rt': False, 'view': 'financeiro_parciais'},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('financeiro.rel_adm_caixa', raise_exception=True)
@require_safe
def caixa(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Diferenças de Caixa.
    """
    return _parciais_or_caixa(request, True, pdf)


@login_required
@permission_required('financeiro.rel_adm_parciais', raise_exception=True)
@require_safe
def parciais(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Diferenças Totais.
    """
    return _parciais_or_caixa(request, False, pdf)


def _parciais_or_caixa(request, caixa=False, pdf=False):
    """
     Utilizado nos requests do relatório de caixa e do relatório de parciais.
     Foi feito isso para fazer o tratamento separado das permissões de acesso aos relatórios.
    """
    if request.GET.get('termo'):
        termo_id = int(request.GET.get('termo'))
        termo = get_object_or_404(Termo, id=termo_id)
        retorno = []

        for parcial in Auditoria.objects.filter(pagamento__protocolo__termo=termo)\
                .values_list('parcial', flat=True).distinct():
            parcs = {'parcial': parcial}
            # ads = Auditoria.objects.filter(parcial=parcial, pagamento__protocolo__termo=termo)

#                 pgs = []
#                 for a in ads:
#                     if caixa:
#                         if a.pagamento.conta_corrente and a.pagamento.conta_corrente.despesa_caixa and a.pagamento not in pgs:
#                             pgs.append(a.pagamento)
#                         else:
#                             if a.pagamento not in pgs:
#                                 pgs.append(a.pagamento)

            ch = ExtratoCC.objects.filter(extrato_financeiro__parcial=parcial, extrato_financeiro__termo=termo)
            if caixa:
                ch = ch.filter(despesa_caixa=True)

    # for p in pgs:
    #    if p.conta_corrente and p.conta_corrente not in ch:
#        ch.append(p.conta_corrente)

            ret = []
            total_diff = Decimal('0.0')
            for ecc in ch:
                pagos = ecc.pagamento_set.aggregate(Sum('valor_fapesp'))
                pago = pagos['valor_fapesp__sum'] or Decimal('0.0')
                pagos = ecc.pagamento_set.aggregate(Sum('valor_patrocinio'))
                # pago = pago + (pagos['valor_patrocinio__sum'] or Decimal('0.0'))
                diff = ecc.valor+pago
                total_diff += diff
                este = {'cheque': ecc, 'diff': -diff}
                pgtos = []
                for p in ecc.pagamento_set.all()\
                        .select_related('protocolo', 'origem_fapesp__item_outorga__natureza_gasto',
                                        'origem_fapesp__item_outorga__natureza_gasto__modalidade',
                                        'origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla'):
                    ok = True
                    for a in p.auditoria_set.distinct('parcial'):
                        if a.parcial != parcial:
                            ok = False
                            break
                    pgtos.append({'pg': p, 'naparcial': ok})
                este.update({'pgtos': pgtos})

                ret.append(este)

            parcs.update({'dados': ret, 'diff': -total_diff})
            retorno.append(parcs)

        return render_to_response('financeiro/parciais.html',
                                  {'caixa': caixa, 'parciais': retorno, 'termo': termo},
                                  context_instance=RequestContext(request))
    else:
        view = 'parciais'
        if caixa:
            view = 'caixa'
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'caixa': caixa, 'view': view},
                                  context_instance=RequestContext(request))


@login_required_or_403
@require_safe
def ajax_escolhe_extrato(request):
    termo_id = request.GET.get('termo')
    try:
        termo = Termo.objects.get(id=termo_id)
    except (Termo.DoesNotExist, ValueError):
        termo = None

    ef = ExtratoFinanceiro.objects.filter(termo=termo)
    extratos = []
    for e in ef:
        extratos.append({'pk': e.id, 'valor': e.__unicode__()})

    json = simplejson.dumps(extratos)
    return HttpResponse(json, content_type="application/json")


@login_required
@permission_required('financeiro.rel_adm_prestacao', raise_exception=True)
@require_safe
def presta_contas(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Prestação de contas.

    """
    if request.GET.get('termo'):
        termo_id = request.GET.get('termo')
        termo = get_object_or_404(Termo, id=termo_id)
        m = []
        for ng in Natureza_gasto.objects.filter(termo=termo).select_related('modalidade'):
            mod = {'modalidade': ng.modalidade.nome}
            parcs = []
            for p in Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=ng)\
                    .values_list('parcial', flat=True).distinct():
                pgtos = []
                pag = None
                for a in Auditoria.objects.filter(pagamento__origem_fapesp__item_outorga__natureza_gasto=ng, parcial=p)\
                        .order_by('pagina')\
                        .select_related('pagamento', 'pagamento__protocolo', 'pagamento__origem_fapesp__item_outorga',
                                        'pagamento__conta_corrente', 'pagamento__conta_corrente__extrato_financeiro',
                                        'pagamento__conta_corrente__extrato_financeiro__comprovante'):
                    auditorias = []
                    if a.pagamento != pag:
                        pgtos.append({'pg': a.pagamento, 'pagina': a.pagina, 'auditorias': auditorias})
                        pag = a.pagamento

                        for auditoria in a.pagamento.auditoria_set.all().select_related('tipo', 'estado'):
                            auditorias.append({'auditoria': auditoria})

                parcs.append({'num': p, 'pgtos': pgtos})
            mod.update({'parcial': parcs})
            m.append(mod)
        if pdf:
            return render_to_pdf_weasy('financeiro/presta_contas.pdf',
                                       {'modalidades': m, 'termo': termo}, request=request,
                                       filename='presta_contas_%s.pdf' % termo.__unicode__())
        else:
            return render_to_response('financeiro/presta_contas.html',
                                      {'modalidades': m, 'termo': termo},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'view': 'presta_contas'},
                                  context_instance=RequestContext(request))


@login_required
def tipos_documentos(context):

    protocolos = []
    for p in Protocolo.objects.filter(pagamento__isnull=False):
        ads = Auditoria.objects.filter(pagamento__protocolo=p)
        audits = []
        for a in ads:
            aa = {'tipo': a.tipo.nome}
            if a.arquivo:
                aa.update({'arquivo': a.arquivo.url})
            if a.pagamento.conta_corrente:
                aa.update({'pagamento': a.pagamento.conta_corrente.cod_oper})
            audits.append(aa)
        protocolos.append({'tipo': p.tipo_documento.nome, 'auditorias': audits})

    return render_to_response('financeiro/tipos.html', {'protocolos': protocolos})


@login_required_or_403
@require_safe
def ajax_get_recursos_vigentes(request):
    """
    AJAX para buscar os dados dos recursos.
    Recebe parametro para filtra por estado (ex: Vigente) ou buscar todos os registros
    """
    estado = request.GET.get('estado')
    if estado and estado != '':
        recursos = PlanejaAquisicaoRecurso.objects.filter(os__estado__nome=estado)\
            .select_related('os', 'os__tipo', 'projeto', 'tipo', )
    else:
        recursos = PlanejaAquisicaoRecurso.objects.all().select_related('os', 'os__tipo', 'projeto', 'tipo', )

    retorno = [{'pk': r.pk, 'valor': r.__unicode__()} for r in recursos]

    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_POST
def ajax_insere_extrato_cc(request):
    """
    AJAX para inserir no extrato de conta corrente a liberação do financeiro para o Cartão Pesquisa BB
    Recebe o id do extrato do financeiro
    """
    extrato_id = request.POST.get('id')
    retorno = 1

    ef = get_object_or_404(ExtratoFinanceiro, pk=extrato_id)
    if ef.extratocc_set.count() > 0:
        retorno = 2
    else:
        ecc1 = ExtratoCC.objects.create(data_oper=ef.data_libera, historico=u'Liberação de verba MP', valor=-ef.valor,
                                        cod_oper=ef.data_libera.strftime('%Y%m%d9'))

        if ef.taxas > 0:
            ecc2 = ExtratoCC.objects.create(data_oper=ef.data_libera, historico=u'Liberação de verba TX',
                                            valor=ef.taxas*Decimal('1.00'), cod_oper=ef.data_libera.strftime('%Y%m%d9'))
            ecc3 = ExtratoCC.objects.create(data_oper=ef.data_libera, historico=u'Pagamento TX',
                                            valor=ef.taxas*Decimal('-1.00'),
                                            cod_oper=ef.data_libera.strftime('%Y%m%d9'))
            if not ecc2 or not ecc3:
                retorno = 0

        if not ecc1:
            retorno = 0

    return HttpResponse(simplejson.dumps(retorno), content_type='application/json')


@login_required
@require_safe
def gerencial_anual(request, pdf=0):

    if 'ano' not in request.GET:
        from django.utils import timezone
        return TemplateResponse(request, 'financeiro/sel_ano.html', {'anos': range(timezone.now().year, 1994, -1)})

    ano = request.GET.get('ano')

    totais = Pagamento.objects.filter(conta_corrente__data_oper__year=ano)\
        .values_list('origem_fapesp__item_outorga__natureza_gasto__modalidade__nome',
                     'origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional')\
        .order_by('origem_fapesp__item_outorga__natureza_gasto__modalidade__nome').annotate(total=Sum('valor_fapesp'))
    por_termo = Pagamento.objects.filter(conta_corrente__data_oper__year=ano)\
        .values_list('origem_fapesp__item_outorga__natureza_gasto__termo',
                     'origem_fapesp__item_outorga__natureza_gasto__modalidade__nome')\
        .order_by('origem_fapesp__item_outorga__natureza_gasto__modalidade__nome',
                  'origem_fapesp__item_outorga__natureza_gasto__termo').annotate(total=Sum('valor_fapesp'))

    termos_ano = Pagamento.objects.filter(conta_corrente__data_oper__year=ano)\
        .values_list('origem_fapesp__item_outorga__natureza_gasto__termo', flat=True)\
        .order_by('origem_fapesp__item_outorga__natureza_gasto__termo').distinct()

    termos_ano = [Termo.objects.get(id=t) for t in termos_ano if t]

    modalidades = []
    i = 0
    for t in totais:
        if not t[0]:
            continue
        modalidade = {'modalidade': t[0], 'total': t[2], 'moeda_nacional': t[1]}
        termos = []
        j = 0
        while j < len(termos_ano):
            if i >= len(por_termo) or termos_ano[j].id != por_termo[i][0]:
                termos.append({'termo': termos_ano[j], 'valor': Decimal('0.0')})
            else:
                termos.append({'termo': termos_ano[j], 'valor': por_termo[i][2]})
                i += 1
            j += 1
        modalidade.update({'termos': termos})

        totais_itens = Pagamento.objects.filter(conta_corrente__data_oper__year=ano,
                                                origem_fapesp__item_outorga__natureza_gasto__modalidade__nome=t[0],
                                                origem_fapesp__item_outorga__natureza_gasto__termo__in=termos_ano)\
            .values_list('origem_fapesp__item_outorga__descricao').order_by('origem_fapesp__item_outorga__descricao')\
            .annotate(total=Sum('valor_fapesp'))
        itens = []
        for item in totais_itens:
            it = {'descricao': item[0], 'total': item[1]}
            itens_termos = []
            for termo in termos_ano:
                item_termo = totais_itens.filter(origem_fapesp__item_outorga__natureza_gasto__termo=termo,
                                                 origem_fapesp__item_outorga__descricao=item[0])
                if item_termo.count() > 0:
                    itens_termos.append(item_termo[0][1])
                else:
                    itens_termos.append(Decimal('0.0'))
            it.update({'termos': itens_termos})
            itens.append(it)

        modalidade.update({'itens': itens})
        modalidades.append(modalidade)

    if pdf == '1':
        return render_to_pdf_weasy('financeiro/gerencial_anual.pdf',
                                   {'modalidades': modalidades, 'ano': ano, 'termos': termos_ano},
                                   request, filename='gerencial_anual.pdf')
    else:
        return TemplateResponse(request, 'financeiro/gerencial_anual.html',
                                {'modalidades': modalidades, 'ano': ano, 'termos': termos_ano})
