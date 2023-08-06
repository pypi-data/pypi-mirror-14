# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controle',
            name='membro',
            field=models.ForeignKey(verbose_name='Membro', to='membro.Membro'),
        ),
    ]
