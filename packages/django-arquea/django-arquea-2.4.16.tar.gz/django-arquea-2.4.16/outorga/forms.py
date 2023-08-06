# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
from models import Item, OrigemFapesp, Termo, Natureza_gasto, Acordo, Contrato
from memorando.models import Pergunta
from utils.request_cache import get_request_cache


class OrigemFapespInlineForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrigemFapespInlineForm, self).__init__(data, files, auto_id, prefix, initial, error_class,
                                                     label_suffix, empty_permitted, instance)

        cache = get_request_cache()
        if cache.get('outorga.Acordo.all') is None:
            cache.set('outorga.Acordo.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in Acordo.objects.all().order_by('descricao')])
        self.fields['acordo'].choices = cache.get('outorga.Acordo.all')

        cache = get_request_cache()
        if cache.get('outorga.Item.all') is None:
            cache.set('outorga.Item.all', [('', '---------')] +
                      [(p.id, p.__unicode__())
                       for p in Item.objects.all().select_related('natureza_gasto', 'natureza_gasto__termo')])
        self.fields['item_outorga'].choices = cache.get('outorga.Item.all')

    class Meta:
        model = OrigemFapesp
        fields = ('acordo', 'item_outorga')


class ItemAdminForm(forms.ModelForm):
    """
    O método '__init__' Redefine os campoa 'item' e 'natureza_gasto'
                        Cria os campos 'termo' e 'modalidade' para filtrar os campos 'item' e 'natureza_gasto'
    O método 'clean'	Verifica se o termo e a modalidade do item anterior são os mesmos do item em edição.
    A class 'Meta'	Define o modelo a ser utilizado.
    A class 'Media'     Define os arquivos .j que serão utilizados (ajax/javascript)
    """
    # Redefine os campos 'termo', 'modalidade' e 'item_outorga'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ItemAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                            error_class, label_suffix, empty_permitted, instance)

        if instance:
            # Permite selecionar as naturezas de gasto da outorga da natureza de gasto selecionada.
            n = self.fields['natureza_gasto']
            n.queryset = Natureza_gasto.objects.filter(termo=instance.natureza_gasto.termo)\
                .select_related('termo', 'modalidade')

            self.fields['termo'].initial = instance.natureza_gasto.termo.id
        else:
            self.fields['natureza_gasto'].choices = \
                [(p.id, "%s" % (p.__unicode__()))
                 for p in Natureza_gasto.objects.all().select_related('termo', 'modalidade')]

        # mensagens de erro
        self.fields['descricao'].error_messages['required'] = u'O campo DESCRIÇÃO é obrigatório'
        self.fields['entidade'].error_messages['required'] = u'O campo ENTIDADE é obrigatório'
        self.fields['quantidade'].error_messages['required'] = u'O campo QUANTIDADE é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'
        self.fields['justificativa'].error_messages['required'] = u'O campo JUSTIFICATIVA é obrigatório'

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
                                   widget=forms.Select(attrs={'onchange': 'ajax_filter_termo_natureza("/outorga/'
                                                                          'seleciona_termo_natureza", "natureza_gasto",'
                                                                          ' this.value, this.id);',
                                                              'class': 'auxiliary'}))

    # Define o modelo
    class Meta:
        model = Item
        fields = ['natureza_gasto', 'descricao', 'entidade', 'quantidade', 'valor', 'justificativa', 'obs', ]

    # Define os arquivos .js que serão utilizados.
    class Media:
        js = ('/site-media/js/selects.js',)


class OrigemFapespAdminForm(forms.ModelForm):

    """
    O método '__init__'	Redefine o campo 'item_outorga'
    Cria os campos 'termo' e 'modalidade' para filtrar o campo 'item_outorga'
    A class 'Meta'      Define o modelo a ser utilizado.
    A class 'Media'	Define os arquivos .j que serão utilizados (ajax/javascript)
    """
    # Redefine os campos 'termo', 'modalidade' e 'item_outorga'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrigemFapespAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                    error_class, label_suffix, empty_permitted, instance)

#
        self.fields['acordo'].choices = [('', '---------')] + \
                                        [(p.id, p.__unicode__()) for p in Acordo.objects.all().order_by('descricao')]
        self.fields['item_outorga'].choices = [('', '---------')] + \
                                              [(p.id, p.__unicode__()) for p in Item.objects.all()
                                                  .select_related('natureza_gasto', 'natureza_gasto__termo')]

        # mensagens de erro
        self.fields['acordo'].error_messages['required'] = u'O campo ACORDO é obrigatório'
        self.fields['item_outorga'].error_messages['required'] = u'O campo ITEM DE OUTORGA é obrigatório'

    # Define o modelo
    class Meta:
        model = OrigemFapesp
        fields = ['acordo', 'item_outorga', ]

    # Define os arquivos .js que serão utilizados.
    class Media:
        js = ('/site-media/js/selects.js', )


class ContratoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ContratoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                error_class, label_suffix, empty_permitted, instance)

        self.fields['anterior'].choices = [('', '---------')] + \
                                          [(p.id, "%s | %s" % (p.__unicode__(), p.numero))
                                           for p in Contrato.objects.all().order_by('entidade', '-data_inicio')]

        # mensagens de erro
        self.fields['numero'].error_messages['required'] = u'O campo NUMERO é obrigatório'
        self.fields['data_inicio'].error_messages['required'] = u'O campo INÍCIO é obrigatório'
        self.fields['entidade'].error_messages['required'] = u'O campo ENTIDADE é obrigatório'
        self.fields['arquivo'].error_messages['required'] = u'O campo ARQUIVO é obrigatório'


class OrdemDeServicoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OrdemDeServicoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                      error_class, label_suffix, empty_permitted, instance)

        self.fields['contrato'].choices = [('', '---------')] + \
                                          [(p.id, "%s | %s" % (p.__unicode__(), p.numero))
                                           for p in Contrato.objects.all().select_related('entidade')
                                              .order_by('entidade', '-data_inicio')]

        self.fields['pergunta'].choices = [(p.id, "%s" % (p.__unicode__()))
                                           for p in Pergunta.objects.all().select_related('memorando')]

        # mensagens de erro
        self.fields['acordo'].error_messages['required'] = u'O campo ACORDO é obrigatório'
        self.fields['tipo'].error_messages['required'] = u'O campo TIPO é obrigatório'
        self.fields['numero'].error_messages['required'] = u'O campo NUMERO é obrigatório'
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'
        self.fields['data_inicio'].error_messages['required'] = u'O campo INÍCIO é obrigatório'
        self.fields['contrato'].error_messages['required'] = u'O campo CONTRATO é obrigatório'
        self.fields['descricao'].error_messages['required'] = u'O campo DESCRIÇÃO é obrigatório'


class OutorgaAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(OutorgaAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['categoria'].error_messages['required'] = u'O campo CATEGORIA é obrigatório'
        self.fields['termo'].error_messages['required'] = u'O campo TERMO é obrigatório'
        self.fields['termino'].error_messages['required'] = u'O campo TÉRMINO é obrigatório'
        self.fields['data_solicitacao'].error_messages['required'] = u'O campo SOLICITAÇÃO é obrigatório'


class ModalidadeAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ModalidadeAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                  error_class, label_suffix, empty_permitted, instance)

    def clean(self):
        cleaned_data = super(ModalidadeAdminForm, self).clean()

        if any(self.errors):
            return self.cleaned_data

        sigla = self.cleaned_data.get('sigla')
        if not sigla:
            self._errors["sigla"] = self.error_class([u'Sigla não pode ser vazia'])
            del cleaned_data["sigla"]

        return self.cleaned_data


class TermoAdminForm(forms.ModelForm):

    rt = forms.BooleanField(label=u'Carregar itens de Reserva Técnica?', required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(TermoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                             error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'

    def clean(self):
        cleaned_data = super(TermoAdminForm, self).clean()

        if any(self.errors):
            return self.cleaned_data

        ano = self.cleaned_data.get('ano')
        if ano is None:
            self._errors["ano"] = self.error_class([u'O campo ANO não pode ser vazio.'])
            del cleaned_data["ano"]
        elif ano is not None and ano < 1900:
            self._errors["ano"] = self.error_class([u'O campo ANO deve possuir 4 dígitos.'])
            del cleaned_data["ano"]

        return self.cleaned_data


class AcordoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(AcordoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                              error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'
        self.fields['descricao'].error_messages['required'] = u'O campo DESCRIÇÃO é obrigatório'


class ArquivoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ArquivoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['outorga'].error_messages['required'] = u'O campo OUTORGA é obrigatório'
        self.fields['arquivo'].error_messages['required'] = u'O campo ARQUIVO é obrigatório'


class CategoriaAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(CategoriaAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['nome'].error_messages['required'] = u'O campo NOME é obrigatório'


class EstadoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(EstadoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                              error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['nome'].error_messages['required'] = u'O campo NOME é obrigatório'


class Natureza_gastoAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(Natureza_gastoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                      error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['termo'].error_messages['required'] = u'O campo TERMO DE OUTORGA é obrigatório'
        self.fields['modalidade'].error_messages['required'] = u'O campo MODALIDADE é obrigatório'
        self.fields['valor_concedido'].error_messages['required'] = u'O campo VALOR CONCEDIDO é obrigatório'
