# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.urlresolvers import reverse
from django.test import TestCase
from datetime import date

from identificacao.models import Entidade
from repositorio.models import Tipo, Estado, Repositorio, Natureza, Servico
from patrimonio.models import Tipo as TipoPatrimonio, Patrimonio
from membro.models import Membro


class RepositorioTest(TestCase):
    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml']

    def setUp(self):
        tipoPatr = TipoPatrimonio.objects.create(nome='roteador')
        Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400",
                                  checado=True)

        tipoPatrFilho = TipoPatrimonio.objects.create(nome='placa')
        Patrimonio.objects.create(ns='kjfd1234cdf', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe",
                                  checado=True)

        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def test_save__numero_sequencial(self):
        entidade = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True,
                                           url='')

        tipo = Tipo.objects.create(entidade=entidade, nome="tipo_nome")
        estado = Estado.objects.create()
        natureza = Natureza.objects.create(nome="problema")

        responsavel = Membro.objects.create(nome='Antonio')

        repositorio1 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 10), tipo=tipo, estado=estado,
                                                  ocorrencia=u'Ocorrência de teste número 1', responsavel=responsavel,
                                                  natureza=natureza)
        repositorio2 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 13), tipo=tipo, estado=estado,
                                                  ocorrencia=u'Ocorrência de teste número 2', responsavel=responsavel,
                                                  natureza=natureza)

        self.assertEqual(repositorio1.numero + 1, repositorio2.numero)

    def test_view__filtra_patrimonio(self):

        url = reverse("repositorio.views.ajax_seleciona_patrimonios")
        response = self.client.get(url, {'string': '3456'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"ns": "AF345678GB3489X"')


class RepositorioRelatorioTest(TestCase):
    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(RepositorioRelatorioTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

        tipoPatr = TipoPatrimonio.objects.create(nome='roteador')
        Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400",
                                  checado=True)

        tipoPatrFilho = TipoPatrimonio.objects.create(nome='placa')
        Patrimonio.objects.create(ns='kjfd1234cdf', modelo='Placa mãe', tipo=tipoPatrFilho, apelido="Placa mãe",
                                  checado=True)

        # Grupo 1 de repositórios
        entidade = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True,
                                           url='')
        tipo = Tipo.objects.create(entidade=entidade, nome="tipo_nome")
        natureza = Natureza.objects.create(nome="problema")
        servico1 = Servico.objects.create(nome="servico1")
        servico2 = Servico.objects.create(nome="servico2")

        estado = Estado.objects.create()
        responsavel = Membro.objects.create(nome='Antonio')

        repositorio1 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 14), tipo=tipo, estado=estado,
                                                  ocorrencia=u'Ocorrência de teste número 1', responsavel=responsavel,
                                                  natureza=natureza)
        repositorio1.servicos.add(servico2)
        repositorio2 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 10), tipo=tipo, estado=estado,
                                                  ocorrencia=u'Ocorrência de teste número 2', responsavel=responsavel,
                                                  natureza=natureza)
        repositorio2.servicos.add(servico1, servico2)

        # Grupo 2 de repositórios
        entidade = Entidade.objects.create(sigla='DELL', nome='Dell', cnpj='00.000.000/0000-00', fisco=True, url='')
        tipo = Tipo.objects.create(entidade=entidade, nome="tipo_nome dell")
        natureza = Natureza.objects.create(nome="incidente")

        estado = Estado.objects.create()
        responsavel = Membro.objects.create(nome='Rogerio')

        repositorio3 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 13), tipo=tipo, estado=estado,  # @UnusedVariable
                                                  ocorrencia=u'Ocorrência de teste número 3', responsavel=responsavel,
                                                  natureza=natureza)

        repositorio4 = Repositorio.objects.create(data_ocorrencia=date(2014, 2, 11), tipo=tipo, estado=estado,  # @UnusedVariable
                                                  ocorrencia=u'Ocorrência de teste número 4', responsavel=responsavel,
                                                  natureza=natureza)

    def test_view__relatorio_repositorio__sem_filtro(self):
        url = reverse("repositorio.views.relatorio_repositorio")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/repositorio/relatorio/repositorio">Relatório do Repositório</a>')

        # assert filtro
        self.assertContains(response, u'<h1 repeat="1">Relatório do repositório  </h1>')
        self.assertContains(response, u'<h3>Filtro</h3>')
        self.assertContains(response, u'<select name="entidade" id="id_entidade"')
        self.assertContains(response, u'<select name="nome" id="id_nome">')
        self.assertContains(response, u'<select name="natureza" id="id_natureza">')
        self.assertContains(response, u'<select name="servico" id="id_servico">')
        self.assertContains(response, u'<input name="data_de" id="id_data_de" style="display:inline" value="" />')
        self.assertContains(response, u'<input name="data_ate" id="id_data_ate"  style="display:inline" value="" />')
        self.assertNotContains(response, u'<h4>')

    def test_view__relatorio_repositorio__entidade1(self):
        url = reverse("repositorio.views.relatorio_repositorio")
        response = self.client.get(url, {'entidade': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/repositorio/relatorio/repositorio">Relatório do Repositório</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/repositorio/relatorio/repositorio/1" method="GET" '
                                      u'id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="natureza" value="0" />')
        self.assertContains(response, u'<input type="hidden" name="servico" value="0" />')
        self.assertContains(response, u'<input type="hidden" name="data_de" value="" />')
        self.assertContains(response, u'<input type="hidden" name="data_ate" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h4>SAC  - tipo_nome - problema</h4>')
        self.assertContains(response, u'<span id="span_repositorio_1">2014-02-14 - </span>')
        self.assertContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 1</div>')
        self.assertContains(response, u'<span id="span_repositorio_2">2014-02-10 - </span>')
        self.assertContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 2</div>')
        self.assertContains(response, u'    servico1')
        self.assertContains(response, u'    servico2')

    def test_view__relatorio_repositorio__entidade1__servico(self):
        url = reverse("repositorio.views.relatorio_repositorio")
        response = self.client.get(url, {'entidade': '1', 'servico': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/repositorio/relatorio/repositorio">Relatório do Repositório</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/repositorio/relatorio/repositorio/1" method="GET" '
                                      u'id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="natureza" value="0" />')
        self.assertContains(response, u'<input type="hidden" name="servico" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="data_de" value="" />')
        self.assertContains(response, u'<input type="hidden" name="data_ate" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h4>SAC  - tipo_nome - problema</h4>')
        self.assertNotContains(response, u'<span id="span_repositorio_1">2014-02-14 - </span>')
        self.assertNotContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 1</div>')
        self.assertContains(response, u'<span id="span_repositorio_2">2014-02-10 - </span>')
        self.assertContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 2</div>')
        self.assertContains(response, u'    servico1')
        self.assertContains(response, u'    servico2')

    def test_view__relatorio_repositorio__entidade2(self):
        url = reverse("repositorio.views.relatorio_repositorio")
        response = self.client.get(url, {'entidade': '2'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/repositorio/relatorio/repositorio">Relatório do Repositório</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/repositorio/relatorio/repositorio/1" method="GET" '
                                      u'id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="2" />')
        self.assertContains(response, u'<input type="hidden" name="natureza" value="0" />')
        self.assertContains(response, u'<input type="hidden" name="servico" value="0" />')
        self.assertContains(response, u'<input type="hidden" name="data_de" value="" />')
        self.assertContains(response, u'<input type="hidden" name="data_ate" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h4>DELL  - tipo_nome dell - incidente</h4>')
        self.assertContains(response, u'<span id="span_repositorio_3">2014-02-13 - </span>')
        self.assertContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 3</div>')
        self.assertContains(response, u'<span id="span_repositorio_4">2014-02-11 - </span>')
        self.assertContains(response, u'<div class="div_item_conteudo">Ocorrência de teste número 4</div>')
        self.assertNotContains(response, u'    servico1')
        self.assertNotContains(response, u'    servico2')

    def test_view__ajax_repositorio_tipo_nomes(self):
        url = reverse("repositorio.views.ajax_repositorio_tipo_nomes")
        response = self.client.get(url, {'id_entidade': '2'})

        self.assertEqual(200, response.status_code)

        # asssert dos dados
        self.assertContains(response, u'tipo_nome dell')
