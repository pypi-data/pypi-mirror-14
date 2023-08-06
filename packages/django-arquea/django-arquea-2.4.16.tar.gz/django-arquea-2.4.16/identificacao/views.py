# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe

import json as simplejson
from utils.functions import render_to_pdf_weasy
from identificacao.models import Entidade, Endereco, EntidadeHistorico,\
    Identificacao, Ecossistema, Acesso, NivelAcesso, Agenda, TipoEntidade


@login_required
@require_safe
def ajax_escolhe_entidade(request):
    ent_id = request.GET.get('entidade')
    entidade = get_object_or_404(Entidade, pk=ent_id)

    retorno = []
    for ed in Endereco.objects.filter(entidade=entidade):
        descricao = '%s' % (ed.__unicode__())
        retorno.append({'pk': ed.pk, 'valor': descricao})

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required
@require_safe
def ajax_escolhe_entidade_filhos(request):
    ent_id = request.GET.get('entidade')
    entidade = get_object_or_404(Entidade, pk=ent_id)

    enderecos = []
    filhos = []

    for ed in Endereco.objects.filter(entidade=entidade):
        descricao = '%s' % (ed.__unicode__())
        enderecos.append({'pk': ed.pk, 'valor': descricao})

    if not enderecos:
        enderecos = [{"pk": "0", "valor": "Nenhum registro"}]

    for f in entidade.entidade_em.all():
        filhos.append({'pk': f.id, 'valor': f.sigla})

    retorno = {'enderecos': enderecos, 'filhos': filhos}

    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required
@require_safe
def ajax_escolhe_endereco(request):
    end_id = request.GET.get('endereco')
    endereco = get_object_or_404(Endereco, pk=end_id)

    retorno = []
    for d in endereco.enderecodetalhe_set.all():
        descricao = '%s' % (d.__unicode__())
        retorno.append({'pk': d.pk, 'valor': descricao})

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required
@permission_required('identificacao.rel_tec_arquivos', raise_exception=True)
@require_safe
def arquivos_entidade(request):
    """
     Relatório Técnico - Relatório de Documentos por entidade.

    """
    return render_to_response('identificacao/arquivos_entidade.html',
                              {'entidades': [e for e in Entidade.objects.all() if e.arquivoentidade_set.count() > 0]},
                              context_instance=RequestContext(request))


@login_required
@permission_required('identificacao.rel_adm_agenda', raise_exception=True)
@require_safe
def agenda(request, tipo=8, pdf=None):
    """
     Relatório Administrativo - Relatório de Agenda

    """
    agenda = request.GET.get('agenda')
    if agenda:
        entidades = []
        tipos = TipoEntidade.objects.filter(id__in=EntidadeHistorico.objects.filter(
            ativo=True, entidade__agendado__agenda__id=agenda, entidade__agendado__ativo=True).values_list(
            'tipo', flat=True).distinct().order_by('tipo'))
        for e in Entidade.objects.filter(entidadehistorico__ativo=True, entidade__isnull=True, agendado__ativo=True,
                                         agendado__agenda__id=agenda, entidadehistorico__tipo__id=tipo).distinct():
            areas = []
            for a in Identificacao.objects.filter(endereco__entidade=e).order_by('area').values_list('area', flat=True)\
                    .distinct():
                area = {'area': a, 'contatos': Identificacao.objects.filter(endereco__entidade=e, area=a)
                        .order_by('contato')}
                areas.append(area)
            entidades.append({'entidade': e, 'areas': areas})
            for ef in e.entidade_em.filter(entidadehistorico__ativo=True, agendado__agenda__id=agenda,
                                           agendado__ativo=True):
                areas = []
                for a in Identificacao.objects.filter(endereco__entidade=ef).order_by('area')\
                        .values_list('area', flat=True).distinct():
                    area = {'area': a, 'contatos': Identificacao.objects.filter(endereco__entidade=ef, area=a)
                            .order_by('contato')}
                    areas.append(area)
                entidades.append({'entidade': ef, 'filho': True, 'areas': areas})

        if pdf:
            return render_to_pdf_weasy('identificacao/agenda.pdf', {'entidades': entidades},
                                       request=request, filename='agenda.pdf')
        return TemplateResponse(request, 'identificacao/agenda.html',
                                {'entidades': entidades, 'tipo': int(tipo), 'tipos': tipos, 'agenda': agenda})
    else:
        agendas = Agenda.objects.order_by('nome')
        return TemplateResponse(request, 'identificacao/agendas.html', {'agendas': agendas})


@login_required
@permission_required('identificacao.rel_adm_ecossistema', raise_exception=True)
@require_safe
def planilha_ecossistema(request, tipo='par'):
    """
    Relatório Administrativo - Relatório de Ecossistema

    """
    if tipo == 'par':
        return TemplateResponse(request, 'identificacao/ecossistema_par.html',
                                {'ec': Ecossistema.objects.filter(
                                    identificacao__endereco__entidade__entidadehistorico__tipo__nome__in=['Equipe', 'Participante'])})
    elif tipo == 'tic':
        return TemplateResponse(request, 'identificacao/ecossistema_tic.html',
                                {'ec': Ecossistema.objects.filter(
                                    identificacao__endereco__entidade__entidadehistorico__tipo__nome__in=['TIC'])})
    else:
        raise Http404


@login_required
def acessos_terremark(request):

    if 'entidade' not in request.GET:
        entidade_ids = Acesso.objects.values_list('identificacao__endereco__entidade', flat=True).distinct()
        entidades = Entidade.objects.filter(id__in=entidade_ids).order_by('sigla')
        return TemplateResponse(request, 'identificacao/acessos.html', {'entidades': entidades})

    import csv

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="acessos.csv"'

    writer = csv.writer(response, delimiter=';', quotechar='"')

    entidade = request.GET.get('entidade')

    for acesso in Acesso.objects.filter(identificacao__endereco__entidade__id=entidade):
        fn = acesso.identificacao.contato.primeiro_nome or ''
        un = acesso.identificacao.contato.ultimo_nome or ''
        email = acesso.identificacao.contato.email or ''
        telefones = acesso.identificacao.contato.tel
        tels = telefones.split()
        ddd = ''
        cel = ''
        fixo = ''
        for t in tels:
            t = t.rstrip(',')
            if t.startswith('('):
                ddd = t
            elif t.startswith('2') or t.startswith('3') or t.startswith('4') or t.startswith('5'):
                fixo = '%s %s %s' % (fixo, ddd, t)
                ddd = ''
            else:
                cel = '%s %s %s' % (cel, ddd, t)
                ddd = ''

        writer.writerow([fn.encode('iso-8859-1'), un.encode('iso-8859-1'), fixo, cel, email] + ['']*16)
        niveis = acesso.niveis.all()
        linha = [''] * 21
        if acesso.liberacao:
            linha[7] = acesso.liberacao.strftime("%d-%m-%Y %I:%M%p")
        if acesso.encerramento:
            linha[8] = acesso.encerramento.strftime("%d-%m-%Y %I:%M%p")

        for na in NivelAcesso.objects.all():
            linha[6] = na.nome.encode('iso-8859-1')
            if na in niveis:
                linha[13] = 'X'
            writer.writerow(linha)
            linha[13] = linha[7] = linha[8] = ''

    return response
