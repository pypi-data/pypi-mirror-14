# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from models import Cotacao, TipoDocumento, Protocolo, Feriado, Arquivo, Descricao

from outorga.models import Termo
from identificacao.models import Entidade, Identificacao

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# class ContratoAdminForm(forms.ModelForm):
#
#     """
#     Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Contrato'.
#
#     A função '__init__': Define o campo 'data_vencimento' como obrigatório no cadastramento de um Contrato.
#                         Define um novo 'label' para o campo que indica o contrato anterior e permite selecionar como
#                         'contrato anterior' os protocolos definidos como 'Contrato' ou 'Ordem de Serviço'
#                         Define um novo 'label' para o campo 'identificacao'.
#                         Limita a seleção do tipo do documento apenas para as opções 'Contrato' e 'Ordem de Serviço'.
#     Cria um campo 'entidade' para filtrar o campo identificação.
#     A 'class Meta' define o modelo que será utilizado.
#     """
#
#
#     entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
#             widget=forms.Select(attrs={'onchange': 'filter_select("id_identificacao", "id_entidade");'}))
#
#
#     class Meta:
#         model = Contrato
#
#
#     class Media:
#         js = ('/media/js/selects.js', '/media/js/protocolo.js')
#
#
#     # Redefine os campos 'data_vencimento', 'protocolo', 'tipo_documento' e 'identificacao'.
#     def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
#                 initial=None, error_class=ErrorList, label_suffix=':',
#                 empty_permitted=False, instance=None):
#
#         super(ContratoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
#                                             error_class, label_suffix, empty_permitted, instance)
#
#         # Define a data de vencimento como obrigatória.
#         dv = self.fields['data_vencimento']
#         dv.required = True
#
#
#         # Define novo 'label' para o campo do protocolo anterior e permite selecionar apenas 'Contrato'.
#         pt = self.fields['protocolo']
#         pt.label = u'Contrato anterior'
#         pt.queryset = Protocolo.objects.filter(tipo_documento__nome__in=[u'Contrato'])
#
#
#         # Permite selecionar apenas as opções 'Contrato' e 'Ordem de Serviço' no tipo do documento.
#         tp = self.fields['tipo_documento']
#         tp.queryset = TipoDocumento.objects.filter(nome__in=[u'Contrato', u'Ordem de Serviço'])
#
#
#         # Define novo 'label' para o campo da identificação.
#         iden = self.fields['identificacao']
#         iden.label = u'Contato'


class CotacaoAdminForm(forms.ModelForm):
    """
    Uma instância dessa classe faz algumas definições para a tela de cadastramento do modelo 'Contacao'.

    A função '__init__' Define um novo 'label' para o campo que indica o pedido anterior e permite selecionar como
                        pedido anterior apenas os protocolos diferentes de 'Contrato' e 'Ordem de Serviço'.
                        Define que o campo 'protocolo' será filtrado pelo campo 'termo'.
                        Define um novo 'label' para o campo 'identificacao'.
    Cria novos campos 'termo' para filtrar o campo 'protocolo'.
                      'entidade' para filtrar o campo 'identificacao'.
    A 'class Meta' define o modelo que será utilizado.
    """
    termo = forms.ModelChoiceField(Termo.objects.all(),
                                   widget=forms.Select(
                                       attrs={'onchange': 'filter_select("id_protocolo", "id_termo");'}))

    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
                                      widget=forms.Select(
                                          attrs={'onchange': 'filter_select("id_identificacao", "id_entidade");'}))

    class Meta:
        model = Cotacao
        fields = ['estado', 'termo', 'entidade', 'identificacao', 'descricao2', 'moeda_estrangeira', 'data_validade',
                  'data_chegada', 'origem', 'valor_total', 'obs', 'aceito', 'entrega', 'protocolo', 'parecer']

    class Media:
        js = ('js/selects.js', 'js/protocolo.js')

    # Redefine os campos 'protocolo' e 'identificacao'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(CotacaoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)

        # Gera uma lista com os tipos de documento diferentes de 'Cotação', 'Contrato' e 'Ordem de Serviço'
        nomes = []
        tipo = TipoDocumento.objects.all()
        for t in tipo:
            if t.nome.lower() != u'contrato' and t.nome.lower() != u'ordem de serviço' and t.nome.lower() != u'cotação':
                nomes.append(t.nome)

        # # Define novo 'label' e permite selecionar protocolos diferentes de 'Cotação', 'Contrato' e
        # 'Ordem de Serviço'.
        # pt = self.fields['protocolo']
        # pt.label = u'Pedido'
        # pt.required = True
        # pt.queryset = Protocolo.objects.filter(tipo_documento__nome__in=nomes)

        # Define novo 'label' para o campo da identificação.
        iden = self.fields['identificacao']
        iden.label = u'Contato'

        self.fields['protocolo'].choices = [('', '---------')] + \
                                           [(p.id, p.__unicode__())
                                            for p in Protocolo.objects.all().prefetch_related('itemprotocolo_set')
                                               .select_related('tipo_documento').order_by('data_vencimento')]

        self.fields['identificacao'].choices = [('', '---------')] + \
                                               [(p.id, p.__unicode__())
                                                for p in Identificacao.objects.all()
                                                   .select_related('endereco', 'endereco__entidade', 'contato')]

        self.fields['descricao2'].choices = [('', '---------')] + \
                                            [(p.id, p.__unicode__())
                                             for p in Descricao.objects.all().select_related('entidade',)]


class ProtocoloAdminForm(forms.ModelForm):
    """
    Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Protocolo'.

    A função '__init__': Permite selecionar como pedido anterior os protocolos diferentes de 'Contrato', 'Cotação',
                         ou 'Ordem de Serviço'.
    Cria o campo 'entidade' para filtrar o campo 'identificacao'.
    A 'class Meta' define o modelo que será utilizado.
    """
#    entidade = forms.ModelChoiceField(Entidade.objects.all(), required=False,
#            widget=forms.Select(attrs={'onchange': 'filter_select("id_identificacao", "id_entidade");'}))

    # referencia = forms.ChoiceField(choices=[(obj['descricao'], obj['descricao']) for obj in
    #  Protocolo.objects.order_by().values('descricao').distinct()],
    # label='Referente a', widget=forms.Select(attrs={'onchange':'referente("id_referencia", "id_descricao");'}))

    class Meta:
        model = Protocolo
        fields = ['data_chegada', 'origem', 'valor_total', 'obs', 'estado', 'termo', 'descricao2', 'tipo_documento',
                  'num_documento', 'moeda_estrangeira', 'referente', 'procedencia', 'data_validade', 'data_vencimento',
                  'responsavel']

    class Media:
        js = ('js/selects.js', 'js/protocolo.js',)

    # Verifica se o termo do protocolo é o mesmo termo do item do pedido de outorga relacionada a despesa
    # desse protocolo.
#    def clean(self):
#        cleaned_data = self.cleaned_data
#        termo1 = cleaned_data['termo']

#        proto = self.instance
#        if proto and termo1:

#            try:
#                despesa = Despesa.objects.filter(protocolo=proto)
#            except ObjectDoesNotExist:
#                return cleaned_data

#            for d in despesa:
#                item = d.item_pedido
#                if item:
#                    termo2 = item.natureza_gasto.outorga.termo

#                    if termo1 != termo2:
#                        raise forms.ValidationError(_(u'Este protocolo possui despesa atrelada a
# outro termo de outorga'))

#        return cleaned_data

    # Redefine o campo 'protocolo'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        termos = Termo.objects.order_by('-ano')
        if termos and not instance:
            initial = {'termo': termos[0].id}

        super(ProtocoloAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted, instance)

        # Gera uma lista com os tipos de documento diferentes de 'Contrato' e 'Ordem de Serviço'
        nomes = []
        tipo = TipoDocumento.objects.all()
        for t in tipo:
            if t.nome.lower() != u'contrato' and t.nome.lower() != u'ordem de serviço' and t.nome.lower() != u'cotação':
                nomes.append(t.nome)

        # Permite selecionar protocolos diferentes de 'Contrato', 'Ordem de Serviço' e 'Cotação'.
        # pt = self.fields['protocolo']
        # pt.queryset = Protocolo.objects.filter(tipo_documento__nome__in=nomes)


class ItemAdminForm(forms.ModelForm):
    marca = forms.CharField(max_length=100, required=False, label=_('Marca'))
    modelo = forms.CharField(max_length=100, required=False, label=_('Modelo'))
    ns = forms.CharField(max_length=30, required=False, label=_(u'Número de série'))


class FeriadoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(FeriadoAdminForm, self).clean()
        feriado = self.cleaned_data.get('feriado')
        tipo = self.cleaned_data.get('tipo')

        # Verifica se um feriado fixo ocorre na data especificada do tipo de feriado
        if tipo and not tipo.movel and (tipo.dia != feriado.day or tipo.mes != feriado.month):
            self._errors["tipo"] = self.error_class([u"Feriado fixo deve ser no mesmo dia/mês especificado no tipo do "
                                                     u"feriado. Este feriado ocorre no dia %s/%s" %
                                                     (tipo.dia, tipo.mes)])
            del cleaned_data["tipo"]

        fid = self.cleaned_data.get('id')
        # Verifica se já há uma data de feriado cadastrada no mesmo dia
        f = Feriado.objects.filter(feriado=feriado)
        if f.count() > 0 and fid and f.id != fid:
            raise forms.ValidationError(u"O feriado nesta data já existe.")

        return self.cleaned_data


class TipoFeriadoAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(TipoFeriadoAdminForm, self).clean()
        movel = self.cleaned_data.get('movel')
        dia = self.cleaned_data.get('dia')
        mes = self.cleaned_data.get('mes')

        # Verifica se um feriado fixo ocorre na data especificada do tipo de feriado
        if not movel:
            if not dia:
                self._errors["dia"] = self.error_class([u"Feriado fixo deve ter o dia especificado"])
                del cleaned_data["dia"]
            if not mes:
                self._errors["mes"] = self.error_class([u"Feriado fixo deve ter o mês especificado"])
                del cleaned_data["mes"]

        return self.cleaned_data


class ArquivoAdminForm(forms.ModelForm):

    protocolo = forms.ModelChoiceField(Protocolo.objects.all().select_related('tipo_documento'))

    class Meta:
        model = Arquivo
        fields = ['protocolo', 'arquivo']

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance:
            if initial:
                initial.update({'protocolo': instance.protocolo})
            else:
                initial = {'protocolo': instance.protocolo}

        super(ArquivoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                               error_class, label_suffix, empty_permitted, instance)
