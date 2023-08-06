# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import django
from django import forms
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.core import urlresolvers
from django.db.models.fields.related import ManyToOneRel
from django.forms.utils import ErrorList
from django.utils.html import mark_safe

from django.utils.translation import ugettext_lazy as _
from PIL import Image as Img
import StringIO

from outorga.models import Termo, OrigemFapesp
from protocolo.models import Protocolo
from memorando.models import Pergunta
from rede.models import PlanejaAquisicaoRecurso, Recurso
from financeiro.models import ExtratoPatrocinio, Estado, TipoComprovante, CODIGO_FINANCEIRO,\
    Pagamento, ExtratoFinanceiro, ExtratoCC, Auditoria
from utils.request_cache import get_request_cache
from membro.models import Membro
from decimal import Decimal


class RecursoInlineAdminForm(forms.ModelForm):
    # Foi codificado no label um Checkbox para exibir somente os recursos vigentes
    # Ele chama um AJAX para repopular o SELECT
    # O estado inicial é exibir somente os vigentes

    obs = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '3', 'style': 'width:400px'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(RecursoInlineAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                     error_class, label_suffix, empty_permitted, instance)

        # Configurando o campo de 'planejamento', pois o processamento do __unicode__
        # é muito demorado quando são carregados mais que 5 recursos. Há casos com mais
        # de 10 recursos no InlineAdminForm
        cache = get_request_cache()
        if cache.get('rede.PlanejaAquisicaoRecurso.all') is None:
            cache.set('rede.PlanejaAquisicaoRecurso.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in PlanejaAquisicaoRecurso.objects.all()
                      .select_related('os', 'os__tipo', 'tipo', 'projeto', )])
        self.fields['planejamento'].choices = cache.get('rede.PlanejaAquisicaoRecurso.all')

        self.fields['planejamento'].label = \
            mark_safe('<a href="#"  onclick="window.open(\'%s\'+$(\'#\'+$(this).parent().attr(\'for\')).val() + '
                      '\'/\', \'_blank\');return true;">Planejamento:</a> <input type="checkbox" '
                      'onclick="get_recursos($(this));"> Exibir somente os vigentes.'
                      % urlresolvers.reverse('admin:rede_planejaaquisicaorecurso_changelist'))

    class Meta:
        model = Recurso
        fields = ['planejamento', 'quantidade', 'valor_mensal_sem_imposto', 'valor_imposto_mensal', 'obs', ]


class PagamentoAdminForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance and not data:
            initial = {'termo': instance.protocolo.termo.id}

        super(PagamentoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted, instance)

        if 'pergunta' in self.fields:
            self.fields['pergunta'].queryset = Pergunta.objects.all().select_related('memorando')

        if 'patrocinio' in self.fields:
            self.fields['patrocinio'].queryset = ExtratoPatrocinio.objects.all().select_related('localiza')

        # Permite selecionar apenas as despesas com valor superior a soma dos valores de suas fontes pagadoras.
        t = None
        if data:
            if 'termo' in data and data['termo'] is not None and data['termo'] != '':
                t = Termo.objects.get(id=data['termo'])
        elif instance:
            termo = instance.protocolo.termo
            t = termo  # Termo.objects.get(id=termo)

        if t:
            self.fields['origem_fapesp'].choices = [('', '---------')] + \
                                                   [(p.id, p.__unicode__())
                                                    for p in OrigemFapesp.objects.filter(
                                                       item_outorga__natureza_gasto__termo=t).select_related(
                                                       'acordo', 'item_outorga', 'item_outorga__natureza_gasto',
                                                       'item_outorga__natureza_gasto__termo', ).order_by(
                                                       'acordo__descricao', 'item_outorga__natureza_gasto__modalidade')]
            self.fields['protocolo'].choices = [('', '---------')] + \
                                               [(p.id, p.__unicode__()) for p in Protocolo.objects.filter(termo=t)
                                                   .prefetch_related('itemprotocolo_set')
                                                   .select_related('tipo_documento').order_by('data_vencimento')]
        else:
            cache = get_request_cache()
            if cache.get('protocolo.Protocolo.all') is None:
                cache.set('protocolo.Protocolo.all', [('', '---------')] +
                          [(p.id, p.__unicode__()) for p in Protocolo.objects.all()
                          .prefetch_related('itemprotocolo_set')
                          .select_related('tipo_documento').order_by('data_vencimento')])
            self.fields['protocolo'].choices = cache.get('protocolo.Protocolo.all')

            cache = get_request_cache()
            if cache.get('outorga.OrigemFapesp.all') is None:
                cache.set('outorga.OrigemFapesp.all', [('', '---------')] +
                          [(p.id, p.__unicode__()) for p in OrigemFapesp.objects.all()
                          .select_related('acordo', 'item_outorga', 'item_outorga__natureza_gasto',
                                          'item_outorga__natureza_gasto__termo', )
                          .order_by('acordo__descricao', 'item_outorga__natureza_gasto__modalidade')])
            self.fields['origem_fapesp'].choices = cache.get('outorga.OrigemFapesp.all')

        if self.fields.has_key('membro'):
            self.fields['membro'].choices = [('', '---------')] + \
                                            [(p.id, p.__unicode__()) for p in Membro.objects.all().order_by('nome')]

        # mensagens de erro
        self.fields['protocolo'].error_messages['required'] = u'O campo PROTOCOLO é obrigatório'
        self.fields['valor_fapesp'].error_messages['required'] = u'O campo VALOR ORIGINÁRIO DA FAPESP é obrigatório'
        self.fields['valor_patrocinio'].error_messages['required'] = u'O campo VALOR ORIGINÁRIO' \
                                                                     u' DE PATROCÍNI é obrigatório'

    class Meta:
        model = Pagamento
        fields = ['termo', 'valor_fapesp', 'protocolo', 'origem_fapesp', 'valor_patrocinio', ]

    class Media:
        js = ('js/selects.js',)

    cod_oper = forms.CharField(label=_(u'Código da operação'), required=False,
                               widget=forms.TextInput(
                                   attrs={'onchange': 'ajax_filter_cc_cod(this.value);', 'class': 'auxiliary'}))
    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
                                   widget=forms.Select(attrs={'onchange': 'ajax_filter_origem_protocolo(this.id, '
                                                                          'this.value);', 'class': 'auxiliary'}))
    numero = forms.CharField(label=_(u'Número do protocolo'), required=False,
                             widget=forms.TextInput(
                                 attrs={'onchange': 'ajax_filter_protocolo_numero(this.value);', 'class': 'auxiliary'}))
    origem_fapesp = forms.ModelChoiceField(OrigemFapesp.objects.all(), label=_(u'Origem Fapesp'), required=False,
                                           widget=forms.Select(attrs={'onchange': 'ajax_prox_audit(this.value);'}))

    # tornando clicável o label do campo conta_corrente
    conta_corrente = forms.ModelChoiceField(queryset=ExtratoCC.objects.all(),
                                            required=False,
                                            label=mark_safe('<a href="#" onclick="window.open(\'/admin/financeiro/extratocc'
                                                            '/\'+$(\'#id_conta_corrente\').val() + \'/\', \'_blank\');'
                                                            'return true;">Conta corrente</a>'),)
    # tornando clicável o label do campo protocolo
    protocolo = forms.ModelChoiceField(queryset=Protocolo.objects.all(),
                                       label=mark_safe('<a href="#" onclick="window.open(\'/admin/protocolo/protocolo'
                                                       '/\'+$(\'#id_protocolo\').val() + \'/\', \'_blank\');'
                                                       'return true;">Protocolo</a>'),)

    def clean(self):
        cleaned_data = super(PagamentoAdminForm, self).clean()

        if any(self.errors):
            return self.cleaned_data

        valor = self.cleaned_data.get('valor_fapesp')
        origem = self.cleaned_data.get('origem_fapesp')

        if valor and not origem:
            self._errors["origem_fapesp"] = self.error_class([u'Valor da FAPESP obriga a ter uma origem da FAPESP'])
            del cleaned_data["origem_fapesp"]

        return self.cleaned_data


class ExtratoFinanceiroAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ExtratoFinanceiroAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                         error_class, label_suffix, empty_permitted, instance)

        sorted_codigo = sorted(CODIGO_FINANCEIRO, key=lambda x: x[1])
        
        self.fields['cod'].choices = [('', '---------')] + sorted_codigo
        
        # restringindo a seleção de extratoCC
        # Deixa uma mensagem com o link para o registro do Extrato CC, se existir
        self.fields['entrada_extrato_cc'].widget = forms.HiddenInput()
        if instance and instance.entrada_extrato_cc:
            self.fields['entrada_extrato_cc'].label = mark_safe('Entrada já criada no <strong>'
                                                            '<a href="#" onclick="window.open(\'/financeiro/extratocc'
                                                            '/\'+$(\'#id_entrada_extrato_cc\').val() + \'/\', \'_blank\'); return true;">'
                                                            'extrato da conta corrente</a></strong>')
        else:
            self.fields['entrada_extrato_cc'].label = ''

        # mensagens de erro
        self.fields['termo'].error_messages['required'] = u'O campo TERMO DE OUTORGA é obrigatório'
        self.fields['data_libera'].error_messages['required'] = u'O campo DATA é obrigatório'
        self.fields['cod'].error_messages['required'] = u'O campo CODIGO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'

    class Meta:
        model = ExtratoFinanceiro
        fields = ['termo', 'data_libera', 'cod', 'valor', 'comprovante', 'tipo_comprovante', 'parcial']


class ExtratoPatrocinioAdminForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ExtratoPatrocinioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                         error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['localiza'].error_messages['required'] = u'O campo LOCALIZAÇÃO DO PATROCÍONIO é obrigatório'
        self.fields['data_oper'].error_messages['required'] = u'O campo DATA DA OPERAÇÃO é obrigatório'
        self.fields['cod_oper'].error_messages['required'] = u'O campo CÓDIGO DA OPERAÇÃO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'
        self.fields['historico'].error_messages['required'] = u'O campo HISTÓRICO é obrigatório'
        self.fields['obs'].error_messages['required'] = u'O campo OBS é obrigatório'

    class Meta:
        model = ExtratoPatrocinio
        fields = ['localiza', 'data_oper', 'cod_oper', 'historico', 'valor', 'obs']


class ExtratoCCAdminForm(forms.ModelForm):

    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo'), required=False,
                                   widget=forms.Select(attrs={'onchange': 'ajax_filter_financeiro(this.value);',
                                                              'class': 'auxiliary'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(ExtratoCCAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted, instance)

        # mensagens de erro
        self.fields['data_oper'].error_messages['required'] = u'O campo DATA DA OPERAÇÃO é obrigatório'
        self.fields['cod_oper'].error_messages['required'] = u'O campo DOCUMENTO é obrigatório'
        self.fields['historico'].error_messages['required'] = u'O campo HISTORICO é obrigatório'
        self.fields['valor'].error_messages['required'] = u'O campo VALOR é obrigatório'

    class Meta:
        model = ExtratoCC
        fields = ['termo', 'extrato_financeiro', 'despesa_caixa', 'data_oper', 'cod_oper', 'historico', 'valor']

    def clean_imagem(self):
        imagem = self.cleaned_data.get('imagem', False)
        if imagem and imagem.name:
            # Verificando a extensão do arquivo de imagem. Pode conter somente JPEG.
            imagem_split = imagem.name.split('.')
            extensao = ''
            if len(imagem_split) > 1:
                extensao = imagem_split[-1]

            if not (extensao.lower() in ['jpeg', 'jpg']):
                raise forms.ValidationError(_(u'Somente utilizar imagens JPEG.'))

            # Verificando se a proporção das dimensões da imagem parecem ser a de um cheque
            image_read = Img.open(StringIO.StringIO(imagem.read()))
            (imw, imh) = image_read.size
            ratio = Decimal(imw) / Decimal(imh)
            if ratio < 2:
                raise forms.ValidationError(_(u'Dimensões da imagem do cheque incorreta. (Proporção = %.3f)' % ratio))

        return imagem


class AuditoriaPagamentoChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.unicode_para_auditoria()


class AuditoriaAdminForm(forms.ModelForm):
    parcial = forms.IntegerField(label=u'Parcial',
                                 widget=forms.TextInput(attrs={'onchange': 'ajax_nova_pagina(this);'}))
    pagamento = AuditoriaPagamentoChoiceField(queryset=Pagamento.objects.all()
                                              .select_related('protocolo',
                                                              'origem_fapesp__item_outorga__natureza_gasto',
                                                              'origem_fapesp__item_outorga__natureza_gasto__modalidade'),
                                              label=mark_safe('<a href="#" onclick="window.open(\'/financeiro/pagamento'
                                                              '/\'+$(\'#id_pagamento\').val() + \'/\', \'_blank\');'
                                                              'return true;">Pagamento</a>'),)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(AuditoriaAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                 error_class, label_suffix, empty_permitted, instance)

        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Auditoria._meta.get_field('pagamento'), to=Pagamento, field_name='id')  # @UndefinedVariable
        else:
            rel = ManyToOneRel(Pagamento, 'id')

        self.fields['pagamento'].widget = RelatedFieldWidgetWrapper(self.fields['pagamento'].widget, rel,
                                                                    self.admin_site)

        # mensagens de erro
        self.fields['pagamento'].error_messages['required'] = u'O campo PAGAMENTO é obrigatório'
        self.fields['estado'].error_messages['required'] = u'O campo ESTADO é obrigatório'
        self.fields['tipo'].error_messages['required'] = u'O campo TIPO é obrigatório'
        self.fields['parcial'].error_messages['required'] = u'O campo PARCIAL é obrigatório'
        self.fields['pagina'].error_messages['required'] = u'O campo PAGINA é obrigatório'

    class Meta:
        model = Auditoria
        fields = ['estado', 'pagamento', 'tipo', 'parcial', 'pagina', 'arquivo', 'obs']


class PagamentoAuditoriaAdminInlineForm(forms.ModelForm):
    """
    Form de Auditoria utilizado como inline dentro do form do Pagamento
    """
    estado = forms.ModelChoiceField(Estado.objects.all(),
                                    label=u'Estado',
                                    widget=forms.Select(
                                        attrs={'onchange': 'ajax_prox_audit($("#id_origem_fapesp").val());'}))

    tipo = forms.ModelChoiceField(TipoComprovante.objects.all(),
                                  label=u'Tipo',
                                  widget=forms.Select(
                                      attrs={'onchange': 'ajax_prox_audit($("#id_origem_fapesp").val());'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(PagamentoAuditoriaAdminInlineForm, self).__init__(data, files, auto_id, prefix, initial,
                                                                error_class, label_suffix, empty_permitted, instance)

        cache = get_request_cache()
        if cache.get('financeiro.Estado.all') is None:
            cache.set('financeiro.Estado.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in Estado.objects.all()])
        self.fields['estado'].choices = cache.get('financeiro.Estado.all')

        if cache.get('financeiro.TipoComprovante.all') is None:
            cache.set('financeiro.TipoComprovante.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in TipoComprovante.objects.all()])
        self.fields['tipo'].choices = cache.get('financeiro.TipoComprovante.all')

    class Meta:
        model = Auditoria
        fields = ['estado', 'pagamento', 'tipo', 'parcial', 'pagina', 'arquivo', 'obs']
