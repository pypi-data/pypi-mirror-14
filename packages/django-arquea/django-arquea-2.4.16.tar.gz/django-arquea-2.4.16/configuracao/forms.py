# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.html import mark_safe
from ckeditor.widgets import CKEditorWidget
from .models import ClassesExtra


class ContentTypeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '%s/%s' % (obj.app_label, obj.model)


class ClassesExtraForm(forms.ModelForm):
    content_type = ContentTypeChoiceField(queryset=ContentType.objects.order_by('app_label', 'model'))
    help = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = ClassesExtra
        fields = '__all__'


class LayoutPaginaAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LayoutPaginaAdminForm, self).__init__(*args, **kwargs)

        self.fields['logo_cabecalho'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/configuracao/layoutlogo/\'+'
                                                        '$(\'#id_logo_cabecalho\').val() + \'/\', \'_blank\');'
                                                        'return true;">Logo do cabecalho</a> (185x150)')

        self.fields['logo_rodape'].label = mark_safe('<a href="#" onclick="window.open(\'/admin/configuracao/layoutlogo/\'+'
                                                     '$(\'#id_logo_rodape\').val() + \'/\', \'_blank\');'
                                                     'return true;">Logo do rodape</a> (150x150)')
