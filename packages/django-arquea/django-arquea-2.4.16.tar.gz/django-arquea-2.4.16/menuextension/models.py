# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import Library
from treemenus.models import MenuItem


register = Library()


class MenuItemExtension(models.Model):
    menu_item = models.OneToOneField(MenuItem, related_name="extension")
    visivel = models.BooleanField(default=False)
    css = models.CharField(_(u'CSS style'), null=True, blank=True, max_length=300)
