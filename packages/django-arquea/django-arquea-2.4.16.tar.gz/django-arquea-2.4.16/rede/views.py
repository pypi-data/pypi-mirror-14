# -* coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date
from django.contrib.auth.decorators import permission_required, login_required
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe

from decimal import Decimal
import json as simplejson

from configuracao.models import Variavel
from financeiro.models import Pagamento
from identificacao.models import Entidade, Identificacao, ASN
from outorga.models import OrdemDeServico, Termo, EstadoOS
from rede.modelsResource import BlocosIP_Rel_Lista_BlocoIP_Resource,\
    BlocosIP_Rel_Lista_Inst_BlocoIP_Resource, CustoTerremarkRecursoResource,\
    RecursoOperacionalResource, CrossConnectionResource
from rede.models import PlanejaAquisicaoRecurso, Projeto, Enlace, BlocoIP,\
    TipoServico, Recurso, Beneficiado, IFCConector, CrossConnection
from utils.functions import render_to_pdf_weasy


@login_required
@require_safe
def ajax_escolhe_pagamento(request):
    retorno = []
    termo = request.GET.get('termo')

    if termo:
        for p in Pagamento.objects.filter(protocolo__termo__id=termo):
            if p.conta_corrente:
                descricao = 'Doc. %s, cheque %s, valor %s' % (p.protocolo.num_documento, p.conta_corrente.cod_oper,
                                                              p.valor_fapesp)
            else:
                descricao = 'Doc. %s, valor %s' % (p.protocolo.num_documento, p.valor_patrocinio)

            retorno.append({'pk': p.pk, 'valor': descricao})

    if not retorno:
        retorno = [{"pk": "0", "valor": "Nenhum registro"}]

    json = simplejson.dumps(retorno)
    return HttpResponse(json, content_type="application/json")


@login_required
@permission_required('rede.rel_tec_planejamento', raise_exception=True)
@require_safe
def planejamento(request, pdf=0):
    """
     Relatório Técnico - Relatório de Planejamento por ano.

    """
    anoproj = request.GET.get('anoproj')
    if anoproj:
        ano, proj = anoproj.split('/')
    else:
        ano = None
        proj = None
    contrato = request.GET.get('contrato')
    os = request.GET.get('os')

    if not ano and not proj and not contrato and not os:
        return TemplateResponse(request, 'rede/escolhe_ano.html',
                                {'anoproj': [(p[0], Projeto.objects.get(id=p[1]))
                                             for p in PlanejaAquisicaoRecurso.objects.values_list('ano', 'projeto')
                                             .order_by('ano').distinct()],
                                 'oss': OrdemDeServico.objects.all()})

    entidades = []

    for e in Entidade.objects.filter(contrato__ordemdeservico__planejaaquisicaorecurso__isnull=False).distinct():
        entidade = {'entidade': e}
        planejamentos = PlanejaAquisicaoRecurso.objects.filter(os__contrato__entidade=e)
        if ano:
            planejamentos = planejamentos.filter(ano=ano)
        if proj:
            planejamentos = planejamentos.filter(projeto__id=proj)
        if os:
            planejamentos = planejamentos.filter(os__id=os)
        projetos = []
        for p in Projeto.objects.filter(planejaaquisicaorecurso__in=planejamentos).distinct():
            projeto = {'projeto': p, 'plan': planejamentos.filter(projeto=p)}
            projetos.append(projeto)
        entidade.update({'projetos': projetos})
        entidades.append(entidade)

    if pdf:
        return render_to_pdf_weasy('rede/planejamento.pdf', {'entidades': entidades, 'ano': ano}, request=request,
                                   filename='planejamento%s.pdf' % ano)
    return TemplateResponse(request, 'rede/planejamento.html',
                            {'entidades': entidades, 'ano': ano, 'projeto': proj, 'os': os})


@login_required
@permission_required('rede.rel_tec_info', raise_exception=True)
@require_safe
def planilha_informacoes_gerais(request):
    """
     Relatório Técnico - Relatório de Dados cadastrais dos participantes.

    """
    info = Enlace.objects.filter(participante__entidade__entidadehistorico__ativo=True)
    return TemplateResponse(request, 'rede/informacoes_gerais.html', {'info': info})


@login_required
def planilha_informacoes_tecnicas(request, id=None):
    if not id:
        raise Http404
    tecnicos = Identificacao.objects.filter(area__contains='Tec')
    adm = Identificacao.objects.filter(Q(area__contains='Adm') | Q(area__contains='Gest'))
    asns = ASN.objects.all()  # filter(pais='BR')
    blocos_ips = BlocoIP.objects.all()
    dados = []
    for e in Enlace.objects.filter(id=id):
        entidade = e.participante.entidade
        contato_tec = tecnicos.filter(endereco__entidade=entidade)
        contato_adm = adm.filter(endereco__entidade=entidade)
        asn = asns.filter(entidade=entidade)
        blocos = blocos_ips.filter(designado=entidade)
        # operadoras = e.enlaceoperadora_set.all()
        operadoras = e.segmento_set.filter(data_desativacao__isnull=True)
        dados.append({"enlace": e, "contatos_tec": contato_tec, "contatos_adm": contato_adm, "asn": asn,
                      "bloco_ip": blocos, "operadoras": operadoras})
    return TemplateResponse(request, 'rede/informacoes_tecnicas.html', {'dados': dados})


@login_required
def imprime_informacoes_gerais(request):
    contatos = request.GET.get('contatos')
    info = []
    tecnicos = Identificacao.objects.filter(area__contains='Tec')
    asns = ASN.objects.all()  # filter(pais='BR')
    blocos_ips = BlocoIP.objects.all()
    for e in Enlace.objects.filter(participante__entidade__entidadehistorico__ativo=True):
        entidade = e.participante.entidade
        if contatos:
            contato_tec = tecnicos.filter(endereco__entidade=entidade)
        else:
            contato_tec = None
        asn = asns.filter(entidade=entidade)
        blocos = blocos_ips.filter(designado=entidade)
        operadoras = e.segmento_set.filter(data_desativacao__isnull=True)
        info.append({'info': e, "contatos_tec": contato_tec, "asn": asn, "bloco_ip": blocos, "operadoras": operadoras})

    return render_to_pdf_weasy('rede/informacoes_gerais.pdf', {'info': info}, request=request,
                               filename='informacoes_gerais.pdf')


@login_required
def blocos_texto(request):
    return TemplateResponse(request, 'rede/blocos.txt', {'blocos': BlocoIP.objects.all()}, content_type='text/plain')


@login_required
@require_safe
def planeja_contrato(request):
    """
    Ajax utilizado na tela de filtro do relatório em #Relatório Técnico - Relatório de Planejamento por ano.

    Retorna as OSs de um dado Ano - Projeto.

    """
    ano = request.GET.get('ano')
    proj_id = request.GET.get('proj_id')

    os_ids = PlanejaAquisicaoRecurso.objects.filter(ano=ano, projeto__id=proj_id).order_by('os')\
        .values_list('os', flat=True)
    oss = [{'pk': o.id, 'valor': '%s - %s' % (o.contrato, o)} for o in OrdemDeServico.objects.filter(id__in=os_ids)]
    json = simplejson.dumps({'oss': oss})

    return HttpResponse(json, content_type="application/json")


@login_required
@permission_required('rede.rel_tec_servico_processo', raise_exception=True)
@require_safe
def planejamento2(request, pdf=0):
    """
     Relatório Técnico - Relatório de Serviços contratados por processo.

    """
    entidade_id = request.GET.get('entidade')
    termo_id = request.GET.get('termo')
    if entidade_id and termo_id:
        entidade = Entidade.objects.filter(id=entidade_id)
        termo = Termo.objects.filter(id=termo_id)
    else:
        entidade = None
        termo = None

    beneficiado_id = request.GET.get('beneficiado')
    if beneficiado_id:
        beneficiado = Entidade.objects.filter(id=beneficiado_id)
    else:
        beneficiado = None
    descricoes_ids = request.GET.getlist('tiposervico')
    if entidade and termo:
        igeral = Decimal('0.0')
        tgeral = Decimal('0.0')
        if beneficiado:
            beneficiado = beneficiado[0]
        entidade = entidade[0]
        termo = termo[0]
        pagamentos = []
        pgs = Pagamento.objects.filter(recurso__id__isnull=False, protocolo__termo=termo)\
            .order_by('protocolo__num_documento').distinct()
        if beneficiado:
            pgs = pgs.filter(recurso__planejamento__beneficiado__entidade=beneficiado)
        if descricoes_ids:
            pgs = pgs.filter(recurso__planejamento__tipo__id__in=descricoes_ids)
        pgs = pgs.select_related('protocolo')

        for p in pgs:
            imposto = Decimal('0.0')
            total = Decimal('0.0')
            recursos = []
            rcs = p.recurso_set.filter(planejamento__os__contrato__entidade=entidade)
            if beneficiado:
                rcs = rcs.filter(planejamento__beneficiado__entidade=beneficiado)
            if descricoes_ids:
                rcs = rcs.filter(planejamento__tipo__id__in=descricoes_ids)
            rcs = rcs.select_related('planejamento', 'planejamento__os', 'planejamento__os__contrato',
                                     'planejamento__os__tipo', 'planejamento__tipo')

            for r in rcs:
                if beneficiado:
                    b = r.planejamento.beneficiado_set.get(entidade=beneficiado)
                imposto += Decimal(str(r.quantidade))*r.valor_imposto_mensal*Decimal(str(b.porcentagem()/100)) \
                    if beneficiado else Decimal(str(r.quantidade))*r.valor_imposto_mensal
                total += Decimal(str(r.quantidade))*r.valor_mensal_sem_imposto*Decimal(str(b.porcentagem()/100)) \
                    if beneficiado else Decimal(str(r.quantidade))*r.valor_mensal_sem_imposto
                unitario_sem = r.valor_mensal_sem_imposto*Decimal(str(b.porcentagem()/100)) \
                    if beneficiado else r.valor_mensal_sem_imposto
                unitario_com = r.valor_imposto_mensal*Decimal(str(b.porcentagem()/100))\
                    if beneficiado else r.valor_imposto_mensal
                sub_sem = Decimal(str(r.quantidade)) * unitario_sem
                sub_com = Decimal(str(r.quantidade)) * unitario_com
                recursos.append({'os': r.planejamento.os, 'quantidade': r.quantidade, 'sem': unitario_sem,
                                 'com': unitario_com, 'sub_sem': sub_sem, 'sub_com': sub_com,
                                 'tipo': r.planejamento.tipo, 'referente': r.planejamento.referente,
                                 'beneficiados': None if beneficiado else r.planejamento.beneficiado_set.all()
                                                      .select_related('entidade').order_by('quantidade')})
            pagamentos.append({'nf': p.protocolo.num_documento, 'sem': total, 'com': imposto, 'recursos': recursos})
            igeral += imposto
            tgeral += total
        if pdf:
            return render_to_pdf_weasy('rede/planejamento2.pdf',
                                       {'beneficiado': beneficiado, 'entidade': entidade, 'termo': termo,
                                        'pagamentos': pagamentos, 'sem': tgeral, 'com': igeral},
                                       request=request, filename="servicos_contratados_por_processo.pdf")
        else:
            return TemplateResponse(request, 'rede/planejamento2.html',
                                    {'beneficiado': beneficiado, 'entidade': entidade, 'termo': termo,
                                     'pagamentos': pagamentos, 'sem': tgeral, 'com': igeral,
                                     'servicos': descricoes_ids})
    else:
        return TemplateResponse(request, 'rede/escolhe_entidade_termo.html',
                                {'entidades': Entidade.objects.filter(contrato__ordemdeservico__planejaaquisicaorecurso__id__isnull=False).distinct(),
                                 'termos': Termo.objects.all(), 'beneficiados': Entidade.objects.all(),
                                 'descricoes': TipoServico.objects.order_by('nome')})


@login_required
@permission_required('rede.rel_tec_blocosip', raise_exception=True)
@require_safe
def blocosip(request, tipo=None):
    return _blocos_ip_superbloco(request, tipo)


@login_required
@permission_required('rede.rel_tec_blocosip_ansp', raise_exception=True)
@require_safe
def blocosip_ansp(request, tipo=None):
    return _blocos_ip_superbloco(request, 'ansp')


def _blocos_ip_superbloco(request, tipo=None):
    """
     Relatório Técnico - Relatório de Lista de blocos IP.
    """
    # Template
    #
    # tipo: transito
    #     Adiciona o filtro de flag transito=True para as QuerySets
    # tipo: ansp
    #     Adiciona o filtro de superbloco com propriedade da ANSP para as QuerySets
    #
    if tipo == 'ansp':
        template = 'rede/blocosip_ansp.html'
    else:
        template = 'rede/blocosip.html'

    # Filtros selecionados
    anunciante = request.GET.get('anunciante')
    proprietario = request.GET.get('proprietario')
    usuario = request.GET.get('usuario')
    designado = request.GET.get('designado')

    # Filtro - lista de dados
    if tipo == 'ansp' or tipo == 'inst_ansp':
        ent_asn_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP").values_list('asn', flat=True)\
            .distinct()
        ent_proprietario_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('proprietario', flat=True).distinct()
        ent_usuario_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('usuario', flat=True).distinct()
        ent_designado_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('designado', flat=True).distinct()
    else:
        ent_asn_ids = BlocoIP.objects.values_list('asn', flat=True).distinct()
        ent_proprietario_ids = BlocoIP.objects.values_list('proprietario', flat=True).distinct()
        ent_usuario_ids = BlocoIP.objects.values_list('usuario', flat=True).distinct()
        ent_designado_ids = BlocoIP.objects.values_list('designado', flat=True).distinct()

    filtro_asns = ASN.objects.filter(id__in=ent_asn_ids)
    filtro_proprietario = ASN.objects.filter(id__in=ent_proprietario_ids)
    filtro_usuarios = Entidade.objects.filter(id__in=ent_usuario_ids)
    filtro_designados = Entidade.objects.filter(id__in=ent_designado_ids)

    if len(request.GET) < 1:
        return TemplateResponse(request, template,
                                {'tipo': tipo, 'filtro_asns': filtro_asns, 'filtro_proprietario': filtro_proprietario,
                                 'filtro_usuarios': filtro_usuarios, 'filtro_designados': filtro_designados})
    else:
        # Buscando blocos filhos que são restritos pelos filtros
        blocos_filhos = BlocoIP.objects.all().filter(superbloco__isnull=False)
        if anunciante and anunciante != '0':
            blocos_filhos = blocos_filhos.filter(asn__id=anunciante)
        if proprietario and proprietario != '0':
            blocos_filhos = blocos_filhos.filter(proprietario__id=proprietario)
        if usuario and usuario != '0':
            blocos_filhos = blocos_filhos.filter(usuario__id=usuario)
        if designado and designado != '0':
            blocos_filhos = blocos_filhos.filter(designado__id=designado)

        # Buscando os superblocos dos filhos encontrados acima
        blocos_com_filhos_filtrados = BlocoIP.objects.all()\
            .filter(id__in=blocos_filhos.values_list('superbloco__id', flat=True))
#         if tipo == 'transito':
#             blocos_com_filhos_filtrados = blocos_com_filhos_filtrados.filter(transito=True)

        # Buscando superblocos restritos pelos filtros
        blocos_filtrados = BlocoIP.objects.filter(superbloco__isnull=True)
        if tipo == 'ansp':
            blocos_filtrados = blocos_filtrados.filter(proprietario__entidade__sigla="ANSP")
        if anunciante and anunciante != '0':
            blocos_filtrados = blocos_filtrados.filter(asn__id=anunciante)
        if proprietario and proprietario != '0':
            blocos_filtrados = blocos_filtrados.filter(proprietario__id=proprietario)
        if usuario and usuario != '0':
            blocos_filtrados = blocos_filtrados.filter(usuario__id=usuario)
        if designado and designado != '0':
            blocos_filtrados = blocos_filtrados.filter(designado__id=designado)

        # combinando as duas listas
        # Obs: Fazendo o exclude no Union, para poder reaproveitar a queryset na geração do XLS,
        # que não deve incluir o 'bloco_com_filhos_filtrados'
        blocos = blocos_com_filhos_filtrados | blocos_filtrados.exclude(id__in=blocos_com_filhos_filtrados)
        if request.GET.get('porusuario'):
            blocos = blocos.order_by('usuario__sigla')
        else:
            blocos = blocos.order_by('ip', 'mask')

        # Gerando o contexto para o template
        blocos_contexto = []
        for b in blocos:
            subnivel = []
            for sb in blocos_filhos.filter(superbloco=b):
                subnivel.append({'id': sb.id, 'obj': sb, 'netmask': sb.netmask, 'enabled': True})

            # O atributo 'enabled' serve para esconder os superblocos que não
            # atendem ao filtro. Isso ocorre quando são encontrados itens somente nos filhos.
            enabled = False
            if (anunciante == '0' or (b.asn and str(b.asn.id) == anunciante)) and \
                    (proprietario == '0' or (b.proprietario and str(b.proprietario.id) == proprietario)) and \
                    (usuario == '0' or (b.usuario and str(b.usuario.id) == usuario)) and \
                    (designado == '0' or (b.designado and str(b.designado.id) == designado)):
                enabled = True

            blocos_contexto.append({'id': b.id, 'obj': b, 'subnivel': subnivel, 'netmask': b.netmask,
                                    'enabled': enabled})

        if request.GET.get('xls') and request.GET.get('xls') == '1':
            # Export para Excel/XLS
            # Obs: Não deve incluir o 'bloco_com_filhos_filtrados' pois
            # ele incluir os blocos pais mas que não satisfazem os filtros
            queryset = (blocos_filhos | blocos_filtrados)

            if tipo == 'ansp':
                queryset = queryset.filter(proprietario__entidade__sigla="ANSP")

            queryset = queryset.order_by('ip', 'mask')
            dataset = BlocosIP_Rel_Lista_BlocoIP_Resource().export(queryset=queryset)

            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')

            today = date.today()
            if tipo:
                response['Content-Disposition'] = "attachment; filename=blocosip_%s_%d_%02d_%02d.xls" %\
                                                  (tipo, today.year, today.month, today.day)
            else:
                response['Content-Disposition'] = "attachment; filename=blocosip_%d_%02d_%02d.xls" % \
                                                  (today.year, today.month, today.day)

            return response

        elif request.GET.get('porusuario'):
            return TemplateResponse(request, 'rede/blocosip.html.notree', {'blocos': blocos_contexto})

        return TemplateResponse(request, template,
                                {'tipo': tipo, 'blocos': blocos_contexto, 'filtro_asns': filtro_asns,
                                 'filtro_proprietario': filtro_proprietario, 'filtro_usuarios': filtro_usuarios,
                                 'filtro_designados': filtro_designados})


@login_required
@permission_required('rede.rel_tec_blocosip_transito', raise_exception=True)
@require_safe
def blocosip_transito(request):
    return _blocos_ip_continuo(request, 'rede/blocosip_transito.html', 'transito')


@login_required
@permission_required('rede.rel_tec_blocosip_inst_transito', raise_exception=True)
@require_safe
def blocosip_inst_transito(request):
    return _blocos_ip_continuo(request, 'rede/blocosip_inst_transito.html', 'inst_transito')


@login_required
@permission_required('rede.rel_tec_blocosip_inst_ansp', raise_exception=True)
@require_safe
def blocosip_inst_ansp(request):
    return _blocos_ip_continuo(request, 'rede/blocosip_inst_ansp.html', 'inst_ansp')


def _blocos_ip_continuo(request, template, tipo=None):
    """
     Relatório Técnico - Relatório de Lista de blocos IP
     É feito uma seleção dos blocos continuamente, sem fazer a relação hierárquica de
     superblocos.
    """
    # Template
    #
    # tipo: transito
    #     Adiciona o filtro de flag transito=True para as QuerySets
    # tipo: ansp
    #     Adiciona o filtro de superbloco com propriedade da ANSP para as QuerySets
    #

    # Filtros selecionados
    anunciante = request.GET.get('anunciante')
    proprietario = request.GET.get('proprietario')
    usuario = request.GET.get('usuario')
    designado = request.GET.get('designado')

    # Filtro - lista de dados
    if tipo == 'transito' or tipo == 'inst_transito':
        ent_asn_ids = BlocoIP.objects.filter(transito=True).values_list('asn', flat=True).distinct()
        ent_proprietario_ids = BlocoIP.objects.filter(transito=True).values_list('proprietario', flat=True).distinct()
        ent_usuario_ids = BlocoIP.objects.filter(transito=True).values_list('usuario', flat=True).distinct()
        ent_designado_ids = BlocoIP.objects.filter(transito=True).values_list('designado', flat=True).distinct()
    elif tipo == 'ansp' or tipo == 'inst_ansp':
        ent_asn_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP").\
            values_list('asn', flat=True).distinct()
        ent_proprietario_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('proprietario', flat=True).distinct()
        ent_usuario_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('usuario', flat=True).distinct()
        ent_designado_ids = BlocoIP.objects.filter(proprietario__entidade__sigla="ANSP")\
            .values_list('designado', flat=True).distinct()

    filtro_asns = ASN.objects.filter(id__in=ent_asn_ids)
    filtro_proprietario = ASN.objects.filter(id__in=ent_proprietario_ids)
    filtro_usuarios = Entidade.objects.filter(id__in=ent_usuario_ids)
    filtro_designados = Entidade.objects.filter(id__in=ent_designado_ids)

    if len(request.GET) < 1:
        return TemplateResponse(request, template,
                                {'tipo': tipo, 'filtro_asns': filtro_asns, 'filtro_proprietario': filtro_proprietario,
                                 'filtro_usuarios': filtro_usuarios, 'filtro_designados': filtro_designados})
    else:
        # Buscando blocos filhos que são restritos pelos filtros
        blocos = BlocoIP.objects.all()
        if tipo == 'inst_transito' or tipo == 'transito':
            blocos = blocos.filter(transito=True)
        if tipo == 'inst_ansp' or tipo == 'ansp':
            blocos = blocos.filter(proprietario__entidade__sigla="ANSP")
        if anunciante and anunciante != '0':
            blocos = blocos.filter(asn__id=anunciante)
        if proprietario and proprietario != '0':
            blocos = blocos.filter(proprietario__id=proprietario)
        if usuario and usuario != '0':
            blocos = blocos.filter(usuario__id=usuario)
        if designado and designado != '0':
            blocos = blocos.filter(designado__id=designado)

        # ordenando os blocos
        if tipo == 'inst_ansp' or tipo == 'ansp':
            blocos = blocos.order_by('usuario__sigla')
        elif tipo == 'inst_transito':
            blocos = blocos.order_by('proprietario__entidade__sigla')
        else:  # tipo =='transito'
            blocos = blocos.order_by('ip', 'mask')

        # Gerando o contexto para o template
        blocos_contexto = []
        for b in blocos:
            blocos_contexto.append({'id': b.id, 'obj': b, 'netmask': b.netmask})

        if request.GET.get('xls') and request.GET.get('xls') == '1':
            # Export para Excel/XLS
            dataset = BlocosIP_Rel_Lista_Inst_BlocoIP_Resource().export(queryset=blocos)

            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')

            today = date.today()
            response['Content-Disposition'] = "attachment; filename=blocosip_%s_%d_%02d_%02d.xls" % \
                                              (tipo, today.year, today.month, today.day)

            return response

        return TemplateResponse(request, template,
                                {'tipo': tipo, 'blocos': blocos_contexto, 'filtro_asns': filtro_asns,
                                 'filtro_proprietario': filtro_proprietario, 'filtro_usuarios': filtro_usuarios,
                                 'filtro_designados': filtro_designados})


@login_required
@permission_required('rede.rel_ger_custo_terremark', raise_exception=True)
@require_safe
def custo_terremark(request, pdf=0, xls=0):
    """
     Relatório Gerencial - Relatório de Custo dos recursos contratados.

     OBS:
     O relatório filtra implicitamente pela entidade Terremark.

    """
    # Variável indicando o datacenter. Ex: 1 == terremark
    datacenter_id = Variavel.objects.get(nome=Variavel.DATACENTER_IDS)

    # Filtrando por Entidade
    recursos = Recurso.objects.filter(planejamento__os__contrato__entidade_id=datacenter_id.valor) \
                              .order_by('planejamento__projeto__nome', 'planejamento__tipo__nome',
                                        'planejamento__referente', 'planejamento__os__numero',
                                        '-ano_referencia', '-mes_referencia')
    # Otimizando o queryset do relatorio
    recursos = recursos.select_related('planejamento', 'planejamento__projeto', 'planejamento__tipo',
                                       'planejamento__unidade', 'planejamento__os', 'planejamento__os__contrato',
                                       'planejamento__os__tipo', 'pagamento', 'pagamento__protocolo',
                                       'pagamento__protocolo__termo')

    estado_selected = 0
    estado = request.GET.get('estado')
    # Filtro do estado da OS
    if estado and estado > '0':
        estado_selected = int(request.GET.get('estado'))
        recursos = recursos.filter(planejamento__os__estado__id=estado_selected)

    if request.GET.get('acao') and request.GET.get('acao') == '2':
        # Export para Excel/XLS
        dataset = CustoTerremarkRecursoResource().export(queryset=recursos)

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=custo_terremark.xls"

        return response

    elif pdf or (request.GET.get('acao') and request.GET.get('acao') == '1'):
        # Export para PDF
        return render_to_pdf_weasy(template_src='rede/tabela_terremark.pdf',
                                   context_dict={'recursos': recursos, 'estado_selected': estado_selected},
                                   request=request, filename='custos_dos_recursos_contratados.pdf')

    return TemplateResponse(request, 'rede/tabela_terremark.html',
                            {'recursos': recursos, 'filtro_estados': EstadoOS.objects.all(),
                             'estado_selected': estado_selected, 'estado': estado})


@login_required
@permission_required('rede.rel_tec_recursos_operacional', raise_exception=True)
@require_safe
def relatorio_recursos_operacional(request, pdf=0, xls=0):
    """
    Relatório Técnico - Relatório de recursos.

    Relatório operacional para visualização dos recursos.
    """

    # Variável indicando o datacenter. Ex: 1 == terremark
    datacenter_id = Variavel.objects.get(nome=Variavel.DATACENTER_IDS)

    # Filtrando por Entidade
    planejamentos = PlanejaAquisicaoRecurso.objects.filter(os__contrato__entidade_id=datacenter_id.valor)\
        .prefetch_related('beneficiado_set').select_related('os', 'os__estado', 'os__contrato', 'projeto', 'tipo')\
        .order_by('projeto__nome', 'tipo__nome', 'os__numero')

    estado_selected = 0

    # Filtro selecionado do estado da OS
    estado = request.GET.get('estado')
    if estado and estado > '0':
        estado_selected = int(request.GET.get('estado'))
        planejamentos = planejamentos.filter(os__estado__id=estado_selected)

    # Dados para montar o filtro dos estados
    filtro_estados = EstadoOS.objects.all()

    # Filtro selecionado do beneficiado
    beneficiado_selected = 0
    beneficiado = request.GET.get('beneficiado')
    if beneficiado and beneficiado > '0':
        beneficiado_selected = int(request.GET.get('beneficiado'))

    # Restringindo a lista de dados do filtro de beneficiados de acordo com o
    # filtro de Estado da OS selecionado
    if estado and estado > '0':
        filtro_beneficiados = Beneficiado.objects.filter(planejamento__os__estado__id=estado_selected)\
            .distinct('entidade__nome').order_by('entidade__nome').select_related('entidade')
    else:
        filtro_beneficiados = Beneficiado.objects.all().distinct('entidade__nome').order_by('entidade__nome')\
            .select_related('entidade')

    # Montando os dados de contexto
    context_dict = []
    for p in planejamentos:
        ctx_beneficiados = []

        # Filtra os beneficiados, se for informado o parametro no REQUEST
        beneficiados = []
        if beneficiado_selected != 0:
            beneficiados = p.beneficiado_set.filter(entidade_id=beneficiado_selected)
        else:
            beneficiados = p.beneficiado_set.all()

        beneficiados = beneficiados.select_related('entidade', 'estado')

        for b in beneficiados:
            beneficiado = {'id': b.id, 'entidade': b.entidade.nome, 'quantidade': b.quantidade, 'estado': b.estado}
            ctx_beneficiados.append(beneficiado)

        if beneficiado_selected == 0 or len(ctx_beneficiados) > 0:
            ctx_planejamento = {'id': p.id, 'beneficiados': ctx_beneficiados, 'contrato': p.os.contrato, 'os': p.os,
                                'classificacao': p.projeto, 'descricao': p.tipo, 'referente': p.referente,
                                'entidade': '', 'quantidade': p.quantidade, }
            context_dict.append(ctx_planejamento)

    if request.GET.get('acao') and request.GET.get('acao') == '2':
        # Export para Excel/XLS
        beneficiados = Beneficiado.objects.all()

        if beneficiado_selected != 0:
            beneficiados = Beneficiado.objects.filter(entidade_id=beneficiado_selected)

        if estado and estado > '0':
            beneficiados = beneficiados.filter(planejamento__os__estado__id=estado_selected)

        beneficiados = beneficiados.order_by('planejamento__projeto__nome', 'planejamento__tipo__nome',
                                             'planejamento__os__numero')

        dataset = RecursoOperacionalResource().export(queryset=beneficiados)

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = "attachment; filename=recursos_tecnicos.xls"

        return response

    elif request.GET.get('acao') and request.GET.get('acao') == '1':
        # Export para PDF
        return render_to_pdf_weasy(template_src='rede/recurso_operacional.pdf',
                                   context_dict={'planejamentos': context_dict}, request=request,
                                   filename='recursos_tecnicos.pdf')

    return TemplateResponse(request, 'rede/recurso_operacional.html',
                            {'planejamentos': context_dict, 'filtro_estados': filtro_estados, 'estado': estado,
                             'estado_selected': estado_selected, 'filtro_beneficiados': filtro_beneficiados,
                             'beneficiado_selected': beneficiado_selected, 'beneficiado': beneficiado})


@login_required
@permission_required('rede.rel_tec_crossconnection', raise_exception=True)
@require_safe
def crossconnection(request):
    """
     Relatório Técnico - Relatório de Cross Connection.
    """
    template = 'rede/crossconnection.html'
    # Filtros selecionados
    rack = request.GET.get('rack')
    shelf = request.GET.get('shelf')
    conector = request.GET.get('conector')
    projeto = request.GET.get('projeto')

    filtro_rack = IFCConector.objects.order_by().values_list('rack', flat=True).distinct()
    filtro_shelf = IFCConector.objects.order_by().values_list('shelf', flat=True).distinct()
    filtro_conector = IFCConector.objects.order_by().values_list('tipoConector__sigla', flat=True).distinct()
    filtro_projeto = CrossConnection.objects.order_by().values_list('ordemDeServico', flat=True).distinct()

    if len(request.GET) < 1:
        return TemplateResponse(request, template,
                                {'filtro_rack': filtro_rack, 'filtro_shelf': filtro_shelf,
                                 'filtro_conector': filtro_conector, 'filtro_projeto': filtro_projeto})
    else:
        cross = CrossConnection.objects.all().order_by('origem__rack', 'origem__shelf', 'origem__porta',
                                                       'destino__rack', 'destino__shelf', 'destino__porta')

        # Filtrando o resultado
        if rack and rack != '0':
            cross = cross.filter(Q(origem__rack=rack) | Q(destino__rack=rack))
        if shelf and shelf != '0':
            cross = cross.filter(Q(origem__shelf=shelf) | Q(destino__shelf=shelf))
        if conector and conector != '0':
            cross = cross.filter(Q(origem__tipoConector__sigla=conector) | Q(destino__tipoConector__sigla=conector))
        if projeto and projeto != '0':
            cross = cross.filter(ordemDeServico=projeto)

        if request.GET.get('xls') and request.GET.get('xls') == '1':
            # Export para Excel/XLS
            queryset = cross
            dataset = CrossConnectionResource().export(queryset=queryset)

            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel;charset=utf-8')

            today = date.today()
            response['Content-Disposition'] = "attachment; filename=cross_connection_%d_%02d_%02d.xls" % \
                                              (today.year, today.month, today.day)

            return response

        return TemplateResponse(request, template,
                                {'cross': cross, 'filtro_rack': filtro_rack, 'filtro_shelf': filtro_shelf,
                                 'filtro_conector': filtro_conector, 'filtro_projeto': filtro_projeto})
