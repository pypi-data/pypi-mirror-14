# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date, timedelta, datetime
from decimal import Decimal
from django.http import QueryDict
from django.conf import settings
from utils.UnitTestCase import UnitTestCase
import mock
from django.core.urlresolvers import reverse

from outorga.models import Termo, Item, OrigemFapesp, Estado as EstadoOutorga, Categoria, Outorga, Modalidade, \
    Natureza_gasto, Acordo, Contrato, OrdemDeServico, TipoContrato, ArquivoOS, Arquivo, EstadoOS
from financeiro.models import Pagamento, ExtratoCC, Estado as EstadoFinanceiro
from identificacao.models import Entidade, Contato, Identificacao, Endereco
from protocolo.models import Protocolo, ItemProtocolo, TipoDocumento, Origem, Estado as EstadoProtocolo

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TermoTest(UnitTestCase):
    def setUp(self):
        super(TermoTest, self).setUp()

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
        m1 = Modalidade.objects.create(sigla='STB0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m11 = Modalidade.objects.create(sigla='STB1', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)
        m22 = Modalidade.objects.create(sigla='STE1', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m11, termo=t, valor_concedido='3000000.00')
        n3 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='1000000.00')
        n4 = Natureza_gasto.objects.create(modalidade=m22, termo=t, valor_concedido='2000000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        ent3 = Entidade.objects.create(sigla='TERREMARK', nome='Terremark do Brasil', cnpj='00.000.000/0000-00',
                                       fisco=True, url='')

        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)
        end3 = Endereco.objects.create(entidade=ent3)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)
        i3 = Item.objects.create(entidade=ent3, natureza_gasto=n3, descricao='Serviço de Conexão',
                                 justificativa='Ligação SP-CPS', quantidade=12, valor=100000)
        i4 = Item.objects.create(entidade=ent3, natureza_gasto=n4, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Ajuste na cobrança do Link Internacional', quantidade=6, valor=50000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='', ativo=True)
        cot2 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='', ativo=True)
        cot3 = Contato.objects.create(primeiro_nome='Marcos', email='alex@alex.com.br', tel='', ativo=True)

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, funcao='Tecnico', area='Estoque', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=cot2, funcao='Gerente', area='Redes', ativo=True)
        iden3 = Identificacao.objects.create(endereco=end3, contato=cot3, funcao='Diretor', area='Redes', ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=datetime(2008, 9, 30, 10, 10), origem=og,
                                      estado=ep, num_documento=8888, data_vencimento=date(2008, 10, 5),
                                      descricao='Conta mensal - armazenagem 09/2008', valor_total=None, moeda_estrangeira=False)

        p2 = Protocolo.objects.create(termo=t, identificacao=iden2, tipo_documento=td, data_chegada=datetime(2008, 9, 30, 10, 10), origem=og,
                                      estado=ep, num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', valor_total=None, moeda_estrangeira=False)

        p3 = Protocolo.objects.create(termo=t, identificacao=iden3, tipo_documento=td, data_chegada=datetime(2008, 9, 30, 10, 10),
                                      origem=og, estado=ep, num_documento=5555, data_vencimento=date(2008, 10, 15),
                                      descricao='Serviço de Conexão Local - 09/2009', valor_total=None, moeda_estrangeira=False)

        # Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.create(protocolo=p1, descricao='Tarifa mensal - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=2500)
        ip2 = ItemProtocolo.objects.create(protocolo=p1, descricao='Reajuste tarifa mensal - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=150)
        ip3 = ItemProtocolo.objects.create(protocolo=p2, descricao='Conexão Internacional - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=250000)
        ip4 = ItemProtocolo.objects.create(descricao='Reajuste do serviço de Conexão Internacional - 09/2009',  # @UnusedVariable
                                           protocolo=p2, quantidade=1, valor_unitario=50000)
        ip5 = ItemProtocolo.objects.create(protocolo=p3, descricao='Conexão Local - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=85000)
        ip6 = ItemProtocolo.objects.create(protocolo=p3, descricao='Reajuste do serviço de Conexão Local - 09/2009',  # @UnusedVariable
                                           quantidade=1, valor_unitario=15000)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')
        ef2 = EstadoOutorga.objects.create(nome='Concluído')  # @UnusedVariable

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 10), cod_oper=4444,
                                       valor='250000', historico='TED', despesa_caixa=False)
        ex3 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 10), cod_oper=4444,
                                       valor='50000', historico='TED', despesa_caixa=False)
        ex4 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 15), cod_oper=5555,
                                       valor='100000', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        a3 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')
        a4 = Acordo.objects.create(estado=ef1, descricao='Acordo de patrocínio entre ANSP e Telefônica')  # @UnusedVariable

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        of2 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i2)
        of3 = OrigemFapesp.objects.create(acordo=a3, item_outorga=i3)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')  # @UnusedVariable
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='250000')  # @UnusedVariable
        fp3 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex3, valor_patrocinio='50000', valor_fapesp=0)  # @UnusedVariable
        fp4 = Pagamento.objects.create(protocolo=p3, conta_corrente=ex4, origem_fapesp=of3, valor_fapesp='100000')  # @UnusedVariable

    def tearDown(self):
        super(TermoTest, self).tearDown()

    def test_unicode(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.__unicode__(), u'08/22222-2')

    def test_valor_concedido_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.real, Decimal('4500000'))

    def test_termo_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.termo_real(), '<b>R$ 4.500.000,00</b>')

    def test_termo_real_negativo(self):
        termo = Termo.objects.get(pk=1)

        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = -5000000
        n1.save()

        self.assertEquals(termo.termo_real(), '-')

    def test_valor_concedido_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.dolar, Decimal('3000000'))

    def test_termo_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.termo_dolar(), '$ 3,000,000.00')

    def test_termo_dolar_negativo(self):
        termo = Termo.objects.get(pk=1)

        n1 = Natureza_gasto.objects.get(pk=3)
        n1.valor_concedido = -9000000
        n1.save()

        self.assertEquals(termo.termo_dolar(), '-')

    def test_duracao_meses(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.duracao_meses(), '12 meses')

    def test_duracao_meses__menos_1_mes(self):
        termo = Termo.objects.get(pk=1)
        termo.inicio = date(2008, 12, 15)

        self.assertEquals(termo.duracao_meses(), '-')

    def test_duracao_meses__1_mes(self):
        termo = Termo.objects.get(pk=1)
        termo.inicio = date(2008, 12, 1)

        self.assertEquals(termo.duracao_meses(), u'1 mês')

    def test_duracao_meses__2_meses(self):
        termo = Termo.objects.get(pk=1)
        termo.inicio = date(2008, 10, 4)

        self.assertEquals(termo.duracao_meses(), '3 meses')

    def test_total_realizado_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.total_realizado_real, Decimal('252650.00'))

    def test_formata_realizado_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_realizado_real(), '<b>R$ 252.650,00</b>')

    def test_formata_realizado_real__vazio(self):
        termo = Termo.objects.get(pk=1)

        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 0
        pg1.save()

        pg2 = Pagamento.objects.get(pk=2)
        pg2.valor_fapesp = 0
        pg2.save()

        self.assertEquals(termo.formata_realizado_real(), '-')

    def test_formata_realizado_real__negativo(self):
        termo = Termo.objects.get(pk=1)

        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 9000000
        pg1.save()

        self.assertEquals(termo.formata_realizado_real(), u'<span style="color: red"><b>R$ 9.250.000,00</b></span>')

    def test_total_realizado_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.total_realizado_dolar, Decimal('100000.00'))

    def test_formata_realizado_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_realizado_dolar(), '$ 100,000.00')

    def test_formata_realizado_dolar__vazio(self):
        termo = Termo.objects.get(pk=1)

        pg2 = Pagamento.objects.get(pk=2)
        pg2.valor_fapesp = 0
        pg2.save()

        pg4 = Pagamento.objects.get(pk=4)
        pg4.valor_fapesp = 0
        pg4.save()

        self.assertEquals(termo.formata_realizado_dolar(), '-')

    def test_formata_realizado_dolar__negativo(self):
        termo = Termo.objects.get(pk=1)

        m1 = Modalidade.objects.get(sigla='STB0')
        m1.moeda_nacional = False
        m1.save()
        m2 = Modalidade.objects.get(sigla='STB1')
        m2.moeda_nacional = False
        m2.save()

        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 9000000
        pg1.save()

        self.assertEquals(termo.formata_realizado_dolar(), u'<span style="color: red">$ 9,350,000.00</span>')

    def test_num_processo(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.num_processo, '08/22222-2')

    def test_vigencia(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.vigencia, '12 meses')

    def test_saldo_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.saldo_real(), Decimal('4247350.00'))

    def test_saldo_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.saldo_dolar(), Decimal('2900000.00'))

    def test_formata_saldo_real(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_saldo_real(), '<b>R$ 4.247.350,00</b>')

    def test_formata_saldo_dolar(self):
        termo = Termo.objects.get(pk=1)
        self.assertEquals(termo.formata_saldo_dolar(), '$ 2,900,000.00')

    def test_termo_ativo__none(self):
        termo = Termo.termo_ativo()
        self.assertIsNone(termo)

    def test_termo_ativo(self):
        hoje = datetime.now().date()

        termo = Termo.objects.get(pk=1)
        termo.inicio = hoje - timedelta(days=1)
        termo.save()

        outorga = Outorga.objects.get(pk=1)
        outorga.termino = hoje + timedelta(days=1)
        outorga.save()

        termo = Termo.termo_ativo()
        self.assertEquals(termo.id, 1)


#     def test_real(self):
#         termo = Termo.objects.get(pk=1)
#         self.assertEquals(Termo.termos_auditoria_fapesp_em_aberto(), ['<Termo: 08/22222-2>'])
#
#     def test_real(self):
#         termo = Termo.objects.get(pk=1)
#         self.assertEquals(Termo.termos_auditoria_interna_em_aberto(), ['<Termo: 08/22222-2>'])


class CategoriaTest(UnitTestCase):
    def setUp(self):
        super(CategoriaTest, self).setUp()
        c = Categoria.objects.create(nome='Transposicao')  # @UnusedVariable

    def tearDown(self):
        super(CategoriaTest, self).tearDown()

    def test_unicode(self):
        c = Categoria.objects.get(pk=1)
        self.assertEquals(c.__unicode__(), u'Transposicao')


class OutorgaTest(UnitTestCase):
    def setUp(self):
        super(OutorgaTest, self).setUp()
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='1500000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',  # @UnusedVariable
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

    def tearDown(self):
        super(OutorgaTest, self).tearDown()

    def test_unicode(self):
        o1 = Outorga.objects.get(pk=1)
        self.assertEquals(o1.__unicode__(), '08/22222-2 - Inicial')

    def test_inicio(self):
        o1 = Outorga.objects.get(pk=1)
        self.assertEquals(o1.inicio, '01/01/2008')

    def test_mostra_categoria(self):
        o1 = Outorga.objects.get(pk=1)
        self.assertEquals(o1.mostra_categoria(), 'Inicial')

    def test_mostra_termo(self):
        o1 = Outorga.objects.get(pk=1)
        self.assertEquals(o1.mostra_termo(), '08/22222-2')

    def test_existe_arquivo(self):
        o1 = Outorga.objects.get(pk=1)
        self.assertEquals(o1.existe_arquivo(), ' ')

    def test_existe_arquivo__com_arquivo(self):
        o1 = Outorga.objects.get(pk=1)
        o1.arquivo = 'teste.pdf'

        self.assertEquals(o1.existe_arquivo(), '<center><a href="%s?outorga__id__exact=1">'
                                               '<img src="%simg/arquivo.png" /></a></center>'
                          % (reverse('admin:outorga_arquivo_changelist'), settings.STATIC_URL))


class OutorgaViewTest(UnitTestCase):
    def setUp(self):
        super(OutorgaViewTest, self).setUp()
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='1500000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

        # Entidades para o teste da View ###
        cont1 = Contrato.objects.create(numero='1111/11', descricao='contrato1', entidade=ent1, auto_renova=False,
                                        data_inicio=date(2013, 1, 02), limite_rescisao=date(2013, 1, 3))

        # Cria uma Ordem de Serviço
        estadoOs = EstadoOS.objects.create(nome="Vigente")
        tipo = TipoContrato.objects.create(nome='Tipo Fixo')
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')
        acordo = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        os = OrdemDeServico.objects.create(acordo=acordo, contrato=cont1, tipo=tipo, estado=estadoOs, numero=66666,  # @UnusedVariable
                                           data_inicio=date(2008, 2, 1), data_rescisao=date(2008, 11, 1),
                                           antes_rescisao=2, descricao='OS 34567 - Contratação de mais um link')

        of1 = OrigemFapesp.objects.create(acordo=acordo, item_outorga=i1)  # @UnusedVariable

    def test_call__relatorio_contratos_por_entidade(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import contratos
            mock_request = mock.Mock()
            # mockin request GET parameters
            mock_request.method = "GET"
            mock_request.GET = QueryDict("entidade=0&estadoos=0")

            # call view
            contratos(mock_request)

            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/contratos.html', 'Template errado.')
            self.assertEquals(args[2]['entidades'][0]['entidade'], 'GTECH')
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['numero'], '1111/11')
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['inicio'], date(2013, 1, 2))
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['termino'], date(2013, 1, 3))
#             self.assertEquals(args[2]['entidades'][0]['contratos'][0]['arquivo'], '1111/11')
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['auto'], False)
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['os'][0].tipo.nome, 'Tipo Fixo')
            self.assertEquals(args[2]['entidades'][0]['contratos'][0]['os'][0].numero, u'66666')

    def test_call__relatorio_contratos_por_entidade__sem_os(self):
        os = OrdemDeServico.objects.get(pk=1)
        os.delete()

        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import contratos
            mock_request = mock.Mock()
            # mockin request GET parameters
            mock_request.method = "GET"
            mock_request.GET = QueryDict("entidade=1&estadoos=0")

            # call view
            contratos(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            print args[2]
            print args[2]['entidades'][0]['contratos'][0]

            self.assertTrue(len(args[2]['entidades'][0]['contratos'][0]['os']) == 0,
                            'Ordemdeservico não deve estar na resposta da view.')

    def test_call__relatorio_termos(self):

        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import relatorio_termos
            mock_request = mock.Mock()
            mock_request.method = "GET"
            # call view
            relatorio_termos(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/termos.html')
            self.assertEquals(args[2]['termos'][0].processo, 22222)

    def test_call__relatorio_termos__request_post(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import relatorio_termos
            mock_request = mock.Mock()
            mock_request.method = "POST"
            # call view
            relatorio_termos(mock_request)
            self.assertTrue(len(mock_render.mock_calls) == 0, 'Não deve responder request com POST.')

    def test_call__lista_acordos(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import lista_acordos
            mock_request = mock.Mock()
            mock_request.method = "GET"
            # call view
            lista_acordos(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/acordos.html')

            self.assertEquals(args[2]['processos'][0]['processo'].processo, 22222)
            self.assertEquals(args[2]['processos'][0]['acordos'][0]['acordo'].__unicode__(),
                              u'Acordo entre Instituto UNIEMP e SAC')
            self.assertEquals(args[2]['processos'][0]['acordos'][0]['itens'][0]['modalidade'], u'STB0')
            self.assertEquals(args[2]['processos'][0]['acordos'][0]['itens'][0]['entidade'].sigla, u'GTECH')
            self.assertEquals(args[2]['processos'][0]['acordos'][0]['itens'][0]['descricao'], u'Armazenagem')

    def test_call__lista_acordos__sem_origemfapesp(self):
        origemFapesp = OrigemFapesp.objects.get(pk=1)
        origemFapesp.delete()

        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import lista_acordos
            mock_request = mock.Mock()
            mock_request.method = "GET"
            # call view
            lista_acordos(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/acordos.html')

            self.assertEquals(args[2]['processos'][0]['processo'].processo, 22222)
            self.assertTrue(len(args[2]['processos'][0]['acordos']) == 0)

    def test_call__lista_acordos__pdf(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import lista_acordos
            mock_request = mock.Mock()
            mock_request.method = "GET"
            # call view
            response = lista_acordos(mock_request, pdf=True)
            logger.debug("Content-Type: application/pdf" in str(response))
            logger.debug("filename=file.pdf" in str(response))

    def test_call__item_modalidade__pagina_filtro_inicial(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import item_modalidade
            mock_request = mock.Mock()
            # mockin request GET parameters
            mock_request.method = "GET"
            mock_request.GET = QueryDict([])

            # call view
            item_modalidade(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/termo_mod.html')

            self.assertIsNotNone(args[2]['termos'])
            self.assertIsNotNone(args[2]['modalidades'])
            self.assertIsNotNone(args[2]['entidadesProcedencia'])
            self.assertIsNotNone(args[2]['entidadesFabricante'])
            self.assertIsNotNone(args[2]['entidadesItemOutorga'])

            self.assertIsNone(args[2]['termo'])
            self.assertIsNone(args[2]['modalidade'])
            self.assertIsNone(args[2]['entidade'])

            # Verificando se não entrou no if errado dentro da view, buscando mais informações que deveria
            self.assertFalse('itens' in args[2])

    def test_call__item_modalidade__sem_entidade(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import item_modalidade
            mock_request = mock.Mock()
            # mockin request GET parameters
            mock_request.method = "GET"
            mock_request.GET = QueryDict("&termo=1&modalidade=1")
            # call view
            item_modalidade(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/por_item_modalidade.html')

            self.assertIsNotNone(args[2]['termo'])
            self.assertIsNotNone(args[2]['modalidade'])
            self.assertIsNotNone(args[2]['itens'])
            self.assertIsNone(args[2]['entidade'])

    def test_call__item_modalidade(self):
        mock_render = mock.MagicMock()
        with mock.patch.multiple('outorga.views', render=mock_render, login_required=lambda x: x):  # @UndefinedVariable

            from outorga.views import item_modalidade
            mock_request = mock.Mock()
            # mockin request GET parameters
            mock_request.method = "GET"
            mock_request.GET = QueryDict("&termo=1&modalidade=1&entidade=1")
            # call view
            item_modalidade(mock_request)
            _, args, _ = mock_render.mock_calls[0]

            self.assertEquals(args[1], 'outorga/por_item_modalidade.html')

            self.assertIsNotNone(args[2]['termo'])
            self.assertIsNotNone(args[2]['modalidade'])
            self.assertIsNotNone(args[2]['itens'])
            self.assertIsNotNone(args[2]['entidade'])


class Natureza_gastoTest(UnitTestCase):
    def setUp(self):
        super(Natureza_gastoTest, self).setUp()

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
        m1 = Modalidade.objects.create(sigla='STB0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)
        m2 = Modalidade.objects.create(sigla='STB2', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido=Decimal('30000'))
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido=Decimal('100000'))

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', nome='Granero Tech', cnpj='00.000.000/0000-00', fisco=True,
                                       url='')
        ent2 = Entidade.objects.create(sigla='TERREMARK', nome='Terremark do Brasil', cnpj='00.000.000/0000-00',
                                       fisco=True, url='')

        end1 = Endereco.objects.create(entidade=ent1)
        end2 = Endereco.objects.create(entidade=ent2)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Armazenagem',
                                 justificativa='Armazenagem de equipamentos', quantidade=12, valor=2500)
        i2 = Item.objects.create(entidade=ent2, natureza_gasto=n1, descricao='Servico de Conexao',
                                 justificativa='Ligação SP-CPS', quantidade=12, valor=000000)
        i3 = Item.objects.create(entidade=ent2, natureza_gasto=n2, descricao='Servico de Conexao',
                                 justificativa='Ligação SP-CPS', quantidade=12, valor=100000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        cot2 = Contato.objects.create(primeiro_nome='Marcos', email='alex@alex.com.br', tel='')

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, funcao='Tecnico', area='Estoque', ativo=True)
        iden2 = Identificacao.objects.create(endereco=end2, contato=cot2, funcao='Diretor', area='Redes', ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=8888, data_vencimento=date(2008, 10, 5),
                                      descricao='Conta mensal - armazenagem 09/2008', moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden2, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=5555, data_vencimento=date(2008, 10, 15),
                                      descricao='Serviço de Conexão Local - 09/2009', moeda_estrangeira=False)

        # Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.create(protocolo=p1, descricao='Tarifa mensal - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=2500)
        ip2 = ItemProtocolo.objects.create(protocolo=p1, descricao='Reajuste tarifa mensal - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=150)
        ip3 = ItemProtocolo.objects.create(protocolo=p2, descricao='Conexão Local - 09/2009', quantidade=1,  # @UnusedVariable
                                           valor_unitario=85000)
        ip4 = ItemProtocolo.objects.create(protocolo=p2, descricao='Reajuste do serviço de Conexão Local - 09/2009',  # @UnusedVariable
                                           quantidade=1, valor_unitario=15000)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create(nome='Aprovado')
        ef2 = EstadoOutorga.objects.create(nome='Concluído')  # @UnusedVariable

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 9, 25), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 15), cod_oper=5555,
                                       valor='100000', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e GTech')
        a2 = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e Terremark')

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        of2 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i2)
        of3 = OrigemFapesp.objects.create(acordo=a2, item_outorga=i3)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')  # @UnusedVariable
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of2, valor_fapesp='100000')  # @UnusedVariable
        fp3 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of3, valor_fapesp='100000')  # @UnusedVariable

    def tearDown(self):
        super(Natureza_gastoTest, self).tearDown()

    def test_unicode(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.__unicode__(), u'08/22222-2 - STB0')

    def test_mostra_termo(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.mostra_termo(), u'08/22222-2')

    def test_mostra_modalidade(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.mostra_modalidade(), u'STB0')

    def test_get_absolute_url(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.get_absolute_url(), reverse('admin:outorga_natureza_gasto_change', args=(1,)))

    def test_formata_valor(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.formata_valor(1200000.00), u'R$ 1.200.000,00')

    def test_total_realizado(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.total_realizado, Decimal('102650'))

    def test_total_realizado_parcial(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEqual(n1.total_realizado_parcial(5, 2008, 9, 2008), Decimal('2650'))
        self.assertEqual(n1.total_realizado_parcial(5, 2008, 12, 2008), Decimal('102650'))
        self.assertEqual(n1.total_realizado_parcial(10, 2008, 12, 2008), Decimal('100000'))

    def test_formata_total_realizado__zero(self):
        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 0
        pg1.save()

        pg2 = Pagamento.objects.get(pk=2)
        pg2.valor_fapesp = 0
        pg2.save()

        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.formata_total_realizado(), '-', 'Total realizado possui valor diferente de zero.')

    def test_formata_total_realizado__negativo(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.formata_total_realizado(), '<span style="color: red">R$ 102.650,00</span>',
                          'Total realizado não possui valor negativo.')

    def test_formata_total_realizado__positivo(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = 9000000
        self.assertEquals(n1.formata_total_realizado(), 'R$ 102.650,00', 'Total realizado não possui valor positivo.')

    def test_soma_itens_menos_que_concedido(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.soma_itens(), '<span style="color: red">R$ 2.500,00</span>')

    def test_soma_itens(self):
        n2 = Natureza_gasto.objects.get(pk=2)
        self.assertEquals(n2.soma_itens(), 'R$ 100.000,00')

    def test_soma_itens__diff_total(self):
        n2 = Natureza_gasto.objects.get(pk=2)
        n2.valor_concedido = n2.valor_concedido - 100000
        self.assertEquals(n2.soma_itens(), '<span style="color: red">R$ 100.000,00</span>',
                          'Valor concedido é diferente do total dos itens.')

    def test_soma_itens__zero(self):
        n2 = Natureza_gasto.objects.get(pk=2)
        n2.valor_concedido = 0
        i1 = Item.objects.get(pk=1)
        i1.valor = 0
        i1.save()

        i2 = Item.objects.get(pk=2)
        i2.valor = 0
        i2.save()

        i3 = Item.objects.get(pk=3)
        i3.valor = 0
        i3.save()

        self.assertEquals(n2.soma_itens(), '-', 'A soma dos valores dos itens não é zero.')

    def test_todos_itens(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        r = n1.todos_itens()
        self.assertTrue(len(r) == 2)
        self.assertEquals(str(r[0]), u'08/22222-2 - Armazenagem')
        self.assertEquals(str(r[1]), u'08/22222-2 - Servico de Conexao')

    def test_total_concedido_mod_termo(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.total_concedido_mod_termo(), 'R$ 30.000,00')

    def test_total_concedido_mod_termo__zero(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = 0
        n1.save()

        self.assertEquals(n1.total_concedido_mod_termo(), 'R$ 0,00')

    def test_v_concedido(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        self.assertEquals(n1.v_concedido(), 'R$ 30.000,00')

    def test_v_concedido__zero(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = 0
        n1.save()

        self.assertEquals(n1.v_concedido(), 'R$ 0,00')

    def test_v_concedido__none(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = None

        self.assertEquals(n1.v_concedido(), '-')

    def test_saldo__negativo(self):
        n1 = Natureza_gasto.objects.get(pk=1)

        self.assertEquals(n1.saldo(), '<span style="color: red">R$ -72.650,00</span>')

    def test_saldo__positivo(self):
        n1 = Natureza_gasto.objects.get(pk=1)
        n1.valor_concedido = 9000000

        self.assertEquals(n1.saldo(), 'R$ 8.897.350,00')

    def test_valor_saldo(self):
        n1 = Natureza_gasto.objects.get(pk=1)

        self.assertEquals(n1.valor_saldo(), Decimal('-72650.00'))


class ItemTest(UnitTestCase):
    def setUp(self):
        super(ItemTest, self).setUp()
        # Cria Termo
        eo1 = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, inicio=date(2008, 1, 1), estado=eo1, processo=22222, digito=2)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1), termino=date(2008, 12, 31),  # @UnusedVariable
                                    data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)
        m2 = Modalidade.objects.create(sigla='STF0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='300000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent1)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)
        i2 = Item.objects.create(entidade=ent1, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Ajuste na cobrança do Link Internacional', quantidade=6, valor=50000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='')

        iden1 = Identificacao.objects.create(contato=cot1, funcao='Gerente', area='Redes', ativo=True,
                                             endereco=endereco)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 10, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=5555, data_vencimento=date(2008, 11, 10),
                                      descricao='Serviço de Conexão Internacional - 10/2009', moeda_estrangeira=False)
        p3 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 10, 31, 10, 10), origem=og, estado=ep,
                                      num_documento=666, data_vencimento=date(2008, 11, 12),
                                      descricao='Serviço de Conexão Internacional - 10/2009', moeda_estrangeira=False)

        # Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.create(protocolo=p1, quantidade=1, valor_unitario=250000,  # @UnusedVariable
                                           descricao='Conexão Internacional - 09/2009')
        ip2 = ItemProtocolo.objects.create(protocolo=p1, quantidade=1, valor_unitario=50000,  # @UnusedVariable
                                           descricao='Reajuste do serviço de Conexão Internacional - 09/2009')
        ip3 = ItemProtocolo.objects.create(protocolo=p2, quantidade=1, valor_unitario=250000,  # @UnusedVariable
                                           descricao='Conexão Internacional - 10/2009')
        ip4 = ItemProtocolo.objects.create(protocolo=p2, quantidade=1, valor_unitario=50000,  # @UnusedVariable
                                           descricao='Reajuste do serviço de Conexão Internacional - 10/2009')

        # Criar Fonte Pagadora
        ef1 = EstadoFinanceiro.objects.create(nome='Aprovado')  # @UnusedVariable
        ef2 = EstadoFinanceiro.objects.create(nome='Concluído')  # @UnusedVariable

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 10), cod_oper=333333,
                                       valor='300000', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 11, 30), data_oper=date(2008, 11, 10), cod_oper=444444,
                                       valor='300000', historico='TED', despesa_caixa=False)
        ex3 = ExtratoCC.objects.create(data_extrato=date(2008, 11, 30), data_oper=date(2008, 11, 12), cod_oper=555555,
                                       valor='10', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=eo1, descricao='Acordo entre Instituto UNIEMP e SAC')

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='300000')  # @UnusedVariable
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of1, valor_fapesp='300000')  # @UnusedVariable
        fp3 = Pagamento.objects.create(protocolo=p3, conta_corrente=ex3, origem_fapesp=of1, valor_fapesp='10')  # @UnusedVariable

    def test_unicode(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.__unicode__(), u'08/22222-2 - Serviço de Conexão Internacional')

    def test_mostra_termo(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_termo(), u'08/22222-2')

    def test_mostra_descricao(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_descricao(), u'Serviço de Conexão Internacional')

    def test_mostra_modalidade(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_modalidade(), u'STE0')

    def test_mostra_quantidade(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_quantidade(), 12)

    def test_mostra_quantidade__zero(self):
        item = Item.objects.get(pk=1)
        item.quantidade = 0
        self.assertEquals(item.mostra_quantidade(), '-')

    def test_mostra_valor_realizado(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.mostra_valor_realizado(), '$ 600,010.00')

    def test_mostra_valor_realizado__vazio(self):
        item = Item.objects.get(pk=1)

        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 0
        pg1.save()

        pg2 = Pagamento.objects.get(pk=2)
        pg2.valor_fapesp = 0
        pg2.save()

        pg3 = Pagamento.objects.get(pk=3)
        pg3.valor_fapesp = 0
        pg3.save()

        self.assertEquals(item.mostra_valor_realizado(), '-')

    def test_valor(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.valor, 250000.00)

    def test_saldo(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.saldo(), -350010.00)

    def test_saldo_sem_pagamento(self):
        item = Item.objects.get(pk=2)
        self.assertEquals(item.saldo(), 50000.00)

    def test_saldo_null(self):
        item = Item.objects.get(pk=1)
        item.valor = None
        self.assertEquals(item.saldo(), -600010.00)

    def test_saldo_null_sem_pagamento(self):
        item = Item.objects.get(pk=2)
        item.valor = None
        self.assertEquals(item.saldo(), 0.00)

    def test_calcula_total_despesas(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.calcula_total_despesas(), 600010.00)

    def test_calcula_total_despesas__vazia(self):
        item2 = Item.objects.get(pk=2)
        of = OrigemFapesp.objects.get(pk=1)
        of.item_outorga = item2
        of.save()

        item = Item.objects.get(pk=1)
        self.assertEquals(item.calcula_total_despesas(), Decimal(0.00))

    def test_protocolos_pagina(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.protocolos_pagina(),
                          u'<a href="%s?fontepagadora__origem_fapesp__item_outorga__id=1">'
                          u'Despesas</a>' % reverse('admin:protocolo_protocolo_changelist'))

    def test_pagamentos_pagina(self):
        item = Item.objects.get(pk=1)
        self.assertEquals(item.pagamentos_pagina(),
                          u'<a href="%s?origem_fapesp__item_outorga=1">Despesas</a>'
                          % reverse('admin:financeiro_pagamento_changelist'))

    def test_calcula_realizado_mes(self):
        item = Item.objects.get(pk=1)
        dt = date(2008, 11, 11)
        self.assertEquals(item.calcula_realizado_mes(dt, False), 300010.00)

    def test_calcula_realizado_mes__vazio(self):
        item2 = Item.objects.get(pk=2)
        of = OrigemFapesp.objects.get(pk=1)
        of.item_outorga = item2
        of.save()

        item = Item.objects.get(pk=1)
        dt = date(2008, 11, 11)
        self.assertEquals(item.calcula_realizado_mes(dt, False), Decimal(0.00))

    def test_calcula_realizado_mes__dolar(self):
        modalidade = Modalidade.objects.get(sigla='STE0')
        modalidade.moeda_nacional = True
        modalidade.save()

        item = Item.objects.get(pk=1)
        dt = date(2008, 11, 11)
        self.assertEquals(item.calcula_realizado_mes(dt, False), 300010.00)

    def test_calcula_realizado_mes__filtro_dias(self):
        item = Item.objects.get(pk=1)
        dt = date(2008, 11, 11)
        self.assertEquals(item.calcula_realizado_mes(dt, True), 10.00)


class AcordoTest(UnitTestCase):
    def setUp(self):
        super(AcordoTest, self).setUp()
        eo1 = EstadoOutorga.objects.create(nome='Vigente')
        a = Acordo.objects.create(estado=eo1, descricao='Acordo entre Instituto UNIEMP e SAC')  # @UnusedVariable

    def test_unicode(self):
        a = Acordo.objects.get(pk=1)
        self.assertEquals(a.__unicode__(), 'Acordo entre Instituto UNIEMP e SAC')


class ModalidadeTest(UnitTestCase):
    def setUp(self):
        super(ModalidadeTest, self).setUp()
        eo1 = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, inicio=date(2008, 1, 1), estado=eo1, processo=22222, digito=2)
        t2 = Termo.objects.create(ano=2007, inicio=date(2007, 1, 1), estado=eo1, processo=3333, digito=3)  # @UnusedVariable

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)
        m2 = Modalidade.objects.create(sigla='STF0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='300000.00')  # @UnusedVariable

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent1)  # @UnusedVariable

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Link Internacional', quantidade=12, valor=250000)

        # Cria Natureza de Gasto
#         t = Termo.objects.create(ano=2008, processo=51885, digito=8, inicio=date(2008,1,1), 'estado=e)
#         o = Outorga.objects.create(termo=t, categoria=c, data_solicitacao=date(2007,12,1), termino=date(2008,12,31),
#         data_presta_contas=date(2009,1,31))
#         n = Natureza_gasto.objects.create(modalidade=m, outorga=o)

    def test_unicode(self):
        m = Modalidade.objects.get(sigla='STE0')
        self.assertEquals(m.__unicode__(), u'STE0 - Servicos de Terceiro no Exterior')

    def test_modalidades_termo(self):
        modalidade = Modalidade.objects.get(sigla='STE0')
        termo = Termo.objects.get(pk=1)
        self.assertEquals(str(modalidade.modalidades_termo(termo)),
                          '[<Modalidade: STE0 - Servicos de Terceiro no Exterior>]')


class EstadoTest(UnitTestCase):
    def setUp(self):
        super(EstadoTest, self).setUp()
        # Cria Estado
        e = EstadoOutorga.objects.create(nome='Vigente')  # @UnusedVariable

    def test_unicode(self):
        e = EstadoOutorga.objects.get(pk=1)
        self.assertEquals(e.__unicode__(), u'Vigente')


class OrigemFapespTest(UnitTestCase):
    def setUp(self):
        super(OrigemFapespTest, self).setUp()
        # Cria Termo
        eo1 = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, inicio=date(2008, 1, 1), estado=eo1, processo=22222, digito=2)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))
        o2 = Outorga.objects.create(termo=t, categoria=c2, data_solicitacao=date(2008, 4, 1),  # @UnusedVariable
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STE0', nome='Servicos de Terceiro no Exterior', moeda_nacional=False)
        m2 = Modalidade.objects.create(sigla='STF0', nome='Servicos de Terceiro no Brasil', moeda_nacional=True)

        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')
        n2 = Natureza_gasto.objects.create(modalidade=m2, termo=t, valor_concedido='300000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent1)

        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, descricao='Serviço de Conexão Internacional',
                                 justificativa='Link Internacional', quantidade=12, valor=250000)
        i2 = Item.objects.create(entidade=ent1, natureza_gasto=n2, descricao='Serviço de Conexão Internacional',  # @UnusedVariable
                                 justificativa='Ajuste na cobrança do Link Internacional', quantidade=6, valor=50000)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create(nome='Aprovado')
        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        og = Origem.objects.create(nome='Motoboy')

        cot1 = Contato.objects.create(primeiro_nome='Alex', email='alex@alex.com.br', tel='', ativo=True)

        iden1 = Identificacao.objects.create(contato=cot1, funcao='Gerente', area='Redes', ativo=True,
                                             endereco=endereco)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 9, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=7777, data_vencimento=date(2008, 10, 10),
                                      descricao='Serviço de Conexão Internacional - 09/2009', moeda_estrangeira=False)
        p2 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 10, 30, 10, 10), origem=og, estado=ep,
                                      num_documento=5555, data_vencimento=date(2008, 11, 10),
                                      descricao='Serviço de Conexão Internacional - 10/2009', moeda_estrangeira=False)
        p3 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, valor_total=None,
                                      data_chegada=datetime(2008, 10, 31, 10, 10), origem=og, estado=ep,
                                      num_documento=666, data_vencimento=date(2008, 11, 12),
                                      descricao='Serviço de Conexão Internacional - 10/2009', moeda_estrangeira=False)

        # Cria Item do Protocolo
        ip1 = ItemProtocolo.objects.create(protocolo=p1, quantidade=1, valor_unitario=250000,  # @UnusedVariable
                                           descricao='Conexão Internacional - 09/2009')
        ip2 = ItemProtocolo.objects.create(protocolo=p1, quantidade=1, valor_unitario=50000,  # @UnusedVariable
                                           descricao='Reajuste do serviço de Conexão Internacional - 09/2009')
        ip3 = ItemProtocolo.objects.create(protocolo=p2, quantidade=1, valor_unitario=250000,  # @UnusedVariable
                                           descricao='Conexão Internacional - 10/2009')
        ip4 = ItemProtocolo.objects.create(protocolo=p2, quantidade=1, valor_unitario=50000,  # @UnusedVariable
                                           descricao='Reajuste do serviço de Conexão Internacional - 10/2009')

        # Criar Fonte Pagadora
        ef1 = EstadoFinanceiro.objects.create(nome='Aprovado')  # @UnusedVariable
        ef2 = EstadoFinanceiro.objects.create(nome='Concluído')  # @UnusedVariable

        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 10), cod_oper=333333,
                                       valor='300000', historico='TED', despesa_caixa=False)
        ex2 = ExtratoCC.objects.create(data_extrato=date(2008, 11, 30), data_oper=date(2008, 11, 10), cod_oper=444444,
                                       valor='300000', historico='TED', despesa_caixa=False)
        ex3 = ExtratoCC.objects.create(data_extrato=date(2008, 11, 30), data_oper=date(2008, 11, 12), cod_oper=555555,
                                       valor='10', historico='TED', despesa_caixa=False)

        a1 = Acordo.objects.create(estado=eo1, descricao='Acordo entre Instituto UNIEMP e SAC')

        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)

        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='300000')  # @UnusedVariable
        fp2 = Pagamento.objects.create(protocolo=p2, conta_corrente=ex2, origem_fapesp=of1, valor_fapesp='300000')  # @UnusedVariable
        fp3 = Pagamento.objects.create(protocolo=p3, conta_corrente=ex3, origem_fapesp=of1, valor_fapesp='10')  # @UnusedVariable

    def tearDown(self):
        super(OrigemFapespTest, self).tearDown()

    def test_unicode(self):
        of = OrigemFapesp.objects.get(pk=1)
        self.assertEquals(of.__unicode__(),
                          u'Acordo entre Instituto UNIEMP e SAC - STE0 - 08/22222-2 - Serviço de Conexão Internacional')

    def test_gasto_zero(self):
        pg1 = Pagamento.objects.get(pk=1)
        pg1.valor_fapesp = 0
        pg1.save()

        pg2 = Pagamento.objects.get(pk=2)
        pg2.valor_fapesp = 0
        pg2.save()

        pg3 = Pagamento.objects.get(pk=3)
        pg3.valor_fapesp = 0
        pg3.save()

        of = OrigemFapesp.objects.get(pk=1)

        self.assertEquals(of.gasto(), Decimal('0.0'))

    def test_gasto(self):
        of = OrigemFapesp.objects.get(pk=1)
        self.assertEquals(of.gasto(), Decimal('600010.00'))

    def test_termo(self):
        of = OrigemFapesp.objects.get(pk=1)
        self.assertEquals(str(of.termo()), u'08/22222-2')


class ContratoTest(UnitTestCase):
    def setUp(self):
        super(ContratoTest, self).setUp()

        # Cria um Contrato
        ent = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        ct = Contrato.objects.create(data_inicio=date(2008, 1, 1), auto_renova=True, limite_rescisao=date(2008, 1, 11),  # @UnusedVariable
                                     entidade=ent)

    def tearDown(self):
        super(ContratoTest, self).tearDown()

    def test_unicode(self):
        ct = Contrato.objects.get(pk=1)
        self.assertEquals(ct.__unicode__(), u'SAC - 01/01/2008')

    def test_existe_arquivo__com_arquivo(self):
        ct = Contrato.objects.get(pk=1)

        ct.arquivo = ""
        ct.arquivo.name = 'test_img_file.gif'
        ct.arquivo._commited = True
        ct.save()

        self.assertEquals(ct.existe_arquivo(), u' ')

    def test_existe_arquivo__com_arquivo_e_path(self):
        ct = Contrato.objects.get(pk=1)

        ct.arquivo = ""
        ct.arquivo.name = 'teste/teste/test_img_file.gif'
        ct.arquivo._commited = True
        ct.save()

        self.assertEquals(ct.existe_arquivo(),
                          u'<center><a href="%steste/teste/test_img_file.gif"><img src="%simg/arquivo.png" /></a>'
                          u'</center>' % (settings.MEDIA_URL, settings.STATIC_URL))

    def test_existe_arquivo__nulo(self):
        ct = Contrato.objects.get(pk=1)
        ct.arquivo = None

        self.assertEquals(ct.existe_arquivo(), u' ')


class OrdemDeServicoTest(UnitTestCase):
    def setUp(self):
        super(OrdemDeServicoTest, self).setUp()

        # Cria um Contrato
        ent = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        ct = Contrato.objects.create(data_inicio=date(2008, 1, 1), auto_renova=True, limite_rescisao=date(2008, 1, 11),
                                     entidade=ent)

        ef1 = EstadoOutorga.objects.create(nome='Aprovado')
        tipo = TipoContrato.objects.create(nome='Tipo Fixo')
        # Cria uma Ordem de Serviço
        estadoOs = EstadoOS.objects.create(nome="Vigente")
        a = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        os = OrdemDeServico.objects.create(acordo=a, contrato=ct, tipo=tipo, estado=estadoOs, antes_rescisao=2,  # @UnusedVariable
                                           data_inicio=date(2008, 2, 1), data_rescisao=date(2008, 11, 1), numero=66666,
                                           descricao='OS 34567 - Contratação de mais um link')

    def tearDown(self):
        super(OrdemDeServicoTest, self).tearDown()

    def test_unicode(self):
        os = OrdemDeServico.objects.get(pk=1)
        self.assertEquals(os.__unicode__(), u'Tipo Fixo 66666')

    def test_mostra_prazo__positivo(self):
        os = OrdemDeServico.objects.get(pk=1)
        self.assertEquals(os.mostra_prazo(), u'2 dias')

    def test_mostra_prazo__negativo(self):
        os = OrdemDeServico.objects.get(pk=1)
        os.antes_rescisao = -1
        self.assertEquals(os.mostra_prazo(), u'-')

    def test_mostra_prazo__um(self):
        os = OrdemDeServico.objects.get(pk=1)
        os.antes_rescisao = 1
        self.assertEquals(os.mostra_prazo(), u'1 dias')

    def test_entidade(self):
        os = OrdemDeServico.objects.get(pk=1)
        self.assertEquals(str(os.entidade()), u'SAC')

    def test_primeiro_arquivo__vazio(self):
        os = OrdemDeServico.objects.get(pk=1)
        self.assertIsNone(os.primeiro_arquivo())

    def test_primeiro_arquivo(self):
        os = OrdemDeServico.objects.get(pk=1)

        arquivo = ArquivoOS(os=os)
        arquivo.data = "2013-01-01"
        arquivo.arquivo = ""
        arquivo.arquivo.name = 'test_img_file.gif'
        arquivo.save()

        self.assertEquals(os.primeiro_arquivo(), 'test_img_file.gif')

        arquivo.arquivo.delete()
        arquivo.delete()


class ArquivoTest(UnitTestCase):
    def setUp(self):
        super(ArquivoTest, self).setUp()

        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)

        # Cria Outorga
        c1 = Categoria.objects.create(nome='Inicial')
        c2 = Categoria.objects.create(nome='Aditivo')  # @UnusedVariable

        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Arquivo
        arq = Arquivo(outorga=o1)
        arq.save()
        # Criando um dirty Mock para o teste do arquivo
        arq.arquivo = ""
        arq.arquivo.name = 'test_img_file.gif'
        arq.arquivo._commited = True
        arq.save()

    def test_unicode(self):
        arq = Arquivo.objects.get(pk=1)
        self.assertEquals(arq.__unicode__(), u'test_img_file.gif')

    def test_unicode__path(self):
        arq = Arquivo.objects.get(pk=1)
        arq.arquivo.name = 'teste/teste/test_img_file.gif'
        arq.arquivo._commited = True
        arq.save()
        self.assertEquals(arq.__unicode__(), u'test_img_file.gif')

    def test_concessao(self):
        arq = Arquivo.objects.get(pk=1)
        self.assertEquals(arq.concessao().id, 1)

    def test_mostra_termo(self):
        arq = Arquivo.objects.get(pk=1)
        self.assertEquals(arq.mostra_termo(), '08/22222-2')


class ArquivoOSTest(UnitTestCase):
    def setUp(self):
        super(ArquivoOSTest, self).setUp()

        # Cria um Contrato
        ent = Entidade.objects.create(sigla='SAC', nome='SAC do Brasil', cnpj='00.000.000/0000-00', fisco=True, url='')
        ct = Contrato.objects.create(data_inicio=date(2008, 1, 1), auto_renova=True, limite_rescisao=date(2008, 1, 11),
                                     entidade=ent)

        ef1 = EstadoOutorga.objects.create(nome='Aprovado')
        tipo = TipoContrato.objects.create(nome='Tipo Fixo')
        # Cria uma Ordem de Serviço
        estadoOs = EstadoOS.objects.create(nome="Vigente")
        a = Acordo.objects.create(estado=ef1, descricao='Acordo entre Instituto UNIEMP e SAC')
        os = OrdemDeServico.objects.create(acordo=a, contrato=ct, tipo=tipo, estado=estadoOs, antes_rescisao=2,  # @UnusedVariable
                                           data_inicio=date(2008, 2, 1), data_rescisao=date(2008, 11, 1), numero=66666,
                                           descricao='OS 34567 - Contratação de mais um link')

    def tearDown(self):
        super(ArquivoOSTest, self).tearDown()

    def test_unicode(self):
        orderServico = OrdemDeServico.objects.get(pk=1)
        arquivo = ArquivoOS(os=orderServico)
        arquivo.data = "2013-01-01"
        # Criando um dirty Mock para o teste do arquivo
        arquivo.arquivo = ""
        arquivo.arquivo.name = 'test_img_file.gif'
        arquivo.arquivo._commited = True
        arquivo.save()

        orderServico.arquivo = arquivo

        self.assertEquals(arquivo.__unicode__(), u'test_img_file.gif')

        arquivo.delete()

    def test_unicode_com_path(self):
        orderServico = OrdemDeServico.objects.get(pk=1)
        arquivo = ArquivoOS(os=orderServico)
        arquivo.data = "2013-01-01"

        # Criando um dirty Mock para o teste do arquivo
        arquivo.arquivo = ""
        arquivo.arquivo.name = 'tmp/teste/test_img_file.gif'
        arquivo.arquivo._commited = True
        arquivo.save()

        orderServico.arquivo = arquivo

        self.assertEquals(arquivo.__unicode__(), u'test_img_file.gif')

        arquivo.delete()
