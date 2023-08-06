# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import django
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
import datetime
import csv

from import_export.admin import ExportMixin

from utils.admin import AdminImageWidget
from utils.functions import clone_objects
from patrimonio.models import Tipo, Distribuicao, DistribuicaoUnidade,\
    UnidadeDimensao, Direcao, TipoEquipamento, Dimensao, PlantaBaixaObjeto,\
    PlantaBaixaDataCenter, PlantaBaixaPosicao, Estado, HistoricoLocal,\
    Patrimonio, Equipamento
from patrimonio.modelsResource import PatrimonioResource
from patrimonio.forms import HistoricoLocalAdminFormSet,\
    PatrimonioHistoricoLocalAdminForm, PatrimonioAdminForm,\
    HistoricoLocalAdminForm, EquipamentoAdminForm, PlantaBaixaObjetoForm,\
    PlantaBaixaDataCenterForm


admin.site.register(Estado)
admin.site.register(Tipo)
admin.site.register(Distribuicao)
admin.site.register(DistribuicaoUnidade)
admin.site.register(UnidadeDimensao)
admin.site.register(Direcao)
admin.site.register(TipoEquipamento)


class PatrimonioEstadoListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Estado')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (e.id, e.nome) for e in Estado.objects.all()
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return queryset

        s_value = int(self.value())
        q = queryset.filter(historicolocal__estado_id=s_value).distinct()

        ids = []
        for p in q.prefetch_related(Prefetch('historicolocal_set')):
            if p.historico_atual_prefetched and p.historico_atual_prefetched.estado_id == s_value:
                pass
            else:
                ids.append(p.id)

        return q.exclude(id__in=ids)


class HistoricoLocalInline(admin.StackedInline):
    fieldsets = (
        ('', {
            'fields': (('entidade',), ('endereco', 'posicao'), ('descricao', 'data', 'estado', 'memorando'))
        }),
    )

    model = HistoricoLocal
    fk_name = 'patrimonio'
    formset = HistoricoLocalAdminFormSet
    form = PatrimonioHistoricoLocalAdminForm
    choices = 1
    extra = 1


class PatrimonioAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = PatrimonioResource

    fieldsets = (
        ('Pagamento', {
            'fields': (('termo', 'npgto',), ('pagamento', 'valor',)),
            'classes': ('wide',)
        }),
        ('Geral', {
            'fields': (('agilis', 'checado',),
                       ('tipo', 'apelido', 'tem_numero_fmusp', 'numero_fmusp'),
                       ('filtro_equipamento', 'equipamento',),
                       ('marca', 'part_number', 'modelo',),
                       'ns',
                       'descricao',
                       ('complemento', 'tamanho',),
                       ('entidade_procedencia',),
                       ('nf', 'patrimonio'),)
        }),
        ('Extras', {
            'classes': ('collapse',),
            'fields': ('obs', 'titulo_autor', 'isbn', 'revision', 'version', 'garantia_termino'),
        }),
        ('Patrimônios contidos', {
            'classes': ('collapse',),
            'fields': ('form_filhos',),
        }),
    )

    readonly_fields = ('marca', 'part_number', 'modelo')
    form = PatrimonioAdminForm
    change_list_template = 'admin/patrimonio/patrimonio/change_list.html'
    list_display = ('tipo', 'descricao', 'complemento', 'posicao', 'agilis', 'modelo', 'ns', 'nf', 'valor', 'estado')
    # list_select_related pode ser somente boolean no 1.5
    if django.VERSION[0:2] >= (1, 6):
        list_select_related = ('tipo', 'equipamento', 'pagamento__protocolo__termo')
    else:
        list_select_related = True
    list_filter = (('tipo', admin.RelatedOnlyFieldListFilter), 'pagamento__protocolo__termo', PatrimonioEstadoListFilter)
    inlines = [HistoricoLocalInline]
    search_fields = ('descricao', 'ns', 'pagamento__protocolo__num_documento', 'historicolocal__descricao',
                     'equipamento__entidade_fabricante__sigla', 'equipamento__part_number', 'equipamento__modelo',
                     'historicolocal__posicao', 'apelido')
    actions = ['action_mark_agilis', 'action_unmark_agilis', 'action_mark_checado', 'action_clone']

    def __init__(self, model, admin_site, *args, **kwargs):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(PatrimonioAdmin, self).__init__(model, admin_site, *args, **kwargs)

    def get_export_queryset(self, request):
        """
        Gera o queryset utilizado na geração da exportação para Excell
        """
        queryset = super(PatrimonioAdmin, self).get_export_queryset(request)
        return queryset.select_related('tipo', 'equipamento', 'pagamento__protocolo__termo', 'entidade_procedencia',
                                       'equipamento__entidade_fabricante')

    def marca(self, instance):
        entidade_fabricante = '&nbsp;'
        if instance is not None and instance.equipamento is not None and \
                instance.equipamento.entidade_fabricante is not None:
            entidade_fabricante = instance.equipamento.entidade_fabricante.sigla
        return mark_safe("<span id='id_marca' class='input_readonly'>"+entidade_fabricante+"</span>")

    def modelo(self, instance):
        modelo = ''
        if instance is not None and instance.equipamento is not None:
            modelo = instance.equipamento.modelo

        return mark_safe("<span id='id_modelo' class='input_readonly'>"+modelo+"</span>")

    def part_number(self, instance):
        part_number = ''
        if instance is not None and instance.equipamento is not None:
            part_number = instance.equipamento.part_number

        return mark_safe("<span id='id_part_number' class='input_readonly'>"+part_number+"</span>")

    def action_clone(self, request, queryset):
        clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = u'1 patrimônio copiado'
        else:
            message = u'%s patrimônios copiados' % total
        self.message_user(request, message)

    action_clone.short_description = _(u"Duplicar os patrimônios selecionados")

    def action_mark_agilis(self, request, queryset):
        queryset.update(agilis=True)
    action_mark_agilis.short_description = _(u'Marcar para o Agilis')

    def action_unmark_agilis(self, request, queryset):
        queryset.update(agilis=False)
    action_unmark_agilis.short_description = _(u'Desmarcar para o Agilis')

    def action_mark_checado(self, request, queryset):
        queryset.update(checado=True)
    action_mark_checado.short_description = _(u'Marcar como checado')

    def get_urls(self):
        urls = super(PatrimonioAdmin, self).get_urls()

        my_urls = patterns("", url("^conserta/$", conserta_posicoes))

        return my_urls+urls

admin.site.register(Patrimonio, PatrimonioAdmin)


class HistoricoLocalAdmin(admin.ModelAdmin):

    """
    Permite consulta por 'nome' e 'sigla' da entidade,
                         'nome' do contato,
                         'funcao' e 'area' da identificacao,
                         'rua', 'complemento', 'bairro', 'cidade', 'cep', 'estado' e 'pais' do endereço,
                         'descricao' do item do protocolo,
                         'número do documento' e 'descricao' do protocolo e,
                         'descricao' e 'data' do histórico.
    """
    form = HistoricoLocalAdminForm
    fieldsets = (
        (None, {
            'fields': ('data', 'patrimonio', 'endereco', 'descricao'),
            'classes': ('wide',)
        }),
    )

    list_display = ('data', 'patrimonio', 'endereco', 'descricao')

    search_fields = ['endereco__endereco__entidade__nome', 'endereco__endereco__entidade__sigla',
                     'endereco__endereco__rua', 'endereco__endereco__compl', 'endereco__endereco__bairro',
                     'endereco__endereco__cidade', 'endereco__endereco__estado', 'endereco__endereco__cep',
                     'endereco__endereco__pais', 'descricao', 'data', 'patrimonio__pagamento__protocolo__descricao',
                     'patrimonio__pagamento__protocolo__protocolo__num_documento',
                     'patrimonio__pagamento__protocolo__protocolo__descricao']

admin.site.register(HistoricoLocal, HistoricoLocalAdmin)


class EquipamentoAdmin(admin.ModelAdmin):
    search_fields = ['part_number', 'descricao', 'modelo', 'entidade_fabricante__sigla']
    list_display = ('descricao', 'part_number', 'tipo')
    list_select_related = ('tipo',)
    list_filter = (('tipo', admin.RelatedOnlyFieldListFilter),
                   ('entidade_fabricante', admin.RelatedOnlyFieldListFilter),)

    form = EquipamentoAdminForm

    def __init__(self, model, admin_site):
        """
        Utilizado para setar o admin_site para o forms
        """
        self.form.admin_site = admin_site
        super(EquipamentoAdmin, self).__init__(model, admin_site)

    def get_urls(self):
        urls = super(EquipamentoAdmin, self).get_urls()

        my_urls = patterns("", url("^conserta/$", conserta_posicoes))
        return my_urls+urls

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Sobrescrevendo os campos de imagens para poder apresentar um preview na tela do admin
        if db_field.name == 'imagem' or db_field.name == 'imagem_traseira':
            kwargs.pop("request", None)
            kwargs['widget'] = AdminImageWidget
            return db_field.formfield(**kwargs)
        return super(EquipamentoAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(Equipamento, EquipamentoAdmin)


class DimensaoAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (('unidade', 'altura', 'largura', 'profundidade'), 'peso'),
            'classes': ('wide',)
        }),
    )

admin.site.register(Dimensao, DimensaoAdmin)


class PlantaBaixaObjetoAdmin(admin.ModelAdmin):
    form = PlantaBaixaObjetoForm
    list_display = ('data_center', 'patrimonio', 'titulo',)

admin.site.register(PlantaBaixaObjeto, PlantaBaixaObjetoAdmin)


class PlantaBaixaDataCenterAdmin(admin.ModelAdmin):
    form = PlantaBaixaDataCenterForm

admin.site.register(PlantaBaixaDataCenter, PlantaBaixaDataCenterAdmin)


class PlantaBaixaPosicaoAdmin(admin.ModelAdmin):
    form = PlantaBaixaObjetoForm
    list_display = ('objeto', 'descricao', 'x', 'y', 'w', 'h', 'cor')


admin.site.register(PlantaBaixaPosicao, PlantaBaixaPosicaoAdmin)


@staff_member_required
def conserta_posicoes(request):

    if request.method == 'GET':
        return TemplateResponse(request, 'patrimonio/conserta.html')
    ok = []
    failed = []
    if request.FILES:
        with request.FILES['racks'] as racksfile:
            rackscsv = csv.DictReader(racksfile, delimiter=';', quotechar='"')
            for row in rackscsv:
                try:
                    rack = Patrimonio.objects.get(id=row['rack_id'])
                    p = Patrimonio.objects.get(id=row['id'])
                    hl_rack = rack.historico_atual
                    if p.patrimonio == rack and p.historico_atual.posicao and\
                            p.historico_atual.posicao.endswith('%03d' % int(row['posicao'])):
                        continue
                    hl = HistoricoLocal()
                    hl.endereco = hl_rack.endereco
                    hl.estado = hl_rack.estado
                    hl.data = datetime.datetime.now()
                    hl.posicao = '%s.F%03d' % (rack.apelido.split()[-1], int(row['posicao']))
                    hl.patrimonio = p
                    p.patrimonio = rack
                    p.save()
                    hl.save()
                    ok.append('%s - %s' % (p.apelido or p.id, row['posicao']))
                except:
                    failed.append('%s - %s' % (row['id'], row['posicao']))

    return TemplateResponse(request, 'patrimonio/conserta.html', {'ok': ok, 'failed': failed})
