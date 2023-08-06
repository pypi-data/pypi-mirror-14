# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
import logging
import re
from membro.models import Membro, DadoBancario, Ferias, ControleFerias, Controle

# Get an instance of a logger
logger = logging.getLogger(__name__)

EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'  # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain


# Faz a validação de um e-mmail
def is_valid_email(value):
    return EMAIL_RE.search(value)


class MembroAdminForm(forms.ModelForm):

    """
    O método '__init__'		É usado para recuperar o 'id' do membro.
    O método 'clean_email'	Identifica cada e-mail do campo 'email' e verifica se eles são validos.
    O método 'clean_cpf'	Verifica se o CPF informado pertence a um membro cadastrado.
    A class 'Meta'		Define o modelo a ser usado.
    """

    # Redefine os campos 'data_vencimento', 'protocolo', 'tipo_documento' e 'identificacao'.
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(MembroAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                              error_class, label_suffix, empty_permitted, instance)

        try:
            self.id = instance.id
        except:
            self.id = None

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

    # Verifica a unicidade do CPF.
    def clean_cpf(self):
        value = self.cleaned_data['cpf']

        if not value:
            return value

        membro = Membro.objects.filter(cpf=value)
        for mb in membro:
            if mb.id != self.id:
                raise forms.ValidationError(u'O CPF %s já está cadastrado' % value)

        # Always return the cleaned data.
        return value

    class Meta:
        model = Membro
        fields = ['nome', 'email', 'ramal', 'foto', 'site', 'contato', 'data_nascimento', 'rg', 'cpf', 'url_lattes',
                  'obs']


class DadoBancarioAdminForm(forms.ModelForm):

    """
    Uma instância dessa classe faz algumas definições/limitações para a tela de cadastramento do modelo 'Tarefa'.

    O método '__init__'		Limita a seleção do campo 'membro' para selecionar apenas funcionários.
    O campo 'entidade'		Foi criado para filtrar o campo 'equipe'.
    A class 'Meta'		Define o modelo que será utilizado.
    A class 'Media'		Define os arquivo .js que serão utilizados.
    """
    class Meta:
        model = DadoBancario
        fields = ['membro', 'banco', 'agencia', 'ag_digito', 'conta', 'cc_digito']

    class Media:
        js = ('/site-media/js/selects.js', '/site-media/js/membro.js')


class FeriasAdminForm(forms.ModelForm):
    """
    Inicializar o 'queryset' do campo membro com os valores corretos (apenas funcionarios)
    """
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):

        super(FeriasAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                              error_class, label_suffix, empty_permitted, instance)

        funcionarios = Membro.objects.all()
        for m in funcionarios:
            if not m.funcionario:
                funcionarios = funcionarios.exclude(id=m.id)
        self.fields['membro'].queryset = funcionarios

    class Meta:
        model = Ferias
        fields = ['membro', 'inicio', 'realizado']


class ControleFeriasAdminForm(forms.ModelForm):

    def clean(self):
        termino = self.cleaned_data.get('termino')

        if not termino:
            return self.cleaned_data

        inicio = self.cleaned_data.get('inicio')
        if inicio > termino:
            raise forms.ValidationError(u"Data de término anterior à data de início")

        oficial = self.cleaned_data.get('oficial')

        dias = termino - inicio
        if oficial and dias.days != 19 and dias.days != 29:
            raise forms.ValidationError(u'Férias oficiais devem durar 20 ou 30 dias')

        # Restrição para termos um melhor controle do período de férias tirado de fato para conta no relatório de
        # controle de horas trabalhadas.
        # A marcação de oficial fica para a 'configuração' das férias, adiantamento, venda de dias e período oficial.
        dias_uteis_fato = self.cleaned_data.get('dias_uteis_fato')
        if oficial and dias_uteis_fato:
            raise forms.ValidationError(u'Não marcar os "Dias úteis tirados de fato" em férias oficiais. Criar um novo '
                                        u'"Controle de Férias" para especificar o período de férias tirados de fato.')

        dias_uteis_aberto = self.cleaned_data.get('dias_uteis_aberto')
        if not oficial and dias_uteis_aberto:
            raise forms.ValidationError(u'Marcar os "Dias úteis em aberto" somente nas férias oficiais.')

        return self.cleaned_data

    class Meta:
        model = ControleFerias
        fields = ['ferias', 'inicio', 'termino', 'oficial', 'obs', 'vendeu10', 'antecipa13', 'dias_uteis_fato',
                  'dias_uteis_aberto', 'arquivo_oficial']


class BaseControleFeriasAdminFormSet(BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return

#         if self.total_form_count() > 3:
#             raise forms.ValidationError(u'Não pode haver mais de 3 Controles de Férias')

        oficiais = 0
        nao_oficiais = 1
        for i in range(0, self.total_form_count()-1):
            form = self.forms[i]
            if form.cleaned_data.get('oficial') is True:
                oficiais += 1
            else:
                nao_oficiais += 1

#         if oficiais > 1 or nao_oficiais > 2:
#             raise forms.ValidationError(u'No máximo um período oficial e dois não oficiais')

ControleFeriasAdminFormSet = inlineformset_factory(Ferias, ControleFerias, formset=BaseControleFeriasAdminFormSet,
                                                   fields=['ferias', 'inicio', 'termino', 'oficial', 'obs', 'vendeu10',
                                                           'antecipa13', 'dias_uteis_fato', 'dias_uteis_aberto',
                                                           'arquivo_oficial'],)


class ControleObs(forms.ModelForm):

    class Meta:
        model = Controle
        fields = ('obs',)


class ControleAdminForms(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ControleAdminForms, self).clean()

        entrada = cleaned_data.get("entrada")
        saida = cleaned_data.get("saida")

        # Checar horarios de entrada e saida
        if entrada and saida and entrada > saida:
            msg = _(u"Entrada não pode ser depois que a saída.")
            self._errors["entrada"] = self.error_class([msg])
            self._errors["saida"] = self.error_class([msg])

            # These fields are no longer valid. Remove them from the cleaned data.
            del cleaned_data["entrada"]
            del cleaned_data["saida"]

        if entrada and saida:
            almoco = cleaned_data.get("almoco")
            tempo_de_trabalho = saida - entrada
            try:
                total_seconds = tempo_de_trabalho.total_seconds()
            except AttributeError:
                total_seconds = tempo_de_trabalho.seconds + tempo_de_trabalho.days * 24 * 3600

            # se for mais que 20h de trabalho
            if total_seconds > 72000:
                msg = _(u"Período de trabalho maior que 20h.")
                self._errors["saida"] = self.error_class([msg])
                del cleaned_data["saida"]

            # Checar se horario de almoço vai fazer as horas ficarem negativas
            if almoco and total_seconds <= (almoco * 60):
                msg = _(u"Período de trabalho menor que o tempo de almoço.")
                self._errors["almoco"] = self.error_class([msg])
                del cleaned_data["almoco"]

        # Always return the full collection of cleaned data.
        return cleaned_data


class DispensaLegalAdminForms(forms.ModelForm):

    def clean(self):
        cleaned_data = super(DispensaLegalAdminForms, self).clean()

        dias_uteis = cleaned_data.get("dias_uteis")
        if dias_uteis and dias_uteis != 0:
            msg = _(u"Dias úteis não é mais um campo válido. Remover o valor e atualizar o campo de dias corridos.")
            self._errors["dias_uteis"] = self.error_class([msg])
            del cleaned_data["dias_uteis"]

        horas = cleaned_data.get("horas")
        if horas and horas >= 8:
            msg = _(u"Campo de horas deve ser menor que 8h")
            self._errors["horas"] = self.error_class([msg])
            del cleaned_data["horas"]

        minutos = cleaned_data.get("minutos")
        if minutos and minutos >= 60:
            msg = _(u"Campo de minutos deve ser menor que 60min")
            self._errors["minutos"] = self.error_class([msg])
            del cleaned_data["minutos"]

        dias_corridos = cleaned_data.get("dias_corridos")
        if (not dias_corridos or dias_corridos == 0) and (not horas or horas == 0) and (not minutos or minutos == 0):
            msg = _(u"Deve haver ao menos um lançamento de duração da dispensa.")
            self._errors["dias_corridos"] = self.error_class([msg])
            self._errors["horas"] = self.error_class([msg])
            self._errors["minutos"] = self.error_class([msg])

        return cleaned_data
