# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import utils.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acesso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('liberacao', models.DateTimeField(null=True, verbose_name='Libera\xe7\xe3o', blank=True)),
                ('encerramento', models.DateTimeField(null=True, blank=True)),
                ('obs', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Agendado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ativo', models.BooleanField(default=False)),
                ('agenda', models.ForeignKey(to='identificacao.Agenda')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArquivoEntidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('arquivo', models.FileField(upload_to=b'entidade')),
                ('data', models.DateField()),
            ],
            options={
                'ordering': ('tipo', '-data'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ASN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(verbose_name='N\xfamero do AS')),
                ('pais', models.CharField(max_length=3, null=True, verbose_name='Pa\xeds', blank=True)),
            ],
            options={
                'ordering': ('numero',),
                'verbose_name': 'ASN',
                'verbose_name_plural': 'ASNs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primeiro_nome', models.CharField(help_text='ex. Jo\xe3o Andrade', max_length=100, verbose_name='Primeiro nome')),
                ('ultimo_nome', models.CharField(max_length=45, verbose_name='\xdaltimo nome')),
                ('email', models.CharField(help_text='ex. joao@joao.br', max_length=100, verbose_name='E-mail', blank=True)),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('tel', models.CharField(help_text='ex. Com. (11)2222-2222, Cel. (11)9999-9999, Fax (11)3333-3333, ...', max_length=100, verbose_name='Telefone')),
                ('documento', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'ordering': ('primeiro_nome', 'ultimo_nome'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ecossistema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('incentivo', models.BooleanField(default=False, verbose_name='Incentivar a dar palestra?')),
                ('monitora', models.BooleanField(default=False, verbose_name='Monitorar o convite?')),
                ('data_envio', models.DateField(null=True, verbose_name='Data de envio do e-mail', blank=True)),
                ('data_resposta', models.DateField(null=True, verbose_name='Data de resposta ao e-mail', blank=True)),
                ('dar_palestra', models.BooleanField(default=False, verbose_name='Vai dar palestra?')),
                ('palestrante', models.CharField(max_length=50, null=True, blank=True)),
                ('tema', models.CharField(max_length=50, null=True, blank=True)),
                ('temas_adicionais', models.TextField(null=True, verbose_name='Temas adicionais sugeridos', blank=True)),
                ('data_envio_postal', models.DateField(null=True, verbose_name='Data de envio do material postal', blank=True)),
                ('inscricoes_solicitadas', models.IntegerField(null=True, verbose_name='N\xfamero de inscri\xe7\xf5es solicitadas', blank=True)),
                ('inscricoes_aceitas', models.IntegerField(null=True, verbose_name='N\xfamero de inscri\xe7\xf5es aceitas', blank=True)),
                ('comentarios', models.TextField(null=True, verbose_name='Coment\xe1rios', blank=True)),
                ('hotel', models.BooleanField(default=False, verbose_name='Quer hotel?')),
                ('contato_pat', models.BooleanField(default=False, verbose_name='Contato para patroc\xednio?')),
                ('vip', models.BooleanField(default=False)),
                ('chaser', models.CharField(max_length=40, null=True, blank=True)),
                ('vai_pat', models.BooleanField(default=False, verbose_name='Vai patrocinar?')),
            ],
            options={
                'ordering': ('identificacao__endereco__entidade__sigla',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rua', models.CharField(help_text='ex. R. Dr. Ov\xeddio Pires de Campos', max_length=100, verbose_name='Logradouro')),
                ('num', models.IntegerField(help_text='ex. 215', null=True, verbose_name='Num.', blank=True)),
                ('compl', models.CharField(help_text='ex. 2. andar - Pr\xe9dio da PRODESP', max_length=100, verbose_name='Complemento', blank=True)),
                ('bairro', models.CharField(help_text='ex. Cerqueira C\xe9sar', max_length=50, verbose_name='Bairro', blank=True)),
                ('cidade', models.CharField(help_text='ex. S\xe3o Paulo', max_length=50, verbose_name='Cidade', blank=True)),
                ('cep', models.CharField(help_text='ex. 05403010', max_length=8, verbose_name='CEP', blank=True)),
                ('estado', models.CharField(help_text='ex. SP', max_length=50, verbose_name='Estado', blank=True)),
                ('pais', models.CharField(help_text='ex. Brasil', max_length=50, verbose_name='Pa\xeds', blank=True)),
                ('data_inatividade', models.DateField(null=True, verbose_name='Data de inatividade', blank=True)),
            ],
            options={
                'ordering': ('entidade',),
                'verbose_name': 'Endere\xe7o',
                'verbose_name_plural': 'Endere\xe7os',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EnderecoDetalhe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('complemento', models.TextField()),
                ('ordena', models.CharField(max_length=1000, null=True, editable=False)),
                ('mostra_bayface', models.BooleanField(default=False, help_text='Project-Id-Version: Django\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2013-05-02 16:18+0200\nPO-Revision-Date: 2010-05-13 15:35+0200\nLast-Translator: Django team\nLanguage-Team: English <en@li.org>\nLanguage: en\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n', verbose_name='Mostra no bayface')),
                ('detalhe', models.ForeignKey(verbose_name='ou Detalhe pai', blank=True, to='identificacao.EnderecoDetalhe', null=True)),
                ('endereco', models.ForeignKey(blank=True, to='identificacao.Endereco', null=True)),
            ],
            options={
                'ordering': ('ordena',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(help_text='Raz\xe3o Social (ex. Telecomunica\xe7\xf5es de S\xe3o Paulo S.A.)', max_length=255, verbose_name='Nome')),
                ('url', models.URLField(help_text='ex. www.telefonica.com.br', verbose_name='URL', blank=True)),
                ('sigla', models.CharField(help_text='Nome Fantasia (ex. TELEF\xd4NICA)', unique=True, max_length=20, verbose_name='Sigla')),
                ('cnpj', utils.models.CNPJField(help_text='ex. 00.000.000/0000-00', max_length=18, verbose_name='CNPJ', blank=True)),
                ('fisco', models.BooleanField(default=False, help_text='ex. Ativo no site da Receita Federal?', verbose_name='Fisco')),
                ('recebe_doacao', models.BooleanField(default=False, verbose_name='Recebe doa\xe7\xe3o de equipamentos?')),
                ('entidade', models.ForeignKey(related_name='entidade_em', verbose_name='Faz parte de', blank=True, to='identificacao.Entidade', null=True)),
            ],
            options={
                'ordering': ('sigla',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntidadeHistorico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inicio', models.DateField()),
                ('termino', models.DateField(null=True, blank=True)),
                ('ativo', models.BooleanField(default=False, verbose_name='Ativo')),
                ('obs', models.TextField(null=True, verbose_name='Observa\xe7\xe3o', blank=True)),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Identificacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('historico', models.DateTimeField(default=datetime.datetime(2015, 5, 17, 17, 27, 21, 123767), verbose_name='Hist\xf3rico', editable=False)),
                ('area', models.CharField(help_text='ex. Administra\xe7\xe3o', max_length=50, verbose_name='\xc1rea', blank=True)),
                ('funcao', models.CharField(help_text='ex. Gerente Administrativo', max_length=50, verbose_name='Fun\xe7\xe3o', blank=True)),
                ('ativo', models.BooleanField(default=False, verbose_name='Ativo')),
                ('contato', models.ForeignKey(verbose_name='Contato', to='identificacao.Contato')),
                ('endereco', models.ForeignKey(verbose_name='Entidade', to='identificacao.Endereco')),
            ],
            options={
                'ordering': ('endereco', 'contato'),
                'verbose_name': 'Identifica\xe7\xe3o',
                'verbose_name_plural': 'Identifica\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NivelAcesso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=50)),
                ('explicacao', models.TextField(verbose_name=b'Explica\xc3\xa7\xc3\xa3o')),
            ],
            options={
                'verbose_name': 'N\xedvel de acesso',
                'verbose_name_plural': 'N\xedveis de acesso',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PapelEntidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField()),
                ('entidade', models.ForeignKey(to='identificacao.Entidade')),
            ],
            options={
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
                'permissions': (('rel_adm_agenda', 'Rel. Adm. - Agenda'), ('rel_adm_ecossistema', 'Rel. Adm. - Ecossistema'), ('rel_tec_arquivos', 'Rel. Adm. - Documentos por entidade')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoArquivoEntidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoDetalhe',
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
            name='TipoEntidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('nome',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='papelentidade',
            name='tipo',
            field=models.ForeignKey(to='identificacao.TipoEntidade'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='identificacao',
            unique_together=set([('endereco', 'contato')]),
        ),
        migrations.AddField(
            model_name='entidadehistorico',
            name='tipo',
            field=models.ForeignKey(to='identificacao.TipoEntidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='enderecodetalhe',
            name='tipo',
            field=models.ForeignKey(to='identificacao.TipoDetalhe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='endereco',
            name='entidade',
            field=models.ForeignKey(verbose_name='Entidade', to='identificacao.Entidade'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='endereco',
            unique_together=set([('rua', 'num', 'compl', 'bairro', 'cidade', 'cep', 'estado', 'pais')]),
        ),
        migrations.AddField(
            model_name='ecossistema',
            name='identificacao',
            field=models.ForeignKey(verbose_name='Entidade/contato', to='identificacao.Identificacao'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asn',
            name='entidade',
            field=models.ForeignKey(blank=True, to='identificacao.Entidade', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivoentidade',
            name='entidade',
            field=models.ForeignKey(to='identificacao.Entidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='arquivoentidade',
            name='tipo',
            field=models.ForeignKey(to='identificacao.TipoArquivoEntidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agendado',
            name='entidade',
            field=models.ForeignKey(to='identificacao.Entidade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agenda',
            name='entidades',
            field=models.ManyToManyField(to='identificacao.Entidade', through='identificacao.Agendado'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acesso',
            name='detalhe',
            field=models.ManyToManyField(to='identificacao.EnderecoDetalhe', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acesso',
            name='identificacao',
            field=models.ForeignKey(verbose_name='Identifica\xe7\xe3o', to='identificacao.Identificacao'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acesso',
            name='niveis',
            field=models.ManyToManyField(to='identificacao.NivelAcesso', null=True, verbose_name='N\xedveis de acesso', blank=True),
            preserve_default=True,
        ),
    ]
