# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns


urlpatterns = patterns('memorando.views',
                       (r'simples/(?P<mem>\d+)$', 'simples'),
                       (r'fapesp/(?P<mem>\d+)$', 'fapesp'),
                       (r'relatorio/(?P<mem>\d+)$', 'relatorio'),
                       (r'relatorio$', 'relatorio'),
                       (r'pagamentos$', 'ajax_escolhe_pagamentos'),
                       (r'perguntas$', 'ajax_filtra_perguntas'),
                       (r'escolhe_pergunta$', 'ajax_escolhe_pergunta'),
                       )
