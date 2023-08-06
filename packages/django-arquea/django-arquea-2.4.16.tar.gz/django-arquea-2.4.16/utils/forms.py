# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django import forms
from django.contrib.admin.widgets import AdminDateWidget


NARA_DATE_FORMATS = ('%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d')


class NARADateField(forms.DateField):

    def __init__(self, input_formats=None, *args, **kwargs):
        super(NARADateField, self).__init__(input_formats=NARA_DATE_FORMATS, *args, **kwargs)
        self.widget = AdminDateWidget()
