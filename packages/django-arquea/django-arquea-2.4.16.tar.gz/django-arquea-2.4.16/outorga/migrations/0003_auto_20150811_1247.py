# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0002_auto_20150517_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateRT',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=255, verbose_name='Descri\xe7\xe3o')),
                ('modalidade', models.ForeignKey(to='outorga.Modalidade')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='rt',
            field=models.BooleanField(default=False),
        ),
    ]
