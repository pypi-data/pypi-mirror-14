# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from utils.functions import clone_objects
from import_export.admin import ExportMixin

from identificacao.models import Entidade
from rede.models import Segmento, Beneficiado, TipoConector, Operadora,\
    EnlaceOperadora, Banda, IPBorda, Enlace, TipoServico, Projeto, Unidade, RIR,\
    Canal, Interface, Uso, Sistema, Estado, CrossConnectionHistorico, BlocoIP,\
    IFCConector, CrossConnection, Recurso, PlanejaAquisicaoRecurso
from rede.modelsResource import BlocosIPResource, CrossConnectionResource
from rede.forms import BlocoIPAdminForm, RecursoAdminForm,\
    PlanejaAquisicaoRecursoAdminForm, IFCConectorAdminForm,\
    CrossConnectionAdminForm


class DesignadoFilter(SimpleListFilter):
    title = u'designado'
    parameter_name = 'designado'

    def lookups(self, request, model_admin):
        entidade_ids = BlocoIP.objects.values_list('designado', flat=True).distinct().order_by()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        result_id = self.value()
        if result_id:
            return queryset.filter(designado__id__exact=result_id)
        else:
            return queryset


class UsuarioFilter(SimpleListFilter):
    title = u'usado por'
    parameter_name = 'usado'

    def lookups(self, request, model_admin):
        entidade_ids = BlocoIP.objects.values_list('usuario', flat=True).distinct().order_by()
        return [(e.id, e.sigla) for e in Entidade.objects.filter(id__in=entidade_ids)]

    def queryset(self, request, queryset):
        result_id = self.value()
        if result_id:
            return queryset.filter(usuario__id__exact=result_id)
        else:
            return queryset


class SuperblocoFilter(SimpleListFilter):
    title = 'tipo de bloco'
    parameter_name = 'bloco'

    def lookups(self, request, model_admin):
        return [('super', 'Apenas super blocos')]

    def queryset(self, request, queryset):
        if self.value() == 'super':
            return queryset.filter(superbloco__isnull=True)
        return queryset


class BlocoIPAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = BlocosIPResource
    form = BlocoIPAdminForm

    fieldsets = (
        (None, {
            'fields': (('ip', 'mask', 'net_mask', 'transito'), ('asn', 'proprietario'), ('designado', 'usuario'),
                       ('superbloco', 'rir'), 'obs'),
            'classes': ('wide',)
            }
         ),
    )

    list_display = ('cidr', 'asn_anunciante_numero', 'asn_anunciante_sigla',
                    'asn_proprietario_numero', 'asn_proprietario_sigla', 'usu', 'desig', 'rir', 'transito')
    search_fields = ('ip', 'asn__numero', 'asn__entidade__sigla', 'proprietario__numero',
                     'proprietario__entidade__sigla', 'usuario__sigla', 'designado__sigla', 'obs')
    list_filter = (SuperblocoFilter, 'asn', 'proprietario', DesignadoFilter, UsuarioFilter)
    ordering = ['ip', 'asn__entidade__sigla', 'proprietario']
    admin_order_field = ['ip', 'asn__entidade__sigla', 'proprietario__entidade__sigla', 'usuario', 'designado', 'rir',
                         'transito']

    def get_export_queryset(self, request):
        """
        Gera o queryset utilizado na geração da exportação para Excell
        """
        queryset = super(BlocoIPAdmin, self).get_export_queryset(request)
        return queryset.select_related('cidr', 'asn', 'proprietario', 'usu', 'desig', 'rir', 'transito', 'obs')

    def asn_anunciante_numero(self, obj):
        if obj.asn:
            return "%d" % obj.asn.numero
        return '-'
    asn_anunciante_numero.short_description = 'ASN Anunciante'
    asn_anunciante_numero.admin_order_field = 'asn__numero'

    def asn_anunciante_sigla(self, obj):
        if obj.asn and obj.asn.entidade:
            return "%s" % obj.asn.entidade.sigla
        return '-'
    asn_anunciante_sigla.short_description = 'Anunciante'
    asn_anunciante_sigla.admin_order_field = 'asn__entidade__sigla'

    def asn_proprietario_numero(self, obj):
        if obj.proprietario:
            return "%d" % obj.proprietario.numero
        return '-'
    asn_proprietario_numero.short_description = 'ASN Proprietário'
    asn_proprietario_numero.admin_order_field = 'proprietario__numero'

    def asn_proprietario_sigla(self, obj):
        if obj.proprietario and obj.proprietario.entidade:
            return "%s" % obj.proprietario.entidade.sigla
        return '-'
    asn_proprietario_sigla.short_description = 'Proprietário'
    asn_proprietario_sigla.admin_order_field = 'proprietario__entidade__sigla'


class SegmentoInline(admin.StackedInline):
    fieldsets = (
        (None, {
            'fields': (('operadora', 'banda', 'link_redundante'),
                       ('data_ativacao', 'data_desativacao', 'uso', 'sistema', 'canal'),
                       ('designacao', 'interfaces'), 'obs'),
            'classes': ('wide',)
            }
         ),
        )
    model = Segmento
    extra = 1


class EnlaceAdmin(admin.ModelAdmin):
    search_fields = ('participante__entidade__sigla',)

    inlines = [SegmentoInline]
    # list_display = ('participante_display', 'entrada_display', 'banda', 'operadora')


class RecursoAdmin(admin.ModelAdmin):
    form = RecursoAdminForm

    fieldsets = (
        (None, {
            'fields': ('planejamento', ('termo', 'pagamento'), 'obs',
                       ('quantidade', 'mes_referencia', 'ano_referencia'),
                       ('valor_imposto_mensal', 'valor_mensal_sem_imposto'),),
            'classes': ('wide',)
        }),
    )


class BeneficiadoInline(admin.TabularInline):
    model = Beneficiado
    extra = 2


class PlanejaAquisicaoRecursoAdmin(admin.ModelAdmin):

    form = PlanejaAquisicaoRecursoAdminForm
    fieldsets = (
        (None, {
            'fields': (('os', 'ano'), ('tipo', 'referente'), ('quantidade', 'valor_unitario'),
                       ('projeto', 'unidade', 'instalacao'), 'banda', 'obs'),
            'classes': ('wide',)
        }),
    )
    list_display = ('projeto', 'quantidade', 'tipo', 'os', 'referente', 'valor_unitario', 'instalacao')
    actions = ['action_clone']
    search_fields = ('os__numero', 'referente', 'tipo__nome')
    inlines = [BeneficiadoInline]

    def action_clone(self, request, queryset):
        for obj in queryset:
            bs = obj.beneficiado_set.all()
            obj.pk = None
            obj.save()

            for b in bs:
                b.pk = None
                b.planejamento = obj
                b.save()
    action_clone.short_description = u'Clonar Planejamentos selecionados'


class TipoServicoAdmin(admin.ModelAdmin):

    actions = ['action_clone']

    def action_clone(self, request, queryset):
        clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = _(u'1 tipo de serviço copiado')
        else:
            message = _(u'%s tipos de serviço copiados') % total
        self.message_user(request, message)

    action_clone.short_description = _(u"Copiar os tipos de serviço selecionados")


class TipoConectorAdmin(admin.ModelAdmin):
    list_display = ('sigla', )
    search_fields = ('sigla',)
    ordering = ['sigla']


class TipoConectorFilter(SimpleListFilter):
    title = u'Tipo de conector'
    parameter_name = 'tipoConector'

    def lookups(self, request, model_admin):
        tipoConector_ids = IFCConector.objects.values_list('tipoConector', flat=True).distinct().order_by()
        return [(e.id, e.sigla) for e in TipoConector.objects.filter(id__in=tipoConector_ids)]

    def queryset(self, request, queryset):
        result_id = self.value()
        if result_id:
            return queryset.filter(tipoConector__id__exact=result_id)
        else:
            return queryset


class IFCConectorAdmin(ExportMixin, admin.ModelAdmin):
    form = IFCConectorAdminForm

    fieldsets = (
        (None, {
            'fields': (('rack', 'shelf', 'porta'), 'tipoConector', 'ativo', 'obs', ),
            'classes': ('wide',)
        }),
    )

    list_display = ('rack', 'shelf', 'porta', 'tipoConector', 'ativo')
    search_fields = ('rack', 'porta', 'tipoConector__sigla')
    list_filter = ('rack', TipoConectorFilter)


class OrigemRackFilter(SimpleListFilter):
    title = u'Rack Origem'
    parameter_name = 'origem'

    def lookups(self, request, model_admin):
        racks = CrossConnection.objects.values_list('origem__rack', flat=True).distinct().order_by()
        return [(e, e) for e in IFCConector.objects.filter(rack__in=racks).values_list('rack', flat=True)
                .distinct().order_by()]

    def queryset(self, request, queryset):
        rack = self.value()
        if rack:
            return queryset.filter(origem__rack__exact=rack)
        else:
            return queryset


class DestinoRackFilter(SimpleListFilter):
    title = u'Rack Destino'
    parameter_name = 'destino'

    def lookups(self, request, model_admin):
        racks = CrossConnection.objects.values_list('destino__rack', flat=True).distinct().order_by()
        return [(e, e) for e in IFCConector.objects.filter(rack__in=racks).values_list('rack', flat=True)
                .distinct().order_by()]

    def queryset(self, request, queryset):
        rack = self.value()
        if rack:
            return queryset.filter(destino__rack__exact=rack)
        else:
            return queryset


class CrossConnectionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CrossConnectionResource
    form = CrossConnectionAdminForm

    fieldsets = (
        ('IFC', {
            'fields': ('origem', 'destino'),
            'classes': ('wide',)
        }),
        ('Descrição', {
            'fields': ('circuito', 'ordemDeServico', 'obs', 'ativo')
        }),
    )

    list_display = ('origem__rack', 'origem__shelf', 'origem__porta', 'origem__tipoConector', 'destino__rack',
                    'destino__shelf', 'destino__porta', 'destino__tipoConector', 'ordemDeServico', 'circuito', )
    search_fields = ('origem__rack', 'destino__rack', 'circuito', 'ordemDeServico',)
    ordering = ['origem__rack', 'origem__shelf', 'origem__porta', 'destino__rack', 'destino__shelf', 'destino__porta']
    admin_order_field = ['origem__rack', 'destino__rack']
    list_filter = (OrigemRackFilter, DestinoRackFilter, 'ordemDeServico')

    def get_export_queryset(self, request):
        """
        Gera o queryset utilizado na geração da exportação para Excell
        """
        queryset = super(CrossConnectionAdmin, self).get_export_queryset(request)
        return queryset

    def origem__rack(self, obj):
        if obj.origem:
            return "%s" % obj.origem.rack
        return '-'
    origem__rack.short_description = 'Rack 1'
    origem__rack.admin_order_field = 'origem__rack'

    def origem__shelf(self, obj):
        if obj.origem:
            return "%s" % obj.origem.shelf
        return '-'
    origem__shelf.short_description = 'Shelf'
    origem__shelf.admin_order_field = 'origem__shelf'

    def origem__porta(self, obj):
        if obj.origem:
            return "%s" % obj.origem.porta
        return '-'
    origem__porta.short_description = 'Porta'
    origem__porta.admin_order_field = 'origem__porta'

    def origem__tipoConector(self, obj):
        if obj.origem:
            return "%s" % obj.origem.tipoConector
        return '-'
    origem__tipoConector.short_description = 'Conector'
    origem__tipoConector.admin_order_field = 'origem__tipoConector'

    def destino__rack(self, obj):
        if obj.destino:
            return "%s" % obj.destino.rack
        return '-'
    destino__rack.short_description = 'Rack 2'
    destino__rack.admin_order_field = 'destino__rack'

    def destino__shelf(self, obj):
        if obj.destino:
            return "%s" % obj.destino.shelf
        return '-'
    destino__shelf.short_description = 'Shelf'
    destino__shelf.admin_order_field = 'destino__shelf'

    def destino__porta(self, obj):
        if obj.destino:
            return "%s" % obj.destino.porta
        return '-'
    destino__porta.short_description = 'Porta'
    destino__porta.admin_order_field = 'destino__porta'

    def destino__tipoConector(self, obj):
        if obj.destino:
            return "%s" % obj.destino.tipoConector
        return '-'
    destino__tipoConector.short_description = 'Conector'
    destino__tipoConector.admin_order_field = 'destino__tipoConector'


admin.site.register(BlocoIP, BlocoIPAdmin)
admin.site.register(Operadora)
admin.site.register(EnlaceOperadora)
admin.site.register(Banda)
admin.site.register(IPBorda)
admin.site.register(Enlace, EnlaceAdmin)

admin.site.register(TipoServico, TipoServicoAdmin)
admin.site.register(Projeto)
admin.site.register(Unidade)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(PlanejaAquisicaoRecurso, PlanejaAquisicaoRecursoAdmin)
admin.site.register(RIR)

admin.site.register(Segmento)
admin.site.register(Canal)
admin.site.register(Interface)
admin.site.register(Uso)
admin.site.register(Sistema)
admin.site.register(Estado)

admin.site.register(TipoConector, TipoConectorAdmin)
admin.site.register(IFCConector, IFCConectorAdmin)
admin.site.register(CrossConnection, CrossConnectionAdmin)
admin.site.register(CrossConnectionHistorico)
