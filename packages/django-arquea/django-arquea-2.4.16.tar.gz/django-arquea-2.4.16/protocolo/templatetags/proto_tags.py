# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.template import Library
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from decimal import Decimal

from membro.models import Membro
from protocolo.models import Protocolo, Cotacao
import unicodedata
import re

register = Library()


@register.inclusion_tag('admin/protocolo/protocolo/vencendo.html')
def mostra_vencer():
    choices = [p for p in Protocolo.objects.all() if p.pagamentos_amanha()]
    return {'existe': len(choices), 'choices': choices}


@register.simple_tag
def detalha_externo(field):
    try:
        rel = field.field.widget.rel.to
        if rel in field.field.widget.admin_site._registry:
            url = "'../../../%s/%s/'" % (rel._meta.app_label, rel._meta.object_name.lower())
            return mark_safe('<a href="javascript:void(0);" id="detail_%s" '
                             'onclick="window.open(%s+document.forms[0][\'%s\'].value+\'/\');">%s</a>' %
                             (rel._meta.object_name.lower(), url, field.html_name, 'Detalhe'))
        else:
            return ''
    except:
        return ''


@register.simple_tag
def link_cotacao(pk):
    try:
        p = Protocolo.objects.get(pk=pk)
    except Protocolo.DoesNotExist:
        return ''

    try:
        c = p.cotacao  # @UnusedVariable
    except Cotacao.DoesNotExist:
        return ''

    return mark_safe('<a href="/protocolo/%s/cotacoes">%s</a>' % (pk, _(u'Ver cotações')))


# @register.inclusion_tag()
# Definindo abaixo do método para poder receber o context
def lista_relatorios(context):
    gerenciais = []
    administrativos = []
    tecnicos = []
    verificacoes = []

    user = context['user']

    if user.is_superuser or user.has_perm('financeiro.rel_adm_pagamentos_mes'):
        administrativos.append({'url': '/financeiro/relatorios/pagamentos_mes', 'nome': u'Pagamentos por mês'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_pagamentos_parcial'):
        administrativos.append({'url': '/financeiro/relatorios/pagamentos_parcial', 'nome': u'Pagamentos por parcial'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_parciais'):
        administrativos.append({'url': '/financeiro/relatorios/parciais', 'nome': u'Diferenças totais'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_caixa'):
        administrativos.append({'url': '/financeiro/relatorios/caixa', 'nome': u'Diferenças de caixa'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_extrato'):
        administrativos.append({'url': '/financeiro/extrato', 'nome': u'Panorama da conta corrente'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_extrato_mes'):
        administrativos.append({'url': '/financeiro/extrato_mes', 'nome': u'Extrato da conta corrente por mês'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_extrato_tarifas'):
        administrativos.append({'url': '/financeiro/extrato_tarifas', 'nome': u'Extrato de tarifas por mês'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_extrato_financeiro'):
        administrativos.append({'url': '/financeiro/extrato_financeiro', 'nome': u'Extrato do financeiro por mês'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_extrato_financeiro_parciais'):
        administrativos.append({'url': '/financeiro/extrato_financeiro_parciais',
                                'nome': u'Extrato do financeiro por parcial'})

    if user.is_superuser or user.has_perm('financeiro.rel_adm_prestacao'):
        administrativos.append({'url': '/financeiro/relatorios/prestacao', 'nome': u'Prestação de contas'})

    if user.is_superuser or user.has_perm('protocolo.rel_adm_descricao'):
        administrativos.append({'url': '/protocolo/descricao', 'nome': u'Protocolos por descrição'})

    if user.is_superuser or user.has_perm('memorando.rel_adm_memorando'):
        administrativos.append({'url': '/memorando/relatorio', 'nome': u'Memorandos FAPESP'})

    if user.is_superuser or user.has_perm('outorga.rel_adm_item_modalidade'):
        administrativos.append({'url': '/outorga/relatorios/item_modalidade',
                                'nome': u'Itens do orçamento por modalidade'})

    if user.is_superuser or user.has_perm('identificacao.rel_adm_agenda'):
        administrativos.append({'url': '/identificacao/agenda', 'nome': u'Agenda'})

    if user.is_superuser or user.has_perm('identificacao.rel_adm_ecossistema'):
        administrativos.append({'url': '/identificacao/ecossistema/par', 'nome': u'Ecossistema'})

    if user.is_superuser or user.has_perm('membro.rel_adm_mensalf'):
        administrativos.append({'url': '/membro/mensalf', 'nome': u'Controle de horário mensal'})

    if user.is_superuser or user.has_perm('patrimonio.rel_adm_por_termo'):
        administrativos.append({'url': '/patrimonio/relatorio/por_termo', 'nome': u'Patrimônio por termo de outorga'})

    if user.is_superuser or user.has_perm('membro.rel_adm_logs'):
        administrativos.append({'url': '/membro/logs', 'nome': u'Registro de uso do sistema por ano'})

    if user.is_superuser or user.has_perm('patrimonio.rel_adm_presta_contas'):
        administrativos.append({'url': '/patrimonio/relatorio/presta_contas',
                                'nome': u'Prestação de contas patrimonial (em construção)'})

    if user.is_superuser or user.has_perm('identificacao.rel_tec_arquivos'):
        # Movido da área técnica para a administrativa
        administrativos.append({'url': '/identificacao/relatorios/arquivos', 'nome': u'Documentos por entidade'})

    if user.is_superuser or user.has_perm('repositorio.rel_ger_repositorio'):
        # Movido da área aministrativa para gerencial
        gerenciais.append({'url': '/repositorio/relatorio/repositorio', 'nome': u'Repositório'})

    if user.is_superuser or user.has_perm('financeiro.rel_ger_gerencial'):
        gerenciais.append({'url': '/financeiro/relatorios/gerencial', 'nome': u'Gerencial'})

    if user.is_superuser or user.has_perm('financeiro.rel_ger_gerencial'):
        gerenciais.append({'url': '/financeiro/relatorios/gerencial_anual', 'nome': u'Gerencial por ano'})

    if user.is_superuser or user.has_perm('financeiro.rel_ger_acordos'):
        gerenciais.append({'url': '/financeiro/relatorios/acordos', 'nome': u'Acordos'})

    if user.is_superuser or user.has_perm('outorga.rel_ger_contratos'):
        gerenciais.append({'url': '/outorga/relatorios/contratos', 'nome': u'Contratos'})

    if user.is_superuser or user.has_perm('outorga.rel_ger_lista_acordos'):
        gerenciais.append({'url': '/outorga/relatorios/lista_acordos', 'nome': u'Concessões por  acordo'})

    if user.is_superuser or user.has_perm('outorga.rel_ger_acordo_progressivo'):
        gerenciais.append({'url': '/outorga/relatorios/acordo_progressivo', 'nome': u'Gerencial progressivo'})

    if user.is_superuser or user.has_perm('processo.rel_ger_processos'):
        gerenciais.append({'url': '/processo/processos', 'nome': u'Processos'})

    if user.is_superuser or user.has_perm('rede.rel_ger_custo_terremark'):
        gerenciais.append({'url': '/rede/custo_terremark', 'nome': u'Custos dos recursos contratados'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_estado'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_estado', 'nome': u'Patrimônio por estado do item'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_local'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_local', 'nome': u'Patrimônio por localização'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_local_termo'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_local_termo',
                         'nome': u'Patrimônio por localização (com Termo)'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_local_rack'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_local_rack', 'nome': u'Patrimônios por local e rack'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_tipo'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_tipo', 'nome': u'Patrimônio por tipo'})

    if user.is_superuser or user.has_perm('rede.rel_tec_planejamento'):
        tecnicos.append({'url': '/rede/planejamento', 'nome': u'Planejamento por ano'})

    if user.is_superuser or user.has_perm('rede.rel_tec_servico_processo'):
        tecnicos.append({'url': '/rede/planejamento2', 'nome': u'Serviços contratados por processo'})

    if user.is_superuser or user.has_perm('rede.rel_tec_info'):
        tecnicos.append({'url': '/rede/info', 'nome': u'Dados cadastrais dos participantes'})
    if user.is_superuser or user.has_perm('patrimonio.rel_tec_racks'):
        tecnicos.append({'url': '/patrimonio/racks', 'nome': u'Bayfaces'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_racks'):
        tecnicos.append({'url': '/patrimonio/relatorio_rack', 'nome': u'Relatorio por rack (em construção)'})

    if user.is_superuser or user.has_perm('patrimonio.rel_tec_planta_baixa_edit'):
        tecnicos.append({'url': '/patrimonio/planta_baixa_edit', 'nome': u'Planta Baixa - Racks (em construção)'})
    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_marca'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_marca', 'nome': u'Patrimônio por marca'})
    if user.is_superuser or user.has_perm('rede.rel_tec_blocosip'):
        tecnicos.append({'url': '/rede/relatorios/blocosip', 'nome': u'Lista de blocos IP'})
    if user.is_superuser or user.has_perm('patrimonio.rel_tec_patr_tipo_equipamento'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_tipo_equipamento2',
                         'nome': u'Patrimônio por tipo de equipamento'})
    if user.is_superuser or user.has_perm('patrimonio.rel_tec_por_tipo_equipamento'):
        tecnicos.append({'url': '/patrimonio/relatorio/por_tipo_equipamento', 'nome': u'Busca por tipo de equipamento'})
    if user.is_superuser or user.has_perm('rede.rel_tec_recursos_operacional'):
        tecnicos.append({'url': '/rede/relatorio_recursos_operacional', 'nome': u'Relatório de recursos'})

    if user.is_superuser or user.has_perm('rede.rel_tec_blocosip_transito'):
        tecnicos.append({'url': '/rede/relatorios/blocosip_transito', 'nome': u'Lista de blocos IP - Trânsito'})
    if user.is_superuser or user.has_perm('rede.rel_tec_blocosip_inst_transito'):
        tecnicos.append({'url': '/rede/relatorios/blocosip_inst_transito',
                         'nome': u'Lista de blocos IP - Instituição Trânsito'})

    if user.is_superuser or user.has_perm('rede.rel_tec_blocosip_ansp'):
        tecnicos.append({'url': '/rede/relatorios/blocosip_ansp', 'nome': u'Lista de blocos IP - ANSP'})
    if user.is_superuser or user.has_perm('rede.rel_tec_blocosip_inst_ansp'):
        tecnicos.append({'url': '/rede/relatorios/blocosip_inst_ansp',
                         'nome': u'Lista de blocos IP - Instituição ANSP'})

    if user.is_superuser or user.has_perm('rede.rel_tec_crossconnection'):
        tecnicos.append({'url': '/rede/relatorios/crossconnection', 'nome': u'Lista de Cross Connections'})

    if user.is_superuser:
        verificacoes.append({'url': '/verificacao/relatorio/equipamento_consolidado',
                             'nome': u'Verificação de equipamentos'})

    if user.is_superuser:
        verificacoes.append({'url': '/verificacao/relatorio/patrimonio_consolidado',
                             'nome': u'Verificação de patrimônio'})

    if user.is_superuser:
        verificacoes.append({'url': '/carga/', 'nome': u'Carga de planilha de patrimônio'})

    if user.is_superuser:
        verificacoes.append({'url': '/verificacao/versao', 'nome': u'Verificação de versão'})

    gerenciais.sort(key=lambda x: x['nome'])
    administrativos.sort(key=lambda x: x['nome'])
    tecnicos.sort(key=lambda x: x['nome'])
    verificacoes.sort(key=lambda x: x['nome'])

    retorno = {'relatorios': []}
    if len(gerenciais) > 0:
        retorno['relatorios'].append({'nome': u'gerenciais', 'rel': gerenciais})
    if len(administrativos) > 0:
        retorno['relatorios'].append({'nome': u'administrativos', 'rel': administrativos})
    if len(tecnicos) > 0:
        retorno['relatorios'].append({'nome': u'técnicos', 'rel': tecnicos})
    if len(verificacoes) > 0:
        retorno['relatorios'].append({'nome': u'de verificações (Acesso restrito)', 'rel': verificacoes})

    return retorno

# Register the custom tag as an inclusion tag with takes_context=True.
register.inclusion_tag('admin/relatorios.html', takes_context=True)(lista_relatorios)


@register.filter(name='moeda_css')
def moeda_css(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, com valor negativo em cor vermelha em css
    """
    return mark_safe(moeda(value, nac, False, True))


@register.filter(name='moeda_valor')
def moeda_valor(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, mas remover o prefixo da moeda (ex: R$)
    """
    return mark_safe(moeda(value, nac, True, False))


@register.filter(name='moeda_valor_css')
def moeda_valor_css(value, nac=1):
    """
    Novo metodo para formatar o valor em moeda, mas remover o prefixo da moeda (ex: R$),
    com valor negativo em cor vermelha em css
    """
    return mark_safe(moeda(value, nac, True, True))


@register.filter(name='moeda')
def moeda(value, nac=True, nosep=False, css=False):
    if nac:
        sep = ','
    else:
        sep = '.'

    try:
        v = Decimal(value)
    except:
        return value

    try:
        i, d = str(value).split('.')
    except ValueError:
        i = str(value)
        d = '00'

    # Corrigindo o tamanho da decimal para 2 dígitos
    if len(d) > 2:
        d = d[:2]
    if len(d) == 1:
        d = d[:1] + '0'

    s = '%s'
    # Verifica se adiciona () para números negativos
    # Se for especificado como CSS, o tratamento ocorre no final
    if i[0] == '-':
        i = i[1:len(i)]

    res = []
    p = len(i)
    while p > 2:
        res.append(i[p-3:p])
        p -= 3
    if p > 0:
        res.append(i[0:p])

    si = '.'
    m = 'R$'
    if sep == '.':
        si = ','
        m = 'US$'

    res.reverse()
    i = si.join(res)

    # valor com os separadores
    valor = s % (sep.join((i, d)))

    # Juntando o número, separador de dígito, e digitos
    # Adiciona, ou não, o valor de moeda
    retorno = None
    if nosep:
        retorno = valor
    else:
        retorno = '%s %s' % (m, valor)

    # tratamento de negativos
    if v < 0:
        if css is False:
            retorno = '(%s)' % retorno
        else:
            retorno = '-%s' % retorno

    # Faz o tratamento de negativo utilizando CSS com cor vermelha
    if css and v < 0:
        retorno = '<span style="color: red">%s</span>' % retorno

    return mark_safe(retorno)


@register.inclusion_tag('membro/controle.html')
def controle_horario(user):
    try:
        membro = Membro.objects.get(contato__email=user.email)
    except Membro.DoesNotExist:
        return {'acao': None}

    controles = membro.controle_set.all()
    acao = u'entrada'
    if controles:
        controle = controles[0]
        if controle.saida is None:
            acao = u'saída'

    return {'acao': acao, 'user': user.first_name}


@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(int(value))


@register.filter
def has_group(user, group_name):
    """
    Filter to check if a user belongs to a certain group.
    Usage:

    {% if request.user|has_group:"xxx" %}
       Do something
    {% endif %}

    """

    return user.groups.filter(name=group_name).exists()


@register.filter
def has_permission(user, url):
    """
        Verifica se o usuário tem permissão de acesso a URL
        Usage:

        {% if request.user|has_permission:"url" %}
           Do something
        {% endif %}
    """
    try:
        if url:
            myurl = resolve(url)

            url_splitted = myurl.url_name.split("_")

            model_name = 'xxx'
            if len(url_splitted) == 3:
                model_name = url_splitted[1]
            elif len(url_splitted) == 4:
                model_name = url_splitted[1] + "_" + url_splitted[2]

            permission_name = url_splitted[0] + ".change_" + model_name
            retorno = user.has_perm(permission_name)
            return retorno
    except:
        return False

    return False


@register.filter(name='stripaccents')
def stripaccents(value, arg=""):
    """
    Remove os acentos das letras:
    Ex: troca o caracter acentuado É por E
    """
    if type(value) == str:
        return value
    return ''.join((c for c in unicodedata.normalize('NFD', value) if unicodedata.category(c) != 'Mn'))


def menu_has_permission(context, menuitem):
    """
        Verifica o menu possui algum sub-menu com permissão de acesso.
        Usage:
        {% menu_has_permission "codigo_permissao" as permitted %}

        O codigo_permissao precisa ser o identificador completo da permissão. Ex:
            patrimonio.change_historicolocal

    """

    retorno = False

    if menuitem.url:

        myurl = resolve(menuitem.url)

        url_splitted = myurl.url_name.split("_")

        model_name = 'xxx'
        if len(url_splitted) == 3:
            model_name = url_splitted[1]
        elif len(url_splitted) == 4:
            model_name = url_splitted[1] + "_" + url_splitted[2]

        permission_name = url_splitted[0] + ".change_" + model_name
        retorno = context['user'].has_perm(permission_name)

    if not retorno and menuitem.has_children():
        for child in menuitem.children():
            retorno = retorno or menu_has_permission(context, child)

    return retorno
register.assignment_tag(takes_context=True)(menu_has_permission)


@register.filter
def replace(string, args):
    args = args.split(args[0])

    return re.sub(args[1], args[2], string)
