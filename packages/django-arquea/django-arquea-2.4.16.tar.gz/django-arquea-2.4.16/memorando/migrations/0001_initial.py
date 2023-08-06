# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '__first__'),
        ('identificacao', '__first__'),
        ('membro', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'memorando')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Corpo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resposta', models.TextField()),
                ('anexo', models.FileField(upload_to=b'memorando', null=True, verbose_name='Anexo (em pdf)', blank=True)),
                ('concluido', models.BooleanField(default=False, verbose_name=b'Ok')),
            ],
            options={
                'ordering': ('pergunta__numero', 'memorando__data'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Aguardando assinatura', unique=True, max_length=30, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemorandoFAPESP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero do memorando')),
                ('arquivo', models.FileField(null=True, upload_to=b'memorando', blank=True)),
                ('termo', models.ForeignKey(to='outorga.Termo')),
            ],
            options={
                'verbose_name': 'Memorando da FAPESP',
                'verbose_name_plural': 'Memorandos da FAPESP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemorandoResposta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(editable=False)),
                ('anexa_relatorio', models.BooleanField(default=False, verbose_name='Anexar relat\xf3rio de invent\xe1rio?')),
                ('data', models.DateField()),
                ('arquivo', models.FileField(upload_to=b'memorando', null=True, verbose_name=b'Documento assinado', blank=True)),
                ('protocolo', models.FileField(null=True, upload_to=b'memorando', blank=True)),
                ('obs', models.TextField(null=True, blank=True)),
                ('introducao', models.TextField(null=True, verbose_name='Introdu\xe7\xe3o', blank=True)),
                ('conclusao', models.TextField(null=True, verbose_name='Conclus\xe3o', blank=True)),
                ('assinatura', models.ForeignKey(to='membro.Assinatura')),
                ('assunto', models.ForeignKey(to='memorando.Assunto')),
                ('estado', models.ForeignKey(to='memorando.Estado')),
                ('identificacao', models.ForeignKey(verbose_name='Identifica\xe7\xe3o', to='identificacao.Identificacao')),
                ('memorando', models.ForeignKey(to='memorando.MemorandoFAPESP')),
            ],
            options={
                'ordering': ('data',),
                'verbose_name': 'Memorando de resposta \xe0 FAPESP',
                'verbose_name_plural': 'Memorandos de resposta \xe0 FAPESP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemorandoSimples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('superior', models.IntegerField(default=3)),
                ('inferior', models.IntegerField(default=2)),
                ('esquerda', models.IntegerField(default=3)),
                ('direita', models.IntegerField(default=3)),
                ('data', models.DateField(auto_now_add=True)),
                ('destinatario', models.TextField(verbose_name='Destinat\xe1rio')),
                ('numero', models.IntegerField(editable=False)),
                ('corpo', models.TextField()),
                ('equipamento', models.BooleanField(default=False, verbose_name=b'Equipamento?')),
                ('envio', models.BooleanField(default=False, verbose_name=b'Envio?')),
                ('assinado', models.FileField(upload_to=b'memorandos', null=True, verbose_name='Memorando assinado', blank=True)),
                ('assinatura', models.ForeignKey(to='membro.Membro')),
                ('assunto', models.ForeignKey(to='memorando.Assunto', null=True)),
                ('pai', models.ForeignKey(verbose_name='Memorando pai', blank=True, to='memorando.MemorandoSimples', null=True)),
            ],
            options={
                'ordering': ('-data',),
                'verbose_name_plural': 'Memorandos Simples',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pergunta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=10, verbose_name='N\xfamero da pergunta')),
                ('questao', models.TextField(verbose_name='Quest\xe3o')),
                ('memorando', models.ForeignKey(to='memorando.MemorandoFAPESP')),
            ],
            options={
                'ordering': ('numero',),
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
                'permissions': (('rel_adm_memorando', 'Rel. Adm. - Memorandos FAPESP'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='corpo',
            name='memorando',
            field=models.ForeignKey(to='memorando.MemorandoResposta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='corpo',
            name='pergunta',
            field=models.ForeignKey(to='memorando.Pergunta'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivo',
            name='memorando',
            field=models.ForeignKey(to='memorando.MemorandoSimples'),
            preserve_default=True,
        ),
    ]
