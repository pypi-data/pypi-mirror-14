# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import Truncator


class ForeignKeySearchInput(forms.HiddenInput):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input
    instead in a <select> box.
    """
    class Media:
        css = {
            'all': ('/site-media/css/jquery.autocomplete.css',)
        }
        js = (
            '/site-media/js/lib/jquery.js',
            '/site-media/js/lib/jquery.bgiframe.min.js',
            '/site-media/js/lib/jquery.ajaxQueue.js',
            '/site-media/js/jquery.autocomplete.js'
        )

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        trunc = Truncator(obj)
        return trunc.words(obj, 14)

    def __init__(self, rel, search_fields, attrs=None):
        self.rel = rel
        self.search_fields = search_fields
        super(ForeignKeySearchInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(ForeignKeySearchInput, self).render(name, value, attrs)
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        return rendered + mark_safe(u'''
            <style type="text/css" media="screen">
                #lookup_%(name)s {
                    padding-right:16px;
                    background: url(
                        %(admin_media_prefix)simg/admin/selector-search.gif
                    ) no-repeat right;
                }
                #del_%(name)s {
                    display: none;
                }
            </style>
<input type="text" id="lookup_%(name)s" value="%(label)s" />
<a href="#" id="del_%(name)s">
<img src="%(admin_media_prefix)simg/admin/icon_deletelink.gif" />
</a>
<script type="text/javascript">
            if ($('#lookup_%(name)s').val()) {
                $('#del_%(name)s').show()
            }
            $('#lookup_%(name)s').autocomplete('../search/', {
                extraParams: {
                    search_fields: '%(search_fields)s',
                    app_label: '%(app_label)s',
                    model_name: '%(model_name)s',
                },
            }).result(function(event, data, formatted) {
                if (data) {
                    $('#id_%(name)s').val(data[1]);
                    $('#del_%(name)s').show();
                }
            });
            $('#del_%(name)s').click(function(ele, event) {
                $('#id_%(name)s').val('');
                $('#del_%(name)s').hide();
                $('#lookup_%(name)s').val('');
            });
            </script>
        ''') % {
            'search_fields': ','.join(self.search_fields),
            'admin_media_prefix': settings.ADMIN_MEDIA_PREFIX,
            'model_name': self.rel.to._meta.model_name,
            'app_label': self.rel.to._meta.app_label,
            'label': label,
            'name': name,
        }


class PlainTextWidget(forms.Widget):

    def render(self, name, value, attrs=None):
        if value is None:
            v = ''
        else:
            v = mark_safe(value)
        return mark_safe(u'<span name="%s" id="id_%s">%s</span>' % (name, name, v))
