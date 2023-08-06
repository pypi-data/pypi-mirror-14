# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipamento',
            name='ean',
        ),
        migrations.RemoveField(
            model_name='equipamento',
            name='ncm',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='cfop',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='ncm',
        ),
        migrations.RemoveField(
            model_name='patrimonio',
            name='ocst',
        ),
    ]
