# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from tinymce.widgets import TinyMCE

from utils import widgets
from identificacao.models import Identificacao
from memorando.models import MemorandoFAPESP, MemorandoResposta, Pergunta,\
    MemorandoSimples, Corpo


class MemorandoRespostaForm(forms.ModelForm):
    introducao = forms.CharField(required=False, label=u'Introdução',
                                 widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height': 500}))
    conclusao = forms.CharField(required=False, label=u'Conclusão',
                                widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height': 500}))
    memorando = forms.ModelChoiceField(MemorandoFAPESP.objects.all(), label=u'Memorando FAPESP',
                                       widget=forms.Select(attrs={'onchange': 'ajax_filter_perguntas(this.value);'}))

    def __init__(self, *args, **kwargs):
        super(MemorandoRespostaForm, self).__init__(*args, **kwargs)

        self.fields['identificacao'].choices = [('', '---------')] + \
                                               [(p.id, p.__unicode__()) for p in Identificacao.objects.all()
                                                .select_related('endereco__entidade', 'contato')]

    class Meta:
        model = MemorandoResposta
        fields = ['memorando', 'assunto', 'identificacao', 'estado', 'introducao', 'conclusao', 'assinatura', 'data',
                  'arquivo', 'protocolo', 'anexa_relatorio', 'obs']


class PerguntaAdminForm(forms.ModelForm):
    questao = forms.CharField(label=u'Questão',
                              widget=TinyMCE(attrs={'cols': 100, 'rows': 30}, mce_attrs={'height': 120}))

    class Meta:
        model = Pergunta
        fields = ['numero', 'questao']


class MemorandoSimplesForm(forms.ModelForm):
    # corpo = forms.CharField(widget=TinyMCE(attrs={'cols': 160, 'rows': 180}, mce_attrs={'height':500}))
    corpo = forms.CharField(widget=CKEditorWidget())

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(MemorandoSimplesForm, self).__init__(data, files, auto_id, prefix, initial,
                                                   error_class, label_suffix, empty_permitted, instance)

        self.fields['pai'].choices = [('', '---------')] + \
                                     [(p.id, p.__unicode__())
                                      for p in MemorandoSimples.objects.all().select_related('assunto')]

    class Meta:
        model = MemorandoSimples
        fields = ['superior', 'inferior', 'direita', 'esquerda', 'destinatario', 'assunto', 'corpo', 'equipamento',
                  'envio', 'assinatura', 'assinado', 'pai']


class CorpoAdminForm(forms.ModelForm):
    # MemorandoResposta - corpo de cada pergunta/resposta do memorando
    pergunta = forms.ModelChoiceField(Pergunta.objects.all().select_related('memorando'),
                                      label=_(u'Pergunta'),
                                      widget=forms.Select(attrs={'onchange': 'ajax_select_pergunta(this.id);'}))
    perg = forms.CharField(label='Texto da pergunta', widget=widgets.PlainTextWidget, required=False)
    resposta = forms.CharField(label='Resposta',
                               widget=TinyMCE(attrs={'cols': 50, 'rows': 30}, mce_attrs={'height': 120}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(CorpoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                             error_class, label_suffix, empty_permitted, instance)
        if data:
            pergunta_id = data.get('pergunta')
            if pergunta_id:
                pgta = Pergunta.objects.select_related('memorando').get(id=pergunta_id)
                self.fields['perg'].initial = pgta.questao
        elif instance and hasattr(instance, 'pergunta'):
            self.fields['perg'].initial = instance.pergunta.questao

    class Meta:
        model = Corpo
        fields = ['pergunta', 'perg', 'resposta', 'anexo', 'concluido']

    class Media:
        js = ('js/selects.js', )


class BaseCorpoInlineFormSet(BaseInlineFormSet):
    # MemorandoResposta - corpo de cada pergunta/resposta do memorando
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None):

        super(BaseCorpoInlineFormSet, self).__init__(data=data, files=files, instance=instance, save_as_new=save_as_new,
                                                     prefix=prefix, queryset=queryset)

        if data:
            memorando_id = data.get('memorando')
            if memorando_id:
                m = MemorandoFAPESP.objects.get(id=memorando_id)
                for f in self.forms:
                    f.fields['pergunta'].queryset = Pergunta.objects.select_related('memorando').filter(memorando=m)
                self.empty_form.fields['pergunta'].queryset = Pergunta.objects.select_related('memorando').filter(memorando=m)

        elif instance and hasattr(instance, 'memorando'):
            m = instance.memorando
            for f in self.forms:
                f.fields['pergunta'].queryset = Pergunta.objects.select_related('memorando').filter(memorando=m)
            self.empty_form.fields['pergunta'].queryset = Pergunta.objects.select_related('memorando').filter(memorando=m)

        else:
            for f in self.forms:
                f.fields['pergunta'].queryset = Pergunta.objects.none()
            self.empty_form.fields['pergunta'].queryset = Pergunta.objects.none()

CorpoFormSet = inlineformset_factory(MemorandoResposta, Corpo, formset=BaseCorpoInlineFormSet,
                                     fields=['pergunta', 'resposta', 'anexo', 'concluido'])
