# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '0004_auto_20150517_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identificacao',
            name='historico',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 17, 18, 6, 1, 8306), verbose_name='Hist\xf3rico', editable=False),
            preserve_default=True,
        ),
    ]
