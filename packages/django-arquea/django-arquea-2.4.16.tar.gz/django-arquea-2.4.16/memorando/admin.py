# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from utils.functions import clone_objects
from memorando.models import Estado, Assunto, Arquivo, Pergunta, Corpo,\
    MemorandoFAPESP, MemorandoResposta, MemorandoSimples
from memorando.forms import PerguntaAdminForm, CorpoAdminForm, CorpoFormSet,\
    MemorandoRespostaForm, MemorandoSimplesForm


class PerguntaInline(admin.TabularInline):
    fieldsets = ((None, {'fields': ('numero', 'questao')}),)
    model = Pergunta
    form = PerguntaAdminForm
    extra = 2


class MemorandoFAPESPAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('termo', 'numero'), 'arquivo')}),)
    inlines = [PerguntaInline]
    list_per_page = 10
    list_display = ('termo', 'numero')


class CorpoInline(admin.TabularInline):
    # MemorandoResposta - corpo de cada pergunta/resposta do memorando
    fieldsets = ((None, {'fields': ('pergunta', 'perg', 'resposta', 'anexo', 'concluido')}),)
    form = CorpoAdminForm
    formset = CorpoFormSet
    model = Corpo
    extra = 10


class MemorandoRespostaAdmin(admin.ModelAdmin):
    fieldsets = (
        (_(u'Memorando'), {
            'fields': (('memorando', 'assunto'), 'identificacao', 'estado'),
            }),
        (None, {
            'fields': ('introducao', 'conclusao', ('assinatura', 'data'), 'arquivo', 'protocolo', 'anexa_relatorio'),
            }),
        (_(u'Observação'), {
            'fields': ('obs', ),
            'classes': ('collapse',)
        }),
    )
    inlines = [CorpoInline]
    list_display = ('__unicode__', 'termo', 'memorando', 'assunto')
    form = MemorandoRespostaForm

admin.site.register(Estado)
admin.site.register(MemorandoFAPESP, MemorandoFAPESPAdmin)
admin.site.register(MemorandoResposta, MemorandoRespostaAdmin)
admin.site.register(Assunto)


class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 1


class MemorandoSimplesAdmin(admin.ModelAdmin):
    form = MemorandoSimplesForm
    list_display = ('num_memo', 'assunto', 'destinatario', 'data')
    # list_select_related pode ser somente boolean no 1.5
    if django.VERSION[0:2] >= (1, 6):
        list_select_related = ('assunto', )
    else:
        list_select_related = True

    inlines = [ArquivoInline]
    search_fields = ['assunto__descricao', 'corpo', 'data']

    fieldsets = (
        (u'Margens (em cm)', {
            'fields': (('superior', 'inferior', 'direita', 'esquerda'),),
            }),
        (None, {
            'fields': ('destinatario', 'assunto', 'corpo', ('equipamento', 'envio'), ('assinatura', 'assinado', 'pai')),
            }),
    )
    actions = ['action_clone']

    def action_clone(self, request, queryset):
        clone_objects(queryset)
        total = queryset.count()
        if total == 1:
            message = u'1 memorando copiado'
        else:
            message = u'%s memorandos copiados' % total
        self.message_user(request, message)

    action_clone.short_description = _(u"Duplicar os memorandos selecionados")

admin.site.register(MemorandoSimples, MemorandoSimplesAdmin)
