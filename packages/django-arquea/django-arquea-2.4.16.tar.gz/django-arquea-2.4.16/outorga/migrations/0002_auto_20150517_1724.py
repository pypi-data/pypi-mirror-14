# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0001_initial'),
        ('memorando', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemDeServico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=20, verbose_name='N\xfamero')),
                ('data_inicio', utils.models.NARADateField(verbose_name='In\xedcio')),
                ('data_rescisao', utils.models.NARADateField(null=True, verbose_name='T\xe9rmino', blank=True)),
                ('antes_rescisao', models.IntegerField(null=True, verbose_name='Prazo p/ solicitar rescis\xe3o (dias)', blank=True)),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o')),
                ('substituicoes', models.TextField(null=True, blank=True)),
                ('acordo', models.ForeignKey(to='outorga.Acordo')),
                ('contrato', models.ForeignKey(to='outorga.Contrato')),
                ('estado', models.ForeignKey(to='outorga.EstadoOS')),
                ('pergunta', models.ManyToManyField(to='memorando.Pergunta', null=True, blank=True)),
            ],
            options={
                'ordering': ('tipo', 'numero'),
                'verbose_name': 'Altera\xe7\xe3o de contrato (OS)',
                'verbose_name_plural': 'Altera\xe7\xe3o de contratos (OS)',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ordemdeservico',
            name='tipo',
            field=models.ForeignKey(to='outorga.TipoContrato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivoos',
            name='os',
            field=models.ForeignKey(related_name='arquivos', to='outorga.OrdemDeServico'),
            preserve_default=True,
        ),

    ]
