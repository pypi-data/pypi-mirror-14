# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0002_auto_20150517_1724'),
        ('identificacao', '0004_auto_20150517_1805'),
        ('financeiro', '0001_initial'),
        ('patrimonio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('velocidade', models.IntegerField()),
                ('unidade', models.IntegerField(choices=[(1, b'bps'), (1000, b'kbps'), (1000000, b'Mbps'), (1000000000, b'Gbps'), (1000000000000, b'Tbps')])),
            ],
            options={
                'ordering': ('unidade', 'velocidade'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Beneficiado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.FloatField()),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlocoIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'Bloco IP')),
                ('mask', models.IntegerField()),
                ('obs', models.TextField(null=True, blank=True)),
                ('transito', models.BooleanField(default=False, verbose_name='Bloco de tr\xe2nsito?')),
                ('asn', models.ForeignKey(verbose_name=b'AS anunciante', to='identificacao.ASN')),
                ('designado', models.ForeignKey(related_name='designa', verbose_name=b'Designado para', blank=True, to='identificacao.Entidade', null=True)),
                ('proprietario', models.ForeignKey(related_name='possui', blank=True, to='identificacao.ASN', help_text='Preencher caso seja diferente do dono do AS.', null=True, verbose_name='AS Propriet\xe1rio')),
            ],
            options={
                'ordering': ('ip',),
                'verbose_name': 'Bloco IP',
                'verbose_name_plural': 'Blocos IP',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Canal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrossConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('circuito', models.CharField(max_length=40, null=True, verbose_name='Circuito', blank=True)),
                ('ordemDeServico', models.CharField(max_length=30, null=True, verbose_name='OS/Projeto', blank=True)),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('ativo', models.BooleanField(default=True, verbose_name='Conector ativo?')),
            ],
            options={
                'verbose_name': 'Cross Connection',
                'verbose_name_plural': 'Cross Connections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrossConnectionHistorico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obs', models.TextField(verbose_name='Observa\xe7\xe3o')),
                ('data', models.DateField(verbose_name='Data')),
                ('crossConnection', models.ForeignKey(verbose_name='Cross Connection', to='rede.CrossConnection')),
            ],
            options={
                'ordering': ('-data', 'id'),
                'verbose_name': 'Hist\xf3rico Local',
                'verbose_name_plural': 'Hist\xf3rico Local',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('obs', models.TextField(null=True, blank=True)),
                ('entrada_ansp', models.ForeignKey(related_name='entrada', verbose_name=b'Ponto de entrada na ANSP', to='identificacao.Endereco')),
            ],
            options={
                'ordering': ('participante',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnlaceOperadora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_ativacao', models.DateField(null=True, blank=True)),
                ('data_desativacao', models.DateField(null=True, blank=True)),
                ('link_redundante', models.BooleanField(default=False)),
                ('obs', models.TextField(null=True, blank=True)),
                ('banda', models.ForeignKey(to='rede.Banda')),
                ('enlace', models.ForeignKey(to='rede.Enlace')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
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
            name='Historico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'rede')),
                ('horario', models.DateTimeField(auto_now=True)),
                ('equipamento', models.ForeignKey(blank=True, to='patrimonio.Patrimonio', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IFCConector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shelf', models.CharField(max_length=5, verbose_name='Shelf')),
                ('porta', models.CharField(max_length=10, verbose_name='Porta')),
                ('ativo', models.BooleanField(default=True, verbose_name='Conector ativo?')),
                ('obs', models.TextField(null=True, blank=True)),
                ('rack', models.ForeignKey(to='identificacao.EnderecoDetalhe')),
            ],
            options={
                'ordering': ('rack__complemento', 'shelf', 'porta'),
                'verbose_name': 'IFC Conector',
                'verbose_name_plural': 'IFC Conectores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IPBorda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name=b'IP de borda')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Midia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operadora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=40)),
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
                'permissions': (('rel_tec_blocosip', 'Rel. T\xe9c. - Lista de blocos IP'), ('rel_ger_custo_terremark', 'Rel. Ger. - Custos dos recursos contratados'), ('rel_tec_info', 'Rel. T\xe9c. - Dados cadastrais dos participantes'), ('rel_tec_planejamento', 'Rel. T\xe9c. - Planejamento por ano'), ('rel_tec_servico_processo', 'Rel. T\xe9c. - Servi\xe7os contratados por processo'), ('rel_tec_recursos_operacional', 'Rel. T\xe9c. - Relat\xf3rio de recursos'), ('rel_tec_blocosip_ansp', 'Rel. T\xe9c. - Blocos IP - ANSP'), ('rel_tec_blocosip_transito', 'Rel. T\xe9c. - Blocos IP - Tr\xe2nsito'), ('rel_tec_blocosip_inst_transito', 'Rel. T\xe9c. - Blocos IP - Inst. Tr\xe2nsito'), ('rel_tec_blocosip_inst_ansp', 'Rel. T\xe9c. - Blocos IP - Inst. ANSP'), ('rel_tec_crossconnection', 'Lista de Cross Connections')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanejaAquisicaoRecurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.FloatField()),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unit\xe1rio sem imposto', max_digits=12, decimal_places=2)),
                ('referente', models.CharField(max_length=150, null=True, blank=True)),
                ('instalacao', models.BooleanField(default=False, verbose_name='Instala\xe7\xe3o')),
                ('obs', models.TextField(null=True, blank=True)),
                ('ano', models.IntegerField()),
                ('banda', models.ForeignKey(blank=True, to='rede.Banda', null=True)),
                ('beneficiados', models.ManyToManyField(to='identificacao.Entidade', through='rede.Beneficiado')),
                ('os', models.ForeignKey(verbose_name='Altera\xe7\xe3o de contrato', blank=True, to='outorga.OrdemDeServico', null=True)),
            ],
            options={
                'ordering': ('os__numero', 'instalacao', 'tipo'),
                'verbose_name': 'Planeja Aquisi\xe7\xe3o de Recursos',
                'verbose_name_plural': 'Planeja Aquisi\xe7\xe3o de Recursos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.GenericIPAddressField()),
                ('mask', models.IntegerField()),
                ('provedor', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.FloatField(verbose_name='Quantidade (meses pagos)')),
                ('valor_mensal_sem_imposto', models.DecimalField(null=True, verbose_name='Valor mensal sem imposto', max_digits=12, decimal_places=2, blank=True)),
                ('valor_imposto_mensal', models.DecimalField(verbose_name='Valor mensal com imposto', max_digits=12, decimal_places=2)),
                ('mes_referencia', models.DecimalField(decimal_places=0, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], max_digits=2, blank=True, null=True, verbose_name='M\xeas inicial de refer\xeancia')),
                ('ano_referencia', models.DecimalField(decimal_places=0, validators=[django.core.validators.MinValueValidator(1950)], max_digits=4, blank=True, null=True, verbose_name='Ano inicial de refer\xeancia')),
                ('obs', models.TextField(null=True, blank=True)),
                ('pagamento', models.ForeignKey(blank=True, to='financeiro.Pagamento', null=True)),
                ('planejamento', models.ForeignKey(to='rede.PlanejaAquisicaoRecurso')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RIR',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rota',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aspath', models.CharField(max_length=255, verbose_name='AS path')),
                ('nexthop', models.GenericIPAddressField()),
                ('preferencial', models.BooleanField(default=False)),
                ('local_pref', models.IntegerField(null=True, blank=True)),
                ('blocoip', models.ForeignKey(verbose_name=b'Bloco IP', to='rede.BlocoIP')),
                ('historico', models.ForeignKey(to='rede.Historico')),
                ('provedor', models.ForeignKey(to='rede.Provedor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Segmento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_ativacao', models.DateField(null=True, verbose_name='Data de ativa\xe7\xe3o', blank=True)),
                ('data_desativacao', models.DateField(null=True, verbose_name='Data de desativa\xe7\xe3o', blank=True)),
                ('link_redundante', models.BooleanField(default=False, verbose_name='Link redundante?')),
                ('obs', models.TextField(null=True, blank=True)),
                ('designacao', models.CharField(max_length=50, null=True, verbose_name='Designa\xe7\xe3o', blank=True)),
                ('banda', models.ForeignKey(to='rede.Banda')),
                ('canal', models.ForeignKey(blank=True, to='rede.Canal', null=True)),
                ('enlace', models.ForeignKey(to='rede.Enlace')),
                ('interfaces', models.ManyToManyField(to='rede.Interface', null=True, blank=True)),
                ('operadora', models.ForeignKey(to='rede.Operadora')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sistema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoConector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(unique=True, max_length=20, verbose_name='Sigla')),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('imagem', models.ImageField(null=True, upload_to=b'conector', blank=True)),
            ],
            options={
                'ordering': ('sigla',),
                'verbose_name': 'Tipo de Conector',
                'verbose_name_plural': 'Tipos de Conectores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoInterface',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=45)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoServico',
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
            name='Unidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='segmento',
            name='sistema',
            field=models.ForeignKey(blank=True, to='rede.Sistema', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='segmento',
            name='uso',
            field=models.ForeignKey(blank=True, to='rede.Uso', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planejaaquisicaorecurso',
            name='projeto',
            field=models.ForeignKey(to='rede.Projeto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planejaaquisicaorecurso',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo de descri\xe7\xe3o', to='rede.TipoServico'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planejaaquisicaorecurso',
            name='unidade',
            field=models.ForeignKey(to='rede.Unidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interface',
            name='midia',
            field=models.ForeignKey(to='rede.Midia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interface',
            name='tipo',
            field=models.ForeignKey(to='rede.TipoInterface'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ifcconector',
            name='tipoConector',
            field=models.ForeignKey(to='rede.TipoConector'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ifcconector',
            unique_together=set([('rack', 'shelf', 'porta')]),
        ),
        migrations.AddField(
            model_name='enlaceoperadora',
            name='ip_borda',
            field=models.ManyToManyField(to='rede.IPBorda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enlaceoperadora',
            name='operadora',
            field=models.ForeignKey(to='rede.Operadora'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enlace',
            name='operadora',
            field=models.ManyToManyField(to='rede.Operadora', through='rede.EnlaceOperadora'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enlace',
            name='participante',
            field=models.ForeignKey(to='identificacao.Endereco'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crossconnection',
            name='destino',
            field=models.ForeignKey(related_name='crossconnection_destino', to='rede.IFCConector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crossconnection',
            name='origem',
            field=models.ForeignKey(related_name='crossconnection_origem', to='rede.IFCConector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blocoip',
            name='rir',
            field=models.ForeignKey(verbose_name=b'RIR', blank=True, to='rede.RIR', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blocoip',
            name='superbloco',
            field=models.ForeignKey(verbose_name=b'Super bloco', blank=True, to='rede.BlocoIP', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blocoip',
            name='usuario',
            field=models.ForeignKey(related_name='usa', blank=True, to='identificacao.Entidade', help_text='Preencher caso seja diferente do designado.', null=True, verbose_name='Usado por'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='blocoip',
            unique_together=set([('ip', 'mask')]),
        ),
        migrations.AddField(
            model_name='beneficiado',
            name='estado',
            field=models.ForeignKey(to='rede.Estado', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='beneficiado',
            name='planejamento',
            field=models.ForeignKey(to='rede.PlanejaAquisicaoRecurso'),
            preserve_default=True,
        ),
    ]
