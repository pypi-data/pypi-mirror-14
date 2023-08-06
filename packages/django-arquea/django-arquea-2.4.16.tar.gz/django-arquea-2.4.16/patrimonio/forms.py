# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import django
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
from django.utils.html import mark_safe
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms.fields import ChoiceField

from utils.request_cache import get_request_cache
from financeiro.models import Pagamento
from memorando.models import MemorandoSimples
from identificacao.models import Entidade, EnderecoDetalhe
from outorga.models import Termo
from patrimonio.models import Equipamento, Patrimonio, HistoricoLocal, Estado


# Exibição de patrimonios filhos em forma de tabela, dentro do form de Patrimonio
class PatrimonioReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        retorno = ''
        if value and len(value) > 0:
            retorno += u'<table>'
            retorno += "<tr><th>Nome</th><th>NS</th><th>Desc</th></tr>"
            if value:
                for v in value:
                    value_id = v[0] or ''
                    retorno += "<tr>"
                    retorno += "<td style='white-space:nowrap;'>" \
                               "<a href='/patrimonio/patrimonio/%s/'>%s</td>" % (value_id, v[1] or '')
                    retorno += "<td style='white-space:nowrap;'>" \
                               "<a href='/patrimonio/patrimonio/%s/'>%s</td>" % (value_id, v[2] or '')
                    retorno += "<td><a href='/patrimonio/patrimonio/%s/'>%s</td>" % (value_id, v[3] or '')
                    retorno += "</tr>"
            retorno += "</table>"
        return mark_safe(retorno)

    def _has_changed(self, initial, data):
        return False


class PatrimonioReadOnlyField(forms.FileField):
    widget = PatrimonioReadOnlyWidget

    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial, help_text=help_text, widget=widget)

    def clean(self, value, initial=None):
        self.widget.initial = initial
        return initial


class AdvancedModelChoiceIterator(forms.models.ModelChoiceIterator):
    """
    Classe para exibição da Entidade no formato Select, ordenado pelo sigla_completa
    que inclui a Entidade pai, no formato "<sigla entidade pai> - <sigla entidade>"
    """
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        else:
            yield ("", "---------")

        choices = []
        # Preenche os valores do compo com o ID, a sigla completa com a entidade pai, e a sigla tabulada
        for item in self.queryset.select_related('entidade', 'entidade__entidade'):

            label = mark_safe(item.sigla_tabulada().replace(' ', '&nbsp;'))
            sortValue = item.sigla_completa()
            choices.append((item.pk, label, sortValue))
        # Reordena os itens utilizando a sigla completa
        choices = sorted(choices, key=lambda obj: obj[2])

        for item in choices:
            yield (item[0], item[1])


class EntidadeModelChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(EntidadeModelChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        # Escolhe entre o empty_label ou senão coloca um valor padrão para o item vazio
        return AdvancedModelChoiceIterator(self)

    choices = property(_get_choices, ChoiceField._set_choices)


class EquipamentoContidoModelChoiceField(forms.ModelChoiceField):
    """
    Classe para exibição de Equipamentos - contidos em.
    Restringe a exibição da descrição em 200 caracteres com a adição de reticências para não exceder a largura da tela
    """
    def label_from_instance(self, obj):
        info = (obj.__unicode__()[:200] + '..') if len(obj.__unicode__()) > 200 else obj.__unicode__()
        return u'%s' % info


class EquipamentoModelChoiceField(forms.ModelChoiceField):
    """
    Classe para exibição de Equipamentos.
    Restringe a exibição da descrição em 150 caracteres com a adição de reticências para não exceder a largura da tela
    """
    def label_from_instance(self, obj):
        info = (obj.descricao[:150] + '..') if len(obj.descricao) > 150 else obj.descricao
        return u'%s - %s' % (info, obj.part_number)


class PatrimonioAdminForm(forms.ModelForm):
    """
    Uma instância dessa classe faz algumas definições para a tela de cadastramento do modelo 'Patrimonio'.

    O método '__init__'        Define as opções do campo 'protocolo' (apenas protocolos diferentes de 'Contrato', 'OS'
     e 'Cotação'.
    O campo 'termo'        Foi criado para filtrar o campo 'protocolo'
    O campo 'protocolo'        Foi criado para filtrar o campo 'itemprotocolo'
    A class 'Meta'        Define o modelo que será utilizado.
    A class 'Media'        Define os arquivos .js que serão utilizados.
    """
    termo = forms.ModelChoiceField(Termo.objects.all(), label=_(u'Termo de outorga'), required=False,
                                   widget=forms.Select(attrs={'class': 'auxiliary'}))

    npgto = forms.CharField(label=_(u'Nº do cheque ou do documento'), required=False,
                            widget=forms.TextInput(
                                attrs={'class': 'auxiliary',
                                       'onchange': 'ajax_filter_pagamentos("/patrimonio/escolhe_pagamento", '
                                                   'this.value);'}))

#    part_number = forms.CharField(required=False, widget=forms.TextInput(
# attrs={'onchange':'ajax_patrimonio_existente(this.value);'}))

    nf = forms.CharField(label=_(u'Nº da NF ou NS'), required=False,
                         widget=forms.TextInput(attrs={'onkeydown': 'if (event.keyCode == 13) {$(\'#id_patrimonio\')'
                                                                    '.focus(); return false;}',
                                                       'onchange': 'ajax_filter_patrimonio(this.value);',
                                                       'class': 'auxiliary'}))

    tem_numero_fmusp = forms.BooleanField(label=u'Tem nº de patrimônio oficial?', required=False,
                                          widget=forms.CheckboxInput(attrs={'onchange': 'ajax_numero_fmusp();'}))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2', 'cols': '152'}))

    filtro_equipamento = forms.CharField(label=_(u'Filtro para busca de Equipamento'), required=False,
                                         widget=forms.TextInput(attrs={'onchange': 'ajax_filter_equipamento'
                                                                                   '(this.value);',
                                                                       'onkeydown': 'return false;',
                                                                       'class': 'auxiliary'}))

    # Uso de Model específico para a adição de reticências na descrição
    # e javascript para adição de link no label para a página do Equipamento selecionado
    equip_window = '<a href="#" onclick="window.open(\'/patrimonio/equipamento/\'+$(\'#id_equipamento\').val()' \
                   ' + \'/\', \'_blank\');return true;">Equipamento</a>'
    equipamento = EquipamentoModelChoiceField(queryset=Equipamento.objects.all(),
                                              required=False,
                                              label=mark_safe(equip_window),
                                              widget=forms.Select(attrs={'style': 'width:800px',
                                                                         'onchange': 'ajax_patr_form_get_equipamento'
                                                                                     '($(\'#id_equipamento\').val());',
                                                                         })
                                              )

    patrimonio_window = '<a href="#" onclick="window.open(\'/patrimonio/patrimonio/\'+' \
                        '$(\'#id_patrimonio\').val() + \'/\', \'_blank\');return true;" >Contido em</a>'
    patrimonio_historico = 'ajax_patrimonio_historico($(\'#id_patrimonio\').val());'
    patrimonio = EquipamentoContidoModelChoiceField(queryset=Patrimonio.objects.all(),
                                                    required=False,
                                                    label=mark_safe(patrimonio_window),
                                                    widget=forms.Select(attrs={'style': 'width:800px ',
                                                                               'onchange': patrimonio_historico
                                                                               }),
                                                    empty_label='---'
                                                    )

    procedencia_window = '<a href="#" onclick="window.open(\'/identificacao/entidade/\'+' \
                         '$(\'#id_entidade_procedencia\').val() + \'/\', \'_blank\');return true;">Procedência</a>'
    entidade_procedencia = EntidadeModelChoiceField(queryset=Entidade.objects.all(),
                                                    required=False,
                                                    label=mark_safe(procedencia_window),
                                                    )

    pagamento_window = '<a href="#" onclick="window.open(\'/admin/financeiro/pagamento/\'+' \
                       '$(\'#id_pagamento\').val() + \'/\', \'_blank\');return true;">Pagamento</a>'
    pagamento = forms.ModelChoiceField(queryset=Pagamento.objects.all(),
                                       required=False,
                                       label=mark_safe(pagamento_window),
                                       )

    form_filhos = PatrimonioReadOnlyField()

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if instance:
            if initial:
                initial.update({'equipamento': instance.equipamento})
            else:
                initial = {'equipamento': instance.equipamento}

            initial.update({'patrimonio': instance.patrimonio})
            initial.update({'form_filhos': [(p.id, p.apelido, p.ns, p.descricao)
                                            for p in Patrimonio.objects.filter(patrimonio=instance)]})
            if instance.pagamento_id:
                initial.update({'termo': instance.pagamento.protocolo.termo})

        super(PatrimonioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                  error_class, label_suffix, empty_permitted, instance)

        pg = self.fields['pagamento']
        if data and 'termo' in data and data['termo']:
            t = data['termo']
            t = Termo.objects.get(id=t)
            pg.queryset = Pagamento.objects.filter(protocolo__termo=t)
        elif instance and instance.pagamento:
            pg.choices = [(p.id, p.__unicode__()) for p in Pagamento.objects.filter(id=instance.pagamento.id)]
        else:
            pg.queryset = Pagamento.objects.filter(id__lte=0)

        pt = self.fields['patrimonio']
        if data and 'patrimonio' in data and data['patrimonio']:
            pt.choices = [(p.id, p.__unicode__()) for p in Patrimonio.objects.filter(id=data['patrimonio'])]
        elif instance and instance.patrimonio:
            pt.choices = [(p.id, p.__unicode__()) for p in Patrimonio.objects.filter(id=instance.patrimonio.id)]
        else:
            pt.queryset = Patrimonio.objects.filter(id__lte=0)

        # Configurando a relação entre Patrimonio e Equipamento para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Patrimonio._meta.get_field('equipamento'), to=Equipamento, field_name='id')  # @UndefinedVariable
        else:
            rel = ManyToOneRel(Equipamento, 'id')

        self.fields['equipamento'].widget = RelatedFieldWidgetWrapper(self.fields['equipamento'].widget, rel,
                                                                      self.admin_site)

        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Patrimonio._meta.get_field('entidade_procedencia'), to=Entidade, field_name='id')  # @UndefinedVariable
        else:
            rel = ManyToOneRel(Entidade, 'id')

        procedencia_field = self.fields['entidade_procedencia']
        procedencia_field.widget = RelatedFieldWidgetWrapper(procedencia_field.widget, rel, self.admin_site)

        """
        et = self.fields['entidade_procedencia']
        if data and data['entidade_procedencia']:
            t = data['entidade_procedencia']
            et.queryset = Entidade.objects.filter(pk=t)
        elif instance and instance.entidade_procedencia:
            et.choices = [(p.id, p.__unicode__()) for p in Entidade.objects.filter(id=instance.entidade_procedencia.id)]
        else:
            # ************ROGERIO: MODIFICAR PARA UM FILTRO POR ATRIBUTO/ FLAG
            #entidadeHistoricoList = EntidadeHistorico.objects.filter(tipo__nome= 'Fabricante')
            .values_list('entidade_id', flat=True)
            #et.queryset = Entidade.objects.filter(id__in=entidadeHistoricoList)
            et.queryset = Entidade.objects.all()
        """
        # Exibe a quantidade de patrimonios filhos no label
        self.fields['form_filhos'].label = u'Patrimônios contidos (%s)' % \
                                           Patrimonio.objects.filter(patrimonio=instance).count()

        filtro_widget = self.fields['filtro_equipamento'].widget
        if instance:
            if instance.equipamento:
                filtro_widget = forms.TextInput(attrs={'onkeydown': 'if (event.keyCode == 13) {$(\'#id_equipamento\')'
                                                                    '.focus(); return false;}',
                                                       'onchange': 'ajax_filter_equipamento(this.value, "%s", "%s");' %
                                                                   (instance.id, instance.equipamento.id)})
            else:
                filtro_widget = forms.TextInput(attrs={'onkeydown': 'if (event.keyCode == 13) {$(\'#id_equipamento\')'
                                                                    '.focus(); return false;}',
                                                       'onchange': 'ajax_filter_equipamento(this.value, "%s");' %
                                                                   instance.id})
        else:
            filtro_widget = forms.TextInput(attrs={'onkeydown': 'if (event.keyCode == 13) {$(\'#id_equipamento\')'
                                                                '.focus(); return false;}',
                                                   'onchange': 'ajax_filter_equipamento(this.value, "");'})

    class Meta:
        model = Patrimonio
        fields = ['termo', 'npgto', 'pagamento', 'valor', 'agilis', 'checado', 'tipo', 'apelido', 'tem_numero_fmusp',
                  'numero_fmusp', 'filtro_equipamento', 'equipamento', 'ns', 'descricao', 'complemento', 'tamanho',
                  'entidade_procedencia', 'nf', 'patrimonio', 'obs', 'titulo_autor', 'isbn', 'revision', 'version',
                  'garantia_termino', 'form_filhos']

    class Media:
        js = ('js/selects.js', 'js/patrimonio.js')

    def clean(self):
        cleaned_data = super(PatrimonioAdminForm, self).clean()

        equipamento = self.cleaned_data.get('equipamento')
        if not equipamento:
            self._errors["equipamento"] = self.error_class([u'Patrimônio deve ter um equipamento associado.'])
            del cleaned_data["equipamento"]

        return cleaned_data


class HistoricoLocalAdminForm(forms.ModelForm):

    class Meta:
        model = HistoricoLocal
        fields = ['data', 'patrimonio', 'endereco', 'descricao']

    class Media:
        js = ('js/selects.js',)

    patrimonio = forms.ModelChoiceField(Patrimonio.objects.all().select_related('pagamento', 'pagamento__protocolo',
                                                                                'pagamento__protocolo__num_documento'),
                                        widget=forms.Select(attrs={'style': 'width:800px'}),)

    endereco = forms.ModelChoiceField(EnderecoDetalhe.objects.all().select_related('detalhe', 'endereco'))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if initial:
            if instance:
                if instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                    initial.update({'entidade': instance.endereco.endereco.entidade})
                if instance.patrimonio:
                    initial.update({'patrimonio': instance.patrimonio})
                if instance.endereco:
                    initial.update({'endereco': instance.endereco})
        else:
            initial = {}
            if instance and instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                initial['entidade'] = instance.endereco.endereco.entidade
            if instance and instance.patrimonio:
                initial['patrimonio'] = instance.patrimonio
            if instance and instance.endereco:
                initial['endereco'] = instance.endereco

        super(HistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                      error_class, label_suffix, empty_permitted, instance)

        if instance and instance.endereco:
            end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)

            if not end:
                end = EnderecoDetalhe.objects.filter(id__lte=0)

            self.fields['endereco'].choices = [(e.id, e.__unicode__()) for e in end]


class PatrimonioHistoricoLocalAdminForm(forms.ModelForm):

    class Meta:
        model = HistoricoLocal
        fields = ['entidade', 'endereco', 'posicao', 'descricao', 'data', 'estado', 'memorando']

    class Media:
        js = ('js/selects.js',)

    entidade = EntidadeModelChoiceField(Entidade.objects.all(), required=False,
                                        widget=forms.Select(attrs={'onchange': 'ajax_select_endereco(this.id);',
                                                                   'class': 'auxiliary'}))

    descricao = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        if initial:
            if instance:
                if instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                    initial.update({'entidade': instance.endereco.endereco.entidade})
        else:
            initial = {}
            if instance and instance.endereco and instance.endereco.endereco and instance.endereco.endereco.entidade:
                initial['entidade'] = instance.endereco.endereco.entidade

        super(PatrimonioHistoricoLocalAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                                error_class, label_suffix, empty_permitted, instance)

        end = None
        if data:
            end_id = data.get(u'%s-endereco' % prefix)
            if end_id and end_id.isdigit():
                end = EnderecoDetalhe.objects.filter(id=end_id)
        elif instance:
            end = EnderecoDetalhe.objects.filter(id=instance.endereco.id)

#         if data and not end:
#             if data.has_key('%s-entidade' % prefix) and data['%s-entidade' % prefix]:
#                 end = EnderecoDetalhe.objects.filter(endereco__entidade__id=data['%s-entidade' % prefix])
#             elif data.has_key('%s-endereco' % prefix) and data['%s-endereco' % prefix]:
#                 end = EnderecoDetalhe.objects.filter(endereco__id=data['%s-endereco' % prefix])

        if not end:
            end = EnderecoDetalhe.objects.filter(id__lte=0)

        # self.fields['endereco'].queryset = end
        self.fields['endereco'].choices = [(e.id, e.__unicode__()) for e in end]

        # Cache dos valores do campo de memorando do histórico
        cache = get_request_cache()
        if cache.get('memorando.MemorandoSimples.all') is None:
            cache.set('memorando.MemorandoSimples.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in MemorandoSimples.objects.all().select_related('assunto', )])
        self.fields['memorando'].choices = cache.get('memorando.MemorandoSimples.all')

        # Cache dos valores do campo de estado do patrionio do histórico
        cache = get_request_cache()
        if cache.get('patrimonio.Estado.all') is None:
            cache.set('patrimonio.Estado.all', [('', '---------')] +
                      [(p.id, p.__unicode__()) for p in Estado.objects.all()])
        self.fields['estado'].choices = cache.get('patrimonio.Estado.all')


class BaseHistoricoLocalAdminFormSet(BaseInlineFormSet):
    """
    Formset para checagem do Historico de Localidade de um Patrimonio.
    Faz a verificação se o Patrimonio está contido em outro Patrimonio na mesma localidade.
    """

    def clean(self):
        cleaned_data = super(BaseHistoricoLocalAdminFormSet, self).clean()
        # Retorna erro para erros de sistemas não tratados
        if any(self.errors):
            raise forms.ValidationError(u'Erro sistema %s' % self.errors)

        form_mais_recente = None
        patrimonio = None

        for i in range(0, self.total_form_count()):
            form = self.forms[i]

            # guardando o patrimonio relacionado a este histórico para posterior verificação
            if not patrimonio and form.cleaned_data.get("patrimonio"):
                patrimonio = form.cleaned_data.get("patrimonio")

            data = form.cleaned_data.get('data')
            # Verifica o historico mais recente, que não foi removido
            if data and (form.cleaned_data.get('DELETE') is None or form.cleaned_data.get('DELETE') is False):
                if form_mais_recente:
                    if data > form_mais_recente.cleaned_data.get('data'):
                        form_mais_recente = form
                else:
                    form_mais_recente = form

        if form_mais_recente:
            cleaned_data = form_mais_recente.cleaned_data

            if cleaned_data.get("patrimonio") and cleaned_data.get("patrimonio").patrimonio:
                contido_em = cleaned_data.get("patrimonio").patrimonio
                endereco = cleaned_data.get("endereco")

                # Verifica se o patrimonio atual não tem endereço/localidade e está dentro de um patrimonio com
                # endereço/localidade
                if (contido_em.historico_atual and not endereco):
                    raise forms.ValidationError(u'Patrimônio deve estar na mesma localização do patrimônio em '
                                                u'que está contido.')

                # Verifica se está no mesmo endereço do patrimonio pai
                if (contido_em.historico_atual and contido_em.historico_atual.endereco != endereco):
                    raise forms.ValidationError(u'Patrimônio deve estar na mesma localização do patrimônio em '
                                                u'que está contido.')

                historicolocal = HistoricoLocal(posicao=cleaned_data.get("posicao"))
                # Verifica se o patrimonio atual não tem posicao/rack e está dentro de um patrimonio com posicao/rack
                if contido_em.historico_atual.posicao_rack and \
                        (not historicolocal.posicao_rack or historicolocal.posicao_rack == ''):
                    raise forms.ValidationError(u'Patrimônio deve estar no mesmo rack do patrimônio em '
                                                u'que está contido.')

                # Verifica se está no mesmo rack do patrimonio pai
                if contido_em.historico_atual and historicolocal and \
                        contido_em.historico_atual.posicao_rack != historicolocal.posicao_rack:
                    raise forms.ValidationError(u'Patrimônio deve estar no mesmo rack do patrimônio em '
                                                u'que está contido.')

                # Verifica se o patrimonio está no mesmo rack/furo do patrimonio pai
                # Não verifica se o patrimonio pai for Rack, pois o Rack não tem posição de furo
                if contido_em.equipamento.tipo.nome != 'Rack' and \
                        contido_em.historico_atual.posicao_furo != historicolocal.posicao_furo:
                    raise forms.ValidationError(u'Patrimônio deve estar no mesmo furo do patrimônio em '
                                                u'que está contido.')
        else:
            if patrimonio:
                contido_em = patrimonio.patrimonio
                if contido_em:
                    # Esse caso deve ocorrer se o patrimonio está contido em outro e o histórico atual foi removido
                    raise forms.ValidationError(u'Patrimônio deve estar na mesma localização do patrimônio em '
                                                u'que está contido.')

        return cleaned_data

HistoricoLocalAdminFormSet = inlineformset_factory(Patrimonio, HistoricoLocal,
                                                   formset=BaseHistoricoLocalAdminFormSet,
                                                   fk_name='patrimonio',
                                                   fields=['data', 'patrimonio', 'endereco', 'descricao'],)


class EquipamentoAdminForm(forms.ModelForm):
    entidade_window = '<a href="#" onclick="window.open(\'/identificacao/entidade/\'+' \
                      '$(\'#id_entidade_fabricante\').val() + \'/\', \'_blank\');return true;">Marca</a>'
    entidade_fabricante = EntidadeModelChoiceField(queryset=Entidade.objects.all(),
                                                   required=False,
                                                   label=mark_safe(entidade_window)
                                                   )

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(EquipamentoAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                   error_class, label_suffix, empty_permitted, instance)

        # Configurando a relação entre Equipamento e Entidade para aparecer o botão de +
        # O self.admin_site foi declarado no admin.py
        if django.VERSION[0:2] >= (1, 6):
            rel = ManyToOneRel(field=Equipamento._meta.get_field('entidade_fabricante'), to=Entidade, field_name='id')  # @UndefinedVariable
        else:
            rel = ManyToOneRel(Entidade, 'id')

        self.fields['entidade_fabricante'].widget = RelatedFieldWidgetWrapper(self.fields['entidade_fabricante'].widget,
                                                                              rel, self.admin_site)

    def clean(self):
        cleaned_data = super(EquipamentoAdminForm, self).clean()

        return cleaned_data


class PlantaBaixaObjetoForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(PlantaBaixaObjetoForm, self).__init__(data, files, auto_id, prefix, initial,
                                                    error_class, label_suffix, empty_permitted, instance)

        if 'patrimonio' in self.fields:
            self.fields['patrimonio'].choices = [('', '---------')] +\
                                                [(p.id, "%s - %s" % (p.id, p.apelido))
                                                 for p in Patrimonio.objects.filter(equipamento__tipo__nome='Rack')]
            self.fields['patrimonio'].label = mark_safe('<a href="#" onclick="window.open(\'/patrimonio/patrimonio/\'+'
                                                        '$(\'#id_patrimonio\').val() + \'/\', \'_blank\');'
                                                        'return true;">Patrimônio</a>')


class PlantaBaixaDataCenterForm(forms.ModelForm):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(PlantaBaixaDataCenterForm, self).__init__(data, files, auto_id, prefix, initial,
                                                        error_class, label_suffix, empty_permitted, instance)

        if 'endereco' in self.fields:
            self.fields['endereco'].choices = [('', '---------')] + \
                                              [(p.id, "%s - %s" % (p.id, p.complemento))
                                               for p in EnderecoDetalhe.objects.filter(
                                                  historicolocal__estado__id=Estado.PATRIMONIO_ATIVO,
                                                  historicolocal__patrimonio__equipamento__tipo__nome='Rack',
                                                  mostra_bayface=True,).order_by('id').distinct()]
