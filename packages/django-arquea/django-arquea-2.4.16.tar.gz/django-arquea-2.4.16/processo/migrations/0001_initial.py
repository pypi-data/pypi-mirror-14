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
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
                ('escopo', models.TextField()),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': '\xc1rea',
                'verbose_name_plural': '\xc1reas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Atribuicao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Atribui\xe7\xe3o',
                'verbose_name_plural': 'Atribui\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
                ('membros', models.ManyToManyField(to='membro.Membro')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('area', models.ForeignKey(to='processo.Area')),
            ],
            options={
                'ordering': ('area', 'nome'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Macroprocesso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.TextField()),
                ('grupo', models.ForeignKey(to='processo.Grupo')),
            ],
            options={
                'ordering': ('grupo', 'nome'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Natureza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Norma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=120)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OTRS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=120)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Papel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'Pap\xe9is',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'default_permissions': (),
                'permissions': (('rel_ger_processos', 'Rel. Ger. - Processos'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Procedimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Processo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.TextField(verbose_name=b'Processo')),
                ('obs', models.TextField(null=True, blank=True)),
                ('entrada_otrs', models.ManyToManyField(related_name='entra_otrs', null=True, to='processo.OTRS', blank=True)),
            ],
            options={
                'ordering': ('macroprocesso', 'nome'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=120)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'Vis\xe3o',
                'verbose_name_plural': 'Vis\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='processo',
            name='entradas',
            field=models.ManyToManyField(related_name='entra', null=True, to='processo.Recurso', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='macroprocesso',
            field=models.ForeignKey(to='processo.Macroprocesso'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='natureza',
            field=models.ForeignKey(to='processo.Natureza'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='normas',
            field=models.ManyToManyField(to='processo.Norma', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='saida_otrs',
            field=models.ManyToManyField(related_name='sai_otrs', null=True, to='processo.OTRS', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='saidas',
            field=models.ManyToManyField(related_name='sai', null=True, to='processo.Recurso', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='processo',
            name='visao',
            field=models.ForeignKey(verbose_name='Vis\xe3o', to='processo.Visao'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='procedimento',
            name='processo',
            field=models.ForeignKey(to='processo.Processo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atribuicao',
            name='equipe',
            field=models.ForeignKey(to='processo.Equipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atribuicao',
            name='papel',
            field=models.ForeignKey(to='processo.Papel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='atribuicao',
            name='processo',
            field=models.ForeignKey(to='processo.Processo'),
            preserve_default=True,
        ),
    ]
