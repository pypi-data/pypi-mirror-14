# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0003_auto_20150811_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templatert',
            options={'verbose_name': 'Template Reserva T\xe9cnica', 'verbose_name_plural': 'Templates Reserva T\xe9cnica'},
        ),
        migrations.AlterField(
            model_name='item',
            name='rt',
            field=models.BooleanField(default=False, verbose_name='Reserva t\xe9cnica?'),
        ),
    ]
