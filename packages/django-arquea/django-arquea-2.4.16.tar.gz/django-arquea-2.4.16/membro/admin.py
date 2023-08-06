# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from membro.forms import MembroAdminForm, ControleFeriasAdminForm,\
    ControleFeriasAdminFormSet, DispensaLegalAdminForms, ControleAdminForms
from membro.models import Historico, Ferias, Membro, Assinatura, ControleFerias,\
    DispensaLegal, Controle, SindicatoArquivo, TipoAssinatura, Cargo,\
    TipoDispensa, DadoBancario


class HistoricoInline(admin.TabularInline):
    model = Historico
    extra = 1


class FeriasInline(admin.TabularInline):
    model = Ferias
    extra = 1
    fields = ('inicio', 'inicio_ferias', 'fim_ferias', 'realizado', 'link_edit')
    readonly_fields = ('inicio_ferias', 'fim_ferias', 'link_edit')


class DadoBancarioInline(admin.TabularInline):
    """
    Permite consulta por 'nome' do contato,
                         'banco', 'agencia' e 'cc' do modelo DadoBancario.
    """

    fieldsets = (
                 (None, {
                     'fields': ('membro', ),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('banco', ('agencia', 'ag_digito', 'conta', 'cc_digito')),
                     'classes': ('wide',)
                 }),
    )
    # list_display = ('membro', 'banco', 'agencia_digito', 'conta_digito')
    # search_fields = ['membro__nome', 'banco', 'agencia', 'cc']

    extra = 1
    model = DadoBancario


class SindicatoArquivosInline(admin.TabularInline):
    """
    Modelo SindicatoArquivos relacionado ao Membro.
    """
    fieldsets = (
                 (None, {
                     'fields': ('ano', 'arquivo',),
                     'classes': ('wide',)
                 }),
    )

    extra = 1
    model = SindicatoArquivo


class MembroAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome', 'rg', 'cpf', 'cargo' e 'email' do membro.
    """

    fieldsets = (
                 (None, {
                     'fields': ('nome', ('email', 'ramal'), ('foto', 'site'), 'contato'),
                     'classes': ('wide',)
                 }),
                 (None, {
                     'fields': ('data_nascimento', ('rg', 'cpf'), 'url_lattes'),
                     'classes': ('wide',)
                 }),
                 ('Observação', {
                     'fields': ('obs', ),
                     'classes': ('collapse',)
                 }),
    )

    list_display = ('nome', 'cargo_atual', 'email', 'existe_ramal', 'existe_curriculo')

    list_display_links = ('nome', )

    form = MembroAdminForm
    inlines = [HistoricoInline, DadoBancarioInline, FeriasInline, SindicatoArquivosInline]

    list_per_page = 10

    search_fields = ['nome', 'rg', 'cpf', 'email']

admin.site.register(Membro, MembroAdmin)


class AssinaturaAdmin(admin.ModelAdmin):
    """
    Permite consulta por 'tipo' de assinatura e,
                         'nome' e 'cargo' do membro.
    """

    fieldsets = (
                 (None, {
                     'fields': (('membro', 'tipo_assinatura'), ),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'tipo_assinatura')

    list_per_page = 10

    search_fields = ['tipo_assinatura__nome', 'membro__nome']

admin.site.register(Assinatura, AssinaturaAdmin)


class ControleFeriasInline(admin.TabularInline):
    model = ControleFerias
    form = ControleFeriasAdminForm
    formset = ControleFeriasAdminFormSet
    extra = 0


class FeriasAdmin(admin.ModelAdmin):
    """
    Permite consulta por 'nome' e 'cargo' do membro,
                         'inicio' e 'termino' de férias.
    """

    fieldsets = (
                 (None, {
                     'fields': ('membro', ),
                     'classes': ('wide',)
                 }),
                 ('Período de Trabalho', {
                     'fields': (('inicio', 'realizado')),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'inicio', 'completo', 'realizado')
    # form = FeriasAdminForm
    inlines = [ControleFeriasInline, ]
    list_per_page = 10

    search_fields = ['membro__nome']   # , 'membro__cargo']

admin.site.register(Ferias, FeriasAdmin)


class DispensaLegalAdmin(admin.ModelAdmin):

    fieldsets = (
                 (None, {
                     'fields': (('membro', 'tipo'), ('inicio_direito', 'dias_corridos', 'horas', 'minutos'), ('dias_uteis',), 'justificativa')
                 }),
                 (None, {
                     'fields': (('inicio_realizada', 'realizada'), ('atestado', 'arquivo'))
                 }),
    )
    list_display = ('membro', 'tipo', 'inicio_direito', 'realizada')
    list_filter = (('membro', admin.RelatedOnlyFieldListFilter),)
    ordering = ('-inicio_direito', 'membro__nome')
    form = DispensaLegalAdminForms

admin.site.register(DispensaLegal, DispensaLegalAdmin)


class ControleMembroListFilter(admin.SimpleListFilter):
    """
    Tela de Controle > Filtro de Membros
    Filtro somente por membros que têm lançamento de controle de horas.
    """
    title = _('membro')
    parameter_name = 'membro'

    def lookups(self, request, model_admin):
        # Filtro de Membros que lançaram horas em controle de horas.
        # Agrupado pelo nome do membro
        membros = model_admin.model.objects.all() \
                        .values('membro__id', 'membro__nome') \
                        .distinct('membro__id', 'membro__nome') \
                        .order_by('membro__nome')
        return [(c['membro__id'], c['membro__nome']) for c in membros]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(membro__id__exact=self.value())
        else:
            return queryset


class ControleAdmin(admin.ModelAdmin):
    list_filter = (ControleMembroListFilter, )
    form = ControleAdminForms

    list_display = ('membro', 'format_entrada', 'format_saida', )
    list_per_page = 20
    ordering = ('-entrada', 'membro__nome')
    search_fields = ['membro__nome']

    def format_entrada(self, obj):
        if obj.entrada:
            if timezone.is_aware(obj.entrada):
                entrada = timezone.localtime(obj.entrada)
            else:
                entrada = obj.entrada
            return entrada.strftime('%d %b %Y - %H:%M')
        return '(Nenhum)'
    format_entrada.short_description = 'Entrada'

    def format_saida(self, obj):
        if obj.saida:
            if timezone.is_aware(obj.saida):
                saida = timezone.localtime(obj.saida)
            else:
                saida = obj.saida
            return saida.strftime('%d %b %Y - %H:%M')
        return '(Nenhum)'
    format_saida.short_description = 'Saída'

    def get_queryset(self, request):
        qs = super(ControleAdmin, self).get_queryset(request)
        if request.user.is_superuser is False:
            qs = qs.filter(membro__email=request.user.email)

        return qs

admin.site.register(Controle, ControleAdmin)


class SindicatoArquivosAdmin(admin.ModelAdmin):
    """
    Permite consulta por 'ano' e 'arquivo' do modelo SindicatoArquivos relacionado ao Membro.
    """
    fieldsets = (
                 (None, {
                     'fields': ('membro', 'ano', 'arquivo',),
                     'classes': ('wide',)
                 }),
    )

    list_display = ('membro', 'ano', 'arquivo', )
    list_filter = (('membro', admin.RelatedOnlyFieldListFilter),
                   ('ano'),)
    search_fields = ['membro__nome', 'ano', 'arquivo', ]
    ordering = ('-ano', 'membro__nome')
    list_per_page = 10

admin.site.register(SindicatoArquivo, SindicatoArquivosAdmin)

admin.site.register(TipoAssinatura)
admin.site.register(Cargo)
admin.site.register(TipoDispensa)
