# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayoutLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=400)),
                ('ordem', models.PositiveSmallIntegerField(help_text='Ordem de exibi\xe7\xe3o do link.')),
            ],
            options={
                'ordering': ('ordem', 'titulo'),
            },
        ),
        migrations.CreateModel(
            name='LayoutLogo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
                ('titulo', models.CharField(max_length=200, verbose_name='T\xedtulo do logo')),
                ('url', models.CharField(max_length=400, null=True, verbose_name='URL do logo', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LayoutPagina',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logo_cabecalho', models.ForeignKey(related_name='+', to='configuracao.LayoutLogo')),
                ('logo_rodape', models.ForeignKey(related_name='+', to='configuracao.LayoutLogo')),
            ],
        ),
        migrations.CreateModel(
            name='LayoutLinkFooter',
            fields=[
                ('layoutlink_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='configuracao.LayoutLink')),
                ('pagina', models.ForeignKey(to='configuracao.LayoutPagina')),
            ],
            options={
                'verbose_name': 'Link do rodap\xe9',
                'verbose_name_plural': 'Links do rodap\xe9',
            },
            bases=('configuracao.layoutlink',),
        ),
        migrations.CreateModel(
            name='LayoutLinkHeader',
            fields=[
                ('layoutlink_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='configuracao.LayoutLink')),
                ('pagina', models.ForeignKey(to='configuracao.LayoutPagina')),
            ],
            options={
                'verbose_name': 'Link do cabe\xe7alho',
                'verbose_name_plural': 'Links do cabe\xe7alho',
            },
            bases=('configuracao.layoutlink',),
        ),
    ]
