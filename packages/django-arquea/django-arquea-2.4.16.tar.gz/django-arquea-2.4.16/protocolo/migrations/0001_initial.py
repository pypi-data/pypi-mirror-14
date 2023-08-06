# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import protocolo.models


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0002_auto_20150517_1724'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('identificacao', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=protocolo.models.upload_dir)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Descricao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=200)),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
                'ordering': ('entidade', 'descricao'),
                'verbose_name': 'Descri\xe7\xe3o',
                'verbose_name_plural': 'Descri\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text=b'ex. Pendente', unique=True, max_length=30, verbose_name='Nome')),
            ],
            options={
                'ordering': ('-nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feriado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feriado', models.DateField(unique=True, verbose_name='Feriado')),
                ('obs', models.CharField(max_length=100, verbose_name='Observa\xe7\xe3o', blank=True)),
            ],
            options={
                'ordering': ('feriado',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItemProtocolo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.TextField(help_text='ex. Despesas da linha 3087-1500 ref. 10/2008', verbose_name='Descri\xe7\xe3o')),
                ('quantidade', models.IntegerField(default=1, help_text='ex. 1', verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(help_text='ex. 286.50', verbose_name='Valor unit\xe1rio', max_digits=12, decimal_places=2)),
                ('ordem_servico', models.ForeignKey(verbose_name='Ordem de Servi\xe7o', blank=True, to='outorga.OrdemDeServico', null=True)),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Item do protocolo',
                'verbose_name_plural': 'Itens do protocolo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Origem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text=b'ex. Correio', unique=True, max_length=20, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Origem',
                'verbose_name_plural': 'Origens',
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
                'permissions': (('rel_adm_descricao', 'Rel. Adm. - Protocolos por descri\xe7\xe3o'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Protocolo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_documento', models.CharField(help_text='ex. 11000-69.356/10/08-00002/00003', max_length=50, verbose_name='N\xfamero', blank=True)),
                ('data_chegada', models.DateTimeField(verbose_name='Recebido em')),
                ('data_vencimento', models.DateField(null=True, verbose_name='Data de vencimento', blank=True)),
                ('data_validade', models.DateField(help_text='ex. Data da validade de uma cota\xe7\xe3o/contrato', null=True, verbose_name='Data de validade', blank=True)),
                ('descricao', models.CharField(default=b'x-x-x', help_text='ex. Conta telef\xf4nica da linha 3087-1500', max_length=200, verbose_name='Descri\xe7\xe3o antiga')),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o', blank=True)),
                ('moeda_estrangeira', models.BooleanField(default=False, help_text='O valor do documento est\xe1 em dolar?', verbose_name='D\xf3lar?')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=12, blank=True, help_text='\xc9 a soma dos valores dos documentos tratados por este protocolo.', null=True, verbose_name='Valor total')),
                ('referente', models.CharField(max_length=100, null=True, verbose_name='Referente', blank=True)),
            ],
            options={
                'ordering': ('descricao', '-data_chegada', 'data_vencimento'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cotacao',
            fields=[
                ('protocolo_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='protocolo.Protocolo')),
                ('parecer', models.TextField(help_text='Justificativa para aceitar ou rejeitar esta cota\xe7\xe3o', verbose_name='Parecer T\xe9cnico', blank=True)),
                ('aceito', models.BooleanField(default=False, help_text='Essa cota\xe7\xe3o foi aceita?', verbose_name='Aceito?')),
                ('entrega', models.CharField(help_text=' ', max_length=20, verbose_name='Entrega', blank=True)),
            ],
            options={
                'ordering': ('-data_chegada',),
                'verbose_name': 'Cota\xe7\xe3o',
                'verbose_name_plural': 'Cota\xe7\xf5es',
            },
            bases=('protocolo.protocolo',),
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text=b'ex. Nota Fiscal', unique=True, max_length=100, verbose_name='Nome')),
                ('sigla', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoFeriado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
                ('movel', models.BooleanField(default=False, verbose_name='M\xf3vel')),
                ('dia', models.IntegerField(null=True, verbose_name='Dia', blank=True)),
                ('mes', models.IntegerField(null=True, verbose_name='Mes', blank=True)),
                ('subtrai_banco_hrs', models.BooleanField(default=False, verbose_name='Subtrai do banco de horas?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='protocolo',
            name='descricao2',
            field=models.ForeignKey(verbose_name='Descri\xe7\xe3o', to='protocolo.Descricao', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='estado',
            field=models.ForeignKey(verbose_name='Estado', to='protocolo.Estado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='identificacao',
            field=models.ForeignKey(verbose_name='Identifica\xe7\xe3o', to='identificacao.Identificacao', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='origem',
            field=models.ForeignKey(verbose_name='Origem', blank=True, to='protocolo.Origem', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='procedencia',
            field=models.ForeignKey(verbose_name='Proced\xeancia', blank=True, to='identificacao.Entidade', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='protocolo',
            field=models.ForeignKey(related_name='anterior', verbose_name='Protocolo anterior', blank=True, to='protocolo.Protocolo', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='responsavel',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text='T\xe9cnico respons\xe1vel pelas cota\xe7\xf5es', null=True, verbose_name='Respons\xe1vel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='termo',
            field=models.ForeignKey(verbose_name='Termo', to='outorga.Termo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='protocolo',
            name='tipo_documento',
            field=models.ForeignKey(verbose_name='Documento', to='protocolo.TipoDocumento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='itemprotocolo',
            name='protocolo',
            field=models.ForeignKey(verbose_name='Protocolo', to='protocolo.Protocolo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feriado',
            name='tipo',
            field=models.ForeignKey(blank=True, to='protocolo.TipoFeriado', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivo',
            name='protocolo',
            field=models.ForeignKey(to='protocolo.Protocolo'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='arquivo',
            unique_together=set([('arquivo', 'protocolo')]),
        ),
    ]
