# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import membro.models
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('identificacao', '0003_auto_20150517_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'membro')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assinatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'ordering': ('membro',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField()),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
                ('hierarquia', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Controle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entrada', models.DateTimeField()),
                ('saida', models.DateTimeField(null=True, blank=True)),
                ('obs', models.TextField(null=True, verbose_name='Coment\xe1rios', blank=True)),
                ('almoco_devido', models.BooleanField(default=True, verbose_name='Hora de almo\xe7o devida?')),
                ('almoco', models.IntegerField(default=60, null=True, verbose_name='Tempo de almo\xe7o em minutos', blank=True)),
            ],
            options={
                'ordering': ('-entrada',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ControleFerias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', utils.models.NARADateField()),
                ('termino', utils.models.NARADateField()),
                ('oficial', models.BooleanField(default=False, verbose_name='Oficial?')),
                ('obs', models.TextField(null=True, blank=True)),
                ('vendeu10', models.BooleanField(default=False, verbose_name='Vendeu 10 dias?')),
                ('antecipa13', models.BooleanField(default=False, verbose_name='Antecipa\xe7\xe3o de 13\xba sal\xe1rio?')),
                ('dias_uteis_fato', models.IntegerField(verbose_name='Dias \xfateis tirados de fato')),
                ('dias_uteis_aberto', models.IntegerField(verbose_name='Dias \xfateis em aberto')),
                ('arquivo_oficial', models.FileField(null=True, upload_to=b'controleferias__arquivooficial', blank=True)),
            ],
            options={
                'verbose_name': 'Controle de f\xe9rias',
                'verbose_name_plural': 'Controles de f\xe9rias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DadoBancario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agencia', models.IntegerField(help_text='ex. 0909', verbose_name='Ag.')),
                ('ag_digito', models.IntegerField(help_text='ex. 9', null=True, verbose_name=b' ', blank=True)),
                ('conta', models.IntegerField(help_text='ex. 01222222', verbose_name='CC')),
                ('cc_digito', models.CharField(help_text='ex. x', max_length=1, verbose_name=b' ', blank=True)),
                ('banco', models.ForeignKey(verbose_name='Banco', to='membro.Banco')),
            ],
            options={
                'ordering': ('banco',),
                'verbose_name': 'Dados banc\xe1rios',
                'verbose_name_plural': 'Dados banc\xe1rios',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DispensaLegal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('justificativa', models.TextField()),
                ('inicio_direito', utils.models.NARADateField(verbose_name='In\xedcio do direito')),
                ('dias_uteis', models.IntegerField(default=0, help_text=b'*mover para dias corridos', null=True, verbose_name='Dias \xfateis.')),
                ('inicio_realizada', utils.models.NARADateField(null=True, verbose_name='In\xedcio da realiza\xe7\xe3o da dispensa', blank=True)),
                ('realizada', models.BooleanField(default=False, verbose_name='J\xe1 realizada?')),
                ('atestado', models.BooleanField(default=False, verbose_name='H\xe1 atestado?')),
                ('arquivo', models.FileField(null=True, upload_to=b'dispensas/', blank=True)),
                ('dias_corridos', models.IntegerField(default=0, null=True, verbose_name='Dura\xe7\xe3o em dias corridos')),
                ('horas', models.IntegerField(default=0, null=True, verbose_name='Horas')),
                ('minutos', models.IntegerField(default=0, null=True, verbose_name='Minutos')),
            ],
            options={
                'verbose_name': 'Dispensa',
                'verbose_name_plural': 'Dispensas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ferias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', utils.models.NARADateField(help_text='In\xedcio do per\xedodo de trabalho', verbose_name='In\xedcio do per\xedodo aquisitivo')),
                ('realizado', models.BooleanField(default=False, verbose_name='F\xe9rias j\xe1 tiradas?')),
            ],
            options={
                'ordering': ('inicio',),
                'verbose_name': 'F\xe9rias',
                'verbose_name_plural': 'F\xe9rias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', models.DateField(verbose_name='In\xedcio')),
                ('termino', models.DateField(null=True, verbose_name='T\xe9rmino', blank=True)),
                ('funcionario', models.BooleanField(default=False, verbose_name='Funcion\xe1rio')),
                ('obs', models.TextField(null=True, blank=True)),
                ('cargo', models.ForeignKey(to='membro.Cargo')),
            ],
            options={
                'ordering': ('-inicio',),
                'verbose_name': 'Hist\xf3rico',
                'verbose_name_plural': 'Hist\xf3ricos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Caio Andrade', max_length=50, verbose_name='Nome')),
                ('rg', models.CharField(help_text='ex. 00.000.000-0', max_length=12, null=True, verbose_name='RG', blank=True)),
                ('cpf', membro.models.CPFField(help_text='ex. 000.000.000-00', max_length=14, null=True, verbose_name='CPF', blank=True)),
                ('email', models.CharField(help_text='ex. nome@empresa.br', max_length=50, verbose_name='E-mail', blank=True)),
                ('ramal', models.IntegerField(null=True, verbose_name='Ramal', blank=True)),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o', blank=True)),
                ('url_lattes', models.URLField(help_text='URL do Curr\xedculo Lattes', verbose_name='Curr\xedculo Lattes', blank=True)),
                ('foto', models.ImageField(null=True, upload_to=b'membro', blank=True)),
                ('data_nascimento', utils.models.NARADateField(help_text='Data de nascimento', null=True, verbose_name='Nascimento', blank=True)),
                ('site', models.BooleanField(default=False, verbose_name='Exibir no site?')),
                ('contato', models.ForeignKey(blank=True, to='identificacao.Contato', null=True)),
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
                'permissions': (('rel_adm_logs', 'Rel. Adm. - Registro de uso do sistema por ano'), ('rel_adm_mensalf', 'Rel. Adm. - Controle de hor\xe1rio mensal')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SindicatoArquivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(null=True, upload_to=b'membro__sindicatoarquivo', blank=True)),
                ('ano', models.IntegerField(null=True, verbose_name='Ano', blank=True)),
                ('membro', models.ForeignKey(verbose_name='Membro', to='membro.Membro')),
            ],
            options={
                'ordering': ('ano',),
                'verbose_name': 'Arquivo do Sindicato',
                'verbose_name_plural': 'Arquivos do Sindicato',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoAssinatura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text=' ', unique=True, max_length=20, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Tipo de Assinatura',
                'verbose_name_plural': 'Tipos de Assinatura',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoDispensa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(help_text='Nome de usu\xe1rio no sistema', max_length=20, verbose_name='Usu\xe1rio')),
                ('sistema', models.CharField(help_text='Nome do Sistema', max_length=50, verbose_name='Sistema')),
                ('membro', models.ForeignKey(verbose_name='Membro', to='membro.Membro')),
            ],
            options={
                'ordering': ('username',),
                'verbose_name': 'Usu\xe1rio',
                'verbose_name_plural': 'Usu\xe1rios',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usuario',
            unique_together=set([('membro', 'username', 'sistema')]),
        ),
        migrations.AddField(
            model_name='historico',
            name='membro',
            field=models.ForeignKey(to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ferias',
            name='membro',
            field=models.ForeignKey(verbose_name='Membro', to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ferias',
            unique_together=set([('membro', 'inicio')]),
        ),
        migrations.AddField(
            model_name='dispensalegal',
            name='membro',
            field=models.ForeignKey(verbose_name='Membro', to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dispensalegal',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo de dispensa', to='membro.TipoDispensa'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dadobancario',
            name='membro',
            field=models.OneToOneField(verbose_name='Membro', to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='dadobancario',
            unique_together=set([('banco', 'agencia', 'ag_digito', 'conta', 'cc_digito')]),
        ),
        migrations.AddField(
            model_name='controleferias',
            name='ferias',
            field=models.ForeignKey(to='membro.Ferias'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='controle',
            name='membro',
            field=models.ForeignKey(to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assinatura',
            name='membro',
            field=models.ForeignKey(verbose_name='Membro', to='membro.Membro'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assinatura',
            name='tipo_assinatura',
            field=models.ForeignKey(verbose_name='Tipo de Assinatura', to='membro.TipoAssinatura'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='assinatura',
            unique_together=set([('membro', 'tipo_assinatura')]),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='membro',
            field=models.ForeignKey(to='membro.Membro'),
            preserve_default=True,
        ),
    ]
