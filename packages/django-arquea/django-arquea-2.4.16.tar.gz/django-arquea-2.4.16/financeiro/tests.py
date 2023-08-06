# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.test import TestCase
from decimal import Decimal

from datetime import date, datetime
from outorga.models import Termo, Item, OrigemFapesp, Estado as EstadoOutorga, Categoria, Outorga, Modalidade, Natureza_gasto, \
    Acordo
from identificacao.models import Entidade, Contato, Identificacao, Endereco
from protocolo.models import Protocolo, TipoDocumento, Origem, Estado as EstadoProtocolo
from financeiro.models import Pagamento, ExtratoCC, Estado as EstadoFinanceiro, TipoComprovante, Auditoria,\
    TipoComprovanteFinanceiro, ExtratoFinanceiro, LocalizaPatrocinio, ExtratoPatrocinio


class ExtratoCCTest(TestCase):
    def setUp(self):
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)
        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB1', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m11 = Modalidade.objects.create(sigla='STB2', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE1', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)  # @UnusedVariable

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m11, termo=t, valor_concedido='3000000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00',
                                       fisco=True, url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00',
                                       fisco=True, url='')

        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        cot2 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='')

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, funcao='Tecnico', area='Estoque', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=cot2, funcao='Gerente', area='Redes', ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=8888, data_vencimento=date(2008, 10, 5),
                                      descricao='Conta mensal - armazenagem 09/2008', valor_total=None,
                                      moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden2, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 11), origem=og, estado=ep,
                                      num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', valor_total=None,
                                      moeda_estrangeira=False)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 1), cod_oper=4444,
                                       valor='250000', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        a3 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')  # @UnusedVariable

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        of2 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i2)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='250000')  # @UnusedVariable

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=fp1, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

    def test_unicode(self):
        extrato = ExtratoCC.objects.get(pk=1)
        self.assertEquals(extrato.__unicode__(), u'2008-10-05 - 333333 - TED - 2650.00')

    def test_saldo(self):
        extrato = ExtratoCC.objects.get(pk=1)
        self.assertEquals(extrato.saldo, Decimal('252650.00'))

    def test_saldo_anterior(self):
        extrato = ExtratoCC.objects.get(pk=1)
        self.assertEquals(extrato.saldo_anterior, Decimal('250000.00'))

    def test_parciais(self):
        extrato = ExtratoCC.objects.get(pk=1)
        self.assertEquals(extrato.parciais(), u'STB1 [parcial 101 (102)]  ')


class TipoComprovanteFinanceiroTest(TestCase):
    def setUp(self):
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")  # @UnusedVariable

    def test_unicode(self):
        tipo = TipoComprovante.objects.get(pk=1)
        self.assertEquals(tipo.__unicode__(), u'Tipo Comprovante 1')


class ExtratoFinanceiroTest(TestCase):
    def setUp(self):
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)

        tcomprov1 = TipoComprovanteFinanceiro.objects.create(nome="Tipo Comprovante Financeiro 1")

        exf1 = ExtratoFinanceiro.objects.create(termo=t, data_libera='2013-08-10', cod='EFC', historico="historico",  # @UnusedVariable
                                                valor=123456, tipo_comprovante=tcomprov1, parcial=543)

    def test_unicode(self):
        exf = ExtratoFinanceiro.objects.get(pk=1)
        self.assertEquals(exf.__unicode__(), u'2013-08-10 - EFC - historico - 123456.00')

    def test_despesa_caixa_falso(self):
        exf = ExtratoFinanceiro.objects.get(pk=1)
        self.assertFalse(exf.despesa_caixa)

    def test_despesa_caixa(self):
        tcomprov1 = TipoComprovanteFinanceiro(pk=1)
        tcomprov1.nome = u'Despesa de caixa'
        tcomprov1.save()

        exf = ExtratoFinanceiro.objects.get(pk=1)
        exf.tipo = tcomprov1
        exf.save()

        self.assertTrue(exf.despesa_caixa)

    def test_cria_entrada_extrato_cc(self):
        exf = ExtratoFinanceiro.objects.get(pk=1)
        self.assertIsNone(exf.entrada_extrato_cc)

        retorno = ExtratoFinanceiro._insere_extrato_cc(exf)
        self.assertEqual(retorno, 1)

        self.assertIsNotNone(exf.entrada_extrato_cc)

    def test_delete_cascade_entrada_extrato_cc(self):
        exf = ExtratoFinanceiro.objects.get(pk=1)
        self.assertIsNone(exf.entrada_extrato_cc)

        # verificando se foi inserido no ExtratoCC
        retorno = ExtratoFinanceiro._insere_extrato_cc(exf)
        self.assertEqual(retorno, 1)

        self.assertIsNotNone(exf.entrada_extrato_cc)

        # removendo o objeto do BD
        exf.entrada_extrato_cc.delete()

        # verificando se o extratoCC foi removido do BD
        extratoccs = ExtratoCC.objects.filter(pk=exf.entrada_extrato_cc_id)
        self.assertEqual(len(extratoccs), 0)

        # verificando se o ExtratoFinanceiro não foi removido do BD com CASCADE
        extratofinanceiro = ExtratoCC.objects.filter(pk=1)
        self.assertIsNotNone(extratofinanceiro)


class PagamentoTest(TestCase):
    def setUp(self):
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB1', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m11 = Modalidade.objects.create(sigla='STB2', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE1', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)  # @UnusedVariable

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m11, termo=t, valor_concedido='3000000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')

        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        cot2 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='')

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, funcao='Tecnico', area='Estoque', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=cot2, funcao='Gerente', area='Redes', ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=8888, data_vencimento=date(2008, 10, 5),
                                      descricao='Conta mensal - armazenagem 09/2008', valor_total=None,
                                      moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden2, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 11), origem=og, estado=ep,
                                      num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', valor_total=None,
                                      moeda_estrangeira=False)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 1), cod_oper=4444,
                                       valor='250000', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        a3 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')  # @UnusedVariable

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        of2 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i2)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')  # @UnusedVariable
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='250000')  # @UnusedVariable

    def test_unicode(self):
        exf = Pagamento.objects.get(pk=1)
        self.assertEquals(exf.__unicode__(), u'8888 - 2650.00 - STB1    ID: 1')

    def test_unicode_com_patrocinio(self):
        exf = Pagamento.objects.get(pk=1)
        exf.valor_patrocinio = 1234

        self.assertEquals(exf.__unicode__(), u'8888 - 3884.00 - STB1    ID: 1')

    def test_unicode_com_auditoria(self):
        exf = Pagamento.objects.get(pk=1)

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=exf, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

        self.assertEquals(exf.__unicode__(), u'8888 - 2650.00 - STB1, parcial 101, página 102    ID: 1')

    def test_unicode_para_auditoria(self):
        exf = Pagamento.objects.get(pk=1)

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=exf, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

        self.assertEquals(exf.unicode_para_auditoria(), u'8888 - 2650.00 - STB1    ID: 1')

    def test_codigo_operacao(self):
        exf = Pagamento.objects.get(pk=1)
        self.assertEquals(exf.codigo_operacao(), 333333)

    def test_codigo_operacao_vazio(self):
        exf = Pagamento.objects.get(pk=1)
        exf.conta_corrente = None

        self.assertEquals(exf.codigo_operacao(), '')

    def test_anexos(self):
        exf = Pagamento.objects.get(pk=1)
        exf.conta_corrente = None

        self.assertEquals(exf.anexos(), u'Não')

    def test_anexos_com_auditoria(self):
        exf = Pagamento.objects.get(pk=1)
        exf.conta_corrente = None

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=exf, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

        self.assertEquals(exf.anexos(), u'Sim')

    def test_termo(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.termo(), u'08/22222-2')

    def test_item(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.item(), u'08/22222-2 - Armazenagem')

    def test_item_sem_origem_fapesp(self):
        exf = Pagamento.objects.get(pk=1)
        exf.origem_fapesp = None

        self.assertEquals(exf.item(), u'Não é Fapesp')

    def test_data(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.data(), date(2008, 10, 5))

    def test_nota(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.nota(), u'8888')

    def test_formata_valor_fapesp(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.formata_valor_fapesp(), u'R$ 2.650,00')

    def test_formata_valor_fapesp_dolar(self):
        exf = Pagamento.objects.get(pk=1)
        exf.origem_fapesp.item_outorga.natureza_gasto.modalidade.moeda_nacional = False

        self.assertEquals(exf.formata_valor_fapesp(), u'US$ 2.650,00')

    def test_pagina(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.pagina(), u'')

    def test_pagina_com_auditoria(self):
        exf = Pagamento.objects.get(pk=1)
        exf.conta_corrente = None

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=exf, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

        self.assertEquals(exf.pagina(), 102)

    def test_parcial(self):
        exf = Pagamento.objects.get(pk=1)

        self.assertEquals(exf.parcial(), u'')

    def test_parcial_com_auditoria(self):
        exf = Pagamento.objects.get(pk=1)
        exf.conta_corrente = None

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")
        audit1 = Auditoria.objects.create(estado=efi1, pagamento=exf, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

        self.assertEquals(exf.parcial(), 101)


class LocalizaPatrocinioTest(TestCase):
    def setUp(self):
        localiza = LocalizaPatrocinio.objects.create(consignado='Consignado')  # @UnusedVariable

    def test_unicode(self):
        localiza = LocalizaPatrocinio.objects.get(pk=1)
        self.assertEquals(localiza.__unicode__(), u'Consignado')


class ExtratoPatrocinioTest(TestCase):
    def setUp(self):
        localiza = LocalizaPatrocinio.objects.create(consignado='Consignado')
        extrato = ExtratoPatrocinio.objects.create(localiza=localiza, data_oper=date(2013, 02, 01), cod_oper=123,  # @UnusedVariable
                                                   valor=1234.56, historico='Histórico', obs='Observação')

    def test_unicode(self):
        extrato = ExtratoPatrocinio.objects.get(pk=1)
        self.assertEquals(extrato.__unicode__(), u'Consignado - 2013-02-01 - 1234.56')


class EstadoTest(TestCase):
    def setUp(self):
        estado = EstadoFinanceiro .objects.create(nome='Estado Financeiro - nome')  # @UnusedVariable

    def test_unicode(self):
        estado = EstadoFinanceiro.objects.get(pk=1)
        self.assertEquals(estado.__unicode__(), u'Estado Financeiro - nome')


class AuditoriaTest(TestCase):
    def setUp(self):
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)
        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB1', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m11 = Modalidade.objects.create(sigla='STB2', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE1', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)  # @UnusedVariable

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m11, termo=t, valor_concedido='3000000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')

        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        cot2 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='')

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, funcao='Tecnico', area='Estoque', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=cot2, funcao='Gerente', area='Redes', ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=8888, data_vencimento=date(2008, 10, 5),
                                      descricao='Conta mensal - armazenagem 09/2008', valor_total=None,
                                      moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden2, tipo_documento=td,
                                      data_chegada=datetime(2008, 9, 30, 10, 11), origem=og, estado=ep,
                                      num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', valor_total=None,
                                      moeda_estrangeira=False)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 1), cod_oper=4444,
                                       valor='250000', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        of2 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i2)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='250000')  # @UnusedVariable

        efi1 = EstadoFinanceiro.objects.create(nome="Estado financeiro 1")
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=fp1, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable
                                          obs='observacao')

    def test_unicode(self):
        audit1 = Auditoria.objects.get(pk=1)
        self.assertEquals(audit1.__unicode__(), u'Parcial: 101, página: 102')


class TipoComprovanteTest(TestCase):
    def setUp(self):
        tcomprov1 = TipoComprovante.objects.create(nome="Tipo Comprovante 1")  # @UnusedVariable

    def test_unicode(self):
        tcomprov1 = TipoComprovante.objects.get(pk=1)
        self.assertEquals(tcomprov1.__unicode__(), u'Tipo Comprovante 1')
