# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memorando', '0001_initial'),
        ('membro', '0001_initial'),
        ('identificacao', '0005_auto_20150517_1806'),
        ('patrimonio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anexo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'repositorio')),
                ('palavras_chave', models.TextField(verbose_name='Palavras chave')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Natureza',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('nome',),
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
                'permissions': (('rel_ger_repositorio', 'Rel. admin. - Reposit\xf3rio'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repositorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(editable=False)),
                ('data', models.DateField(auto_now_add=True, verbose_name='Data de registro')),
                ('data_ocorrencia', models.DateField(verbose_name='Data da ocorr\xeancia')),
                ('ocorrencia', models.TextField(verbose_name='Ocorr\xeancia')),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('anterior', models.ForeignKey(blank=True, to='repositorio.Repositorio', help_text='Item do reposit\xf3rio ao qual este se refere', null=True)),
                ('demais', models.ManyToManyField(related_name='outros', null=True, verbose_name=b'Demais envolvidos', to='membro.Membro', blank=True)),
                ('estado', models.ForeignKey(help_text='Pendente, resolvido, etc.', to='repositorio.Estado')),
                ('memorandos', models.ManyToManyField(to='memorando.MemorandoSimples', null=True, blank=True)),
                ('natureza', models.ForeignKey(help_text='Problema, incidente, etc.', to='repositorio.Natureza')),
                ('patrimonios', models.ManyToManyField(to='patrimonio.Patrimonio', null=True, verbose_name=b'Patrim\xc3\xb4nios', blank=True)),
                ('responsavel', models.ForeignKey(verbose_name=b'Respons\xc3\xa1vel', to='membro.Membro')),
            ],
            options={
                'verbose_name': 'Reposit\xf3rio',
                'verbose_name_plural': 'Reposit\xf3rios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.IntegerField()),
                ('repositorio', models.ForeignKey(to='repositorio.Repositorio')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
                'ordering': ('entidade__sigla', 'nome'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='repositorio',
            name='servicos',
            field=models.ManyToManyField(help_text='Servi\xe7os envolvidos', to='repositorio.Servico', null=True, verbose_name='Servi\xe7os', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='repositorio',
            name='tipo',
            field=models.ForeignKey(help_text='Di\xe1rio de bordo, manuten\xe7\xe3o, etc.', to='repositorio.Tipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='anexo',
            name='repositorio',
            field=models.ForeignKey(to='repositorio.Repositorio'),
            preserve_default=True,
        ),
    ]
