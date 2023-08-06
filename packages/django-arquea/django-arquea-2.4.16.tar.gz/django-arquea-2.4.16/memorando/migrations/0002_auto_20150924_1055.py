# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorando', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memorandosimples',
            options={'ordering': ('-data', '-numero'), 'verbose_name_plural': 'Memorandos Simples'},
        ),
    ]
