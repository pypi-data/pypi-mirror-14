# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import outorga.models
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acordo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o')),
            ],
            options={
                'ordering': ('descricao',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=outorga.models.upload_dir)),
            ],
            options={
                'ordering': ('id',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArquivoOS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=outorga.models.upload_dir_os)),
                ('data', models.DateField()),
                ('historico', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Aditivo', unique=True, max_length=60, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=20, verbose_name='N\xfamero')),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
                ('data_inicio', utils.models.NARADateField(verbose_name='In\xedcio')),
                ('auto_renova', models.BooleanField(default=False, verbose_name='Auto renova\xe7\xe3o?')),
                ('limite_rescisao', utils.models.NARADateField(null=True, verbose_name='t\xe9rmino', blank=True)),
                ('arquivo', models.FileField(upload_to=b'contrato')),
                ('anterior', models.ForeignKey(verbose_name='Contrato anterior', blank=True, to='outorga.Contrato', null=True)),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Vigente', unique=True, max_length=30, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstadoOS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Estado da OS',
                'verbose_name_plural': 'Estados das OSs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(help_text='ex. Loca\xe7\xe3o e armazenamento especializado na Granero Tech.', max_length=255, verbose_name='Descri\xe7\xe3o')),
                ('justificativa', models.TextField(verbose_name='Justificativa')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o', blank=True)),
                ('valor', models.DecimalField(help_text='ex. 150500.50', verbose_name='Valor Concedido', max_digits=12, decimal_places=2)),
                ('entidade', models.ForeignKey(verbose_name='Entidade', to='identificacao.Entidade', null=True)),
            ],
            options={
                'ordering': ('-natureza_gasto__termo__ano', 'descricao'),
                'verbose_name': 'Item do Or\xe7amento',
                'verbose_name_plural': 'Itens do Or\xe7amento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Modalidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(help_text='ex. STB', unique=True, max_length=10, verbose_name='Sigla', blank=True)),
                ('nome', models.CharField(help_text='ex. Servi\xe7os de Terceiros no Brasil', max_length=40, verbose_name='Nome', blank=True)),
                ('moeda_nacional', models.BooleanField(default=True, help_text='ex. Moeda Nacional?', verbose_name='R$')),
            ],
            options={
                'ordering': ('sigla',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Natureza_gasto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor_concedido', models.DecimalField(help_text='ex. 150500.50', verbose_name='Valor Concedido', max_digits=12, decimal_places=2)),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o', blank=True)),
                ('modalidade', models.ForeignKey(verbose_name='Modalidade', to='outorga.Modalidade')),
            ],
            options={
                'ordering': ('-termo__ano',),
                'verbose_name': 'Pasta',
                'verbose_name_plural': 'Pastas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrigemFapesp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acordo', models.ForeignKey(to='outorga.Acordo')),
                ('item_outorga', models.ForeignKey(verbose_name='Item de Outorga', to='outorga.Item')),
            ],
            options={
                'ordering': ('item_outorga',),
                'verbose_name': 'Origem FAPESP',
                'verbose_name_plural': 'Origem FAPESP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Outorga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('termino', utils.models.NARADateField(help_text='T\xe9rmino da vig\xeancia do processo', verbose_name='T\xe9rmino')),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o', blank=True)),
                ('data_presta_contas', utils.models.NARADateField(help_text='Data de Presta\xe7\xe3o de Contas', null=True, verbose_name='Prest. Contas', blank=True)),
                ('data_solicitacao', utils.models.NARADateField(help_text='Data de Solicita\xe7\xe3o do Pedido de Concess\xe3o', verbose_name='Solicita\xe7\xe3o')),
                ('arquivo', models.FileField(null=True, upload_to=outorga.models.upload_dir, blank=True)),
                ('protocolo', models.FileField(null=True, upload_to=outorga.models.upload_dir, blank=True)),
                ('categoria', models.ForeignKey(verbose_name='Categoria', to='outorga.Categoria')),
            ],
            options={
                'ordering': ('data_solicitacao',),
                'verbose_name': 'Concess\xe3o',
                'verbose_name_plural': 'Hist\xf3rico de Concess\xf5es',
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
                'permissions': (('rel_ger_acordo_progressivo', 'Rel. Ger. - Gerencial progressivo'), ('rel_ger_contratos', 'Rel. Ger. - Contratos'), ('rel_adm_item_modalidade', 'Rel. Adm. - Itens do or\xe7amento por modalidade'), ('rel_ger_lista_acordos', 'Rel. Ger. - Concess\xf5es por acordo')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Termo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ano', models.IntegerField(default=0, help_text='ex. 2008', verbose_name='Ano')),
                ('processo', models.IntegerField(default=0, help_text='ex. 52885', verbose_name='Processo')),
                ('digito', models.IntegerField(default=0, help_text='ex. 8', verbose_name='D\xedgito')),
                ('inicio', utils.models.NARADateField(help_text='Data de in\xedcio do processo', null=True, verbose_name='In\xedcio', blank=True)),
                ('parecer', models.FileField(upload_to=b'termo', null=True, verbose_name='Parecer inicial', blank=True)),
                ('parecer_final', models.FileField(upload_to=b'termo', null=True, verbose_name='Parecer final', blank=True)),
                ('projeto', models.FileField(upload_to=b'termo', null=True, verbose_name='Projeto', blank=True)),
                ('orcamento', models.FileField(upload_to=b'termo', null=True, verbose_name='Or\xe7amento', blank=True)),
                ('quitacao', models.FileField(upload_to=b'termo', null=True, verbose_name='Quita\xe7\xe3o', blank=True)),
                ('doacao', models.FileField(upload_to=b'termo', null=True, verbose_name='Doa\xe7\xe3o', blank=True)),
                ('extrato_financeiro', models.FileField(null=True, upload_to=b'termo', blank=True)),
                ('relatorio_final', models.FileField(upload_to=b'termo', null=True, verbose_name='Relat\xf3rio Final', blank=True)),
                ('exibe_rel_ger_progressivo', models.BooleanField(default=True, verbose_name='Exibe o processo no Relat\xf3rio Gerencial Progressivo?')),
                ('estado', models.ForeignKey(verbose_name='Estado', to='outorga.Estado')),
                ('modalidade', models.ManyToManyField(to='outorga.Modalidade', verbose_name='Pasta', through='outorga.Natureza_gasto')),
            ],
            options={
                'ordering': ('-ano',),
                'verbose_name': 'Termo de Outorga',
                'verbose_name_plural': 'Termos de Outorga',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoContrato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Tipo de documento',
                'verbose_name_plural': 'Tipos de documento',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='outorga',
            name='termo',
            field=models.ForeignKey(verbose_name='Termo', to='outorga.Termo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='natureza_gasto',
            name='termo',
            field=models.ForeignKey(verbose_name='Termo de outorga', to='outorga.Termo'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='natureza_gasto',
            unique_together=set([('modalidade', 'termo')]),
        ),
        migrations.AddField(
            model_name='item',
            name='natureza_gasto',
            field=models.ForeignKey(verbose_name='Pasta', to='outorga.Natureza_gasto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivo',
            name='outorga',
            field=models.ForeignKey(related_name='arquivos', to='outorga.Outorga'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='arquivo',
            unique_together=set([('arquivo', 'outorga')]),
        ),
        migrations.AddField(
            model_name='acordo',
            name='estado',
            field=models.ForeignKey(to='outorga.Estado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acordo',
            name='itens_outorga',
            field=models.ManyToManyField(to='outorga.Item', through='outorga.OrigemFapesp'),
            preserve_default=True,
        ),
    ]
