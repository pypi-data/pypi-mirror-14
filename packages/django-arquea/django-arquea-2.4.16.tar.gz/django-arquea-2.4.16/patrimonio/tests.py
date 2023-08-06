# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.urlresolvers import reverse
from django.test import TestCase
from datetime import date

from patrimonio.models import HistoricoLocal, Tipo, Patrimonio, Equipamento, Estado, TipoEquipamento, \
    Direcao, DistribuicaoUnidade, EnderecoDetalhe, UnidadeDimensao, Distribuicao, Dimensao
from protocolo.models import TipoDocumento, Origem, Protocolo, Estado as EstadoProtocolo
from identificacao.models import Entidade, Contato, Endereco, Identificacao, TipoDetalhe
from outorga.models import Termo, Estado as EstadoOutorga, Acordo, OrigemFapesp, Categoria, Outorga, Modalidade,\
    Natureza_gasto, Item
from financeiro.models import ExtratoCC, Estado as EstadoFinanceiro, TipoComprovante, Auditoria, Pagamento

import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


class EstadoTest(TestCase):
    def test_unicode(self):
        est = Estado.objects.create(nome="ESTADO_NOME")

        self.assertEqual(u'ESTADO_NOME', est.__unicode__())


class TipoTest(TestCase):
    def test_unicode(self):
        tipo = Tipo.objects.create(nome="TIPO_NOME")

        self.assertEqual(u'TIPO_NOME', tipo.__unicode__())


class DirecaoTest(TestCase):
    def test_unicode(self):
        direcao = Direcao.objects.create(origem="ORIGEM", destino="DESTINO")

        self.assertEqual(u'ORIGEM - DESTINO', direcao.__unicode__())

    def test_meta(self):
        self.assertEqual(u'Direção', Direcao._meta.verbose_name)  # @UndefinedVariable _meta
        self.assertEqual(u'Direções', Direcao._meta.verbose_name_plural)  # @UndefinedVariable _meta


class DistribuicaoUnidadeTest(TestCase):
    def test_unicode(self):
        distribuicaoUnidade = DistribuicaoUnidade.objects.create(nome="NOME", sigla="SIGLA")

        self.assertEqual(u'SIGLA - NOME', distribuicaoUnidade.__unicode__())


class DistribuicaoTest(TestCase):
    def test_unicode(self):
        distribuicaoUnidade = DistribuicaoUnidade.objects.create(nome="NOME", sigla="SIGLA")
        direcao = Direcao.objects.create(origem="ORIGEM", destino="DESTINO")
        distribuicao = Distribuicao.objects.create(inicio=1, final=2, unidade=distribuicaoUnidade, direcao=direcao)

        self.assertEqual(u'1 - 2', distribuicao.__unicode__())


class UnidadeDimensaoTest(TestCase):
    def test_unicode(self):
        unidadeDimensao = UnidadeDimensao.objects.create(nome="NOME")

        self.assertEqual(u'NOME', unidadeDimensao.__unicode__())

    def test_meta(self):
        self.assertEqual(u'Unidade da dimensão', UnidadeDimensao._meta.verbose_name)  # @UndefinedVariable _meta
        self.assertEqual(u'Unidade das dimensões', UnidadeDimensao._meta.verbose_name_plural)  # @UndefinedVariable _meta


class DimensaoTest(TestCase):
    def test_unicode(self):
        unidadeDimensao = UnidadeDimensao.objects.create(nome="UNIDADE")
        dimensao = Dimensao.objects.create(altura=1, largura=2, profundidade=3, peso=4, unidade=unidadeDimensao)

        self.assertEqual(u'1 x 2 x 3 UNIDADE - 4 kg', dimensao.__unicode__())

    def test_meta(self):
        self.assertEqual(u'Dimensão', Dimensao._meta.verbose_name)  # @UndefinedVariable _meta
        self.assertEqual(u'Dimensões', Dimensao._meta.verbose_name_plural)  # @UndefinedVariable _meta


class HistoricoLocalTest(TestCase):

    def test_criacao_historico_local(self):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True,
                                      url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010',
                                      estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        tipoPatr = Tipo.objects.create(nome='roteador')
        rt = Patrimonio.objects.create(ns='AF345678GB3489X', modelo='NetIron400', tipo=tipoPatr, apelido="NetIron400",
                                       checado=True)
        est = Estado.objects.create()
        hl = HistoricoLocal.objects.create(patrimonio=rt, endereco=endDet, descricao='Emprestimo',
                                           data=date(2009, 2, 5), estado=est)

        self.assertEqual(u'05/02/2009 - NetIron400 - AF345678GB3489X -  | SAC - Dr. Ovidio, 215 - ', hl.__unicode__())

    def test_posicao_furo(self):
        """
        Teste de posicionamento de um equipamento em um furo de um rack
        """
        historico = HistoricoLocal(posicao="R042.F085")
        self.assertEqual(historico.posicao_furo, 85)

        historico = HistoricoLocal(posicao="P042.F017")
        self.assertEqual(historico.posicao_furo, 17)

        historico = HistoricoLocal(posicao="S042.F040")
        self.assertEqual(historico.posicao_furo, 40)

        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEqual(historico.posicao_furo, 49)

        historico = HistoricoLocal(posicao="60")
        self.assertEqual(historico.posicao_furo, 60)

        historico = HistoricoLocal(posicao="")
        self.assertEqual(historico.posicao_furo, -1)

        historico = HistoricoLocal()
        self.assertEqual(historico.posicao_furo, -1)

        historico = HistoricoLocal(posicao="S042.F049-TD")
        self.assertEqual(historico.posicao_furo, 49)

        historico = HistoricoLocal(posicao="S042.F049.TD")
        self.assertEqual(historico.posicao_furo, 49)

        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEqual(historico.posicao_furo, -1)

        historico = HistoricoLocal(posicao="S042.F001")
        self.assertEqual(historico.posicao_furo, 1)

    def test_posicao_colocacao(self):
        """
        Teste de colocaçao de um equipamento relativo ao furo
        Pode ser traseiro, lateral, piso
        """
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEqual(historico.posicao_colocacao, 'TD')

        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEqual(historico.posicao_colocacao, 'TD')

        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEqual(historico.posicao_colocacao, 'piso')

        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEqual(historico.posicao_colocacao, 'piso')

        historico = HistoricoLocal(posicao="60")
        self.assertEqual(historico.posicao_colocacao, None)

        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEqual(historico.posicao_colocacao, None)

        historico = HistoricoLocal(posicao="")
        self.assertEqual(historico.posicao_colocacao, None)

        historico = HistoricoLocal()
        self.assertEqual(historico.posicao_colocacao, None)

    def test_posicao_rack__letra_numero(self):
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEqual(historico.posicao_rack_letra, 'R')
        self.assertEqual(historico.posicao_rack_numero, '042')

        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEqual(historico.posicao_rack_letra, 'P')
        self.assertEqual(historico.posicao_rack_numero, '042')

        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEqual(historico.posicao_rack_letra, 'S')
        self.assertEqual(historico.posicao_rack_numero, '042')

        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEqual(historico.posicao_rack_letra, 'S')
        self.assertEqual(historico.posicao_rack_numero, '042')

        historico = HistoricoLocal(posicao="60")
        self.assertEqual(historico.posicao_rack_letra, None)
        self.assertEqual(historico.posicao_rack_numero, None)

        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEqual(historico.posicao_rack_letra, 'S')
        self.assertEqual(historico.posicao_rack_numero, '042')

        historico = HistoricoLocal(posicao="AB42.F049")
        self.assertEqual(historico.posicao_rack_letra, 'AB')
        self.assertEqual(historico.posicao_rack_numero, '42')

        historico = HistoricoLocal(posicao="ABC42.F049")
        self.assertEqual(historico.posicao_rack_letra, 'ABC')
        self.assertEqual(historico.posicao_rack_numero, '42')

    def test_posicao_rack(self):
        historico = HistoricoLocal(posicao="R042.F085.TD")
        self.assertEqual(historico.posicao_rack, 'R042')

        historico = HistoricoLocal(posicao="P042.F017-TD")
        self.assertEqual(historico.posicao_rack, 'P042')

        historico = HistoricoLocal(posicao="S042.piso")
        self.assertEqual(historico.posicao_rack, 'S042')

        historico = HistoricoLocal(posicao="S042-piso")
        self.assertEqual(historico.posicao_rack, 'S042')

        historico = HistoricoLocal(posicao="60")
        self.assertEqual(historico.posicao_rack, None)

        historico = HistoricoLocal(posicao="S042.F049")
        self.assertEqual(historico.posicao_rack, 'S042')

        historico = HistoricoLocal(posicao="AB42.F049")
        self.assertEqual(historico.posicao_rack, 'AB42')

        historico = HistoricoLocal(posicao="ABC42.F049")
        self.assertEqual(historico.posicao_rack, 'ABC42')


class PatrimonioTest(TestCase):

    def setUp(self):
        tipoPatr = Tipo.objects.create(nome='roteador')
        tipoEquipamento = TipoEquipamento.objects.create(nome="Rack")
        entidade_fabricante = Entidade.objects.create(sigla='DELL', nome='Dell', cnpj='00.000.000/0000-00', fisco=True,
                                                      url='')
        entidade_procedencia = Entidade.objects.create(sigla='PROC', nome='Entidade_Procedencia',
                                                       cnpj='00.000.000/0000-00', fisco=True, url='')
        equipamento = Equipamento.objects.create(tipo=tipoEquipamento, part_number="PN001", modelo="MODEL001",
                                                 entidade_fabricante=entidade_fabricante)

        rt = Patrimonio.objects.create(equipamento=equipamento, ns='AF345678GB3489X', modelo='NetIron400',  # @UnusedVariable rt
                                       tipo=tipoPatr, apelido="NetIron400", checado=True,
                                       entidade_procedencia=entidade_procedencia)

    def _setUpHistorico(self, patrimonio):
        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True,
                                      url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010',
                                      estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create()
        hl = HistoricoLocal.objects.create(patrimonio=patrimonio, endereco=endDet, descricao='Emprestimo',  # @UnusedVariable h1
                                           data=date(2009, 2, 5), estado=est, posicao='S042')
        h2 = HistoricoLocal.objects.create(patrimonio=patrimonio, endereco=endDet, descricao='Emprestimo 2',  # @UnusedVariable h2
                                           data=date(2010, 2, 5), estado=est, posicao='S043')

    def test_historico_atual(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)

        hist = patr.historico_atual
        self.assertEqual('Emprestimo 2', hist.descricao)

    def test_historico_atual_vazio(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')

        hist = patr.historico_atual
        self.assertIsNone(hist)

    def test_historico_atual_prefetched(self):
        """
        Verifica chamanda do historico atual do patrimonio
        """
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)
        hist = patr.historico_atual
        self.assertEqual('Emprestimo 2', hist.descricao)

    def test_marca(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        marca = patr.marca
        self.assertEqual('DELL', marca)

    def test_marca_vazia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento.entidade_fabricante.sigla = None
        self.assertEqual('', patr.marca)

        patr.equipamento.entidade_fabricante = None
        self.assertEqual('', patr.marca)

        patr.equipamento = None
        self.assertEqual('', patr.marca)

    def test_modelo(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        modelo = patr.modelo
        self.assertEqual('MODEL001', modelo)

    def test_modelo_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento = None
        self.assertEqual('', patr.modelo)

    def test_part_number(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        part_number = patr.part_number
        self.assertEqual('PN001', part_number)

    def test_part_number_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.equipamento = None
        self.assertEqual('', patr.part_number)

    def test_procedencia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        procedencia = patr.procedencia
        self.assertEqual('PROC', procedencia)

    def test_procedencia_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.entidade_procedencia = None
        self.assertEqual('', patr.procedencia)

    def test_posicao(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self._setUpHistorico(patr)
        self.assertEqual(' - S043', patr.posicao())

    def test_posicao_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        self.assertEqual('', patr.posicao())

    def test_nf(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')

        protocolo = Protocolo.objects.create(id=1, num_documento='00001', tipo_documento_id=0, estado_id=0, termo_id=0,
                                             data_chegada=date(2000, 1, 1), moeda_estrangeira=False)
        pagamento = Pagamento.objects.create(id=1, protocolo=protocolo, valor_fapesp=0)
        patr.pagamento = pagamento

        self.assertEqual('00001', patr.nf())

    def test_nf_vazio_pagamento_vazio(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = None

        self.assertEqual('', patr.nf())

    def test_auditoria(self):
        # Cria Termo
        e = EstadoOutorga.objects.create(nome='Vigente')
        t = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=e)
        # Cria Outorga
        c1 = Categoria.objects.create()
        o1 = Outorga.objects.create(termo=t, categoria=c1, data_solicitacao=date(2007, 12, 1),  # @UnusedVariable o1
                                    termino=date(2008, 12, 31), data_presta_contas=date(2008, 2, 28))

        # Cria Natureza de gasto
        m1 = Modalidade.objects.create(sigla='STB1', )
        n1 = Natureza_gasto.objects.create(modalidade=m1, termo=t, valor_concedido='1500000.00')

        # Cria Item de Outorga
        ent1 = Entidade.objects.create(sigla='GTECH', cnpj='00.000.000/0000-00', fisco=True, url='')
        end1 = Endereco.objects.create(entidade=ent1)
        i1 = Item.objects.create(entidade=ent1, natureza_gasto=n1, quantidade=12, valor=2500)

        # Cria Protocolo
        ep = EstadoProtocolo.objects.create()
        td = TipoDocumento.objects.create()
        og = Origem.objects.create()
        cot1 = Contato.objects.create()

        iden1 = Identificacao.objects.create(endereco=end1, contato=cot1, ativo=True)

        p1 = Protocolo.objects.create(termo=t, identificacao=iden1, tipo_documento=td, data_chegada=date(2008, 9, 30),
                                      origem=og, estado=ep, num_documento=8888)

        # Criar Fonte Pagadora
        ef1 = EstadoOutorga.objects.create()
        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        a1 = Acordo.objects.create(estado=ef1)
        of1 = OrigemFapesp.objects.create(acordo=a1, item_outorga=i1)
        fp1 = Pagamento.objects.create(protocolo=p1, conta_corrente=ex1, origem_fapesp=of1, valor_fapesp='2650')

        efi1 = EstadoFinanceiro.objects.create()
        tcomprov1 = TipoComprovante.objects.create()

        audit1 = Auditoria.objects.create(estado=efi1, pagamento=fp1, tipo=tcomprov1, parcial=101.0, pagina=102.0,  # @UnusedVariable audit1
                                          obs='observacao')

        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = fp1

        self.assertEqual('STB1 (101/102)', patr.auditoria())

    def test_auditoria_vazia(self):
        patr = Patrimonio.objects.get(ns='AF345678GB3489X')
        patr.pagamento = None

        self.assertEqual('', patr.auditoria())

    def nf(self):
        if self.pagamento is not None and self.pagamento.protocolo is not None:
            return u'%s' % self.pagamento.protocolo.num_documento
        else:
            return ''


class ViewTest(TestCase):

    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpPatrimonio(self, num_documento='', ns=''):

        # Cria Termo
        estadoOutorga = EstadoOutorga.objects.create(nome='Vigente')
        termo = Termo.objects.create(ano=2008, processo=22222, digito=2, inicio=date(2008, 1, 1), estado=estadoOutorga)

        protocolo = Protocolo.objects.create(id=1, num_documento=num_documento, tipo_documento_id=0, estado_id=0,
                                             termo=termo, data_chegada=date(2000, 1, 1), moeda_estrangeira=False)
        ex1 = ExtratoCC.objects.create(data_extrato=date(2008, 10, 30), data_oper=date(2008, 10, 5), cod_oper=333333,
                                       valor='2650', historico='TED', despesa_caixa=False)
        pagamento = Pagamento.objects.create(id=1, protocolo=protocolo, valor_fapesp=1000, conta_corrente=ex1)

        tipoEquipamento = TipoEquipamento.objects.create(nome="Rack")
        entidade_fabricante = Entidade.objects.create(sigla='DELL', nome='Dell', cnpj='00.000.000/0000-00', fisco=True,
                                                      url='')
        equipamento = Equipamento.objects.create(tipo=tipoEquipamento, part_number="PN001", modelo="MODEL001",
                                                 entidade_fabricante=entidade_fabricante,
                                                 descricao="equipamento_descricao")

        tipoPatr = Tipo.objects.create(id=1, nome="TIPO")
        entidade_procedencia = Entidade.objects.create(sigla='PROC', nome='Entidade_Procedencia',
                                                       cnpj='00.000.000/0000-00', fisco=True, url='')

        patr1 = Patrimonio.objects.create(id=1, pagamento=pagamento, tipo=tipoPatr, checado=True,
                                          entidade_procedencia=entidade_procedencia, equipamento=equipamento,
                                          tem_numero_fmusp=True, numero_fmusp="000123")
        patr2 = Patrimonio.objects.create(id=2, ns=ns, tipo=tipoPatr, checado=True,  # @UnusedVariable patr2
                                          entidade_procedencia=entidade_procedencia)

        ent = Entidade.objects.create(sigla='SAC', nome='Global Crossing', cnpj='00.000.000/0000-00', fisco=True,
                                      url='')
        end = Endereco.objects.create(entidade=ent, rua='Dr. Ovidio', num=215, bairro='Cerqueira Cesar', cep='05403010',
                                      estado='SP', pais='Brasil')
        tipoDetalhe = TipoDetalhe.objects.create()
        endDet = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, mostra_bayface=True)
        est = Estado.objects.create(nome="Ativo")
        hl = HistoricoLocal.objects.create(patrimonio=patr1, endereco=endDet, descricao='Emprestimo',  # @UnusedVariable hl
                                           data=date(2009, 2, 5), estado=est, posicao='S042')

    def test_ajax_escolhe_patrimonio__empty(self):
        """
        Verifica chamanda do escolhe_patrimonio com a base vazia
        """
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        self.response = self.client.get(url)
        self.assertEqual(200, self.response.status_code)

        self.assertIn(b'Nenhum registro', self.response.content)

    def test_ajax_escolhe_patrimonio__not_found(self):
        """
        Verifica chamanda do escolhe_patrimonio sem encontrar registro
        """
        self.setUpPatrimonio('1134', '')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '789'})
        self.assertIn(b'Nenhum registro', response.content)

    def test_ajax_escolhe_patrimonio__nf_pagamento(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo num_documento do Protocolo
        """
        self.setUpPatrimonio('1234', '')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '1234'})
        self.assertIn(b'"pk": 1', response.content)

    def test_ajax_escolhe_patrimonio___ns_patrimonio(self):
        """
        Verifica chamanda do escolhe_patrimonio encontrando registro pelo numero de serie do Patrimonio
        """
        self.setUpPatrimonio('', '7890')
        url = reverse("patrimonio.views.ajax_escolhe_patrimonio")
        response = self.client.get(url, {'num_doc': '789'})
        self.assertIn(b'"pk": 2', response.content)

    def test_view__por_estado(self):
        """
        View por estado.
        """
        self.setUpPatrimonio()

        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url, {'estado': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_estado">Patrimônio por estado do item</a>')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1 repeat="1">Patrimônio por estado - Ativo</h1>')
        self.assertContains(response, u'<th>Entidade</th>')
        self.assertContains(response, u'<th>Local</th>')
        self.assertContains(response, u'<th>Procedência</th>')
        self.assertContains(response, u'<th>Marca</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>NS</th>')

        self.assertContains(response, u'<td>SAC</td>')
        self.assertContains(response, u'<td>PROC</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>PN001</td>')
        self.assertContains(response,
                            u'<td><a href="%s"></a></td>' % reverse('admin:patrimonio_patrimonio_change', args=(1,)))

    def test_view__por_estado__parametro_estado_vazio(self):
        """
        View por estado.
        Sem o envio de parametro de estado, deve ir para a tela de filtro de seleção do estado.
        """
        self.setUpPatrimonio()

        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_estado">Patrimônio por estado do item</a>')

        self.assertContains(response, u'<option value="1" >Ativo (1)</option>')

    def test_ajax_patrimonio_historico(self):
        """
        Teste de View de ajax de histórico de patrimonio.
        """
        self.setUpPatrimonio()

        url = reverse("patrimonio.views.ajax_patrimonio_historico")
        response = self.client.get(url, {'id': '1'})

        self.assertEqual(200, response.status_code)

        self.assertContains(response, u'"estado_desc": "Ativo"')
        self.assertContains(response, u'"entidade_id": 3')
        self.assertContains(response, u'"estado_id": 1')
        self.assertContains(response, u'"localizacao_id": 1')
        self.assertContains(response, u'"entidade_desc": "SAC"')
        self.assertContains(response, u'"descricao": "Emprestimo"')
        self.assertContains(response, u'"posicao": "S042"')
        self.assertContains(response, u'"localizacao_desc": "SAC - Dr. Ovidio, 215 - "')

    def test_ajax_escolhe_pagamento(self):
        """
        Teste de View de ajax de pagamentos
        """
        self.setUpPatrimonio('1234', '')

        url = reverse("patrimonio.views.ajax_escolhe_pagamento")

        response = self.client.get(url, {'termo': '1', 'numero': '1234'})

        self.assertEqual(200, response.status_code)

        self.assertContains(response, u'"valor": "Doc. 1234, cheque 333333, valor 1000.00"')

    def test_ajax_escolhe_pagamento__nao_encontrado(self):
        """
        Teste de View de ajax de pagamentos
        """
        self.setUpPatrimonio('1234', '')

        url = reverse("patrimonio.views.ajax_escolhe_pagamento")
        response = self.client.get(url, {'termo': '1', 'numero': '7777777'})

        self.assertEqual(200, response.status_code)
        self.assertContains(response, u'"valor": "Nenhum registro"')

    def test_ajax_escolhe_entidade(self):
        """
        Teste de View de ajax de pagamentos
        """
        self.setUpPatrimonio('1234', '')
        # setup para remover a conta_corrente e forçar outro response
        pgt = Pagamento.objects.get(pk=1)
        pgt.conta_corrente = None
        pgt.save()

        url = reverse("patrimonio.views.ajax_escolhe_pagamento")
        response = self.client.get(url, {'termo': '1', 'numero': '1234'})

        self.assertEqual(200, response.status_code)
        self.assertContains(response, u'"valor": "Doc. 1234, valor None"')

    def test_view__por_tipo(self):
        """
        View de relatório por tipo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo")
        response = self.client.get(url, {'tipo': '1', 'procedencia': '2'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo/">Patrimônios por tipo</a>')

        # asssert dos filtros
        self.assertContains(response, u'<option value="1" selected>TIPO</option>')
        self.assertContains(response, u'<option value="2" selected>PROC</option>')

        # asssert dos botões de PDF e XLS
        self.assertContains(response, u'name="acao" value="2"')
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1 repeat="1">Patrimônios por tipo</h1>')
        self.assertContains(response, u'<h4>Patrimonios do tipo TIPO</h4>')

        self.assertContains(response, u'<th>Checado</th>')
        self.assertContains(response, u'<th>ID</th>')
        self.assertContains(response, u'<th>Procedência</th>')
        self.assertContains(response, u'<th>Marca</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>NS</th>')
        self.assertContains(response, u'<th>Local</th>')
        self.assertContains(response, u'<th>Posição</th>')
        self.assertContains(response, u'<th>Estado</th>')
        self.assertContains(response, u'<th>NF</th>')

        self.assertContains(response, u'<td><a href="%s">1</a></td>'
                            % reverse('admin:patrimonio_patrimonio_change', args=(1,)))
        self.assertContains(response, u'<td>PROC</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>PN001</td>')
        self.assertContains(response, u'<td>SAC - Dr. Ovidio, 215</td>')
        self.assertContains(response, u'<td>Ativo</td>')

    def test_view__por_tipo__sem_parametro_de_tipo(self):
        """
        View de relatório por tipo.
        Sem envio do parametro de tipo para a resposta cair na página de filtro de tipo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo")
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo/">Patrimônios por tipo</a>')

        self.assertContains(response, u'<option value="1">TIPO</option>')

        self.assertNotContains(response, u'<h1 repeat="1">Inventário por tipo</h1>')
        self.assertNotContains(response, u'<h4>Patrimonios do tipo TIPO</h4>')

    def test_view__por_tipo__pdf(self):
        """
        View de relatório por tipo. Resposta em PDF.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo")
        response = self.client.get(url, {'tipo': '1', 'procedencia': '1', 'acao': '1'})

        self.assertEqual(200, response.status_code)
        self.assertContains(response, '%PDF-')

    def test_view__por_tipo__xls(self):
        """
        View de relatório por tipo. Resposta em XLS.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo")
        response = self.client.get(url, {'tipo': '1', 'procedencia': '2', 'acao': '2'})

        self.assertEqual(200, response.status_code)
        self.assertContains(response, 'Tablib')  # identifica a biblioteca que gera o xls
        self.assertContains(response, 'PROC')

    def test_view__por_marca(self):
        """
        View de relatório por marca.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_marca")
        response = self.client.get(url, {'marca': 'DELL'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_marca">Patrimônio por marca</a>')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1 repeat="1">Inventário por marca</h1>')
        self.assertContains(response, u'<td>PROC</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>Ativo</td>')

        self.assertContains(response, u'<td>PROC</td>')

    def test_view__por_marca__sem_filtro(self):
        """
        View de relatório por marca. Teste sem passar o filtro, que deve cair na página de seleção de filtros

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_marca")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_marca">Patrimônio por marca</a>')

        # assert filtro
        self.assertContains(response, u'<option value="DELL">DELL</option>')

        self.assertNotContains(response, u'<h1 repeat="1">Inventário por marca</h1>')

    def test_view__por_marca__pdf(self):
        """
        View de relatório por marca. Resposta em PDF.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_marca", kwargs={'pdf': 1})
        response = self.client.get(url, {'marca': 'DELL'})

        self.assertEqual(200, response.status_code)
        self.assertContains(response, '%PDF-')

    def test_view__por_local(self):
        """
        View de relatório por local.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe2': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local">Patrimônio por localização</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/patrimonio/relatorio/por_local/1" '
                                      u'method="GET" id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe2" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h4 style="clear:both;">SAC - Dr. Ovidio, 215 - SAC - Dr. Ovidio, 215 - </h4>')
        self.assertContains(response, u'<td>PROC</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>Ativo</td>')

    def test_view__por_local__sem_detalhe(self):
        """
        View de relatório por local.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local">Patrimônio por localização</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/patrimonio/relatorio/por_local/1" '
                                      u'method="GET" id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe2" value="" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h4 style="clear:both;">SAC - Dr. Ovidio, 215</h4>')
        self.assertContains(response, u'<td>PROC</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>Ativo</td>')

    def test_view__por_local__pdf(self):
        """
        View de relatório por local. Resposta em PDF.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local", kwargs={'pdf': 1})
        response = self.client.get(url, {'entidade': '1', 'endereco': '1'})

        self.assertEqual(200, response.status_code)

        self.assertContains(response, '%PDF-')

    def test_view__por_local__sem_filtro(self):
        """
        View de relatório por local.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local">Patrimônio por localização</a>')

        # assert filtro
        self.assertContains(response, u'<option value="3">SAC</option>')

        self.assertNotContains(response, u'<h4>')

    def test_view__por_local_rack(self):
        """
        View de relatório por local e rack.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_rack")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_rack">Patrimônio por local e rack</a>')

        # assert filtro
        self.assertContains(response, u'<form action="/patrimonio/relatorio/por_local_rack/1"'
                                      u' method="GET" id="id_form_recurso">')
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="com_fmusp" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'SAC - Dr. Ovidio, 215')
        self.assertContains(response, u'<th>ID</th>')
        self.assertContains(response, u'<th>Tipo</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>NS</th>')
        self.assertContains(response, u'<th>Apelido</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>Posição</th>')
        self.assertContains(response, u'<th>Estado</th>')

        self.assertContains(response, u'<td><div class="level_btn"></div>'
                                      u'<a href="%s">1</a></td>'
                            % reverse('admin:patrimonio_patrimonio_change', args=(1,)))
        self.assertContains(response, u'<td class="clickable">Rack</td>')
        self.assertContains(response, u'<td class="clickable">MODEL001</td>')
        self.assertContains(response, u'<td class="clickable">PN001</td>')
        self.assertContains(response, u'<td class="clickable"></td>')
        self.assertContains(response, u'<td class="clickable"></td>')
        self.assertContains(response, u'<td class="clickable"> - </td>')
        self.assertContains(response, u'<td class="clickable">S042           </td>')
        self.assertContains(response, u'<td class="clickable">Ativo</td>')

    def test_view__por_local_rack__sem_filtro(self):
        """
        View de relatório por local e rack.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_rack", kwargs={'pdf': 0})
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_rack">Patrimônio por local e rack</a>')

        # assert filtro
        self.assertContains(response, u'select name="entidade" id="id_entidade"')
        self.assertContains(response, u'<option value="3">SAC</option>')
        self.assertContains(response, u'select name="endereco" id="id_endereco"')
        self.assertContains(response, u'select name="detalhe" id="id_detalhe"')

    def test_view__por_local_rack__pdf(self):
        """
        View de relatório por local e rack. Resposta em PDF.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_rack", kwargs={'pdf': 1})
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe': '1'})

        self.assertEqual(200, response.status_code)

        self.assertContains(response, '%PDF-')

    def test_view__por_local_termo(self):
        """
        View de relatório por local e termo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_termo">'
                                      u'Patrimônio por localização (com Termo)</a>')

        # assert filtro
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="com_fmusp" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel2" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel3" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'SAC - Dr. Ovidio, 215')

        self.assertContains(response, u'<th>ID</th>')
        self.assertContains(response, u'<th>Processo</th>')
        self.assertContains(response, u'<th>Patr. Oficial</th>')
        self.assertContains(response, u'<th>NF</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>NS</th>')
        self.assertContains(response, u'<th>Apelido</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>Posição</th>')
        self.assertContains(response, u'<th>Estado</th>')

        self.assertContains(response, u'<td><div class="level_btn"></div><a href="%s">1</a></td>'
                            % reverse('admin:patrimonio_patrimonio_change', args=(1,)))
        self.assertContains(response, u'<td class="clickable">08/22222-2</td>')
        self.assertContains(response, u'<td class="clickable">MODEL001</td>')
        self.assertContains(response, u'<td class="clickable">PN001</td>')
        self.assertContains(response, u'<td class="clickable"> - </td>')
        self.assertContains(response, u'<td class="clickable">S042           </td>')
        self.assertContains(response, u'<td class="clickable">Ativo</td>')

    def test_view__por_local_termo__com_fmusp(self):
        """
        View de relatório por local e termo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe': '1', 'com_fmusp': "True"})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_termo">'
                                      u'Patrimônio por localização (com Termo)</a>')

        # assert filtro
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="com_fmusp" value="True" />')
        self.assertContains(response, u'<input type="hidden" name="nivel1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel2" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel3" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<td class="clickable">08/22222-2</td>')

    def test_view__por_local_termo__sem_detalhe(self):
        """
        View de relatório por local e termo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo")
        response = self.client.get(url, {'entidade': '1', 'endereco': '1'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_termo">'
                                      u'Patrimônio por localização (com Termo)</a>')

        # assert filtro
        self.assertContains(response, u'<input type="hidden" name="entidade" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="1" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="" />')
        self.assertContains(response, u'<input type="hidden" name="com_fmusp" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel2" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel3" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<td class="clickable">08/22222-2</td>')

    def test_view__por_local_termo__sem_detalhe__sem_endereco(self):
        """
        View de relatório por local e termo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo")
        response = self.client.get(url, {'entidade': '3'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumbx
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_termo">'
                                      u'Patrimônio por localização (com Termo)</a>')

        # assert filtro
        self.assertContains(response, u'<input type="hidden" name="entidade" value="3" />')
        self.assertContains(response, u'<input type="hidden" name="endereco" value="" />')
        self.assertContains(response, u'<input type="hidden" name="detalhe" value="" />')
        self.assertContains(response, u'<input type="hidden" name="com_fmusp" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel1" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel2" value="" />')
        self.assertContains(response, u'<input type="hidden" name="nivel3" value="" />')

        # asssert dos botões de PDF
        self.assertContains(response, u'name="acao" value="1"')

        # asssert dos dados do relatório
        self.assertContains(response, u'<td class="clickable">08/22222-2</td>')

    def test_view__por_local_termo__sem_filtro(self):
        """
        View de relatório por local e termo.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo", kwargs={'pdf': 0})
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_local_termo">'
                                      u'Patrimônio por localização (com Termo)</a>')

        # assert filtro
        self.assertContains(response, u'<form method="GET">')
        self.assertContains(response, u'<select name="entidade" id="id_entidade"')
        self.assertContains(response, u'<option value="3">SAC</option>')
        self.assertContains(response, u'<select name="endereco" id="id_endereco"')
        self.assertContains(response, u'<select name="detalhe" id="id_detalhe"')
        self.assertContains(response, u'<input type="checkbox" name="com_fmusp"')
        self.assertContains(response, u'<input type="checkbox" name="nivel1"')
        self.assertContains(response, u'<input type="checkbox" name="nivel2"')
        self.assertContains(response, u'<input type="checkbox" name="nivel3"')

        # asssert dos botões de PDF. Não deve aparecer neste caso.
        self.assertNotContains(response, u'name="acao" value="1"')

    def test_view__por_local_termo__pdf(self):
        """
        View de relatório por local e termo. Resposta em PDF.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_local_termo", kwargs={'pdf': 1})
        response = self.client.get(url, {'entidade': '1', 'endereco': '1', 'detalhe': '1'})

        self.assertEqual(200, response.status_code)

        self.assertContains(response, '%PDF-')

    def test_view__por_tipo_equipamento2(self):
        """
        View de relatório de patrimonio por tipo de equipamento (com abertura de jstree).

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo_equipamento2")
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo_equipamento2">'
                                      u'Patrimônio por tipo de equipamento</a>')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1>Patrimônio por tipo de equipamento</h1>')
        self.assertContains(response, u'$("#blocos").jstree')

    def test_view__ajax_abre_arvore_tipo__tipo_equipamento(self):
        """
        View de relatório de patrimonio por tipo de equipamento (com abertura de jstree).

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.ajax_abre_arvore_tipo")
        response = self.client.get(url, {"id": "1", "model": "tipoequipamento"})

        self.assertEqual(200, response.status_code)

        # asssert dos dados do relatório
        self.assertContains(response, u'"data": "equipamento_descricao"')
        self.assertContains(response, u'"o_id": 1')
        self.assertContains(response, u'"o_model": "equipamento"')

    def test_view__ajax_abre_arvore_tipo__equipamento(self):
        """
        View de relatório de patrimonio por tipo de equipamento (com abertura de jstree).

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.ajax_abre_arvore_tipo")
        response = self.client.get(url, {"id": "1", "model": "equipamento"})

        self.assertEqual(200, response.status_code)

        # asssert dos dados do relatório
        # verificando os cabeçalhos/titulos
        self.assertContains(response, u'>Entidade<')
        self.assertContains(response, u'>Local<')
        self.assertContains(response, '>Posi\u00e7\u00e3o<')
        self.assertContains(response, u'>Marca<')
        self.assertContains(response, u'>Part number<')
        self.assertContains(response, u'>Estado<')
        # verificando os dados
        self.assertContains(response, u'>SAC<')
        self.assertContains(response, u'>S042<')
        self.assertContains(response, u'>DELL<')
        self.assertContains(response, u'>MODEL001<')
        self.assertContains(response, u'>PN001<')
        self.assertContains(response, u'>Ativo<')

    def test_view__ajax_abre_arvore_tipo__sem_id(self):
        """
        View de relatório de patrimonio por tipo de equipamento (com abertura de jstree).

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.ajax_abre_arvore_tipo")
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)

        # asssert dos dados do relatório
        self.assertContains(response, u'"data": "Rack')
        self.assertContains(response, u'"id": "tipoequipamento-1"')
        self.assertContains(response, u'"o_model": "tipoequipamento"')
        self.assertContains(response, u'"o_id": 1')

    def test_view__por_tipo_equipamento__sem_filtro(self):
        """
        View de relatório técnico de patrimonio por tipo de equipamento.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo_equipamento")
        response = self.client.get(url)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo_equipamento">'
                                      u'Inventário por tipo de equipamento</a>')

        # assert filtro
        self.assertContains(response, u'<select name="tipo" id="id_tipo" onchange="sel_tipo_equip()">')
        self.assertContains(response, u'<option value="1">Rack</option>')
        self.assertContains(response, u'<select name="estado" id="id_estado">')
        self.assertContains(response, u'<option value="1">Ativo</option>')
        self.assertContains(response, u'<select name="partnumber" id="id_partnumber">')
        self.assertContains(response, u'<option value="PN001">PN001</option>')

    def test_view__por_tipo_equipamento(self):
        """
        View de relatório técnico de patrimonio por tipo de equipamento.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo_equipamento")
        response = self.client.get(url, {'tipo': '1', 'estado': '1', 'partnumber': 'PN001'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo_equipamento">'
                                      u'Inventário por tipo de equipamento</a>')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1 repeat="1">Inventário por tipo de equipamento</h1>')
        self.assertContains(response, u'<h4>Tipo Rack</h4>')

        self.assertContains(response, u'<th>Entidade</th>')
        self.assertContains(response, u'<th>Local</th>')
        self.assertContains(response, u'<th>Posição</th>')
        self.assertContains(response, u'<th>Marca</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>NS</th>')
        self.assertContains(response, u'<th>Estado</th>')

        self.assertContains(response, u'<td>SAC</td>')
        self.assertContains(response, u'<td>S042</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>PN001</td>')
        self.assertContains(response, u'<td><a href="%s"></a></td>'
                            % reverse('admin:patrimonio_patrimonio_change', args=(1,)))
        self.assertContains(response, u'<td>Ativo</td></tr>')

    def test_view__por_tipo_equipamento__filtro_todos_tipos(self):
        """
        View de relatório técnico de patrimonio por tipo de equipamento.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_tipo_equipamento")
        response = self.client.get(url, {'tipo': '0', 'estado': '1', 'partnumber': 'PN001'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_tipo_equipamento">'
                                      u'Inventário por tipo de equipamento</a>')

        # asssert dos dados do relatório
        self.assertContains(response, u'<h1 repeat="1">Inventário por tipo de equipamento</h1>')
        self.assertContains(response, u'<h4>Tipo todos</h4>')

        self.assertContains(response, u'<th>Entidade</th>')
        self.assertContains(response, u'<th>Local</th>')
        self.assertContains(response, u'<th>Posição</th>')
        self.assertContains(response, u'<th>Marca</th>')
        self.assertContains(response, u'<th>Modelo</th>')
        self.assertContains(response, u'<th>Part number</th>')
        self.assertContains(response, u'<th>Descrição</th>')
        self.assertContains(response, u'<th>NS</th>')
        self.assertContains(response, u'<th>Estado</th>')

        self.assertContains(response, u'<td>SAC</td>')
        self.assertContains(response, u'<td>S042</td>')
        self.assertContains(response, u'<td>DELL</td>')
        self.assertContains(response, u'<td>MODEL001</td>')
        self.assertContains(response, u'<td>PN001</td>')
        self.assertContains(response, u'<td><a href="%s"></a></td>'
                            % reverse('admin:patrimonio_patrimonio_change', args=(1,)))
        self.assertContains(response, u'<td>Ativo</td></tr>')

    def test_view__por_termo__sem_filtro(self):
        """
        View de relatório administrativo de patrimônio por termo de outorga.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_termo")
        response = self.client.get(url)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_termo">Patrimônio por termo de outorga</a>')

        # assert filtro
        self.assertContains(response, u'<select name="termo" id="id_termo">')
        self.assertContains(response, u'<option value="1">08/22222-2</option>')
        self.assertContains(response, u'<select name="marca" id="id_marca" multiple size=7>')
        self.assertContains(response, u'<select name="modalidade" id="id_modalidade">')
        self.assertContains(response, u'<select name="agilis" id="id_agilis">')
        self.assertContains(response, u'<select name="doado" id="id_doado">')
        self.assertContains(response, u'<select name="localizado" id="id_localizado">')
        self.assertContains(response, u'<select name="numero_fmusp" id="id_numero_fmusp">')
        self.assertContains(response, u'<label for="id_ver_numero_fmusp">'
                                      u'Apresenta patrimônio oficial no relatório</label>')

    def test_view__por_termo(self):
        """
        View de relatório técnico de patrimonio por tipo de equipamento.

        """
        self.setUpPatrimonio()
        url = reverse("patrimonio.views.por_termo")
        response = self.client.get(url, {'tipo': '1', 'estado': '1', 'partnumber': 'PN001'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_termo">Patrimônio por termo de outorga</a>')

        # asssert dos dados do relatório
        self.assertContains(response, u'<a href="/patrimonio/relatorio/por_termo">Patrimônio por termo de outorga</a>')
        self.assertContains(response, u'<select name="termo" id="id_termo"')
        self.assertContains(response, u'<option value="1">08/22222-2</option>')
        self.assertContains(response, u'<select name="marca" id="id_marca"')
        self.assertContains(response, u'<select name="modalidade" id="id_modalidade"')
        self.assertContains(response, u'<select name="agilis" id="id_agilis"')
        self.assertContains(response, u'<select name="doado" id="id_doado"')
        self.assertContains(response, u'<select name="localizado" id="id_localizado"')
        self.assertContains(response, u'<select name="numero_fmusp" id="id_numero_fmusp"')
        self.assertContains(response, u'<input type="checkbox" name="ver_numero_fmusp" id="id_ver_numero_fmusp"')


class ViewPermissionDeniedTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário sem permissão de superusuário.
    """
    fixtures = ['auth_user.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewPermissionDeniedTest, self).setUp()
        self.response = self.client.login(username='john', password='123456')

    def test_por_estado(self):
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_tipo(self):
        url = reverse("patrimonio.views.por_tipo")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_marca(self):
        url = reverse("patrimonio.views.por_marca")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_local(self):
        url = reverse("patrimonio.views.por_local")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_local_rack(self):
        url = reverse("patrimonio.views.por_local_rack")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_local_termo(self):
        url = reverse("patrimonio.views.por_local_termo")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_tipo_equipamento(self):
        url = reverse("patrimonio.views.por_tipo_equipamento")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_termo(self):
        url = reverse("patrimonio.views.por_termo")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_racks(self):
        url = reverse("patrimonio.views.racks")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_relatorio_rack(self):
        url = reverse("patrimonio.views.relatorio_rack")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_presta_contas(self):
        url = reverse("patrimonio.views.presta_contas")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_por_tipo_equipamento2(self):
        url = reverse("patrimonio.views.por_tipo_equipamento2")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_planta_baixa_edit(self):
        url = reverse("patrimonio.views.planta_baixa_edit")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)


class ViewParcialPermissionTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário com permissão individual por view.
    """
    fixtures = ['auth_user_patrimonio_permission.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewParcialPermissionTest, self).setUp()
        self.response = self.client.login(username='paul', password='123456')

    def test_por_estado(self):
        url = reverse("patrimonio.views.por_estado")
        response = self.client.get(url)
        self.assertContains(response, u'breadcrumbs', status_code=200)
