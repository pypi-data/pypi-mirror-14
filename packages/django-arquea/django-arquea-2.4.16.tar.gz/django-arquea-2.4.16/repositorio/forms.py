# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.forms.utils import ErrorList
from django.db.models import Q
from repositorio.models import Repositorio, Tipo
from patrimonio.models import Patrimonio
from memorando.models import MemorandoSimples
from membro.models import Membro


class RepositorioAdminForm(forms.ModelForm):
    filtra_patrimonio = forms.CharField(label=u'Filtro do patrimônio', required=False,
                                        widget=forms.TextInput(attrs={'onchange': 'ajax_filter_patrimonio(this.value);',
                                                                      'class': 'auxiliary'}))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=':',
                 empty_permitted=False, instance=None):
        super(RepositorioAdminForm, self).__init__(data, files, auto_id, prefix, initial,
                                                   error_class, label_suffix, empty_permitted, instance)

        pt = self.fields['patrimonios']

        if data:
            search_string = data['filtra_patrimonio']
            # Recuperando o dado do filtro do patrimonio, senão o form vai buscar todos os patrimonios
            if search_string:
                pt.queryset = Patrimonio.objects.filter(Q(ns__icontains=search_string) |
                                                        Q(descricao__icontains=search_string) |
                                                        Q(pagamento__protocolo__num_documento__icontains=search_string))
            else:
                pt.queryset = Patrimonio.objects.filter(id__in=[0])
        elif instance:
            pt.queryset = instance.patrimonios
        else:
            pt.queryset = Patrimonio.objects.filter(id__in=[0])

        self.fields['anterior'].choices = [('', '---------')] + \
                                          [(p.id, p.__unicode__())
                                           for p in Repositorio.objects.all()
                                              .select_related('tipo', 'tipo__entidade', 'responsavel')
                                              .order_by('-data', '-numero', 'tipo')]
        self.fields['tipo'].choices = [('', '---------')] + \
                                      [(p.id, p.__unicode__())
                                       for p in Tipo.objects.all().select_related('entidade')
                                          .order_by('entidade__sigla', 'nome')]
        self.fields['responsavel'].choices = [('', '---------')] + \
                                             [(p.id, p.__unicode__())
                                              for p in Membro.objects
                                                 .filter(historico__funcionario=True, historico__termino__isnull=True)
                                                 .order_by('nome')]
        self.fields['demais'].choices = [(p.id, p.__unicode__())
                                         for p in Membro.objects.all()
                                                        .order_by('nome')]
        self.fields['memorandos'].choices = [(p.id, p.__unicode__())
                                             for p in MemorandoSimples.objects.all()
                                                                      .select_related('assunto')
                                                                      .order_by('-data', '-numero')]

    class Meta:
        model = Repositorio
        fields = ['data_ocorrencia', 'tipo', 'natureza', 'estado', 'servicos', 'ocorrencia', 'anterior', 'memorandos',
                  'filtra_patrimonio', 'patrimonios', 'responsavel', 'demais', 'obs']

    class Media:
        js = ('js/selects.js', )
