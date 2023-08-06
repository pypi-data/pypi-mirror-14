# -*- coding: utf-8 -*-

from models import Pesquisa, L2, L3
from django import forms


class PesquisaAdminForm(forms.ModelForm):

    l2 = forms.ModelMultipleChoiceField(L2.objects.all(), required=False,
                                        label=u'Protocolos L2 (ethernet)',
                                        help_text=u'Assinalar os protcolos atendidos pelo equipamento de conexão',
                                        widget=forms.CheckboxSelectMultiple)
    l3 = forms.ModelMultipleChoiceField(L3.objects.all(), required=False, initial=[1],
                                        label=u'Protocolos L3 (TCP/IP)',
                                        help_text=u'Assinalar os protcolos atendidos pelo equipamento de conexão',
                                        widget=forms.CheckboxSelectMultiple(attrs={'onclick': 'muda_l3(this)'}))

    class Meta:
        model = Pesquisa
        fields = ['rede', 'laboratorio', 'endereco', 'cidade', 'instituicao',
                  'responsavel1', 'emailresp1', 'responsavel2', 'emailresp2',
                  'contato1', 'emailcontato1', 'telefone1', 'contato2', 'emailcontato2',
                  'telefone2', 'estado_equipamento', 'equipamento', 'fabricante',
                  'modelo', 'cobre', 'otica', 'l2', 'l2_outro', 'l3', 'l3_outro', 'obs', ]

    class Media:
        js = ('/media/js/pesquisa.js',)
