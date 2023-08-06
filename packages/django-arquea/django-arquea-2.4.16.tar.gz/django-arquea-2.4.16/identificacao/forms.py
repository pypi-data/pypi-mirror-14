# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.utils.html import mark_safe
import re

from identificacao.models import Contato, Endereco, Entidade, EnderecoDetalhe,\
    Identificacao, Acesso


EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


# Faz a validação de um e-mmail
def is_valid_email(value):
    return EMAIL_RE.search(value)


class ContatoAdminForm(forms.ModelForm):

    """
    A função 'clean_email' identifica cada e-mail do campo 'email' e verifica se eles são validos.
    """

    # Define o modelo
    class Meta:
        model = Contato
        fields = ['primeiro_nome', 'ultimo_nome', 'ativo', 'email', 'tel', 'documento']

    # Verifica se os e-mail são válidos.
    def clean_email(self):

        value = self.cleaned_data['email']

        if not value:
            return value
        emails = [e.strip() for e in value.split(',')]
        for email in emails:
            if not is_valid_email(email):
                raise forms.ValidationError(u'%s não é um e-mail válido.' % email)

        # Always return the cleaned data.
        return value


class EnderecoAdminForm(forms.ModelForm):

    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                                      widget=forms.Select(attrs={'onchange': 'ajax_select_endereco2();'}))

    class Meta:
        model = Endereco
        fields = ['entidade', 'rua', 'num', 'compl', 'cep', 'bairro', 'cidade', 'estado', 'pais']

    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/identificacao.js')


class EnderecoDetalheAdminForm(forms.ModelForm):

    # Campo de filtro por Entidade para reduzir a seleção do campo Endereço
    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                                      widget=forms.Select(attrs={'onchange': 'ajax_select_endereco2();',
                                                                 'class': 'auxiliary'}))

    def __init__(self, *args, **kwargs):
        super(EnderecoDetalheAdminForm, self).__init__(*args, **kwargs)

        # Adicionando link para o label do campo de Tipo de Conector
        self.fields['endereco'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/identificacao/endereco/\''
                                                  '+$(\'#id_endereco\').val() + \'/\', \'_blank\');return true;">%s</a>'
                                                  % self.fields['endereco'].label)
        self.fields['detalhe'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/identificacao/endereco'
                                                 'detalhe/\'+$(\'#id_detalhe\').val() + \'/\', \'_blank\');return true;'
                                                 '">%s</a>' % self.fields['detalhe'].label)

        # Populando campos
        entidade_ids = Endereco.objects.all().values('entidade')

        self.fields['entidade'].choices = [('', '---------')] + \
                                          [(p.id, p.__unicode__()) for p in Entidade.objects.all().filter(id__in=entidade_ids)]
        self.fields['endereco'].choices = [('', '---------')] + \
                                          [(p.id, p.__unicode__()) for p in Endereco.objects.all().select_related('entidade')]
        self.fields['detalhe'].choices = [('', '---------')] + \
                                         [(p.id, p.__unicode__()) for p in EnderecoDetalhe.objects.all()
                                          .select_related('detalhe__endereco__entidade__sigla', 'endereco__entidade__sigla')]

    def clean(self):
        cleaned_data = self.cleaned_data
        endereco = cleaned_data.get('endereco')
        detalhe = cleaned_data.get('detalhe')

        if endereco is None and detalhe is None:
            raise forms.ValidationError(u'Endereço e detalhe do endereço não podem ser ambos nulos')
        elif endereco and detalhe:
            raise forms.ValidationError(u'Endereço e detalhe do endereço não podem ser ambos utilizados')

        return cleaned_data

    class Meta:
        model = EnderecoDetalhe
        fields = ['entidade', 'endereco', 'detalhe', 'tipo', 'complemento']

    class Media:
        js = ('js/selects.js',)


class AcessoAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AcessoAdminForm, self).__init__(*args, **kwargs)

        self.fields['identificacao'].choices = [('', '---------')] + \
                                               [(p.id, p.__unicode__()) for p in Identificacao.objects.all()
                                                .select_related('endereco__entidade', 'contato')
                                                .order_by('endereco__entidade__sigla', 'area', 'contato__primeiro_nome')]

        self.fields['detalhe'].choices = [(p.id, p.__unicode__()) for p in EnderecoDetalhe.objects.all()
                                          .select_related('endereco__entidade', 'detalhe__endereco__entidade')]

    class Meta:
        model = Acesso
        fields = ['identificacao', 'niveis', 'liberacao', 'encerramento', 'obs', 'detalhe']


class EnderecoDetalheInlineAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EnderecoDetalheInlineAdminForm, self).__init__(*args, **kwargs)

        self.fields['detalhe'].choices = [('', '---------')] + \
                                         [(p.id, p.__unicode__()) for p in EnderecoDetalhe.objects.all()
                                          .select_related('endereco__entidade', 'detalhe__endereco__entidade')]

    class Meta:
        model = EnderecoDetalhe
        fields = ['tipo', 'complemento', 'detalhe', 'mostra_bayface']
