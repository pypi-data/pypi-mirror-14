# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from utils.functions import clone_objects

from protocolo.models import TipoDocumento, Arquivo, Estado, Origem,\
    ItemProtocolo, Protocolo, Cotacao, Feriado, TipoFeriado, Descricao
from protocolo.forms import ItemAdminForm, ProtocoloAdminForm, CotacaoAdminForm,\
    FeriadoAdminForm, TipoFeriadoAdminForm, ArquivoAdminForm

admin.site.register(TipoDocumento)
admin.site.register(Estado)
admin.site.register(Origem)


class ItemInline(admin.TabularInline):
    model = ItemProtocolo
    extra = 3
    form = ItemAdminForm


class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 3
    verbose_name = ''
    verbose_name_plural = 'Arquivos'


class ProtocoloAdmin(admin.ModelAdmin):
    # Filtra os dados pelos campos: 'estado' e 'data_vencimento'

    # Permite consulta por: 	'nome' e 'sigla' da entidade,
    # 'contato', 'descrição', 'número do documento', 'tipo' e 'estado' do protocolo.

    # Cria o campo 'muda_estado' para informar se o estado anterior é diferente do estado atual.

    # O método 'save_model' Verifica se o estado do protocolo foi definido como 'Encaminha cotação',
    # quando isso ocorrer, será enviado um e-mail para o responsável.
    # Atualiza o campo 'muda_estado' informando se houve mudança no campo 'estado'.

    # O método 'response_change' 	Encaminha o usuário para a tela de cadastramento após a alteração do protocolo
    # com estado
    # classificado como 'Encaminha despesa'.

    # O método 'response_add' 	Encaminha o usuário para a tela de cadastramento após a adição de um novo protocolo
    # com estado  classificado como 'Encaminha despesa'.

    fieldsets = (
        (None, {
            'fields': (('data_chegada', 'origem'), 'valor_total'),
            'classes': ('wide',)
        }),
        ('Obs', {
            'fields': ('obs',),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('estado', 'termo'),
            'classes': ('wide',)
        }),
        (None, {
            'fields': ('descricao2', ('tipo_documento', 'num_documento', 'moeda_estrangeira')),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('referente', 'procedencia', 'data_validade', 'data_vencimento'), ),
            'classes': ('wide',)
        }),
        ('Cotação', {
            'fields': ('responsavel',),
            'classes': ('collapse',)
        }),
    )

    list_display = ('doc_num', 'descricao2', 'referente', 'vencimento', 'chegada', 'mostra_valor', 'existe_arquivo',
                    'colorir', 'cotacoes')
    list_display_links = ('doc_num', )
    related_search_fields = {'identificacao': ('entidade__sigla', )}
    list_filter = ('termo', 'estado', 'data_vencimento',
                   'pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade')
    # list_editable = ('estado',)
    actions = ['action_clone']
    inlines = [ArquivoInline]
    list_per_page = 10
    form = ProtocoloAdminForm
    search_fields = ['descricao2__entidade__sigla', 'descricao2__entidade__nome', 'descricao2__descricao',
                     'num_documento', 'referente']
    muda_estado = 0

    # Não está aceitando o lookup mesmo definido em list_filter, então está colocado aqui.
    # Rever assim que possível
    def lookup_allowed(self, lookup, value):
	if lookup == 'pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__id__exact':
	    return True
	return super(ProtocoloAdmin, self).lookup_allowed(lookup,value)
	
    def action_clone(self, request, queryset):
        clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = _(u'1 protocolo copiado')
        else:
            message = _(u'%s protocolos copiados') % total
        self.message_user(request, message)
    action_clone.short_description = _(u"Copiar os protocolos selecionados")

    # Quando o estado do protocolo for definido como 'Encaminha cotação' será enviado um e-mail para o responsável.
    def save_model(self, request, obj, form, change):
        try:
            antigo = Protocolo.objects.get(pk=obj.pk)
            estado_anterior = antigo.estado
        except Protocolo.DoesNotExist:
            estado_anterior = None

        obj.save()
        if obj.estado != estado_anterior:
            self.muda_estado = 1

        if obj.estado != estado_anterior and obj.estado.nome == u'Encaminha cotação':
            u = obj.responsavel
            if u and u.email:
                mails = [u.email]
                url = request.build_absolute_uri(urlresolvers.reverse('cotacoes'), args=(obj.pk,))
                send_mail('Novo pedido requer cotações',
                          'O pedido %s requer que sejam feitas cotações.\r\nEntre em %s.' % (obj.descricao, url),
                          'Sistema administrativo <sistema@ansp.br>', mails, fail_silently=True)

    # salvar os itens criando patrimonio automaticamente
    #    def save_formset(self, request, form, formset, change):
    #   if change:
    #       formset.save()
    #   else:
    #       for form in formset.forms:
    #       obj = form.save()
    #       e1, created = EstadoPatrimonio.objects.get_or_create(nome='Ativo')
    #       if form.cleaned_data.has_key('marca') and form.cleaned_data['marca']:
    #           Equipamento.objects.create(marca=form.cleaned_data['marca'],
    #                modelo=form.cleaned_data['modelo'],
    #                ns=form.cleaned_data['ns'],
    #                estado=e1,
    #                itemprotocolo=obj)

    # Encaminha o usuário para a tela de cadastramento da Fonte Pagadora quando uma despesa é alterada.
    def response_change(self, request, obj):
        if self.muda_estado:
            self.muda_estado = 0
            if obj.estado.nome == u'Autorizada':
                super(ProtocoloAdmin, self).response_change(request, obj)
                e, created = Estado.objects.get_or_create(nome=u'Solicitar Liberação')  # @UnusedVariable
                url = '/admin/financeiro/fontepagadora/add/?protocolo=%s&valor=%s&estado=%s' % (obj.id, obj.valor, e.id)
                return HttpResponseRedirect(url)

        return super(ProtocoloAdmin, self).response_change(request, obj)

    # Encaminha o usuário para a tela de cadastramento da Fonte Pagadora quando uma despesa é adicionada.
    def response_add(self, request, obj, post_url_continue=None):
        if self.muda_estado:
            self.muda_estado = 0
            if obj.estado.nome == u'Autorizada':
                super(ProtocoloAdmin, self).response_add(request, obj)
                e, created = Estado.objects.get_or_create(nome=u'Solicitar Liberação')  # @UnusedVariable
                url = '/admin/financeiro/fontepagadora/add/?protocolo=%s&valor=%s&estado=%s' % (obj.id, obj.valor, e.id)
                return HttpResponseRedirect(url)

        return super(ProtocoloAdmin, self).response_add(request, obj)

    # # Encaminha o usuário para a tela de cadastramento de despesa após alteração do protocolo.
    # def response_change(self, request, obj):
    #     if self.muda_estado:
    #         self.muda_estado = 0
    #         if obj.estado.nome == u'Encaminha despesa':
    #             super(ProtocoloAdmin,self).response_change(request, obj)
    #             e, created = EstadoDespesa.objects.get_or_create(nome=u'Encaminha para Fonte Pagadora')
    #             if obj.termo is not None:
    #                 url = '/admin/financeiro/despesa/add/?protocolo=%s&valor_despesa=%s&termo=%s&estado=%s' %
    # (obj.id, obj.valor, obj.termo.id, e.id)
    #             else:
    #                 url = '/admin/financeiro/despesa/add/?protocolo=%s&valor_despesa=%s&estado=%s' %
    # (obj.id, obj.valor, e.id)
    #             return HttpResponseRedirect(url)
    #
    #     return super(ProtocoloAdmin,self).response_change(request, obj)
    #
    #
    # # Encaminha o usuário para a tela de cadastramento de despesa após a inclusão de um protocolo.
    # def response_add(self, request, obj, post_url_continue='../%s/'):
    #     if self.muda_estado:
    #         self.muda_estado = 0
    #         if obj.estado.nome == u'Encaminha despesa':
    #             super(ProtocoloAdmin,self).response_add(request, obj)
    #             e, created = EstadoDespesa.objects.get_or_create(nome=u'Encaminha para Fonte Pagadora')
    #             if obj.termo is not None:
    #                 url = '/admin/financeiro/despesa/add/?protocolo=%s&valor_despesa=%s&termo=%s&estado=%s' %
    # (obj.id, obj.valor, obj.termo.id, e.id)
    #             else:
    #                 url = '/admin/financeiro/despesa/add/?protocolo=%s&valor_despesa=%s&estado=%s' %
    # (obj.id, obj.valor, e.id)
    #             return HttpResponseRedirect(url)
    #
    #     return super(ProtocoloAdmin,self).response_change(request, obj)

admin.site.register(Protocolo, ProtocoloAdmin)


class CotacaoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelos campos: 'estado' e 'data_vencimento'

    Permite consulta por: 'nome' e 'sigla' da entidade, 'descrição', 'nome do responsável', 'entrega' e 'estado'

    A função 'save_model' define o tipo do protocolo como 'Cotação' e quando o estado for definido como
    'Encaminha cotação' será enviado um e-mail para todos os componentes do grupo 'adm' informando a cotação vencedora.
    """

    fieldsets = (
        (None, {
            'fields': ('estado', 'termo'),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('entidade', 'identificacao'), 'descricao2', ('moeda_estrangeira', 'data_validade')),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('data_chegada', 'origem', 'valor_total'), 'obs'),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('aceito', 'entrega'), 'protocolo'),
            'classes': ('wide',)
        }),
        ('Parecer Técnico', {
            'fields': ('parecer',),
            'classes': ('collapse',)
        }),
    )
    inlines = [ArquivoInline, ]
    list_display = ('mostra_termo', '__unicode__', 'validade', 'mostra_valor', 'aceito', 'existe_entrega',
                    'existe_arquivo', 'mostra_estado')
    list_display_links = ('__unicode__', )
    list_filter = ('estado', 'data_vencimento')
    list_per_page = 10
    form = CotacaoAdminForm
    search_fields = ('identificacao__endereco__entidade__nome',
                     'identificacao__endereco__entidade__sigla',
                     'descricao', 'estado__nome', 'responsavel__username', 'entrega')

    # Define o tipo do protocolo como 'Cotação' e envia um e-mail para o grupo 'adm' se o estado for 'Primeira opção'.
    def save_model(self, request, obj, form, change):
        if not change:
            tp, created = TipoDocumento.objects.get_or_create(nome=u'Cotação')  # @UnusedVariable
            obj.tipo_documento = tp
        try:
            antigo = Cotacao.objects.get(pk=obj.pk)
            estado_anterior = antigo.estado
        except Cotacao.DoesNotExist:
            estado_anterior = None

        obj.save()

        if obj.estado != estado_anterior and obj.estado.nome == u'Primeira opção':
            g = Group.objects.get(name='adm')
            if g is not None:
                mails = []
                url = request.build_absolute_uri('/admin/protocolo/cotacao/%s' % obj.pk)
                for u in g.user_set.all():
                    if u.email:
                        mails.append(u.email)

                send_mail('Cotação escolhida', 'Foi escolhida uma cotação vencedora para o pedido %s\r\nEntre em %s.' %
                          (obj.protocolo.descricao2, url),
                          'Sistema administrativo <sistema@ansp.br>', mails, fail_silently=True)

    # Redireciona o usuário para uma tela onde mostra todas as cotações de um determinado pedido após a
    # alteração da cotação.
    def response_change(self, request, obj):
        if 'return_to' in request.REQUEST:
            super(CotacaoAdmin, self).response_change(request, obj)
            return HttpResponseRedirect(request.REQUEST['return_to'])
        else:
            return super(CotacaoAdmin, self).response_change(request, obj)

    # Redireciona o usuário para uma tela onde mostra todas as cotações de um determinado pedido após a
    # inclusão da cotação.
    def response_add(self, request, obj, post_url_continue=None):
        if 'return_to' in request.REQUEST:
            super(CotacaoAdmin, self).response_add(request, obj)
            return HttpResponseRedirect(request.REQUEST['return_to'])
        else:
            return super(CotacaoAdmin, self).response_change(request, obj)

admin.site.register(Cotacao, CotacaoAdmin)


class FeriadoListFilter(admin.SimpleListFilter):
    """
    Tela de Feriados > Filtro por ano do feriado
    """
    title = _('ano do feriado')
    parameter_name = 'feriado__ano'

    def lookups(self, request, model_admin):
        feriados = list(set([c for c in model_admin.model.objects.extra(
            select={'year': 'extract( year from feriado )'}).values_list('year', flat=True)]))
        feriados.sort(reverse=True)

        return [(int(c), int(c)) for c in feriados]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(feriado__year=int(self.value()))
        else:
            return queryset


class FeriadoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo campo 'movel'.
    """
    fieldsets = (
        (None, {
            'fields': (('feriado', 'obs'), 'tipo')
        }),
    )

    list_display = ('__unicode__', 'tipo', 'obs', 'get_movel', 'get_subtrai', )
    list_filter = ['tipo', FeriadoListFilter]
    list_per_page = 10
    ordering = ('-feriado', )
    search_fields = ('obs', 'tipo__nome')
    form = FeriadoAdminForm

admin.site.register(Feriado, FeriadoAdmin)


class TipoFeriadoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nome', ('movel', 'subtrai_banco_hrs'), ('dia', 'mes'))
        }),
    )
    list_display = ('__unicode__', 'movel', 'subtrai_banco_hrs', 'dia', 'mes')
    form = TipoFeriadoAdminForm

admin.site.register(TipoFeriado, TipoFeriadoAdmin)


# class ContratoAdmin(admin.ModelAdmin):
#     """
#     Filtra os dados pelo campo 'termo'
#
#     Permite consulta por 'nome' e 'sigla' da entidade, 'nome' do contato, 'descrição', 'categoria', 'estado', 'tipo',
#                         'os' e 'obs'
#
#     A função 'save_model' define o estado como 'Pendente'.
#     """
#
#     fieldsets = (
#                 (None, {
#
#                     'fields': ('termo', ),
#                     'classes': ('wide',)
#                 }),
#                 (None, {
#                     'fields': (('entidade', 'identificacao'), ('tipo_documento', 'os', 'auto_renova'),
# ('descricao', 'categoria', 'moeda_estrangeira')),
#                     'classes': ('wide',)
#                 }),
#                 (None, {
#                     'fields': (('data_inicio', 'data_vencimento'), ('limite_recisao', 'periodo_renova')),
#                     'classes': ('wide',)
#                 }),
#                 (None, {
#                     'fields': (('data_chegada', 'origem'), 'obs'),
#                     'classes': ('wide',)
#                 }),
#     )
#
#     inlines = [ ArquivoInline, ]
#
#     list_display = ('mostra_termo', '__unicode__', 'mostra_categoria', 'descricao', 'formata_inicio', 'vencimento',
# 'formata_recisao', 'formata_periodo', 'estado_contrato', 'existe_arquivo', 'auto_renova')
#
#     list_display_links = ('__unicode__', )
#
#     list_filter = ('termo', )
#
#     list_per_page = 10
#
#     form = ContratoAdminForm
#
#     search_fields = ('identificacao__entidade__nome', 'identificacao__entidade__sigla',
#     'identificacao__contato__nome', 'descricao', 'estado__nome', 'categoria', 'tipo_documento__nome', 'os', 'obs')
#
#
#     # Define o estado como 'Pendente'.
#     def save_model(self, request, obj, form, change):
#         if not change:
#
#             est, created = Estado.objects.get_or_create(nome=u'Pendente')
#
#             obj.estado = est
#         obj.save()
#
# admin.site.register(Contrato,ContratoAdmin)


class ArquivoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo campo 'movel'.
    """

    fieldsets = (
        (None, {
            'fields': ('protocolo', 'arquivo')
        }),
    )

#    list_display = ('protocolo', '__unicode__')
    list_display = ('mostra_termo', 'mostra_entidade', 'mostra_descricao', 'arquivo_link')

    # list_select_related pode ser somente boolean no 1.5
    if django.VERSION[0:2] >= (1, 6):
        list_select_related = ('protocolo__termo', 'protocolo', )
    else:
        list_select_related = True

    search_fields = ('protocolo__identificacao__endereco__entidade__sigla',
                     'protocolo__identificacao__endereco__entidade__nome',
                     'protocolo__descricao', 'arquivo', )

    list_per_page = 10
    form = ArquivoAdminForm

    def arquivo_link(self, obj):
        return u'<a href="/files/%s">%s</a>' % (obj.arquivo, obj)
    arquivo_link.allow_tags = True
    arquivo_link.short_description = "arquivo"

    def __init__(self, *args, **kwargs):
        super(ArquivoAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = []

admin.site.register(Arquivo, ArquivoAdmin)


class DescricaoAdmin(admin.ModelAdmin):
    list_display = ('entidade', 'descricao')
    search_fields = ('entidade__nome', 'entidade__sigla', 'descricao')

admin.site.register(Descricao, DescricaoAdmin)
