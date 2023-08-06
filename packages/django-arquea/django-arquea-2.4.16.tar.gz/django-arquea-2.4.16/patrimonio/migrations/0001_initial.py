# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        ('memorando', '0001_initial'),
        ('identificacao', '0002_auto_20150517_1727'),
        ('financeiro', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dimensao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('altura', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('largura', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('profundidade', models.DecimalField(null=True, max_digits=6, decimal_places=3, blank=True)),
                ('peso', models.DecimalField(null=True, verbose_name=b'Peso (kg)', max_digits=6, decimal_places=3, blank=True)),
            ],
            options={
                'verbose_name': 'Dimens\xe3o',
                'verbose_name_plural': 'Dimens\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Direcao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origem', models.CharField(max_length=15)),
                ('destino', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Dire\xe7\xe3o',
                'verbose_name_plural': 'Dire\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Distribuicao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', models.IntegerField()),
                ('final', models.IntegerField()),
                ('direcao', models.ForeignKey(to='patrimonio.Direcao')),
            ],
            options={
                'verbose_name': 'Distribui\xe7\xe3o',
                'verbose_name_plural': 'Distribui\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DistribuicaoUnidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
                ('sigla', models.CharField(max_length=4)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o')),
                ('part_number', models.CharField(max_length=50, null=True, blank=True)),
                ('modelo', models.CharField(max_length=100, null=True, blank=True)),
                ('ncm', models.CharField(max_length=30, null=True, verbose_name='NCM/SH', blank=True)),
                ('ean', models.CharField(max_length=45, null=True, verbose_name='EAN', blank=True)),
                ('tamanho', models.DecimalField(null=True, verbose_name='Tamanho (em U)', max_digits=5, decimal_places=2, blank=True)),
                ('especificacao', models.FileField(upload_to=b'patrimonio', null=True, verbose_name='Especifica\xe7\xe3o', blank=True)),
                ('imagem', models.ImageField(upload_to=b'patrimonio', null=True, verbose_name='Imagem Frontal do equipamento', blank=True)),
                ('imagem_traseira', models.ImageField(upload_to=b'patrimonio', null=True, verbose_name='Imagem Traseira do equipamento', blank=True)),
                ('titulo_autor', models.CharField(max_length=100, null=True, verbose_name='T\xedtulo e autor', blank=True)),
                ('isbn', models.CharField(max_length=20, null=True, verbose_name='ISBN', blank=True)),
                ('convencoes', models.ManyToManyField(to='patrimonio.Distribuicao', verbose_name='Conven\xe7\xf5es')),
                ('dimensao', models.ForeignKey(blank=True, to='patrimonio.Dimensao', null=True)),
                ('entidade_fabricante', models.ForeignKey(blank=True, to='identificacao.Entidade', help_text='Representa a Entidade que fabrica este equipamento.', null=True, verbose_name='Marca/Editora')),
            ],
            options={
                'ordering': ('descricao',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Doado', unique=True, max_length=30, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HistoricoLocal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.TextField(help_text='ex. Empr\xe9stimo', verbose_name='Ocorr\xeancia')),
                ('data', models.DateField(verbose_name='Data')),
                ('posicao', models.CharField(help_text='<b>[rack:</b>XXX<b>].F[furo:</b>000<b>].[posicao:</b>T,TD,TE,T01,T02,LD,LE,01,02<b>]</b>', max_length=50, null=True, verbose_name='Posi\xe7\xe3o', blank=True)),
                ('endereco', models.ForeignKey(verbose_name='Localiza\xe7\xe3o', to='identificacao.EnderecoDetalhe')),
                ('estado', models.ForeignKey(verbose_name='Estado do Patrim\xf4nio', to='patrimonio.Estado')),
                ('memorando', models.ForeignKey(blank=True, to='memorando.MemorandoSimples', null=True)),
            ],
            options={
                'ordering': ('-data', 'id'),
                'verbose_name': 'Hist\xf3rico Local',
                'verbose_name_plural': 'Hist\xf3rico Local',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Patrimonio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ns', models.CharField(max_length=50, null=True, verbose_name='N\xfamero de s\xe9rie', blank=True)),
                ('complemento', models.CharField(max_length=100, null=True, verbose_name=b'Compl', blank=True)),
                ('valor', models.DecimalField(null=True, verbose_name='Vl unit', max_digits=12, decimal_places=2, blank=True)),
                ('obs', models.TextField(null=True, blank=True)),
                ('agilis', models.BooleanField(default=True, verbose_name='Agilis?')),
                ('checado', models.BooleanField(default=False)),
                ('apelido', models.CharField(max_length=30, null=True, blank=True)),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o NF')),
                ('tem_numero_fmusp', models.BooleanField(default=False, verbose_name=b'Tem n\xc2\xba de patrim\xc3\xb4nio oficial?')),
                ('numero_fmusp', models.IntegerField(null=True, verbose_name=b'N\xc2\xba de patrim\xc3\xb4nio oficial', blank=True)),
                ('descricao_tecnica', models.TextField(null=True, verbose_name='Descri\xe7\xe3o t\xe9cnica', blank=True)),
                ('imagem', models.ImageField(null=True, upload_to=b'patrimonio', blank=True)),
                ('isbn', models.CharField(max_length=20, null=True, verbose_name='ISBN', blank=True)),
                ('titulo_autor', models.CharField(max_length=100, null=True, verbose_name='T\xedtulo e autor', blank=True)),
                ('especificacao', models.FileField(upload_to=b'patrimonio', null=True, verbose_name='Especifica\xe7\xe3o', blank=True)),
                ('tamanho', models.DecimalField(null=True, verbose_name='Tamanho (em U)', max_digits=5, decimal_places=2, blank=True)),
                ('revision', models.CharField(max_length=30, null=True, verbose_name='Revision', blank=True)),
                ('version', models.CharField(max_length=30, null=True, verbose_name='Version', blank=True)),
                ('ncm', models.CharField(max_length=30, null=True, verbose_name='NCM/SH', blank=True)),
                ('ocst', models.CharField(max_length=30, null=True, verbose_name='O/CST', blank=True)),
                ('cfop', models.CharField(max_length=30, null=True, verbose_name='CFOP', blank=True)),
                ('garantia_termino', utils.models.NARADateField(null=True, verbose_name='Data de t\xe9rmino da garantia', blank=True)),
                ('entidade_procedencia', models.ForeignKey(blank=True, to='identificacao.Entidade', help_text='Representa a Entidade que fornece este patrim\xf4nio.', null=True, verbose_name='Proced\xeancia')),
                ('equipamento', models.ForeignKey(blank=True, to='patrimonio.Equipamento', null=True)),
                ('pagamento', models.ForeignKey(blank=True, to='financeiro.Pagamento', null=True)),
                ('patrimonio', models.ForeignKey(related_name='contido', verbose_name='Contido em', blank=True, to='patrimonio.Patrimonio', null=True)),
            ],
            options={
                'ordering': ('tipo', 'descricao'),
                'verbose_name': 'Patrim\xf4nio',
                'verbose_name_plural': 'Patrim\xf4nio',
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
                'permissions': (('rel_tec_planta_baixa_edit', 'Rel. T\xe9c. - Planta baixa - Racks'), ('rel_tec_racks', 'Rel. T\xe9c. - Racks '), ('rel_tec_por_estado', 'Rel. T\xe9c. - Patr por estado do item'), ('rel_tec_por_local', 'Rel. T\xe9c. - Patr por localiza\xe7\xe3o'), ('rel_tec_por_local_rack', 'Rel. T\xe9c. - Patr por local e rack'), ('rel_tec_por_local_termo', 'Rel. T\xe9c. - Patr por localiza\xe7\xe3o (com Termo)'), ('rel_tec_por_marca', 'Rel. T\xe9c. - Patr por marca'), ('rel_adm_por_termo', 'Rel. Adm. - Patr por termo de outorga'), ('rel_tec_por_tipo', 'Rel. T\xe9c. - Patr por tipo'), ('rel_tec_por_tipo_equipamento', 'Rel. T\xe9c. - Busca por tipo de equip'), ('rel_tec_patr_tipo_equipamento', 'Rel. T\xe9c. - Patr por tipo de equip'), ('rel_adm_presta_contas', 'Rel. Adm. - Presta\xe7\xe3o de contas patrimonial'), ('rel_tec_relatorio_rack', 'Rel. T\xe9c. - Relat\xf3rio por rack')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlantaBaixaDataCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w', models.IntegerField(default=800)),
                ('h', models.IntegerField(default=600)),
                ('cor', models.CharField(default=b'#fff', max_length=7, null=True, blank=True)),
                ('endereco', models.ForeignKey(verbose_name='Data center', to='identificacao.EnderecoDetalhe')),
            ],
            options={
                'verbose_name': 'Planta baixa - Data Center',
                'verbose_name_plural': 'Planta baixa - Data Centers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlantaBaixaObjeto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=80)),
                ('data_center', models.ForeignKey(verbose_name='Data center', to='patrimonio.PlantaBaixaDataCenter')),
                ('patrimonio', models.ForeignKey(verbose_name='Patrim\xf4nio', blank=True, to='patrimonio.Patrimonio', null=True)),
            ],
            options={
                'verbose_name': 'Planta baixa - Objeto',
                'verbose_name_plural': 'Planta baixa - Objetos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlantaBaixaPosicao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=80, null=True, blank=True)),
                ('x', models.IntegerField(default=0)),
                ('y', models.IntegerField(default=0)),
                ('w', models.IntegerField(default=100)),
                ('h', models.IntegerField(default=100)),
                ('cor', models.CharField(default=b'EEEEEE', max_length=6, null=True, blank=True)),
                ('objeto', models.ForeignKey(to='patrimonio.PlantaBaixaObjeto')),
            ],
            options={
                'verbose_name': 'Planta baixa - Posi\xe7\xe3o',
                'verbose_name_plural': 'Planta baixa - Posi\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='ex. Open Source', unique=True, max_length=30, verbose_name='Nome')),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoEquipamento',
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
            name='UnidadeDimensao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Unidade da dimens\xe3o',
                'verbose_name_plural': 'Unidade das dimens\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='patrimonio',
            name='tipo',
            field=models.ForeignKey(to='patrimonio.Tipo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicolocal',
            name='pai',
            field=models.ForeignKey(related_name='filhos', blank=True, to='patrimonio.Patrimonio', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='historicolocal',
            name='patrimonio',
            field=models.ForeignKey(verbose_name='Patrim\xf4nio', to='patrimonio.Patrimonio'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='historicolocal',
            unique_together=set([('patrimonio', 'endereco', 'descricao', 'data')]),
        ),
        migrations.AddField(
            model_name='equipamento',
            name='tipo',
            field=models.ForeignKey(blank=True, to='patrimonio.TipoEquipamento', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distribuicao',
            name='unidade',
            field=models.ForeignKey(to='patrimonio.DistribuicaoUnidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dimensao',
            name='unidade',
            field=models.ForeignKey(to='patrimonio.UnidadeDimensao'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='PatrimonioRack',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('patrimonio.patrimonio',),
        ),
    ]
