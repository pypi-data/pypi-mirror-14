# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import utils.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('memorando', '0001_initial'),
        ('protocolo', '0001_initial'),
        ('membro', '__first__'),
        ('outorga', '0002_auto_20150517_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(null=True, upload_to=b'auditoria', blank=True)),
                ('parcial', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999999)])),
                ('pagina', models.IntegerField()),
                ('obs', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtratoCC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_oper', utils.models.NARADateField(verbose_name='Data da opera\xe7\xe3o')),
                ('cod_oper', models.IntegerField(help_text='C\xf3digo com m\xe1ximo de 9 d\xedgitos.', verbose_name='Documento', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999999)])),
                ('despesa_caixa', models.BooleanField(default=False, verbose_name='Despesa de caixa?')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=12, decimal_places=2)),
                ('historico', models.CharField(max_length=30, verbose_name='Hist\xf3rico')),
                ('cartao', models.BooleanField(default=False, verbose_name='Cart\xe3o?')),
                ('data_extrato', utils.models.NARADateField(null=True, verbose_name='Data do extrato', blank=True)),
                ('imagem', models.ImageField(validators=[django.core.validators.RegexValidator(regex=b'.+((\\.jpg)|.+(\\.jpeg))$', message=b'Enviar somente imagem jpeg. A propor\xc3\xa7\xc3\xa3o da largura / altura deve ser maior que 2.')], upload_to=b'extratocc', blank=True, help_text='Somente imagem .jpeg', null=True, verbose_name='Imagem do cheque')),
                ('capa', models.TextField(null=True, blank=True)),
                ('obs', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-data_oper',),
                'verbose_name': 'Extrato de Conta corrente',
                'verbose_name_plural': 'Extratos de Conta corrente',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtratoFinanceiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_libera', utils.models.NARADateField(verbose_name='Data')),
                ('cod', models.CharField(max_length=4, verbose_name='C\xf3digo', choices=[(b'COMP', b'Concessao Bens/Serv. Pais'), (b'PGMP', b'Pgto. Bens/Serv. Pais'), (b'DVMP', b'Devl. Bens/Serv. Pais'), (b'SUMP', b'Supl. Bens/Serv. Pais'), (b'ANMP', b'Anulacao'), (b'ESMP', b'Estorno ANMP'), (b'CAMP', b'Canc. Bens/Serv. Pais'), (b'CORP', b'Concessao Reserva Tecnica Auxil. Pais'), (b'PGRP', b'Pgto. Reserva Tecnica Auxil. Pais'), (b'DVRP', b'Devl. Reserva Tecnica Auxil. Pais'), (b'SURP', b'Supl. Reserva Tecnica Auxil. Pais'), (b'ANRP', b'Anulacao Reserva Tecnica Auxil. Pais'), (b'ESRP', b'Estorno ANRP'), (b'CARP', b'Canc. Reserva Tecnica Auxil. Pais')])),
                ('historico', models.CharField(max_length=40, verbose_name='Hist\xf3rico')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=12, decimal_places=2)),
                ('comprovante', models.FileField(upload_to=b'extratofinanceiro', null=True, verbose_name='Comprovante da opera\xe7\xe3o', blank=True)),
                ('parcial', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999999)])),
                ('taxas', models.IntegerField(default=0)),
                ('termo', models.ForeignKey(verbose_name='Termo de outorga', to='outorga.Termo')),
            ],
            options={
                'ordering': ('-data_libera',),
                'verbose_name': 'Extrato do Financeiro',
                'verbose_name_plural': 'Extratos do Financeiro',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExtratoPatrocinio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_oper', utils.models.NARADateField(verbose_name='Data da opera\xe7\xe3o')),
                ('cod_oper', models.IntegerField(help_text='C\xf3digo com m\xe1ximo de 9 d\xedgitos.', verbose_name='C\xf3digo da opera\xe7\xe3o', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999999)])),
                ('valor', models.DecimalField(max_digits=12, decimal_places=2)),
                ('historico', models.CharField(max_length=30)),
                ('obs', models.TextField()),
            ],
            options={
                'verbose_name': 'Extrato do patroc\xednio',
                'verbose_name_plural': 'Extratos dos patroc\xednios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocalizaPatrocinio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('consignado', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Localiza\xe7\xe3o do patroc\xednio',
                'verbose_name_plural': 'Localiza\xe7\xe3o dos patroc\xednios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valor_fapesp', models.DecimalField(verbose_name='Valor origin\xe1rio da Fapesp', max_digits=12, decimal_places=2)),
                ('valor_patrocinio', models.DecimalField(null=True, verbose_name='Valor origin\xe1rio de patroc\xednio', max_digits=12, decimal_places=2, blank=True)),
                ('reembolso', models.BooleanField(default=False)),
                ('conta_corrente', models.ForeignKey(blank=True, to='financeiro.ExtratoCC', null=True)),
                ('membro', models.ForeignKey(blank=True, to='membro.Membro', null=True)),
                ('origem_fapesp', models.ForeignKey(blank=True, to='outorga.OrigemFapesp', null=True)),
                ('patrocinio', models.ForeignKey(verbose_name='Extrato do patroc\xednio', blank=True, to='financeiro.ExtratoPatrocinio', null=True)),
                ('pergunta', models.ManyToManyField(to='memorando.Pergunta', null=True, blank=True)),
                ('protocolo', models.ForeignKey(to='protocolo.Protocolo')),
            ],
            options={
                'ordering': ('conta_corrente',),
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
                'permissions': (('rel_adm_extrato', 'Rel. admin. - Panorama da conta corrente'), ('rel_adm_extrato_financeiro', 'Rel. admin. - Extrato do financeiro por m\xeas'), ('rel_adm_extrato_financeiro_parciais', 'Rel. admin. - Extrato do financeiro por parcial'), ('rel_adm_extrato_mes', 'Rel. admin. - Extrato da conta corrente por m\xeas'), ('rel_adm_extrato_tarifas', 'Rel. admin. - Extrato de tarifas por m\xeas'), ('rel_ger_acordos', 'Rel. ger. - Acordos'), ('rel_adm_caixa', 'Rel. admin. - Diferen\xe7as de caixa'), ('rel_ger_gerencial', 'Rel. ger. - Gerencial'), ('rel_adm_pagamentos_mes', 'Rel. admin. - Pagamentos po m\xeas'), ('rel_adm_pagamentos_parcial', 'Rel. admin. - Pagamentos por parcial'), ('rel_adm_parciais', 'Rel. admin. - Diferen\xe7as totais'), ('rel_adm_prestacao', 'Rel. admin. - Presta\xe7\xe3o de contas')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoComprovante',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Tipo de comprovante',
                'verbose_name_plural': 'Tipos de comprovante',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoComprovanteFinanceiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='extratopatrocinio',
            name='localiza',
            field=models.ForeignKey(verbose_name='Localiza\xe7\xe3o do patroc\xednio', to='financeiro.LocalizaPatrocinio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extratofinanceiro',
            name='tipo_comprovante',
            field=models.ForeignKey(blank=True, to='financeiro.TipoComprovanteFinanceiro', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extratocc',
            name='extrato_financeiro',
            field=models.ForeignKey(verbose_name='Extrato Financeiro', blank=True, to='financeiro.ExtratoFinanceiro', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auditoria',
            name='estado',
            field=models.ForeignKey(to='financeiro.Estado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auditoria',
            name='pagamento',
            field=models.ForeignKey(to='financeiro.Pagamento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auditoria',
            name='tipo',
            field=models.ForeignKey(to='financeiro.TipoComprovante'),
            preserve_default=True,
        ),
    ]
