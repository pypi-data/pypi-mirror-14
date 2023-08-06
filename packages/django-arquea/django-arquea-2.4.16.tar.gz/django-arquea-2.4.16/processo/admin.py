# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from models import Area, Macroprocesso, Processo, Equipe, Papel, Atribuicao, Grupo, Visao, Natureza, Recurso, Norma, \
    OTRS, Procedimento
from membro.models import Membro
from utils.functions import clone_objects
from django.utils.translation import ugettext_lazy as _


class AtribuicaoInline(admin.TabularInline):
    model = Atribuicao
    extra = 2


class ProcedimentoInline(admin.TabularInline):
    model = Procedimento
    extra = 2


class EquipeAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "membros":
            membros = []
            for m in Membro.objects.all():
                if m.ativo is True:
                    membros.append(m.id)
            kwargs["queryset"] = Membro.objects.filter(id__in=membros)
        return super(EquipeAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('area', 'grupo', 'somacro', 'nome', 'procedimentos')
    actions = ['action_clone']
    search_fields = ('nome', 'macroprocesso__nome', 'macroprocesso__grupo__nome', 'macroprocesso__grupo__area__nome')
    inlines = [AtribuicaoInline, ProcedimentoInline]

    def action_clone(self, request, queryset):
        objs = clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = _(u'1 processo copiado')
        else:
            message = _(u'%s processos copiados') % total
        self.message_user(request, message)

    action_clone.short_description = _(u"Copiar os processos selecionados")


class GrupoAdmin(admin.ModelAdmin):
    list_display = ('area', 'nome')


class MacroprocessoAdmin(admin.ModelAdmin):
    list_display = ('area', 'grupo', 'nome')


admin.site.register(Norma)
admin.site.register(OTRS)
admin.site.register(Recurso)
admin.site.register(Area)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Macroprocesso, MacroprocessoAdmin)
admin.site.register(Processo, ProcessoAdmin)
admin.site.register(Equipe, EquipeAdmin)
admin.site.register(Papel)
admin.site.register(Atribuicao)
admin.site.register(Visao)
admin.site.register(Natureza)
admin.site.register(Procedimento)
