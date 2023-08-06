# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membro', '__first__'),
        ('outorga', '0002_auto_20150517_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaOperacional',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '\xc1rea operacional',
                'verbose_name_plural': '\xc1reas operacionais',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaPrograma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': '\xc1rea do programa',
                'verbose_name_plural': '\xc1reas dos programas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Atribuicao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('relatorio', models.FileField(upload_to=b'evento', null=True, verbose_name='Relat\xf3rio', blank=True)),
                ('area', models.ForeignKey(verbose_name='\xc1rea operacional', to='evento.AreaOperacional')),
                ('membro', models.ForeignKey(to='membro.Membro')),
            ],
            options={
                'verbose_name': 'Atribui\xe7\xe3o',
                'verbose_name_plural': 'Atribui\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=200, verbose_name='Descri\xe7\xe3o')),
                ('inicio', models.DateTimeField(verbose_name='In\xedcio')),
                ('termino', models.DateTimeField(verbose_name='T\xe9rmino')),
                ('url', models.URLField(null=True, verbose_name='URL', blank=True)),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('acordo', models.ForeignKey(blank=True, to='outorga.Acordo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sessao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
                ('local', models.CharField(max_length=100)),
                ('inicio', models.DateTimeField(verbose_name='In\xedcio')),
                ('termino', models.DateTimeField(verbose_name='T\xe9rmino')),
                ('arquivo', models.FileField(null=True, upload_to=b'sessao', blank=True)),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('area', models.ForeignKey(verbose_name='\xc1rea', to='evento.AreaPrograma')),
                ('evento', models.ForeignKey(to='evento.Evento')),
            ],
            options={
                'verbose_name': 'Sess\xe3o',
                'verbose_name_plural': 'Sess\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.ForeignKey(to='evento.Tipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atribuicao',
            name='sessao',
            field=models.ForeignKey(verbose_name='Sess\xe3o', to='evento.Sessao'),
            preserve_default=True,
        ),
    ]
