# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date, datetime
from decimal import Decimal
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone
from membro.models import Membro, Cargo, Historico
from protocolo.models import Feriado, TipoDocumento, Origem, Protocolo, ItemProtocolo, Descricao, Cotacao,\
    Estado as ProtocoloEstado
from identificacao.models import Identificacao, Contato, Entidade, Endereco
from outorga.models import Termo, Outorga, Categoria, Estado as OutorgaEstado
from protocolo.templatetags import proto_tags

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Get current timezone
tz = timezone.get_current_timezone()


# Testes do arquivo com funções localizado em protocolo.templatetags.proto_tags que é utilizado nos templates HTML
class PrototagTest(TestCase):
    def test_moeda_real(self):
        value = 1000.00
        retorno = proto_tags.moeda(value, 1, False, False)

        self.assertEquals(retorno, 'R$ 1.000,00')

    def test_moeda_dolar(self):
        value = 1000.00
        retorno = proto_tags.moeda(value, 0, False, False)

        self.assertEquals(retorno, 'US$ 1,000.00')

    def test_moeda_real_sem_valor_monetario(self):
        value = 1000.00
        retorno = proto_tags.moeda(value, 1, True, False)

        self.assertEquals(retorno, '1.000,00')

    def test_moeda_real_negativo(self):
        value = -300000000.00
        retorno = proto_tags.moeda(value, 1, False, False)

        self.assertEquals(retorno, '(R$ 300.000.000,00)')

    def test_moeda_dolar_negativo(self):
        value = -300000000.00
        retorno = proto_tags.moeda(value, 0, False, False)

        self.assertEquals(retorno, '(US$ 300,000,000.00)')

    def test_moeda_dolar_sem_valor_monetario(self):
        value = -300000000.00
        retorno = proto_tags.moeda(value, 0, True, False)

        self.assertEquals(retorno, '(300,000,000.00)')

    def test_moeda_negativo_css(self):
        value = -300000000.00
        retorno = proto_tags.moeda(value, 1, False, True)

        self.assertEquals(retorno, '<span style="color: red">-R$ 300.000.000,00</span>')


class ProtocoloTest(TestCase):
    def setUp(self):
        mb = Membro.objects.create(nome='Gerson Gomes', email='gerson@gomes.com', cpf='000.000.000-00', site=True)

        cg = Cargo.objects.create(nome='Outorgado')

        ht = Historico.objects.create(inicio=datetime(2008, 1, 1), cargo=cg, membro=mb, funcionario=True)  # @UnusedVariable

        outorgaEstado = OutorgaEstado.objects.create(nome='Pendente')

        t = Termo.objects.create(ano=2008, processo=52885, digito=8, estado=outorgaEstado)

        categoria = Categoria.objects.create(nome='Categoria')

        outorga = Outorga.objects.create(data_solicitacao=datetime(2008, 1, 1), termino=datetime(2009, 1, 1),  # @UnusedVariable
                                         categoria=categoria, termo=t)

        td = TipoDocumento.objects.create(nome='Nota Fiscal')
        c = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        og = Origem.objects.create(nome='Motoboy')
        ent = Entidade.objects.create(sigla='NEXTEL', nome='Nextel', cnpj='', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent)
        iden = Identificacao.objects.create(contato=c, funcao='Tecnico', area='', ativo=True, endereco=endereco)

        desc = Descricao.objects.create(descricao='Descricao', entidade=ent)

        protocoloEstado = ProtocoloEstado.objects.create(nome='Pendente')

        p = Protocolo.objects.create(termo=t, tipo_documento=td, num_documento=2008, estado=protocoloEstado,
                                     identificacao=iden, data_chegada=tz.localize(datetime(2008, 9, 30, 10, 10)),
                                     data_validade=datetime(2009, 8, 25), data_vencimento=datetime(2008, 9, 30),
                                     descricao="Conta mensal", origem=og, valor_total=None, descricao2=desc,
                                     moeda_estrangeira=False)
        ip = ItemProtocolo.objects.create(protocolo=p, descricao='Folha de pagamento', quantidade=2,  # @UnusedVariable
                                          valor_unitario=10000)

    def test_doc_num(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('Nota Fiscal 2008', p.doc_num())

    def test_recebimento(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('30/09/08 10:10', p.recebimento())

    def test_vencimento(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('30/09/08', p.vencimento())

    def test_validade(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('25/08/09', p.validade())

    def test_colorir(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('Pendente', p.colorir())

    def test_pagamentos_amanha(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(True, p.pagamentos_amanha())

    def test_valor(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(Decimal("20000.00"), p.valor)

    def test_mostra_valor(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals('R$ 20.000,00', p.mostra_valor())

    def test_entidade(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(u'NEXTEL', p.entidade())

    def test_unicode(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(u'30/09 - Nota Fiscal 2008 - R$ 20.000,00', p.__unicode__())

    def test_existe_arquivo(self):
        p = Protocolo.objects.get(num_documento=2008)
        self.assertEquals(' ', p.existe_arquivo())

    def test_protocolos_termo(self):
        t = Termo.objects.get(ano=2008)
        p = Protocolo.protocolos_termo(t)
        self.assertEquals('[<Protocolo: 30/09 - Nota Fiscal 2008 - R$ 20.000,00>]', str(p))


class ItemProtocoloTest(TestCase):
    def setUp(self):
        td = TipoDocumento.objects.create(nome='Anexo 9')
        e = ProtocoloEstado.objects.create(nome='Pago')
        c = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        og = Origem.objects.create(nome='Sedex')

        mb = Membro.objects.create(nome='Gerson Gomes', email='gerson@gomes.com', cpf='000.000.000-00', site=True)

        cg = Cargo.objects.create(nome='Outorgado')

        ht = Historico.objects.create(inicio=datetime(2008, 1, 1), cargo=cg, membro=mb, funcionario=True)  # @UnusedVariable

        outorgaEstado = OutorgaEstado.objects.create(nome='Pendente')

        t = Termo.objects.create(ano=2008, processo=52885, digito=8, estado=outorgaEstado)

        ent = Entidade.objects.create(sigla='UNIEMP', nome='Instituto Uniemp', cnpj='', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent)
        iden = Identificacao.objects.create(contato=c, funcao='Tecnico', area='', ativo=True, endereco=endereco)

        desc = Descricao.objects.create(descricao='Descricao', entidade=ent)

        p = Protocolo.objects.create(termo=t, tipo_documento=td, num_documento=2008, estado=e, identificacao=iden,
                                     data_chegada=tz.localize(datetime(2008, 9, 30, 10, 10)), descricao2=desc,
                                     data_validade=date(2009, 8, 25),data_vencimento=date(2008, 9, 30), origem=og,
                                     valor_total=None, descricao="Aditivo Uniemp", moeda_estrangeira=False)

        ip = ItemProtocolo.objects.create(protocolo=p, descricao='Servico de conexao', quantidade=1,  # @UnusedVariable
                                          valor_unitario='59613.59')

    def test_unicode(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals('30/09 - Anexo 9 2008 - R$ 59.613,59 | Servico de conexao', ip.__unicode__())

    def test_valor(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals(Decimal("59613.59"), ip.valor)

    def test_mostra_valor(self):
        ip = ItemProtocolo.objects.get(pk=1)
        self.assertEquals('R$ 59.613,59', ip.mostra_valor())


class EstadoTest(TestCase):
    def test_unicode(self):
        e = ProtocoloEstado.objects.create(nome='Vencido')
        self.assertEquals('Vencido', e.__unicode__())


class TipoDocumentoTest(TestCase):
    def test_unicode(self):
        td = TipoDocumento.objects.create(nome='Oficio')
        self.assertEquals('Oficio', td.__unicode__())


class FeriadoTest(TestCase):
    def test_unicode(self):
        f = Feriado.objects.create(feriado=date(2008, 10, 8))

        self.assertEquals('08/10/08', f.__unicode__())

    def test_dia_feriado(self):
        f = Feriado.objects.create(feriado=date(2008, 10, 8))  # @UnusedVariable
        f = Feriado.objects.create(feriado=date(2008, 5, 18))  # @UnusedVariable
        f = Feriado.objects.create(feriado=date(2008, 2, 22))  # @UnusedVariable

        self.assertEquals(Feriado.dia_de_feriado(date(2008, 2, 22)), True)
        self.assertEquals(Feriado.dia_de_feriado(date(2008, 10, 8)), True)
        self.assertEquals(Feriado.dia_de_feriado(date(2008, 5, 18)), True)

    def test_dia_normal(self):
        f = Feriado.objects.create(feriado=date(2008, 2, 22))  # @UnusedVariable

        self.assertEquals(Feriado.dia_de_feriado(date(2007, 2, 22)), False)
        self.assertEquals(Feriado.dia_de_feriado(date(2007, 10, 8)), False)

    def test_erro_para_feriado_unico(self):
        f = Feriado.objects.create(feriado=date(2008, 10, 8))  # @UnusedVariable

        f = Feriado(feriado=date(2008, 10, 8))
        # deve disparar erro para feriado com data igual
        self.assertRaises(IntegrityError, f.save)

    def test_modificacao_de_feriado_unico(self):
        f = Feriado.objects.create(feriado=date(2008, 10, 8))

        f.obs = 'teste'
        f.save()


class CotacaoTest(TestCase):
    def setUp(self):
        mb = Membro.objects.create(nome='Gerson Gomes', email='gerson@gomes.com', cpf='000.000.000-00', site=True)

        cg = Cargo.objects.create(nome='Outorgado')

        ht = Historico.objects.create(inicio=datetime(2008, 1, 1), cargo=cg, membro=mb, funcionario=True)  # @UnusedVariable

        outorgaEstado = OutorgaEstado.objects.create(nome='Pendente')

        t = Termo.objects.create(ano=2008, processo=52885, digito=8, estado=outorgaEstado)

        ent = Entidade.objects.create(sigla='UNIEMP', nome='Instituto Uniemp', cnpj='', fisco=True, url='')
        endereco = Endereco.objects.create(entidade=ent)

        td = TipoDocumento.objects.create(nome='Anexo 9')
        e = ProtocoloEstado.objects.create(nome='Pago')
        c = Contato.objects.create(primeiro_nome='Joao', email='joao@joao.com.br', tel='')
        og = Origem.objects.create(nome='Sedex')
        iden = Identificacao.objects.create(contato=c, funcao='Tecnico', area='', ativo=True, endereco=endereco)

        cot = Cotacao.objects.create(termo=t, tipo_documento=td, estado=e, identificacao=iden,  # @UnusedVariable
                                     data_chegada=tz.localize(datetime(2008, 12, 12, 9, 10)),
                                     data_validade=date(2009, 12, 13), origem=og, parecer='custo alto', aceito=False,
                                     descricao='Compra de Aparelhos', entrega='confirmada', moeda_estrangeira=False)

    def test_unicode(self):
        cot = Cotacao.objects.get(pk=1)
        self.assertEquals(u'UNIEMP - Compra de Aparelhos', cot.__unicode__())

    def existe_entrega(self):
        cot = Cotacao.objects.get(pk=1)
        self.assertEquals('confirmada', cot.existe_entrega())
