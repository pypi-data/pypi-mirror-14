# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('carga.views',
                       (r'upload_planilha_patrimonio$', 'upload_planilha_patrimonio'),
                       (r'list_planilha_patrimonio$', 'list_planilha_patrimonio'),
                       (r'$', 'list_planilha_patrimonio'),
                       )
