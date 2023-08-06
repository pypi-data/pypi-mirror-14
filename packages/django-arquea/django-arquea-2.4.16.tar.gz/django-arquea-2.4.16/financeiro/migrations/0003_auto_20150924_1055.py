# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_auto_20150811_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extratocc',
            name='cod_oper',
            field=models.IntegerField(help_text='C\xf3digo com m\xe1ximo de 10 d\xedgitos.', verbose_name='Documento', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
