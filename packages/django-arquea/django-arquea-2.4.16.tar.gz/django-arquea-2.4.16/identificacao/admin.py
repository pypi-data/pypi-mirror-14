# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from identificacao.models import EntidadeHistorico, ArquivoEntidade, Agendado,\
    ASN, TipoDetalhe, TipoEntidade, Agenda, TipoArquivoEntidade, NivelAcesso,\
    Ecossistema, Identificacao, EnderecoDetalhe, Endereco, Contato, Entidade,\
    Acesso
from identificacao.forms import EnderecoDetalheInlineAdminForm,\
    EnderecoAdminForm, ContatoAdminForm, EnderecoDetalheAdminForm,\
    AcessoAdminForm


class IdentificacaoInline(admin.TabularInline):
    model = Identificacao
    extra = 1


class EntidadeHistoricoInline(admin.TabularInline):
    model = EntidadeHistorico
    extra = 3


class ArquivoEntidadeInline(admin.TabularInline):
    model = ArquivoEntidade
    extra = 1


class AgendadoInline(admin.TabularInline):
    model = Agendado
    extra = 1


class EnderecoDetalheInline(admin.TabularInline):
    model = EnderecoDetalhe
    extra = 1
    form = EnderecoDetalheInlineAdminForm


class ASNInline(admin.TabularInline):
    model = ASN
    extra = 1


class EnderecoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'sigla' da entidade, 'nome' do contato  e
                         'rua', 'bairro', 'cidade', 'estado', e 'pais' do endereço.
    """
    fieldsets = (
        (None, {
            'fields': ('entidade',),
            'classes': ('wide',)
        }),
        (None, {
            'fields': (('rua', 'num'), ('compl', 'cep'), ('bairro', 'cidade'), ('estado', 'pais'), 'data_inatividade'),
            'classes': ('wide',)
        }),
    )

    list_display = ('__unicode__', 'cep', 'bairro', 'cidade', 'estado', 'pais')
    search_fields = ['entidade__nome', 'entidade__sigla', 'identificacao__contato__primeiro_nome',
                     'identificacao__contato__ultimo_nome', 'rua', 'bairro', 'cidade', 'estado', 'pais']
    inlines = [EnderecoDetalheInline]

admin.site.register(Endereco, EnderecoAdmin)


class EnderecoInline(admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': (('entidade', ), ('rua', 'num', 'compl'), ('cep', 'bairro', 'cidade'), ('estado', 'pais')),
        }),
    )

    form = EnderecoAdminForm
    model = Endereco
    extra = 1


class ContatoAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'email'.
    """
    fieldsets = (
        (None, {
            'fields': (('primeiro_nome', 'ultimo_nome', 'ativo'), ('email', 'tel', 'documento')),
            'classes': ('wide',)
        }),
    )

    list_display = ('nome', 'contato_ent', 'email', 'tel', 'ativo')
    search_fields = ['primeiro_nome', 'ultimo_nome', 'email']
    form = ContatoAdminForm

admin.site.register(Contato, ContatoAdmin)


class EntidadeAdmin(admin.ModelAdmin):
    """
    Permite consulta por 'sigla' e 'nome'.
    """
    fieldsets = (
        (None, {
            'fields': (('entidade', 'sigla', 'nome'), ),
            'classes': ('wide',)
        }),
        (None, {
            'fields': ('url', ('cnpj', 'fisco'), ('recebe_doacao',)),
            'classes': ('wide',)
        }),
    )

    list_display = ('sigla_nome', 'sigla_completa', 'url', 'cnpj', 'fisco', 'recebe_doacao')
    list_filter = ('fisco', )
    inlines = [ArquivoEntidadeInline, ASNInline, EntidadeHistoricoInline, AgendadoInline]
    search_fields = ['sigla', 'nome']

admin.site.register(Entidade, EntidadeAdmin)


class IdentificacaoAdmin(admin.ModelAdmin):
    """
    Permite consulta por 'nome' e 'sigla' da entidade e
                         'nome', 'funcao' e 'area' do contato.
    """
    fieldsets = (
        (None, {
            'fields': (('endereco', 'contato', 'ativo'), ),
            'classes': ('wide',)
        }),
        (None, {
            'fields': ('funcao', 'area'),
            'classes': ('wide',)
        }),
    )

    list_display = ('__unicode__', 'funcao', 'area', 'formata_historico')
    search_fields = ['endereco__entidade__nome', 'endereco__entidade__sigla', 'contato__primeiro_nome',
                     'contato__ultimo_nome', 'funcao', 'area']

admin.site.register(Identificacao, IdentificacaoAdmin)


class EnderecoDetalheEntidadeFilter(SimpleListFilter):
    title = 'Entidade'
    parameter_name = 'endereco__entidade__sigla'

    def lookups(self, request, model_admin):
        entidade_ids = EnderecoDetalhe.objects.values_list('endereco__entidade_id', flat=True).distinct().order_by()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        entidade_id = self.value()
        if entidade_id:
            return queryset.filter(endereco__entidade__id__exact=entidade_id) | \
                   queryset.filter(detalhe__endereco__entidade__id__exact=entidade_id)
        else:
            return queryset


class EnderecoDetalheAdmin(admin.ModelAdmin):
    form = EnderecoDetalheAdminForm

    fieldsets = (
        (None, {
            'fields': ('entidade', ('endereco', 'detalhe'), 'tipo', 'complemento'),
            'classes': ('wide',)
        }),
    )

    search_fields = ['endereco__entidade__sigla', 'endereco__rua', 'detalhe__endereco__entidade__sigla']
    list_filter = (EnderecoDetalheEntidadeFilter, 'tipo')


class ASNAdmin(admin.ModelAdmin):

    list_display = ('numero', 'entidade', 'pais')
    search_fields = ('entidade__sigla', 'numero')


class AcessoAdmin(admin.ModelAdmin):
    form = AcessoAdminForm

    list_display = ('get_entidade', 'get_area', 'get_contato', 'lista_niveis')
    ordering = ('identificacao__endereco__entidade__sigla', 'identificacao__area', 'identificacao__contato__primeiro_nome')

    def get_entidade(self, obj):
        return obj.identificacao.endereco.entidade.sigla
    get_entidade.admin_order_field = 'identificacao__endereco__entidade__sigla'
    get_entidade.short_description = 'Entidade'

    def get_area(self, obj):
        return obj.identificacao.area
    get_area.admin_order_field = 'identificacao__area'
    get_area.short_description = 'Area'

    def get_contato(self, obj):
        return obj.identificacao.contato.nome
    get_contato.admin_order_field = 'identificacao__contato__nome'
    get_contato.short_description = 'Contato'

    def get_queryset(self, request):
        # Sobrescrevendo o get_queryset para poder fazer a otimização com select_related
        return super(AcessoAdmin, self).get_queryset(request) \
            .prefetch_related('niveis') \
            .select_related('identificacao__endereco__entidade', 'identificacao__contato')


admin.site.register(EnderecoDetalhe, EnderecoDetalheAdmin)
admin.site.register(TipoDetalhe)
admin.site.register(TipoEntidade)
admin.site.register(Agenda)
admin.site.register(TipoArquivoEntidade)
admin.site.register(Acesso, AcessoAdmin)
admin.site.register(NivelAcesso)
admin.site.register(ASN, ASNAdmin)
admin.site.register(Ecossistema)
