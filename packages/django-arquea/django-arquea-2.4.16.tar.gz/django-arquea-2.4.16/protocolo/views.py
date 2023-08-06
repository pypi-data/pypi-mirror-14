# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.http import require_safe

from outorga.models import Termo
from protocolo.models import Protocolo, Cotacao, Descricao
from utils.functions import pega_lista, render_to_pdf_weasy


@permission_required('protocolo.change_cotacao')
def cotacoes(request, prot_id):
    """
    Verifica se o usuário tem autorização (pertence ao grupo 'tecnico') e retorna uma lista das cotações de um
    determinado protocolo.
    """
    u = request.user

    if not u.is_authenticated():
        return admin.site.login(request)

    p = get_object_or_404(Protocolo, pk=prot_id)
    if p.tipo_documento.nome != 'Pedido':
        raise Http404

    lista_cotacoes = Cotacao.objects.filter(protocolo=p)
    return render_to_response('protocolo/cotacoes.html',
                              {'lista_cotacoes': lista_cotacoes, 'pai': p, 'user': u,
                               'return_to': '/protocolo/%s/cotacoes' % prot_id},
                              context_instance=RequestContext(request))


@permission_required('protocolo.protocolo')
def escolhe_termo(request):
    return HttpResponse(pega_lista(request, Protocolo, 'termo'), content_type="application/json")


@permission_required('protocolo.protocolo')
def lista_protocolos(request, t_id):
    retorno = []
    for p in Protocolo.objects.filter(termo__id=t_id).order_by('identificacao__endereco__entidade', 'descricao'):
        mod = ''
        for fp in p.fontepagadora_set.all():
            mod += ' %s' % fp.origem_fapesp.item_outorga.natureza_gasto.modalidade
        retorno.append({'entidade': p.identificacao.entidade, 'descricao': p.descricao, 'valor': p.valor,
                        'tipo': p.tipo_documento, 'num': p.num_documento, 'modalidades': mod, 'termo': p.termo})

    return render_to_response('protocolo/listagem.html', {'protocolos': retorno})


# @permission_required('protocolo.change_protocolo')
# def protocolos(request, termo_id):
#     termo = get_object_or_404(Termo, pk=termo_id)
#
#     return render_to_pdf('protocolo/protocolos.pdf',
#           {'termo':termo, 'protocolos':termo.protocolo_set.order_by('descricao2')}, filename='protocolos.pdf')


@login_required
@permission_required('protocolo.rel_adm_descricao', raise_exception=True)
@require_safe
def protocolos_descricao(request, pdf=False):
    """
     Relatório Administrativo - Relatório de Protocolos por descrição.

    """
    if request.GET.get('termo'):
        termo_id = request.GET.get('termo')
        termo = get_object_or_404(Termo, pk=termo_id)
        retorno = []
        for d in Descricao.objects.all():
            desc = {'descricao': d.__unicode__(),
                    'protocolos': Protocolo.objects.filter(descricao2=d, termo=termo)
                    .order_by('-termo__ano', 'referente')}
            retorno.append(desc)

        if pdf:
            return render_to_pdf_weasy('protocolo/descricoes.pdf', {'protocolos': retorno}, request=request,
                                       filename='protocolos.pdf')
        else:
            return render_to_response('protocolo/descricoes.html', {'protocolos': retorno, 'termo': termo},
                                      context_instance=RequestContext(request))
    else:
        return render_to_response('financeiro/relatorios_termo.html',
                                  {'termos': Termo.objects.all(), 'view': 'protocolos_descricao'},
                                  context_instance=RequestContext(request))
