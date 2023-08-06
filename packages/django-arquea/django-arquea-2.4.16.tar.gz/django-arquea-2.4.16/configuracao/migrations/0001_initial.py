# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome_assinatura', models.CharField(max_length=150, verbose_name='Assinatura')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ClassesExtra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('help', models.TextField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('content_type__app_label', 'content_type__model'),
                'verbose_name': 'Ajuda dos modelos',
                'verbose_name_plural': 'Ajudas dos modelos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldsHelp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=30)),
                ('help', models.CharField(max_length=100)),
                ('model', models.ForeignKey(to='configuracao.ClassesExtra')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Papelaria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('papel_timbrado_retrato_a4', models.FileField(null=True, upload_to=b'papel_timbrado_retrato_a4', blank=True)),
                ('retrato_a4_margem_superior', models.DecimalField(null=True, verbose_name='Margem superior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('retrato_a4_margem_inferior', models.DecimalField(null=True, verbose_name='Margem inferior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('papel_timbrado_paisagem_a4', models.FileField(null=True, upload_to=b'papel_timbrado_paisagem_a4', blank=True)),
                ('paisagem_a4_margem_superior', models.DecimalField(null=True, verbose_name='Margem superior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('paisagem_a4_margem_inferior', models.DecimalField(null=True, verbose_name='Margem inferior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('papel_timbrado_retrato_a3', models.FileField(null=True, upload_to=b'papel_timbrado_retrato_a3', blank=True)),
                ('retrato_a3_margem_superior', models.DecimalField(null=True, verbose_name='Margem superior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('retrato_a3_margem_inferior', models.DecimalField(null=True, verbose_name='Margem inferior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('papel_timbrado_paisagem_a3', models.FileField(null=True, upload_to=b'papel_timbrado_paisagem_a3', blank=True)),
                ('paisagem_a3_margem_superior', models.DecimalField(null=True, verbose_name='Margem superior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('paisagem_a3_margem_inferior', models.DecimalField(null=True, verbose_name='Margem inferior em cm', max_digits=3, decimal_places=2, blank=True)),
                ('valido', models.BooleanField(default=True, verbose_name='Template v\xe1lido?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variavel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=60, verbose_name='Nome da vari\xe1vel', choices=[(b'DATACENTER_IDS', b'ID da Entidade do Datacenter principal.'), (b'TERMO_EXCLUIDO_IDS', b'IDs de Termos a serem exclu\xc3\xaddos da vis\xc3\xa3o de relat\xc3\xb3rios, como o de Patrim\xc3\xb4nio por Termo. Ex: 1,2,3')])),
                ('valor', models.CharField(max_length=60, verbose_name='Valor')),
                ('obs', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('nome',),
                'verbose_name': 'Vari\xe1vel',
                'verbose_name_plural': 'Vari\xe1veis',
            },
            bases=(models.Model,),
        ),
    ]
