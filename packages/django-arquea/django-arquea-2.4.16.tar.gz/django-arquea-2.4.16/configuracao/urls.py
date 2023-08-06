# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('configuracao.views',
                       (r'^help/(\w+)/(\w+)/$', 'help_text'),
                       (r'^tooltip/(\w+)/(\w+)$', 'tooltip'),
                       (r'^has_help/(\w+)/(\w+)/$', 'has_help_text')
                       )
