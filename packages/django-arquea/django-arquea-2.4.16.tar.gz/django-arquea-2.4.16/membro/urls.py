# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('membro.views',
                       (r'controle$', 'controle'),
                       (r'mensal/(?P<ano>\d+)/(?P<mes>\d+)$', 'mensal'),
                       (r'detalhes$', 'detalhes'),
                       (r'obs/(?P<controle_id>\d+)$', 'observacao'),
                       (r'mensalf$', 'mensal_func'),
                       (r'logs$', 'uso_admin'),
                       )
