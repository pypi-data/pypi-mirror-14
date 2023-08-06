# -* coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.contrib.auth.decorators import permission_required, login_required
from django.core import serializers
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe
import os
from collections import OrderedDict

from repositorio.models import Repositorio, Anexo, Ticket, Tipo as TipoRepositorio, Natureza, Servico
from patrimonio.models import Patrimonio
from identificacao.models import Entidade
from utils.functions import render_to_pdf_weasy


@login_required
@require_safe
def ajax_seleciona_patrimonios(request):
    search_string = request.GET.get('string')
    patrimonios = Patrimonio.objects.filter(Q(ns__icontains=search_string) | Q(descricao__icontains=search_string) |
                                            Q(pagamento__protocolo__num_documento__icontains=search_string))
    return HttpResponse(serializers.serialize('json', patrimonios))


@login_required
@require_safe
def ajax_repositorio_tipo_nomes(request):
    """
    Ajax utilizado no filtro do relatório do repositório.
    Dado um id de Entidade de um Tipo, retorna os nomes dessa entidade.
    """
    param_entidade_id = request.GET.get('id_entidade')
    # nomes = TipoRepositorio.objects.filter(entidade_id=param_entidade_id).values_list('nome', flat=True)
    # .order_by('nome')
    nomes = TipoRepositorio.objects.filter(entidade_id=param_entidade_id).values('nome').annotate(dcount=Count('nome'))\
        .order_by('nome')

    response = []
    for n in nomes:
        response.append(n['nome'])

    return JsonResponse(response, safe=False)


@login_required
@permission_required('repositorio.rel_ger_repositorio', raise_exception=True)
@require_safe
def relatorio_repositorio(request, pdf=0):
    """
     Relatório Administrativo - Relatório de dados de Repositório

    """
    # Parametros de filtros
    param_entidade_id = request.GET.get('entidade') or request.POST.get('entidade')
    param_nome = request.GET.get('nome') or request.POST.get('nome') or ''
    param_natureza_id = request.GET.get('natureza') or request.POST.get('natureza')
    param_servico_id = request.GET.get('servico') or request.POST.get('servico')
    param_data_de = request.GET.get('data_de') or request.POST.get('data_de') or ''
    param_data_ate = request.GET.get('data_ate') or request.POST.get('data_ate') or ''

    grupos = OrderedDict()
    if param_entidade_id or param_natureza_id or param_servico_id:
        param_entidade_id = param_entidade_id or '0'
        param_natureza_id = param_natureza_id or '0'
        param_servico_id = param_servico_id or '0'

        repositorios = Repositorio.objects.all()
        # Filtrando os dados do repositório
        if param_entidade_id and param_entidade_id != '0':
            repositorios = repositorios.filter(tipo__entidade__id=param_entidade_id)
        if param_nome:
            repositorios = repositorios.filter(tipo__nome__iexact=param_nome)
        if param_natureza_id and param_natureza_id != '0':
            repositorios = repositorios.filter(natureza__id=param_natureza_id)
        if param_servico_id and param_servico_id != '0':
            repositorios = repositorios.filter(servicos__id=param_servico_id)
        if param_data_de:
            repositorios = repositorios.filter(data_ocorrencia__gte=param_data_de)
        if param_data_ate:
            repositorios = repositorios.filter(data_ocorrencia__lte=param_data_ate)

        repositorios = repositorios.select_related('tipo', 'tipo__entidade', 'natureza')\
            .order_by('tipo__entidade__sigla', 'tipo__nome', 'natureza__nome', '-data_ocorrencia', 'estado__nome')

        # Repositórios agrupados por Tipo e Natureza
        for r in repositorios:
            grupo_chave = str(r.tipo_id) + '_' + str(r.natureza_id)
            if grupo_chave in grupos:
                grupo = grupos[grupo_chave]
            else:
                grupo = {'entidade': r.tipo.entidade, 'nome': r.tipo.nome, 'natureza': r.natureza.nome,
                         'repositorios': []}
                grupos.update({grupo_chave: grupo})

            # Carregando os dados de tamanho dos arquivos dos anexos
            anexos = []
            for a in Anexo.objects.filter(repositorio=r):
                if a.arquivo:
                    filepath = os.path.join(settings.MEDIA_ROOT, a.arquivo.__unicode__())
                    str_size = ' - '
                    if os.path.isfile(filepath):
                        size = os.path.getsize(filepath)
                        if size < 1000:
                            str_size = "{:10.3f}".format(size/1000.0)
                        else:
                            str_size = "{:10.0f}".format(size/1000.0)

                    anexo = {'nome': a.arquivo.__unicode__(), 'tamanho': str_size, 'palavras_chave': a.palavras_chave,
                             'path': os.path.join(settings.MEDIA_URL, a.arquivo.__unicode__())}
                    anexos.append(anexo)

            # Guardando os dados do repositório no grupo
            grupo['repositorios'].append({'id': r.id, 'data_ocorrencia': r.data_ocorrencia.isoformat(),
                                          'estado': r.estado, 'ocorrencia': r.ocorrencia,
                                          'servicos': r.servicos.all().order_by('nome'),
                                          'memorandos': r.memorandos.all(),
                                          'tickets': Ticket.objects.filter(repositorio=r).order_by('ticket'),
                                          'patrimonios': r.patrimonios.all().order_by('ns'), 'anexos': anexos
                                          })

    # carregando os dados de exibição dos filtros
    filtro_entidades = Entidade.objects.filter(id__in=TipoRepositorio.objects.all().values_list('entidade_id'))
    filtro_nomes = []
    if param_entidade_id:
        # filtro_nomes = TipoRepositorio.objects.filter(entidade_id=param_entidade_id).values_list('nome', flat=True)
        # .order_by('nome')
        filtro_nomes = TipoRepositorio.objects.filter(entidade_id=param_entidade_id).values('nome')\
            .annotate(dcount=Count('nome')).order_by('nome')
    filtro_naturezas = Natureza.objects.filter(id__in=Repositorio.objects.all().values_list('natureza_id'))
    filtro_servicos = Servico.objects.filter(id__in=Repositorio.objects.all().values_list('servicos__id'))

    template_name = "relatorio_repositorio"
    if pdf:
        return render_to_pdf_weasy('repositorio/%s.pdf' % template_name, {'grupos': grupos.itervalues()},
                                   request=request, filename='%s.pdf' % template_name)

    return TemplateResponse(request, 'repositorio/%s.html' % template_name, {
                            # Dados dos repositórios
                            'grupos': grupos.itervalues(),
                            'qtd_grupos': len(grupos),
                            # Dados dos filtros
                            'filtro_entidades': filtro_entidades,
                            'filtro_nomes': filtro_nomes,
                            'filtro_naturezas': filtro_naturezas,
                            'filtro_servicos': filtro_servicos,
                            # Parametros dos filtros
                            'entidade': param_entidade_id,
                            'natureza': param_natureza_id,
                            'servico': param_servico_id,
                            'nome': param_nome,
                            'data_de': param_data_de,
                            'data_ate': param_data_ate
                            })
