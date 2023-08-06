# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.db.models import Q
from django.forms.utils import ErrorList
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _

from rede.models import PlanejaAquisicaoRecurso, BlocoIP, IFCConector,\
    CrossConnection, Recurso
import ipaddress
from outorga.models import Termo
from financeiro.models import Pagamento


class PlanejaAquisicaoRecursoAdminForm(forms.ModelForm):

    referente = forms.CharField(widget=forms.TextInput(attrs={'size': '150'}), required=False)

    class Meta:
        model = PlanejaAquisicaoRecurso
        fields = ['os', 'ano', 'tipo', 'referente', 'quantidade', 'valor_unitario', 'projeto', 'unidade', 'instalacao',
                  'banda', 'obs']


class BlocoIPAdminForm(forms.ModelForm):

    # Campo de exibição de net mask. Utilizado somente para visualizar o netmask.
    net_mask = forms.CharField(label=_(u'Net Mask'), required=False,
                               widget=forms.TextInput(attrs={'disabled': 'disabled'}))

    def __init__(self, *args, **kwargs):
        super(BlocoIPAdminForm, self).__init__(*args, **kwargs)

        # Adicionando link para o label do campo de Superbloco
        self.fields['superbloco'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/rede/blocoip/\'+'
                                                    '$(\'#id_superbloco\').val() + \'/\', \'_blank\');return true;">'
                                                    'Super bloco</a>')

        if 'instance' in kwargs and kwargs['instance']:
            ip = kwargs['instance'].ip
            mask = kwargs['instance'].mask

            # Preenchendo o campo de exibição de net mask
            if ip and mask:
                self.fields['net_mask'].initial = ipaddress.ip_network(u'%s/%s' % (ip, mask), strict=False).netmask

    def clean(self):
        cleaned_data = super(BlocoIPAdminForm, self).clean()

        ip = self.cleaned_data.get('ip')
        mask = self.cleaned_data.get('mask')

        # Verifica se o IP / Mask foram preenchidos com valores de válidos
        if ip and mask:
            try:
                ipaddress.ip_network(u'%s/%s' % (ip, mask), strict=False)
            except ValueError:
                self._errors["ip"] = self.error_class([u'IP / Mask não representam um endereço de rede válido.'])
                del cleaned_data["ip"]

        return cleaned_data

    class Meta:
        model = BlocoIP
        fields = '__all__'


class RecursoAdminForm(forms.ModelForm):
    """
    Uma instância dessa classe faz algumas definições para a tela de cadastramento do modelo 'Patrimonio'.

    O campo 'termo'             Foi criado para filtrar o campo 'protocolo'
    A class 'Meta'              Define o modelo que será utilizado.
    A class 'Media'             Define os arquivos .js que serão utilizados.
    """
#    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False,
#            widget=forms.Select(attrs={'onchange': 'ajax_filter_pagamentos2("/rede/escolhe_pagamento");'}))

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False)

    pagamento = forms.ModelChoiceField(
        Pagamento.objects.all().select_related('protocolo', 'origem_fapesp', 'protocolo',
                                               'origem_fapesp__item_outorga__natureza_gasto__modalidade'),
        label=mark_safe('<a href="#" onclick="window.open(\'/financeiro/pagamento/\'+$(\'#id_pagamento\').val()'
                        ' + \'/\', \'_blank\');return true;">Pagamento</a>'),)

    planejamento = forms.ModelChoiceField(
        PlanejaAquisicaoRecurso.objects.all().select_related('os', 'os__tipo', 'projeto', 'tipo', ),
        label=mark_safe('<a href="#" onclick="window.open(\'/admin/rede/planejaaquisicaorecurso/\'+$(\'#id_'
                        'planejamento\').val() + \'/\', \'_blank\');return true;">Planejamento</a>'),)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=':', empty_permitted=False, instance=None):

        if instance:
            if initial:
                initial.update({'termo': instance.pagamento.protocolo.termo.id})
            else:
                initial = {'termo': instance.pagamento.protocolo.termo.id}

        super(RecursoAdminForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                               empty_permitted, instance)

        pg = self.fields['pagamento']
        if instance:
            if instance.pagamento is not None:
                pg.queryset = Pagamento.objects.filter(protocolo__termo__id=instance.pagamento.protocolo.termo.id)\
                    .select_related('protocolo', 'origem_fapesp', 'protocolo',
                                    'origem_fapesp__item_outorga__natureza_gasto__modalidade')
            else:
                pg.queryset = Pagamento.objects.filter(id__lte=0)\
                    .select_related('protocolo', 'origem_fapesp', 'protocolo',
                                    'origem_fapesp__item_outorga__natureza_gasto__modalidade')
        elif data and data['termo']:
            t = data['termo']
            pg.queryset = Pagamento.objects.filter(protocolo__termo=t)\
                .select_related('protocolo', 'origem_fapesp', 'protocolo',
                                'origem_fapesp__item_outorga__natureza_gasto__modalidade')
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)\
                .select_related('protocolo', 'origem_fapesp', 'protocolo',
                                'origem_fapesp__item_outorga__natureza_gasto__modalidade')

    class Meta:
        model = Recurso
        fields = ['planejamento', 'termo', 'pagamento', 'obs', 'quantidade', 'mes_referencia', 'ano_referencia',
                  'valor_imposto_mensal', 'valor_mensal_sem_imposto']

    class Media:
        js = ('js/selects.js',)


class IFCConectorAdminForm(forms.ModelForm):

    class Meta:
        model = IFCConector
        fields = ['rack', 'shelf', 'porta', 'tipoConector', 'ativo', 'obs']

    def __init__(self, *args, **kwargs):
        super(IFCConectorAdminForm, self).__init__(*args, **kwargs)

        self.id = None
        if 'instance' in kwargs and kwargs['instance']:
            self.id = kwargs['instance'].id

        # Adicionando link para o label do campo de Tipo de Conector
        self.fields['tipoConector'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/rede/tipoconector/\'+'
                                                      '$(\'#id_tipoConector\').val() + \'/\', \'_blank\');'
                                                      'return true;">Tipo de Conector</a>')


class CrossConnectionAdminForm(forms.ModelForm):

    class Meta:
        model = CrossConnection
        fields = ['origem', 'destino', 'circuito', 'ordemDeServico', 'obs', 'ativo']

    def __init__(self, *args, **kwargs):
        super(CrossConnectionAdminForm, self).__init__(*args, **kwargs)

        self.id = None
        if 'instance' in kwargs and kwargs['instance']:
            self.id = kwargs['instance'].id

        # Adicionando link para o label do campo de Origem
        self.fields['origem'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/rede/ifcconector/\'+$(\''
                                                '#id_origem\').val() + \'/\', \'_blank\');return true;">Origem</a>')
        # Adicionando link para o label do campo de Destino
        self.fields['destino'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/rede/ifcconector/\'+$(\''
                                                 '#id_destino\').val() + \'/\', \'_blank\');return true;">Destino</a>')

    def clean(self):
        cleaned_data = super(CrossConnectionAdminForm, self).clean()

        origem_id = self.cleaned_data.get('origem')
        destino_id = self.cleaned_data.get('destino')

        # Verifica se a origem e destino da cross conexão não são iguais
        if origem_id and destino_id and origem_id == destino_id:
            self._errors["origem"] = self.error_class([u'IFC de origem e destino não podem ser a mesma.'])

        # Verifica se as IFC especificadas já estão cadastradas em outra Cross conexão ativa.
        if origem_id:
            qs = CrossConnection.objects.filter(Q(origem_id=origem_id) | Q(destino_id=origem_id))
            qs = qs.filter(ativo=True)
            if self.id:
                qs = qs.exclude(pk=self.id)
            if qs.count() > 0:
                self._errors["origem"] = self.error_class([u'IFC já cadastrado em uma Cross Conexão.'])
        if destino_id:
            qs = CrossConnection.objects.filter(Q(origem_id=destino_id) | Q(destino_id=destino_id))
            qs = qs.filter(ativo=True)
            if self.id:
                qs = qs.exclude(pk=self.id)
            if qs.count() > 0:
                self._errors["destino"] = self.error_class([u'IFC já cadastrado em uma Cross Conexão.'])

        return cleaned_data
