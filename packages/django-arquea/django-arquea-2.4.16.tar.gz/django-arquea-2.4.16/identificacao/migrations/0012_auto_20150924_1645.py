# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '0011_auto_20150924_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enderecodetalhe',
            name='mostra_bayface',
            field=models.BooleanField(default=False, help_text='', verbose_name='Mostra no bayface'),
        ),
        migrations.AlterField(
            model_name='identificacao',
            name='historico',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 16, 45, 2, 614312), verbose_name='Hist\xf3rico', editable=False),
        ),
    ]
