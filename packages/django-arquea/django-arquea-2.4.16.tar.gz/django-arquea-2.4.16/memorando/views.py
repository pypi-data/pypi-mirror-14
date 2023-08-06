# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import permission_required, login_required
from utils.decorators import login_required_or_403
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_safe

import os
import json as simplejson
from django.conf import settings

from financeiro.models import Pagamento
from outorga.models import Termo
from utils.functions import render_to_pdf_weasy, render_to_pdfxhtml2pdf
from memorando.models import MemorandoSimples, MemorandoFAPESP, Pergunta,\
    MemorandoResposta


@login_required
def simples(request, mem):
    m = get_object_or_404(MemorandoSimples, pk=mem)

    # return render_to_response('memorando/simples.pdf', {'m':m, 't':Termo.termo_ativo()})
    return render_to_pdf_weasy('memorando/simples.pdf', {'m': m, 't': Termo.termo_ativo()}, request=request,
                               filename='memorando_%s.pdf' % m.__unicode__())


@login_required_or_403
@require_safe
def ajax_escolhe_pagamentos(request):
    termo_id = request.GET.get('termo')
    try:
        termo = Termo.objects.get(pk=termo_id)
    except (Termo.DoesNotExist, ValueError):
        termo = None

    pagamentos = []

    for p in Pagamento.objects.filter(protocolo__termo=termo).order_by('protocolo__num_documento'):
        a = p.auditoria_set.all()
        if a.count():
            a = a[0]
            valor = u'%s - %s, parcial %s, página %s' % (p.protocolo.num_documento, p.valor_fapesp, a.parcial, a.pagina)
        else:
            valor = u'%s %s' % (p.protocolo.num_documento, p.valor_fapesp)

            pagamentos.append({'pk': p.id, 'valor': valor})

    json = simplejson.dumps(pagamentos)
    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_escolhe_pergunta(request):
    pergunta_id = request.GET.get('pergunta')
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    json = simplejson.dumps(pergunta.questao)
    return HttpResponse(json, content_type="application/json")


@login_required_or_403
@require_safe
def ajax_filtra_perguntas(request):
    memorando_id = request.GET.get('memorando')
    memorando = get_object_or_404(MemorandoFAPESP, pk=memorando_id)

    perguntas = [{'pk': '', 'valor': '-----------'}]
    for p in memorando.pergunta_set.all():
        perguntas.append({'pk': p.id, 'valor': p.__unicode__()})

    return HttpResponse(simplejson.dumps(perguntas), content_type="application/json")


@login_required
def fapesp(request, mem):
    m = get_object_or_404(MemorandoResposta, pk=mem)
    corpos = []
    anexos = []
    incluidos = {}

    if m.anexa_relatorio:
        from patrimonio.views import por_termo
        from django.contrib.auth.models import User
        from django.http import HttpRequest

        new_request = HttpRequest()
        new_request.user = User.objects.get(email='antonio@ansp.br')
        new_request.GET = {'termo': m.memorando.termo.id, 'agilis': 1, 'modalidade': 1}
        new_request.META = {}
        response = por_termo(new_request, 1)
        anexos.append((response.content, u'Lista patrimonial do processo %s' % m.memorando.termo, 2))

    for c in m.corpo_set.all():
        if c.anexo:
            anexos.append((os.path.join(settings.MEDIA_ROOT, c.anexo.name), u'Pergunta %s' % c.pergunta.numero, 1))
        if c.pergunta.numero in incluidos.keys():
            corpos[incluidos[c.pergunta.numero]]['respostas'].append(c.resposta)
        else:
            incluidos.update({c.pergunta.numero: len(corpos)})
            corpos.append({'numero': c.pergunta.numero, 'pergunta': c.pergunta.questao, 'respostas': [c.resposta]})

    return render_to_pdfxhtml2pdf('memorando/fapesp.pdf', {'m': m, 'corpos': corpos}, request=request,
                                  filename='memorando_%s.pdf' % m.data.strftime('%d_%m_%Y'), attachments=anexos)


@login_required
@permission_required('memorando.rel_adm_memorando', raise_exception=True)
@require_safe
def relatorio(request):
    """
     Relatório Administrativo - Relatório de Memorandos FAPESP.

    """
    mem = request.GET.get('mem')
    if not mem:
        return render_to_response('memorando/escolhe_memorando.html', {'memorandos': MemorandoFAPESP.objects.all()},
                                  context_instance=RequestContext(request))
    m = get_object_or_404(MemorandoFAPESP, pk=mem)
    return render_to_response('memorando/relatorio.html', {'memorando': m}, context_instance=RequestContext(request))
