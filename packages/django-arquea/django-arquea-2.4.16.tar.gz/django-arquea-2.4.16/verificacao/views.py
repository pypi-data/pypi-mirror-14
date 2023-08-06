# -* coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.shortcuts import render


import logging
from verificacao.models import VerificacaoEquipamento,\
    VerificacaoPatrimonioEquipamento, VerificacaoPatrimonio
from patrimonio.models import Tipo, Patrimonio

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def equipamento_consolidado(request):
    retorno = []

    verificacaoEquipamento = VerificacaoEquipamento()

    partNumberVSModeloDiferente = verificacaoEquipamento.partNumberVSModeloDiferente()
    count = sum([len(equipamentos) for equipamentos in partNumberVSModeloDiferente])
    retorno.append({'desc': u'Part Numbers iguais com Modelos diferentes',
                    'url': 'equipamento_part_number_modelo_diferente', 'qtd': count})

    partNumberVazio = verificacaoEquipamento.partNumberVazio()
    count = sum([len(equipamentos) for equipamentos in partNumberVazio])
    retorno.append({'desc': u'Part Numbers vazios', 'url': 'equipamento_part_number_vazio', 'qtd': count})

    partNumberVazioModeloVazio = verificacaoEquipamento.partNumberVazioModeloVazio()
    count = sum([len(equipamentos) for equipamentos in partNumberVazioModeloVazio])
    retorno.append({'desc': u'Part Numbers e Modelos vazios', 'url': 'equipamento_part_number_modelo_vazio',
                    'qtd': count})

    marcaVazia = verificacaoEquipamento.marcaVazia()
    count = len(marcaVazia)
    retorno.append({'desc': u'Marca/Entidade vazia', 'url': 'equipamento_marca_vazia', 'qtd': count})

    return render(request, 'verificacao/equipamento_consolidado.html', {'verificacoes': retorno})


@login_required
def equipamento_marca_vazia(request, json=False):

    verficacao = VerificacaoEquipamento()
    retorno = verficacao.marcaVazia()

    return render(request, 'verificacao/equipamento_marca.html',
                  {'desc': 'Marca/Entidade vazia', 'equipamentos': retorno})


@login_required
def equipamento_part_number_modelo_diferente(request, json=False):

    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVSModeloDiferente()

    return render(request, 'verificacao/equipamento_part_number.html',
                  {'desc': 'Part Numbers iguais com Modelos diferentes', 'equipamentos': retorno})


@login_required
def equipamento_part_number_vazio(request, json=False):

    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVazio()

    return render(request, 'verificacao/equipamento_part_number.html',
                  {'desc': 'Part Numbers vazios', 'equipamentos': retorno})


@login_required
def equipamento_part_number_modelo_vazio(request, json=False):

    verficacao = VerificacaoEquipamento()
    retorno = verficacao.partNumberVazioModeloVazio()

    return render(request, 'verificacao/equipamento_part_number.html',
                  {'desc': 'Part Numbers e Modelos vazios', 'equipamentos': retorno})


@login_required
def check_patrimonio_equipamento(request):
    patrimonios = Patrimonio.objects.filter(equipamento_id__isnull=False).select_related('equipamento')
    patrimonios = patrimonios.filter(Q(~Q(equipamento__tamanho=F('tamanho')), Q(equipamento__tamanho__isnull=False),
                                       Q(tamanho__isnull=False))
                                     )
    c = {}
    c.update({'patrimonios': patrimonios})

    return render(request, 'verificacao/check_patrimonio_equipamento.html', c)


@login_required
def patrimonio_consolidado(request):
    retorno = []

    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verificacaoPatrimonio = VerificacaoPatrimonio()

    equipamentoVazio = verificacaoPatrimonio.equipamentoVazio(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in equipamentoVazio])
    retorno.append({'desc': u'Patrimonios sem Equipamento', 'url': 'patrimonio_equipamento_vazio', 'qtd': count})

    verificacaoPatrimonioEquipamento = VerificacaoPatrimonioEquipamento()

    descricaoDiferente = verificacaoPatrimonioEquipamento.descricaoDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in descricaoDiferente])
    retorno.append({'desc': u'Patrimonio e Equipamento com Descricao diferente',
                    'url': 'patrimonio_equipamento_descricao_diferente', 'qtd': count})

    tamanhoDiferente = verificacaoPatrimonioEquipamento.tamanhoDiferente(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in tamanhoDiferente])
    retorno.append({'desc': u'Patrimonio e Equipamento com Tamanho diferente',
                    'url': 'patrimonio_equipamento_tamanho_diferente', 'qtd': count})

    procedenciaVazia = verificacaoPatrimonio.procedenciaVazia(filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in procedenciaVazia])
    retorno.append({'desc': u'Patrimonio com procedecia vazia', 'url': 'patrimonio_procedencia_vazia', 'qtd': count})

    localidadeDiferente = verificacaoPatrimonio.localidadeDiferente(filtros=filtros_entrada)
    count = sum([len(patrimonios) for patrimonios in localidadeDiferente])
    retorno.append({'desc': u'Patrimonio com localidade diferente dos filhos',
                    'url': 'patrimonio_localidade_diferente', 'qtd': count})

    retorno.append({'desc': u'Verificação de Patrimônios e Equipamentos',
                    'url': 'check_patrimonio_equipamento', 'qtd': None})

    filtros = {"tipos": Tipo.objects.all()}

    return render(request, 'verificacao/patrimonio_consolidado.html', {'verificacoes': retorno, 'filtros': filtros})


@login_required
def patrimonio_localidade_diferente(request):
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.localidadeDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = \
            {"tipos": VerificacaoPatrimonioEquipamento().listaFiltroTipoPatrimonio(verficacao.equipamentoVazio()[0])}

    return render(request, 'verificacao/patrimonio_localidade.html',
                  {'desc': 'Patrimonios com componentes com historico local diferente', 'patrimonios': retorno,
                   'filtros': filtros_saida})


@login_required
def patrimonio_procedencia_vazia(request):
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.procedenciaVazia(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = \
            {"tipos": VerificacaoPatrimonioEquipamento().listaFiltroTipoPatrimonio(verficacao.equipamentoVazio()[0])}

    return render(request, 'verificacao/patrimonio_procedencia.html',
                  {'desc': 'Patrimonios com procedência vazia', 'patrimonios': retorno, 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_vazio(request):
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonio()
    retorno = verficacao.equipamentoVazio(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida =\
            {"tipos": VerificacaoPatrimonioEquipamento().listaFiltroTipoPatrimonio(verficacao.equipamentoVazio()[0])}

    return render(request, 'verificacao/patrimonio.html',
                  {'desc': 'Patrimonios sem Equipamento', 'patrimonios': retorno, 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_part_number_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.partNumberDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos": verficacao.listaFiltroTipoPatrimonio(verficacao.descricaoDiferente()[0])}

    if ajax:
        return render(request, 'verificacao/patrimonio_equipamento-table.html',
                      {'desc': 'Patrimonio e Equipamento com Part Number diferente', 'patrimonios': retorno,
                       'atributo': 'part_number', 'filtros': filtros_saida})
    else:
        return render(request, 'verificacao/patrimonio_equipamento.html',
                      {'desc': 'Patrimonio e Equipamento com Part Number diferente', 'patrimonios': retorno,
                       'atributo': 'part_number', 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_descricao_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.descricaoDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos": verficacao.listaFiltroTipoPatrimonio(verficacao.descricaoDiferente()[0])}

    if ajax:
        return render(request, 'verificacao/patrimonio_equipamento-table.html',
                      {'desc': 'Patrimonio e Equipamento com Descricao diferente', 'patrimonios': retorno,
                       'atributo': 'descricao', 'filtros': filtros_saida})
    else:
        return render(request, 'verificacao/patrimonio_equipamento.html',
                      {'desc': 'Patrimonio e Equipamento com Descricao diferente', 'patrimonios': retorno,
                       'atributo': 'descricao', 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_marca_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.marcaDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos": verficacao.listaFiltroTipoPatrimonio(verficacao.marcaDiferente()[0])}

    if ajax:
        return render(request, 'verificacao/patrimonio_equipamento-table.html',
                      {'desc': 'Patrimonio e Equipamento com Marca diferente', 'patrimonios': retorno,
                       'atributo': 'marca', 'filtros': filtros_saida})
    else:
        return render(request, 'verificacao/patrimonio_equipamento.html',
                      {'desc': 'Patrimonio e Equipamento com Marca diferente', 'patrimonios': retorno,
                       'atributo': 'marca', 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_modelo_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.modeloDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos": verficacao.listaFiltroTipoPatrimonio(verficacao.modeloDiferente()[0])}

    if ajax:
        return render(request, 'verificacao/patrimonio_equipamento-table.html',
                      {'desc': 'Patrimonio e Equipamento com Modelo diferente', 'patrimonios': retorno,
                       'atributo': 'modelo', 'filtros': filtros_saida})
    else:
        return render(request, 'verificacao/patrimonio_equipamento.html',
                      {'desc': 'Patrimonio e Equipamento com Modelo diferente', 'patrimonios': retorno,
                       'atributo': 'modelo', 'filtros': filtros_saida})


@login_required
def patrimonio_equipamento_tamanho_diferente(request):
    ajax = request.GET.get('ajax')
    filtros_entrada = {'filtro_tipo_patrimonio': request.GET.get('filtro_tipo_patrimonio')}

    verficacao = VerificacaoPatrimonioEquipamento()
    retorno = verficacao.tamanhoDiferente(filtros_entrada)

    filtros_saida = []
    if len(retorno) > 0:
        filtros_saida = {"tipos": verficacao.listaFiltroTipoPatrimonio(verficacao.tamanhoDiferente()[0])}

    if ajax:
        return render(request, 'verificacao/patrimonio_equipamento-table.html',
                      {'desc': 'Patrimonio e Equipamento com Tamanho diferente', 'patrimonios': retorno,
                       'atributo': 'tamanho', 'filtros': filtros_saida})
    else:
        return render(request, 'verificacao/patrimonio_equipamento.html',
                      {'desc': 'Patrimonio e Equipamento com Tamanho diferente', 'patrimonios': retorno,
                       'atributo': 'tamanho', 'filtros': filtros_saida})


@login_required
def copy_attribute_to_patrimonio(request):
    # Id do patrimonio
    patrimonio_id = request.GET.get('patrimonio_id')
    # Destino do valor a ser copiado ['patrimonio', 'equipamento']
    to_object = request.GET.get('to_object')
    # Nome do atributo a ser copiado
    att_name = request.GET.get('att_name')

    verficacao = VerificacaoPatrimonioEquipamento()
    verficacao.copy_attribute(to_object, patrimonio_id, att_name)
    if att_name == 'descricao':
        return patrimonio_equipamento_descricao_diferente(request)
    elif att_name == 'modelo':
        return patrimonio_equipamento_modelo_diferente(request)
    elif att_name == 'marca':
        return patrimonio_equipamento_marca_diferente(request)
    elif att_name == 'part_number':
        return patrimonio_equipamento_part_number_diferente(request)
    elif att_name == 'tamanho':
        return patrimonio_equipamento_tamanho_diferente(request)
    elif att_name == 'procedencia':
        return patrimonio_procedencia_vazia(request)
    else:
        raise ValueError('Valor inválido para o parametro. att_name' + str(att_name))


# Verifica a versão dos Python, Django e do PostgreeSQL
def versao(request):
    # Versão do django
    import django
    django_version = 'django ' + str(django.VERSION)

    # Versão do python
    import sys
    python_version = str(sys.version_info)
    python_version = python_version.replace('sys.version_info', 'python ').replace('major=', '').replace('minor=', '') \
                                   .replace('micro=', '').replace('releaselevel=', '').replace('serial=', '')

    # Versão do banco de dados
    from django.db import connection
    version = connection.pg_version
    lst = [str(i) for i in str(version)]
    db_version = "%s (%s, %s, %s)" % (connection.vendor, ''.join(lst[:len(lst)-4]), ''.join(lst[len(lst)-4:len(lst)-2]),
                                      ''.join(lst[len(lst)-2:]))

    return render(request, 'verificacao/versao.html',
                  {'django_version': django_version, 'python_version': python_version, 'db_version': db_version})
