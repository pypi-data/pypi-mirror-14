# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from django.contrib import admin
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.utils import unquote
from django.template.response import TemplateResponse
from rede.models import PlanejaAquisicaoRecurso
from outorga.models import OrdemDeServico, Outorga, Modalidade, Estado, Categoria, Arquivo, ArquivoOS, TipoContrato, \
    EstadoOS, TemplateRT, Natureza_gasto, Item, OrigemFapesp, Acordo, Termo,\
    Contrato
from outorga.forms import ItemAdminForm, OrigemFapespInlineForm, AcordoAdminForm,\
    EstadoAdminForm, CategoriaAdminForm, ModalidadeAdminForm, TermoAdminForm,\
    OutorgaAdminForm, Natureza_gastoAdminForm, ArquivoAdminForm,\
    ContratoAdminForm, OrdemDeServicoAdminForm, OrigemFapespAdminForm


class Natureza_gastoInline(admin.TabularInline):
    model = Natureza_gasto
    extra = 6


class PlanejamentoInline(admin.StackedInline):
    model = PlanejaAquisicaoRecurso
    extra = 2
    fieldsets = (
        (None, {
            'fields': (('os', 'ano'), ('tipo', 'referente'), ('quantidade', 'valor_unitario'),
                       ('projeto', 'unidade', 'instalacao'), 'obs'),
            'classes': ('wide',)
        }),
    )


class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 2
    verbose_name = ''
    verbose_name_plural = 'Arquivos'


class ArquivoOSInline(admin.TabularInline):
    model = ArquivoOS
    extra = 2
    verbose_name = ''
    verbose_name_plural = 'Arquivos'


class ItemInline(admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': ('natureza_gasto', ('descricao', 'entidade', 'quantidade'), 'valor'),
        }),
        (_(u'Justificativa/Observação'), {
            'fields': ('justificativa', 'obs',),
            'classes': ('collapse',)
        }),
    )

    model = Item
    form = ItemAdminForm
    extra = 3
    verbose_name = ''
    verbose_name_plural = 'Itens'


class OutorgaInline(admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': (('data_solicitacao', 'termino', 'data_presta_contas', 'categoria'), ('arquivo', 'protocolo')),
        }),
        ('Observação', {
            'fields': ('obs', ),
            'classes': ('collapse', ),
        }),
    )

    model = Outorga
    extra = 1
    ordering = ('-data_solicitacao',)


class OrigemFapespInline(admin.TabularInline):
    model = OrigemFapesp
    extra = 2
    ordering = ('item_outorga__natureza_gasto__termo', 'item_outorga__descricao')
    form = OrigemFapespInlineForm


class OrigemFapespInlineA(OrigemFapespInline):
    fields = ('termo', 'item_outorga')
    readonly_fields = ('termo',)


class OrdemDeServicoInline(admin.StackedInline):

    fieldsets = (
        (None, {
            'fields': (('acordo', 'estado'), ('tipo', 'numero'), ('data_inicio', 'data_rescisao', 'antes_rescisao'))
        }),
        (_(u'Descrição'), {
            'fields': ('descricao', ),
            'classes': ('collapse', ),
        }),
    )

    model = OrdemDeServico
    extra = 0
    verbose_name = ''
    verbose_name_plural = u'Alteração de contratos'


class AcordoAdmin(admin.ModelAdmin):
    """
    Permite busca por	'nome' do Estado, 'descrição' do Acordo.
    """
    list_display = ('descricao', 'estado', )
    search_fields = ('descricao', 'estado__nome', )
    list_per_page = 10
    inlines = [OrigemFapespInline]
    form = AcordoAdminForm

admin.site.register(Acordo, AcordoAdmin)


class EstadoAdmin(admin.ModelAdmin):
    """
    Permite consulta por:	'nome' do Estado.
    """
    fieldsets = (
        (None, {
            'fields': ('nome', ),
        }),
    )

    list_display = ('nome', )
    search_fields = ('nome', )
    list_per_page = 10
    form = EstadoAdminForm

admin.site.register(Estado, EstadoAdmin)


class CategoriaAdmin(admin.ModelAdmin):
    """
    Permite consulta por:	'nome' da Categoria.
    """
    fieldsets = (
        (None, {
            'fields': ('nome', ),
        }),
    )

    list_display = ('nome', )
    search_fields = ('nome', )
    list_per_page = 10
    form = CategoriaAdminForm

admin.site.register(Categoria, CategoriaAdmin)


class ModalidadeAdmin(admin.ModelAdmin):
    """
    Permite consulta por:	'sigla' e 'nome' da Modalidade.
    """

    fieldsets = (
        (None, {
            'fields': (('sigla', 'nome', 'moeda_nacional'), ),
        }),
    )

    list_display = ('sigla', 'nome', 'moeda_nacional')
    list_display_links = ('sigla', 'nome', )
    list_per_page = 10
    search_fields = ('sigla', 'nome')
    form = ModalidadeAdminForm

admin.site.register(Modalidade, ModalidadeAdmin)


class TermoAdmin(admin.ModelAdmin):
    """
    Permite consulta por:	'ano' e 'processo' do Termo, 'nome' do Outorgado, 'data_concessao' do Termo.
    """
    fieldsets = (
        (None, {
            'fields': (('ano', 'processo', 'digito', 'inicio', 'estado'), 'parecer', 'parecer_final', 'projeto',
                       'orcamento', 'extrato_financeiro', 'quitacao', 'doacao', 'relatorio_final',
                       'exibe_rel_ger_progressivo', 'rt'),
        }),
    )

    list_display = ('__unicode__', 'inicio', 'duracao_meses', 'termo_real', 'formata_realizado_real',
                    'formata_saldo_real', 'termo_dolar', 'formata_realizado_dolar', 'formata_saldo_dolar', 'estado')
    list_filter = (('estado', admin.RelatedOnlyFieldListFilter),)
    list_per_page = 20
    search_fields = ('ano', 'processo', 'inicio')
    inlines = (OutorgaInline, Natureza_gastoInline)
    form = TermoAdminForm

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change and form.cleaned_data['rt']:
            obj.insere_itens_rt()

admin.site.register(Termo, TermoAdmin)


class OutorgaAdmin(admin.ModelAdmin):
    """
    O método 'save_model'	Verifica se oo estado atual é diferente do estado anterior.
    O método 'response_change'	Encaminha o usuário para a tela de edição do termo se o estado for
    definido como 'Aprovado'.

    Filtra os dados por 'termo' e 'estado'.

    Permite consulta pelos campos: 	'nome' da Categoria, 'ano', 'processo' e 'data_concessao' do Termo.
    """
    fieldsets = (
        (None, {
            'fields': (('data_solicitacao', 'termino', 'termo', 'data_presta_contas', 'categoria', 'arquivo'), ),
        }),
        ('Observação', {
            'fields': ('obs', ),
            'classes': ('collapse', ),
        }),
    )

    list_display = ('data_solicitacao', 'inicio', 'termino', 'mostra_termo', 'data_presta_contas',
                    'mostra_categoria', 'arquivo')
    list_display_links = ('mostra_categoria', )
    list_filter = ('termo', )
    list_per_page = 10
    search_fields = ('termo__ano', 'termo__processo', 'categoria__nome', 'data_presta_contas', 'data_solicitacao',
                     'termino')
    form = OutorgaAdminForm

admin.site.register(Outorga, OutorgaAdmin)


class Natureza_gastoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo pedido e pela modalidade.

    Permite consulta pelos campos:	'sigla' e 'nome' da Modalidade, 'categoria' do Pedido de Concessão,
    'ano' e 'processo' do Termo.
    """
    fieldsets = (
        (None, {
            'fields': (('termo', 'modalidade'), 'valor_concedido'),
        }),
        (_(u'Observação'), {
            'fields': ('obs', ),
            'classes': ('collapse',)
        }),
    )

    list_display = ('termo', 'mostra_modalidade', 'v_concedido', 'formata_total_realizado', 'saldo')
    list_display_links = ('termo', 'mostra_modalidade', )
    list_filter = ('termo', 'modalidade')
    list_per_page = 10
    search_fields = ('modalidade__sigla', 'modalidade__nome',  'termo__ano', 'termo__processo')
    form = Natureza_gastoAdminForm

admin.site.register(Natureza_gasto, Natureza_gastoAdmin)


class ItemAdmin(admin.ModelAdmin):
    """
    Filtra os dados por estado e pela natureza do gasto.

    Permite consulta pelos campos: 	'sigla' e 'nome' da Modalidade, 'nome' da Categoria do Pedido de Concessão,
    'ano' e 'processo' do Termo, 'estado', 'descricao' e 'justificativa' do Item do Pedido de Concessão.
    """
    fieldsets = (
        (None, {
            'fields': (('termo', 'natureza_gasto'), ('descricao', 'entidade', 'quantidade'), 'valor'),
        }),
        (_(u'Justificativa/Observação'), {
            'fields': ('justificativa', 'obs',),
        }),
    )

    list_display = ('mostra_termo', 'mostra_modalidade', 'mostra_descricao', 'entidade', 'rt', 'mostra_quantidade',
                    'mostra_valor_realizado', 'pagamentos_pagina')
    list_filter = ('natureza_gasto__termo', 'natureza_gasto__modalidade', ('entidade', admin.RelatedOnlyFieldListFilter),)
    list_per_page = 20
    search_fields = ('natureza_gasto__modalidade__sigla', 'natureza_gasto__modalidade__nome', 'obs',
                     'natureza_gasto__termo__ano', 'natureza_gasto__termo__processo', 'descricao', 'justificativa')
    inlines = [OrigemFapespInline]
    list_display_links = ('mostra_termo', 'mostra_descricao', )
    form = ItemAdminForm

admin.site.register(Item, ItemAdmin)


class ArquivoAdmin(admin.ModelAdmin):
    """
    Filtra os dados pelo id do protocolo.
    Busca arquivo por: 	'ano' e 'processo' do Termo, 'nome' da Categoria e 'arquivo'
    """
    fieldsets = (
        (None, {
            'fields': ('outorga', 'arquivo')
        }),
    )

    list_display = ('mostra_termo', 'concessao', '__unicode__')
    list_display_links = ('__unicode__', )
    list_per_page = 10
    search_fields = ('outorga__termo__ano', 'outorga__termo__processo', 'outorga__categoria__nome', 'arquivo')
    form = ArquivoAdminForm

admin.site.register(Arquivo, ArquivoAdmin)


class ContratoAdmin(admin.ModelAdmin):
    """
    """
    fieldsets = (
        (_(u'Contrato'), {
            'fields': ('anterior', 'numero', ('data_inicio', 'limite_rescisao', 'entidade', 'auto_renova', 'arquivo'))
        }),
    )

    list_display = ('numero', 'data_inicio', 'limite_rescisao', 'entidade', 'auto_renova', 'existe_arquivo')
    list_display_links = ('entidade', )
    list_filter = (('entidade', admin.RelatedOnlyFieldListFilter),)
    list_per_page = 20
    search_fields = ('entidade__sigla', 'entidade__nome', 'data_inicio')
    inlines = (OrdemDeServicoInline, )
    form = ContratoAdminForm

admin.site.register(Contrato, ContratoAdmin)


class OrdemDeServicoListEntidadeFilter(admin.SimpleListFilter):
    """
    Tela de Ordem de servico > Filtro de Entidades.
    Filtro somente por ordem de serviços que possuem a entidade filtrada.
    """
    title = _('entidade')
    parameter_name = 'entidade'

    def lookups(self, request, model_admin):
        entidades = set([c.contrato.entidade
                         for c in model_admin.model.objects.select_related('contrato__entidade').all()])
        return [(c.id, c.sigla) for c in entidades]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contrato__entidade__id__exact=self.value())
        else:
            return queryset


class OrdemDeServicoAdmin(admin.ModelAdmin):
    """
    """
    fieldsets = (
        (None, {
            'fields': ('acordo', 'tipo')
        }),
        (_(u'Ordem de Serviço'), {
            'fields': (('numero', 'estado'), ('data_inicio', 'data_rescisao', 'contrato', 'antes_rescisao'),
                       'descricao', 'pergunta')
        }),
    )

    list_display = ('numero', 'tipo', 'entidade', 'data_inicio', 'data_rescisao', 'mostra_prazo', 'estado', 'descricao')
    list_display_links = ('descricao', )
    list_filter = (OrdemDeServicoListEntidadeFilter,  ('estado', admin.RelatedOnlyFieldListFilter), )
    list_per_page = 20
    inlines = (ArquivoOSInline, PlanejamentoInline)
    search_fields = ('numero', 'acordo__descricao', 'contrato__entidade__sigla', 'contrato__entidade__nome',
                     'descricao', 'data_inicio', 'data_rescisao', 'tipo__nome')
    filter_horizontal = ('pergunta',)
    form = OrdemDeServicoAdminForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            obj = self.get_object(request, unquote(object_id))
            if obj.estado.id != int(request.POST.get('estado')) and request.POST.get('confirma') is None:
                if request.POST.get('nconfirma'):
                    return HttpResponseRedirect(urlresolvers.reverse('admin:outorga_ordemdeservico_change',
                                                                     args=(object_id,)))
                return TemplateResponse(request, 'admin/outorga/ordemdeservico/confirma_alteracao.html',
                                        {'form_url': form_url})

        return super(OrdemDeServicoAdmin, self).change_view(request, object_id, form_url, extra_context)
admin.site.register(OrdemDeServico, OrdemDeServicoAdmin)


class OrigemFapespAdmin(admin.ModelAdmin):
    list_per_page = 10
    form = OrigemFapespAdminForm
admin.site.register(OrigemFapesp, OrigemFapespAdmin)

# admin.site.register(ArquivoOS)
admin.site.register(TipoContrato)
admin.site.register(EstadoOS)
admin.site.register(TemplateRT)
