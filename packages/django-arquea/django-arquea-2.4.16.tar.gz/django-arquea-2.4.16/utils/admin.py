# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
import operator
from widgets import ForeignKeySearchInput
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.admin import RelatedFieldListFilter
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound
from django.template.response import TemplateResponse
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from functions import render_to_pdf_weasy


class AutoCompleteAdmin(admin.ModelAdmin):
    """
    Define metodos para o uso da funcao do 'autocomplete' em campos de chave estrangeira
    sem a necessidade de um select, utilizando apenas um campo de texto.
    Para utiliza-la basta criar uma classe de admin para o seu modelo, herdando desta classe
    ao inves de herdar do ModelAdmin. Nessa classe, defina o atributo related_field_search
    para os campos em que deseja utilizar esta funcao, com os campos onde deve ser feita a busca.
    """

    def __call__(self, request, url):
        if url is None:
            pass
        elif url == 'search':
            return self.search(request)
        return super(AutoCompleteAdmin, self).__call__(request, url)

    def search(self, request):
        """
        Searches in the fields of the given related model and returns the
        result as a simple string to be used by the jQuery Autocomplete plugin
        """
        query = request.GET.get('q', None)
        app_label = request.GET.get('app_label', None)
        model_name = request.GET.get('model_name', None)
        search_fields = request.GET.get('search_fields', None)

        if search_fields and app_label and model_name and query:
            def construct_search(field_name):
                # use different lookup methods depending on the notation
                if field_name.startswith('^'):
                    return "%s__istartswith" % field_name[1:]
                elif field_name.startswith('='):
                    return "%s__iexact" % field_name[1:]
                elif field_name.startswith('@'):
                    return "%s__search" % field_name[1:]
                else:
                    return "%s__icontains" % field_name

            model = models.get_model(app_label, model_name)  # @UndefinedVariable
            qs = model._default_manager.all()
            for bit in query.split():
                or_queries = [models.Q(**{construct_search(
                    smart_str(field_name)): smart_str(bit)})
                              for field_name in search_fields.split(',')]
                other_qs = QuerySet(model)
                other_qs.dup_select_related(qs)
                other_qs = other_qs.filter(reduce(operator.or_, or_queries))
                qs = qs & other_qs
            data = ''.join([u'%s|%s\n' % (f.__unicode__(), f.pk) for f in qs])
            return HttpResponse(data)
        return HttpResponseNotFound()

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overrides the default widget for Foreignkey fields if they are
        specified in the related_search_fields class attribute.
        """
        if isinstance(db_field, models.ForeignKey) and \
                db_field.name in self.related_search_fields:

            kwargs['widget'] = ForeignKeySearchInput(db_field.rel,
                                                     self.related_search_fields[db_field.name])
        return super(AutoCompleteAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class PrintModelAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        if request.method == 'GET' and request.GET.get('pdf') == '1':
            o = request.GET.get('o')
            q = request.GET.copy()
            del q['pdf']
            if o and self.actions is not None:
                try:
                    o = int(o)
                    q['o'] = o - 1
                except:
                    pass
            request.GET = q
            lpp = self.list_per_page
            self.list_per_page = 4000000000
            ldl = self.list_display_links
            self.list_display_links = (None,)
            actions = self.actions
            self.actions = None
            page = super(PrintModelAdmin, self).changelist_view(request, extra_context)
            self.list_per_page = lpp
            self.list_display_links = ldl
            self.actions = actions
            if isinstance(page, TemplateResponse):
                page = render_to_pdf_weasy('admin/change_list.pdf', page.resolve_context(page.context_data),
                                           filename='list_%s.pdf' % self.opts.model_name)
        else:
            if extra_context:
                extra_context = extra_context.update({'pdf': True})
            else:
                extra_context = {'pdf': True}
            page = super(PrintModelAdmin, self).changelist_view(request, extra_context)
        return page


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            output.append(u'<br><img src="%s" alt="%s" style="max-width:400px;max-height:400px;"/><br> %s ' %
                          (image_url, image_url, '',))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

