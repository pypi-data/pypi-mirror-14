# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test import TestCase
from patrimonio.models import Equipamento, Patrimonio, Tipo
from identificacao.models import Entidade
from verificacao.models import VerificacaoPatrimonio,\
    VerificacaoPatrimonioEquipamento, VerificacaoEquipamento


class TestPatrimonioComEquipamenpoVazio(TestCase):

    def setUp(self):
        super(TestPatrimonioComEquipamenpoVazio, self).setUp()

    def tearDown(self):
        super(TestPatrimonioComEquipamenpoVazio, self).tearDown()

    def test_equipamento_vazio(self):
        """
        Testa equipamentos com part_number vazio
        """
        eq = Equipamento.objects.create(id=1, part_number="", modelo="", descricao="")

        tipo1 = Tipo.objects.create(nome='tipo1')
        tipo2 = Tipo.objects.create(nome='tipo2')

        patr1 = Patrimonio.objects.create(part_number="", modelo="m2", descricao="", tipo=tipo1, equipamento=eq,  # @UnusedVariable
                                          checado=True)
        patr2 = Patrimonio.objects.create(part_number="pn1", modelo="m2", descricao="", tipo=tipo2, checado=True)  # @UnusedVariable
        patr3 = Patrimonio.objects.create(part_number="pn1", modelo="m2", descricao="", tipo=tipo2, checado=True)

        verficacao = VerificacaoPatrimonio()
        retorno = verficacao.equipamentoVazio()

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 2)

        # check filter
        filtro = {"filtro_tipo_patrimonio": 1}
        retorno = verficacao.equipamentoVazio(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 0)

        patr3.tipo = tipo1
        patr3.save()

        retorno = verficacao.equipamentoVazio(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 1)

    def test_descricao_diferente(self):
        """
        Testa patrimonio e equipamentos com descricao diferente
        """
        eq1 = Equipamento.objects.create(id=1, part_number="", modelo="", descricao="desc1")
        eq2 = Equipamento.objects.create(id=2, part_number="", modelo="", descricao="")
        eq3 = Equipamento.objects.create(id=3, part_number="", modelo="", descricao="desc3")

        tipo1 = Tipo.objects.create(nome='tipo1')
        tipo2 = Tipo.objects.create(nome='tipo2')

        patr1 = Patrimonio.objects.create(part_number="pt1", modelo="pt1", descricao="desc1", tipo=tipo1,  # @UnusedVariable
                                          equipamento=eq1, checado=True)
        patr2 = Patrimonio.objects.create(part_number="pt2", modelo="pt2", descricao="", tipo=tipo1,  # @UnusedVariable
                                          equipamento=eq2, checado=True)
        patr3 = Patrimonio.objects.create(part_number="pt3", modelo="pt3", descricao="desc11111", tipo=tipo2,
                                          equipamento=eq3, checado=True)

        verficacao = VerificacaoPatrimonioEquipamento()
        retorno = verficacao.descricaoDiferente()

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 1)

        # check filter
        filtro = {"filtro_tipo_patrimonio": 1}
        retorno = verficacao.descricaoDiferente(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 0)

        patr3.tipo = tipo1
        patr3.save()

        retorno = verficacao.descricaoDiferente(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 1)

    def test_tamanho_diferente(self):
        """
        Testa patrimonio e equipamentos com tamanhos diferente
        """
        eq1 = Equipamento.objects.create(id=1, part_number="", modelo="", descricao="", tamanho=1.0)
        eq2 = Equipamento.objects.create(id=2, part_number="", modelo="", descricao="")
        eq3 = Equipamento.objects.create(id=3, part_number="", modelo="", descricao="", tamanho=1.0)

        tipo1 = Tipo.objects.create(nome='tipo1')
        tipo2 = Tipo.objects.create(nome='tipo2')

        patr1 = Patrimonio.objects.create(part_number="pt1", modelo="pt1", descricao="pt1", tamanho=1.0,  # @UnusedVariable
                                          tipo=tipo1, equipamento=eq1, checado=True)
        patr2 = Patrimonio.objects.create(part_number="pt2", modelo="pt2", descricao="pt2", tipo=tipo1,  # @UnusedVariable
                                          equipamento=eq2, checado=True)
        patr3 = Patrimonio.objects.create(part_number="pt3", modelo="pt3", descricao="pt3", tamanho=11.0,
                                          tipo=tipo2, equipamento=eq3, checado=True)

        verficacao = VerificacaoPatrimonioEquipamento()
        retorno = verficacao.tamanhoDiferente()

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 1)

        # check filter
        filtro = {"filtro_tipo_patrimonio": 1}
        retorno = verficacao.tamanhoDiferente(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 0)

        patr3.tipo = tipo1
        patr3.save()

        retorno = verficacao.tamanhoDiferente(filtro)

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 1)

    def test_copy_attribute__equipamento__descricao(self):
        """
        Testa a copia de atributos entre patrimonio e equipamento
        """
        eq1 = Equipamento.objects.create(id=1, part_number="", modelo="", descricao="")
        tipo = Tipo.objects.create()
        patr = Patrimonio.objects.create(id=2, part_number="part_number1", modelo="modelo1", descricao="descricao1",
                                         tipo=tipo, equipamento=eq1, checado=True)

        # verifica se o valor do atributo está diferente ANTES do teste
        self.assertNotEqual(patr.descricao, patr.equipamento.descricao)
        verficacao = VerificacaoPatrimonioEquipamento()
        verficacao.copy_attribute('equipamento', 2, 'descricao')
        patr_retrieve = Patrimonio.objects.get(pk=2)
        eq_retrieve = Equipamento.objects.get(pk=1)
        self.assertEqual(patr_retrieve.descricao, eq_retrieve.descricao)
        self.assertEqual(eq_retrieve.descricao, 'descricao1')

    def test_copy_attribute__patrimonio__descricao(self):
        """
        Testa a copia de atributos entre equipamento e patrimonio
        """
        eq1 = Equipamento.objects.create(id=1, part_number="part_number1", modelo="modelo1", descricao="descricao1")
        tipo = Tipo.objects.create()
        patr = Patrimonio.objects.create(id=2, part_number="", modelo="", descricao="", tipo=tipo, equipamento=eq1,
                                         checado=False)

        # verifica se o valor do atributo está diferente ANTES do teste
        self.assertNotEqual(patr.descricao, patr.equipamento.descricao)
        verficacao = VerificacaoPatrimonioEquipamento()
        verficacao.copy_attribute('patrimonio', 2, 'descricao')
        patr_retrieve = Patrimonio.objects.get(pk=2)
        eq_retrieve = Equipamento.objects.get(pk=1)
        self.assertEqual(patr_retrieve.descricao, eq_retrieve.descricao)
        self.assertEqual(patr_retrieve.descricao, 'descricao1')

    def test_copy_attribute__patrimonio__procedencia(self):
        ent = Entidade.objects.create(sigla='HP', nome='Hewlet', cnpj='00.000.000/0000-00', fisco=True, url='')
        equip = Equipamento.objects.create(id=1, entidade_fabricante=ent)
        tipo = Tipo.objects.create()
        patr = Patrimonio.objects.create(id=2, tipo=tipo, equipamento=equip)

        # verifica se o valor do atributo está diferente ANTES do teste
        self.assertNotEqual(patr.entidade_procedencia, equip.entidade_fabricante)
        verficacao = VerificacaoPatrimonioEquipamento()
        verficacao.copy_attribute('patrimonio', 2, 'procedencia')
        # verifica se o valor do atributo está diferente DEPOIS do teste
        patr_retrieve = Patrimonio.objects.get(pk=2)
        eq_retrieve = Equipamento.objects.get(pk=1)
        self.assertEqual(patr_retrieve.entidade_procedencia, eq_retrieve.entidade_fabricante)


class TestEquipamentoPNvVazio(TestCase):
    """
    Testa equipamentos com part_number vazio e com modelo vazio
    """
    def test_pn_vazio(self):
        eq = Equipamento.objects.create(part_number="", modelo="", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="", modelo="", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVazioModeloVazio()

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 2)


class TestEquipamentoPNvsModelo(TestCase):

    # teste sem nenhum pn duplicado mas sem modelos diferentes
    def test_sem_pn_duplicados(self):
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn2", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno), 0)

    # teste com dois PN duplicados mas sem modelos diferentes
    def test_com_multiplos_pn_duplicados(self):
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn2", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno), 0)

    # teste com dois PN duplicados mas sem modelos diferentes
    def test_com_dois_pn_duplicados(self):
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn2", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn2", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno), 0)

    # teste com dois PN duplicados mas com modelos diferentes
    def test_com_dois_pn_modelos_duplicados_diferentes(self):
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno[0]), 3)

    # teste com dois PN duplicados mas com modelos diferentes
    def test_com_dois_pn_modelos_diferentes(self):
        eq = Equipamento.objects.create(part_number="pn1", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="pn1", modelo="m2", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno[0]), 2)

    # teste com dois PN vazio
    def test_com_dois_pn_modelos_diferentes_e_modelos_iguais(self):
        eq = Equipamento.objects.create(part_number="", modelo="m1", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="p1", modelo="m2", descricao="")  # @UnusedVariable
        eq = Equipamento.objects.create(part_number="p1", modelo="m1", descricao="")  # @UnusedVariable

        verficacao = VerificacaoEquipamento()
        retorno = verficacao.partNumberVSModeloDiferente()

        self.assertEqual(len(retorno), 1)
        self.assertEqual(len(retorno[0]), 2)
