# -*- coding: utf-8 -*-
from utils.SeleniumServerTestCase import SeleniumServerTestCase
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomeTest(SeleniumServerTestCase):

    def setUp(self):
        super(HomeTest, self).setUp()

    def tearDown(self):
        super(HomeTest, self).tearDown()

    def test_home_page(self):
        self.browser.get(self.sistema_url + '/admin/')

        elemHeader = self.browser.find_element_by_css_selector('div#container h1')
        self.assertEquals(elemHeader.text, u'Administração do Site')

    def test_controle_500(self):
        url = self.sistema_url + '/membro/mensalf?ano=2012&mes=1&'

        self.browser.get(url)
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)' % url)
        self.assertTrue(self.is_http_500(), u'Requisicao %s retornou HTTP (500)' % url)

    def test_controle_404(self):
        url = self.sistema_url + '/admin/asdfasdfasdf/'

        self.browser.get(url)
        self.assertTrue(self.is_http_404(), u'Requisicao %s etornou HTTP (404)' % url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)' % url)


class PesquisaTest(SeleniumServerTestCase):

    def setUp(self):
        super(PesquisaTest, self).setUp()

    def tearDown(self):
        super(PesquisaTest, self).tearDown()

    def test__l2s__lista(self):
        url = self.sistema_url + '/admin/pesquisa/l2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__l2s__registro(self):
        url = self.sistema_url + '/admin/pesquisa/l2/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__l2s__registro__save(self):
        url = self.sistema_url + '/admin/pesquisa/l2/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__l3__lista(self):
        url = self.sistema_url + '/admin/pesquisa/l3/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__l3__registro(self):
        url = self.sistema_url + '/admin/pesquisa/l3/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__l3__registro__save(self):
        url = self.sistema_url + '/admin/pesquisa/l3/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)
#
#     def test__kyatera__lista(self):
#         url = self.sistema_url + '/admin/pesquisa/pesquisa/'
#         self.browser.get(url)
#         self.assertLoadPage(url)

# problema de acesso para usuario
# não encontrado o item no Auth para poder habilitar a modificação
#     def test__kyatera__registro(self):
#         url = self.sistema_url + '/admin/pesquisa/pesquisa/23/'
#         self.browser.get(url)
#         self.assertLoadPage(url)

#     def test__kyatera__registro__save(self):
#         url = self.sistema_url + '/admin/pesquisa/pesquisa/23/'
#         self.browser.get(url)
#         self.assertLoadPageAndSaveEdit(url)


class AuthTest(SeleniumServerTestCase):

    def setUp(self):
        super(AuthTest, self).setUp()

    def tearDown(self):
        super(AuthTest, self).tearDown()

    def test__grupos__lista(self):
        url = self.sistema_url + '/admin/auth/group/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__grupos__busca(self):
        url = self.sistema_url + '/admin/auth/group/?q=protocolo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__grupos__registro(self):
        url = self.sistema_url + '/admin/auth/group/8/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__grupos__registro__save(self):
        url = self.sistema_url + '/admin/auth/group/8/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__user__lista(self):
        url = self.sistema_url + '/admin/auth/user/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__user__busca(self):
        url = self.sistema_url + '/admin/auth/user/?q=admin'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__user__registro(self):
        url = self.sistema_url + '/admin/auth/user/78/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__user__registro__save(self):
        url = self.sistema_url + '/admin/auth/user/78/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class EventoTest(SeleniumServerTestCase):

    def setUp(self):
        super(EventoTest, self).setUp()

    def tearDown(self):
        super(EventoTest, self).tearDown()

    def test__evento__lista(self):
        url = self.sistema_url + '/admin/evento/evento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__evento__busca(self):
        url = self.sistema_url + '/admin/evento/evento/?q=palestra'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__evento__registro(self):
        url = self.sistema_url + '/admin/evento/evento/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__evento__registro__save(self):
        url = self.sistema_url + '/admin/evento/evento/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__sessao__lista(self):
        url = self.sistema_url + '/admin/evento/sessao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sessao__busca(self):
        url = self.sistema_url + '/admin/evento/sessao/?q=rnp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sessao__registro(self):
        url = self.sistema_url + '/admin/evento/sessao/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sessao__registro__save(self):
        url = self.sistema_url + '/admin/evento/sessao/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo__lista(self):
        url = self.sistema_url + '/admin/evento/tipo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo__registro(self):
        url = self.sistema_url + '/admin/evento/tipo/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo__registro__save(self):
        url = self.sistema_url + '/admin/evento/tipo/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__areas_do_programa__lista(self):
        url = self.sistema_url + '/admin/evento/areaprograma/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__areas_do_programa__registro(self):
        url = self.sistema_url + '/admin/evento/areaprograma/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__areas_do_programa__registro__save(self):
        url = self.sistema_url + '/admin/evento/areaprograma/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__areas_operacionais__lista(self):
        url = self.sistema_url + '/admin/evento/areaoperacional/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__areas_operacionais__registro(self):
        url = self.sistema_url + '/admin/evento/areaoperacional/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__areas_operacionais__registro__save(self):
        url = self.sistema_url + '/admin/evento/areaoperacional/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class MembroTest(SeleniumServerTestCase):

    def setUp(self):
        super(MembroTest, self).setUp()

    def tearDown(self):
        super(MembroTest, self).tearDown()

    def test__relatorios_administrativos__controle_de_horas__filtro(self):
        url = self.sistema_url + '/membro/mensalf'
        self.browser.get(url)
        self.assertLoadPage(url)

# Não é acessível por usuário sem permissão
#     def test__relatorios_administrativos__controle_de_horas__lista(self):
#         url = self.sistema_url + '/membro/mensalf?ano=2013&mes=0&funcionario=49'
#         self.browser.get(url)
#         self.assertLoadPage(url)
#

    def test__arq_sindicato__lista(self):
        url = self.sistema_url + '/admin/membro/sindicatoarquivo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arq_sindicato__busca_nome(self):
        url = self.sistema_url + '/admin/membro/sindicatoarquivo/?q=amanda'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arq_sindicato__busca_ano(self):
        url = self.sistema_url + '/admin/membro/sindicatoarquivo/?q=2012'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arq_sindicato__registro(self):
        url = self.sistema_url + '/admin/membro/sindicatoarquivo/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arq_sindicato__registro__save(self):
        url = self.sistema_url + '/admin/membro/sindicatoarquivo/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__assinatura__lista(self):
        url = self.sistema_url + '/admin/membro/assinatura/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assinatura__busca(self):
        url = self.sistema_url + '/admin/membro/assinatura/?q=anna'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assinatura__registro(self):
        url = self.sistema_url + '/admin/membro/assinatura/4/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assinatura__registro__save(self):
        url = self.sistema_url + '/admin/membro/assinatura/4/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__cargo__lista(self):
        url = self.sistema_url + '/admin/membro/cargo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cargo__registro(self):
        url = self.sistema_url + '/admin/membro/cargo/45/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cargo__registro__save(self):
        url = self.sistema_url + '/admin/membro/cargo/45/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__controles__lista(self):
        url = self.sistema_url + '/admin/membro/controle/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__controles__lista__filtro(self):
        url = self.sistema_url + '/admin/membro/controle/?membro__id__exact=2'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__controles__registro_filtro(self):
        url = self.sistema_url + '/admin/membro/controle/?membro__id__exact=2'
        self.browser.get(url)
        self.assertLoadPage(url)

# Não é acessível por usuário sem permissão
#     def test__controles__registro(self):
#         url = self.sistema_url + '/admin/membro/controle/2242/'
#         self.browser.get(url)
#         self.assertLoadPage(url)
#

    def test__dispensas__lista(self):
        url = self.sistema_url + '/admin/membro/dispensalegal/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__registro(self):
        url = self.sistema_url + '/admin/membro/dispensalegal/21/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__registro__save(self):
        url = self.sistema_url + '/admin/membro/dispensalegal/21/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__ferias__lista(self):
        url = self.sistema_url + '/admin/membro/ferias/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ferias__busca(self):
        url = self.sistema_url + '/admin/membro/ferias/?q=anna'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ferias__registro(self):
        url = self.sistema_url + '/admin/membro/ferias/12/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ferias__registro__save(self):
        url = self.sistema_url + '/admin/membro/ferias/13'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__membro__lista(self):
        url = self.sistema_url + '/admin/membro/membro/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__busca_nome(self):
        url = self.sistema_url + '/admin/membro/membro/?q=costa'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__busca_email(self):
        url = self.sistema_url + '/admin/membro/membro/?q=ansp.br'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__lista_paginacao(self):
        url = self.sistema_url + '/admin/membro/membro/?p=2'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__membro__busca(self):
        url = self.sistema_url + '/admin/membro/membro/?q=paulo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_dispensa__lista(self):
        url = self.sistema_url + '/admin/membro/tipodispensa/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_dispensa__registro(self):
        url = self.sistema_url + '/admin/membro/tipodispensa/10/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_dispensa__registro__save(self):
        url = self.sistema_url + '/admin/membro/tipodispensa/10/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_de_assinatura__lista(self):
        url = self.sistema_url + '/admin/membro/tipoassinatura/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_assinatura__registro(self):
        url = self.sistema_url + '/admin/membro/tipoassinatura/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_assinatura__registro__save(self):
        url = self.sistema_url + '/admin/membro/tipoassinatura/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class MemorandoTest(SeleniumServerTestCase):

    def setUp(self):
        super(MemorandoTest, self).setUp()

    def tearDown(self):
        super(MemorandoTest, self).tearDown()

    def test__relatorios_administrativos_memorando_fapesp__filtro(self):
        url = self.sistema_url + '/memorando/relatorio'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorios_administrativos_memorando_fapesp__lista(self):
        url = self.sistema_url + '/memorando/relatorio?mem=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assunto__lista(self):
        url = self.sistema_url + '/admin/memorando/assunto/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assunto__registro(self):
        url = self.sistema_url + '/admin/memorando/assunto/17/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__assunto__registro__save(self):
        url = self.sistema_url + '/admin/memorando/assunto/17/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__estados__lista(self):
        url = self.sistema_url + '/admin/memorando/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro(self):
        url = self.sistema_url + '/admin/memorando/estado/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro__save(self):
        url = self.sistema_url + '/admin/memorando/estado/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__memorando_simples__lista(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_simples__busca_assunto(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/?q=termo+de+aceite'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_simples__busca_destinatario(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/?q=level'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_simples__registro(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/257/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_simples__registro__save(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/257/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__memorando_simples__registro_simples_lista(self):
        url = self.sistema_url + '/admin/memorando/memorandosimples/?q=2013'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_fapesp__lista(self):
        url = self.sistema_url + '/admin/memorando/memorandofapesp/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_fapesp__registro(self):
        url = self.sistema_url + '/admin/memorando/memorandofapesp/4/'
        self.browser.get(url)
        self.assertLoadPage(url)
# Removendo o teste de save. Aparentemente está variando conforme o ambiente
# Talvez seja por causa da renderização do editor de HTML que utiliza JS
#     def test__memorando_fapesp__registro__save(self):
#         url = self.sistema_url + '/admin/memorando/memorandofapesp/4/'
#         self.browser.get(url)
#         self.assertLoadPageAndSaveEdit(url)

    def test__memorando_de_resposta_fapesp__lista(self):
        url = self.sistema_url + '/admin/memorando/memorandoresposta/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_de_resposta_fapesp__registro_resposta(self):
        url = self.sistema_url + '/admin/memorando/memorandoresposta/11/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__memorando_de_resposta_fapesp__registro_pdf(self):
        url = self.sistema_url + '/memorando/fapesp/11'
        self.browser.get(url)
        self.assertLoadPage(url)


class IdentificacaoTest(SeleniumServerTestCase):

    def setUp(self):
        super(IdentificacaoTest, self).setUp()

    def tearDown(self):
        super(IdentificacaoTest, self).tearDown()

    def test__relatorio_tecnico__documentos_por_entidade__lista(self):
        url = self.sistema_url + '/identificacao/relatorios/arquivos'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__filtro(self):
        url = self.sistema_url + '/identificacao/agenda'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__aba_participantes(self):
        url = self.sistema_url + '/identificacao/agenda?agenda=3'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__aba_tic(self):
        url = self.sistema_url + '/identificacao/agenda/15/?agenda=3'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__aba_outras(self):
        url = self.sistema_url + '/identificacao/agenda/17/?agenda=3'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__aba_parceira(self):
        url = self.sistema_url + '/identificacao/agenda/3/?agenda=3'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__agenda__aba_fornecedor(self):
        url = self.sistema_url + '/identificacao/agenda/18/?agenda=3'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__ecossistema__aba_participante(self):
        url = self.sistema_url + '/identificacao/ecossistema/par'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__ecossistema__aba_tic(self):
        url = self.sistema_url + '/identificacao/ecossistema/tic'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__asn__lista(self):
        url = self.sistema_url + '/admin/identificacao/asn/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__asn__busca_numero(self):
        url = self.sistema_url + '/admin/identificacao/asn/?q=1251'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__asn__busca_entidade(self):
        url = self.sistema_url + '/admin/identificacao/asn/?q=ansp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__asn__registro(self):
        url = self.sistema_url + '/admin/identificacao/asn/32/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__asn__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/asn/32/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__acesso__lista(self):
        url = self.sistema_url + '/admin/identificacao/acesso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acesso__registro(self):
        url = self.sistema_url + '/admin/identificacao/acesso/23/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acesso__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/acesso/23/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__agenda__lista(self):
        url = self.sistema_url + '/admin/identificacao/agenda/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__agenda__registro(self):
        url = self.sistema_url + '/admin/identificacao/agenda/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__agenda__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/agenda/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__contato__lista(self):
        url = self.sistema_url + '/admin/identificacao/contato/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__contato__busca_nome(self):
        url = self.sistema_url + '/admin/identificacao/contato/?q=lopez'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__contato__busca_entidade(self):
        url = self.sistema_url + '/admin/identificacao/contato/?q=ansp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__contato__registro(self):
        url = self.sistema_url + '/admin/identificacao/contato/480/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__contato__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/contato/480/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__ecossistema__lista(self):
        url = self.sistema_url + '/admin/identificacao/ecossistema/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ecossistema__registro(self):
        url = self.sistema_url + '/admin/identificacao/ecossistema/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ecossistema__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/ecossistema/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__endereco_detalhe__lista(self):
        url = self.sistema_url + '/admin/identificacao/enderecodetalhe/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco_detalhe__busca(self):
        url = self.sistema_url + '/admin/identificacao/enderecodetalhe/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco_detalhe__registro(self):
        url = self.sistema_url + '/admin/identificacao/enderecodetalhe/14/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco_detalhe__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/enderecodetalhe/1432/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__endereco__lista(self):
        url = self.sistema_url + '/admin/identificacao/endereco/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco__busca(self):
        url = self.sistema_url + '/admin/identificacao/endereco/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco__registro(self):
        url = self.sistema_url + '/admin/identificacao/endereco/90/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__endereco__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/endereco/90/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__entidade__lista(self):
        url = self.sistema_url + '/admin/identificacao/entidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__entidade__registro(self):
        url = self.sistema_url + '/admin/identificacao/entidade/488/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__entidade__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/entidade/488/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__identificacao__lista(self):
        url = self.sistema_url + '/admin/identificacao/identificacao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__identificacao__registro(self):
        url = self.sistema_url + '/admin/identificacao/identificacao/553/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__identificacao__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/identificacao/553/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__nivel_de_acesso__lista(self):
        url = self.sistema_url + '/admin/identificacao/nivelacesso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__nivel_de_acesso__registro(self):
        url = self.sistema_url + '/admin/identificacao/nivelacesso/8/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__nivel_de_acesso__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/nivelacesso/8/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_arquivo_entidade__lista(self):
        url = self.sistema_url + '/admin/identificacao/tipoarquivoentidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_arquivo_entidade__registro(self):
        url = self.sistema_url + '/admin/identificacao/tipoarquivoentidade/4/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_arquivo_entidade__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/tipoarquivoentidade/4/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_detalhe__lista(self):
        url = self.sistema_url + '/admin/identificacao/tipodetalhe/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_detalhe__registro(self):
        url = self.sistema_url + '/admin/identificacao/tipodetalhe/8/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_detalhe__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/tipodetalhe/8/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_entidade__lista(self):
        url = self.sistema_url + '/admin/identificacao/tipoentidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_entidade__registro(self):
        url = self.sistema_url + '/admin/identificacao/tipoentidade/6/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_entidade__registro__save(self):
        url = self.sistema_url + '/admin/identificacao/tipoentidade/6/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class MonitorTest(SeleniumServerTestCase):

    def setUp(self):
        super(MonitorTest, self).setUp()

    def tearDown(self):
        super(MonitorTest, self).tearDown()

    def test__link__lista(self):
        url = self.sistema_url + '/admin/monitor/link/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__link__registro(self):
        url = self.sistema_url + '/admin/monitor/link/49/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__link__registro__save(self):
        url = self.sistema_url + '/admin/monitor/link/49/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class FinanceiroTest(SeleniumServerTestCase):

    def setUp(self):
        super(FinanceiroTest, self).setUp()

    def tearDown(self):
        super(FinanceiroTest, self).tearDown()

    def test__relatorio_gerencial__acordo__filtro_inicial(self):
        """
        Verifica se o filtro de acordo lista ao menos os últimos 5 acordos
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos')

        elem = self.browser.find_element_by_css_selector('select#id_termo')

        self.assertTrue(elem.text.find('13/11711-5') >= 0)
        self.assertTrue(elem.text.find('11/52044-6') >= 0)
        self.assertTrue(elem.text.find('10/52277-8') >= 0)
        self.assertTrue(elem.text.find('09/11388-4') >= 0)
        self.assertTrue(elem.text.find('08/52885-8') >= 0)

    def test__relatorio_gerencial__acordo__lista(self):
        """
        Verifica se o relatorio foi aberto
        """
        self.browser.get(self.sistema_url + '/financeiro/relatorios/acordos?termo=21')

        elem = self.browser.find_element_by_css_selector('div#content.colM h1')
        self.assertTrue(elem.text.find('13/11711-5') >= 0)

        # elem = self.browser.find_element_by_css_selector('tr#tr_1_2.nivel1 td')
        # self.assertTrue(elem.text.find(u'Colaboração') >= 0)

        elem = self.browser.find_element_by_css_selector('.nivel3 td a')

    def test__relatorio_gerencial__gerencial__filtro_inicial(self):
        url = self.sistema_url + '/financeiro/relatorios/gerencial'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_gerencial__gerencial__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/gerencial?termo=21'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__diferencas_de_caixa__filtro(self):
        url = self.sistema_url + '/financeiro/relatorios/caixa'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__diferencas_de_caixa__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/caixa?termo=17'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__diferencas_totais__filtro(self):
        url = self.sistema_url + '/financeiro/relatorios/parciais'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__diferencas_totais__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/parciais?termo=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_da_cc__filtro(self):
        url = self.sistema_url + '/financeiro/extrato'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_da_cc__lista(self):
        url = self.sistema_url + '/financeiro/extrato?ano=2008'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_da_cc_por_mes__filtro(self):
        url = self.sistema_url + '/financeiro/extrato_mes'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_da_cc_por_mes__lista(self):
        url = self.sistema_url + '/financeiro/extrato_mes?mes=1&ano=2008'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_de_tarifas_por_mes__filtro(self):
        url = self.sistema_url + '/financeiro/extrato_tarifas'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_de_tarifas_por_mes__lista(self):
        url = self.sistema_url + '/financeiro/extrato_tarifas?mes=1&ano=2008'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_do_financeiro_por_mes__filtro(self):
        url = self.sistema_url + '/financeiro/extrato_financeiro'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_do_financeiro_por_mes__lista(self):
        url = self.sistema_url + '/financeiro/extrato_financeiro?mes=1&termo=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_financeiro_parcial__filtro(self):
        url = self.sistema_url + '/financeiro/extrato_financeiro_parciais'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__extrato_financeiro_parcial__lista(self):
        url = self.sistema_url + '/financeiro/extrato_financeiro_parciais?termo=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__pagamentos_por_mes__filtro(self):
        url = self.sistema_url + '/financeiro/relatorios/pagamentos_mes'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__pagamentos_por_mes__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/pagamentos_mes?mes=1&ano=2008'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__pagamentos_por_parcial__filtro(self):
        url = self.sistema_url + '/financeiro/relatorios/pagamentos_parcial'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__pagamentos_por_parcial__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/pagamentos_parcial?termo=6&parcial=1'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__prestacao_de_contas__filtro(self):
        url = self.sistema_url + '/financeiro/relatorios/prestacao'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__prestacao_de_contas__lista(self):
        url = self.sistema_url + '/financeiro/relatorios/prestacao?termo=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__prestacao_de_contas_patrimonial__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/presta_contas'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__protocolos_por_descricao__filtro(self):
        url = self.sistema_url + '/protocolo/descricao'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__protocolos_por_descricao__lista(self):
        url = self.sistema_url + '/protocolo/descricao?termo=6'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__auditoria__lista(self):
        url = self.sistema_url + '/admin/financeiro/auditoria/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__auditoria__busca(self):
        url = self.sistema_url + '/admin/financeiro/auditoria/?q=135'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__auditoria__registro(self):
        url = self.sistema_url + '/admin/financeiro/auditoria/9064/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__auditoria__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/auditoria/9064/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__lista(self):
        url = self.sistema_url + '/admin/financeiro/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__busca(self):
        url = self.sistema_url + '/admin/financeiro/estado/?q=emprestimo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro(self):
        url = self.sistema_url + '/admin/financeiro/estado/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/estado/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__extrato_cc__lista(self):
        url = self.sistema_url + '/admin/financeiro/extratocc/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_cc__busca(self):
        url = self.sistema_url + '/admin/financeiro/extratocc/?q=100'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_cc__registro(self):
        url = self.sistema_url + '/admin/financeiro/extratocc/6437/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_cc__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/extratocc/6437/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__extrato_financeiro__lista(self):
        url = self.sistema_url + '/admin/financeiro/extratofinanceiro/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_financeiro__busca(self):
        url = self.sistema_url + '/admin/financeiro/extratofinanceiro/?q=estorno'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_financeiro__registro(self):
        url = self.sistema_url + '/admin/financeiro/extratofinanceiro/4311/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_financeiro__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/extratofinanceiro/4311/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__extrato_patrocinio__lista(self):
        url = self.sistema_url + '/admin/financeiro/extratopatrocinio/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_patrocinio__busca(self):
        url = self.sistema_url + '/admin/financeiro/extratopatrocinio/?q=10'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_patrocinio__registro(self):
        url = self.sistema_url + '/admin/financeiro/extratopatrocinio/9/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__extrato_patrocinio__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/extratopatrocinio/9/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__localizacao_dos_patrocinios__lista(self):
        url = self.sistema_url + '/admin/financeiro/localizapatrocinio/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__localizacao_dos_patrocinios__busca(self):
        url = self.sistema_url + '/admin/financeiro/localizapatrocinio/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__localizacao_dos_patrocinios__registro(self):
        url = self.sistema_url + '/admin/financeiro/localizapatrocinio/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__localizacao_dos_patrocinios__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/localizapatrocinio/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__pagamento__lista(self):
        url = self.sistema_url + '/admin/financeiro/pagamento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pagamento__busca_operacao(self):
        url = self.sistema_url + '/admin/financeiro/pagamento/?q=850978'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pagamento__busca_notafiscal(self):
        url = self.sistema_url + '/admin/financeiro/pagamento/?q=200112'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pagamento__registro(self):
        url = self.sistema_url + '/admin/financeiro/pagamento/4690/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pagamento__registro__asve(self):
        url = self.sistema_url + '/admin/financeiro/pagamento/4690/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_comprovante_financeiro__lista(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovantefinanceiro/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_comprovante_financeiro__busca(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovantefinanceiro/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_comprovante_financeiro__registro(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovantefinanceiro/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_comprovante_financeiro__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovantefinanceiro/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_de_comprovante__lista(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovante/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_comprovante__busca(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovante/?q=geral'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_comprovante__registro(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovante/21/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_comprovante__registro__save(self):
        url = self.sistema_url + '/admin/financeiro/tipocomprovante/21/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class OutorgaTest(SeleniumServerTestCase):

    def setUp(self):
        super(OutorgaTest, self).setUp()

    def tearDown(self):
        super(OutorgaTest, self).tearDown()

    def test__relatorio_gerencial__concessoes_por_acordo__lista(self):
        url = self.sistema_url + '/outorga/relatorios/lista_acordos'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_gerencial__gerencial_progressivo__lista(self):
        url = self.sistema_url + '/outorga/relatorios/acordo_progressivo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__item_do_orcamento_por_modalidade__filtro(self):
        url = self.sistema_url + '/outorga/relatorios/item_modalidade'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativo__item_do_orcamento_por_modalidade__lista(self):
        url = self.sistema_url + '/outorga/relatorios/item_modalidade?termo=6&modalidade=9&entidade=0'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acordos__lista(self):
        url = self.sistema_url + '/admin/outorga/acordo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acordos__busca(self):
        url = self.sistema_url + '/admin/outorga/acordo/?q=tidia'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acordos__registro(self):
        url = self.sistema_url + '/admin/outorga/acordo/4/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__acordos__registro__save(self):
        url = self.sistema_url + '/admin/outorga/acordo/4/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__alteracao_de_contrato_os__lista(self):
        url = self.sistema_url + '/admin/outorga/ordemdeservico/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__alteracao_de_contrato_os__busca(self):
        url = self.sistema_url + '/admin/outorga/ordemdeservico/?q=netconn'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__alteracao_de_contrato_os__registro(self):
        url = self.sistema_url + '/admin/outorga/ordemdeservico/98/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__alteracao_de_contrato_os__registro_save(self):
        url = self.sistema_url + '/admin/outorga/ordemdeservico/98/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__arquivos__lista(self):
        url = self.sistema_url + '/admin/outorga/arquivo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arquivos__busca_arquivo(self):
        url = self.sistema_url + '/admin/outorga/arquivo/?q=pdf'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arquivos__busca_pedido(self):
        url = self.sistema_url + '/admin/outorga/arquivo/?q=inicial'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__categorias__lista(self):
        url = self.sistema_url + '/admin/outorga/categoria/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__categorias__busca(self):
        url = self.sistema_url + '/admin/outorga/categoria/?q=aditivo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__categorias__registro(self):
        url = self.sistema_url + '/admin/outorga/categoria/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__categorias__registro__save(self):
        url = self.sistema_url + '/admin/outorga/categoria/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__contratos__lista(self):
        url = self.sistema_url + '/admin/outorga/contrato/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__contratos__busca(self):
        url = self.sistema_url + '/admin/outorga/contrato/?q=uniemp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__lista(self):
        url = self.sistema_url + '/admin/outorga/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__busca(self):
        url = self.sistema_url + '/admin/outorga/estado/?q=ativo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro(self):
        url = self.sistema_url + '/admin/outorga/estado/4/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro__save(self):
        url = self.sistema_url + '/admin/outorga/estado/4/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__concecao_outorga__lista(self):
        url = self.sistema_url + '/admin/outorga/outorga/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__concecao_outorga__busca_categoria(self):
        url = self.sistema_url + '/admin/outorga/outorga/?q=cancelamento'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__concecao_outorga__busca_termo(self):
        url = self.sistema_url + '/admin/outorga/outorga/?q=13708'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__concecao_outorga__registro(self):
        url = self.sistema_url + '/admin/outorga/outorga/26/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__concecao_outorga__registro__save(self):
        url = self.sistema_url + '/admin/outorga/outorga/26/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__item__lista(self):
        url = self.sistema_url + '/admin/outorga/item/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__busca_descricao(self):
        url = self.sistema_url + '/admin/outorga/item/?q=certificados'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__busca_termo(self):
        url = self.sistema_url + '/admin/outorga/item/?q=11711'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__lista_filtro_modalidate(self):
        url = self.sistema_url + '/admin/outorga/item/?natureza_gasto__modalidade__id__exact=2'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__lista_filtro_termo(self):
        url = self.sistema_url + '/admin/outorga/item/?natureza_gasto__termo__id__exact=13'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__registro(self):
        url = self.sistema_url + '/admin/outorga/item/484/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__item__registro__save(self):
        url = self.sistema_url + '/admin/outorga/item/484/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__modalidade__lista(self):
        url = self.sistema_url + '/admin/outorga/modalidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__modalidade__busca_sigla(self):
        url = self.sistema_url + '/admin/outorga/modalidade/?q=det'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__modalidade__busca_nome(self):
        url = self.sistema_url + '/admin/outorga/modalidade/?q=despesas'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__modalidade__registro(self):
        url = self.sistema_url + '/admin/outorga/modalidade/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__modalidade__registro__save(self):
        url = self.sistema_url + '/admin/outorga/modalidade/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__origem_fapesp__lista(self):
        url = self.sistema_url + '/admin/outorga/origemfapesp/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__origem_fapesp__registro(self):
        url = self.sistema_url + '/admin/outorga/origemfapesp/744/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__origem_fapesp__registro__save(self):
        url = self.sistema_url + '/admin/outorga/origemfapesp/744/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__pastas__lista(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__busca_modalidade(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/?q=rei'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__busca_termo(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/?q=11711'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__lista_filtro_termo(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/?&termo__id__exact=17'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__lista_filtro_modalidade(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/?modalidade__id__exact=1'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__registro(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/154/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__pastas__registro__save(self):
        url = self.sistema_url + '/admin/outorga/natureza_gasto/154/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_de_documento__lista(self):
        url = self.sistema_url + '/admin/outorga/tipocontrato/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_documento__registro(self):
        url = self.sistema_url + '/admin/outorga/tipocontrato/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_de_documento__registro__save(self):
        url = self.sistema_url + '/admin/outorga/tipocontrato/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__termo_de_outorga__lista(self):
        url = self.sistema_url + '/admin/outorga/termo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__termo_de_outorga__busca_termo(self):
        url = self.sistema_url + '/admin/outorga/termo/?q=60733'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__termo_de_outorga__registro(self):
        url = self.sistema_url + '/admin/outorga/termo/21/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__termo_de_outorga__registro__save(self):
        url = self.sistema_url + '/admin/outorga/termo/21/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class RedeTest(SeleniumServerTestCase):

    def setUp(self):
        super(RedeTest, self).setUp()

    def tearDown(self):
        super(RedeTest, self).tearDown()

    def test__relatorio_gerencial__custo_de_recursos_contratados__lista(self):
        url = self.sistema_url + '/rede/custo_terremark'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__dados_cadastrais_dos_participantes__lista(self):
        url = self.sistema_url + '/rede/info'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__dados_cadastrais_dos_participantes__lista_info_tec(self):
        url = self.sistema_url + '/rede/info_tec/3'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__filtro_inicial(self):
        url = self.sistema_url + '/rede/blocosip'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_todos(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=0&designado=0'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=0&usuario=0&designado=0'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_proprietario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=32&usuario=0&designado=0'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_usuario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=215&designado=0'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_designado(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=0&proprietario=0&usuario=0&designado=215'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante_designado(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=0&designado=215'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_anunciante_usuario(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=215&designado=0'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__lista_de_bloco_ip__busca_todos_filtros(self):
        url = self.sistema_url + '/rede/blocosip?anunciante=32&proprietario=32&usuario=215&designado=215'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__planejamento_por_ano__filtro_inicial(self):
        url = self.sistema_url + '/rede/planejamento'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__planejamento_por_ano__busca(self):
        url = self.sistema_url + '/rede/planejamento?anoproj=2013%2F1&os='
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__planejamento_por_ano__busca_os(self):
        url = self.sistema_url + '/rede/planejamento?anoproj=2013%2F1&os=109'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__servicos_contratados_por_processo__filtro_inicial(self):
        url = self.sistema_url + '/rede/planejamento2'
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__relatorio_tecnico__servicos_contratados_por_processo__lista(self):
        url = self.sistema_url + '/rede/planejamento2?entidade=1&termo=17&beneficiado='
        req = self.browser.get(url)  # @UnusedVariable

        self.assertLoadPage(url)

    def test__banda__lista(self):
        url = self.sistema_url + '/admin/rede/banda/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__banda__registro(self):
        url = self.sistema_url + '/admin/rede/banda/11/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__banda__registro__save(self):
        url = self.sistema_url + '/admin/rede/banda/11/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__bloco_ip__lista(self):
        url = self.sistema_url + '/admin/rede/blocoip/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__busca_as_anunciante(self):
        url = self.sistema_url + '/admin/rede/blocoip/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__busca_ip(self):
        url = self.sistema_url + '/admin/rede/blocoip/?q=143.108'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__filtro_bloco(self):
        url = self.sistema_url + '/admin/rede/blocoip/?bloco=super'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__filtro_as_anunciante(self):
        url = self.sistema_url + '/admin/rede/blocoip/?asn__id__exact=32'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__registro(self):
        url = self.sistema_url + '/admin/rede/blocoip/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__bloco_ip__registro__save(self):
        url = self.sistema_url + '/admin/rede/blocoip/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__canal__lista(self):
        url = self.sistema_url + '/admin/rede/canal/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace_operadora__lista(self):
        url = self.sistema_url + '/admin/rede/enlaceoperadora/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace_operadora__registro(self):
        url = self.sistema_url + '/admin/rede/enlaceoperadora/34/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace_operadora__registro__save(self):
        url = self.sistema_url + '/admin/rede/enlaceoperadora/34/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__enlace__lista(self):
        url = self.sistema_url + '/admin/rede/enlace/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace__busca(self):
        url = self.sistema_url + '/admin/rede/enlace/?q=fapesp'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace__registro(self):
        url = self.sistema_url + '/admin/rede/enlace/3/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__enlace__registro__save(self):
        url = self.sistema_url + '/admin/rede/enlace/3/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__estados__lista(self):
        url = self.sistema_url + '/admin/rede/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro(self):
        url = self.sistema_url + '/admin/rede/estado/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro__save(self):
        url = self.sistema_url + '/admin/rede/estado/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__interface__lista(self):
        url = self.sistema_url + '/admin/rede/interface/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ipborda__lista(self):
        url = self.sistema_url + '/admin/rede/ipborda/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ipborda__registro(self):
        url = self.sistema_url + '/admin/rede/ipborda/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__ipborda__registro__save(self):
        url = self.sistema_url + '/admin/rede/ipborda/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__operadoras__lista(self):
        url = self.sistema_url + '/admin/rede/operadora/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__operadoras__registro(self):
        url = self.sistema_url + '/admin/rede/operadora/8/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__operadoras__registro__save(self):
        url = self.sistema_url + '/admin/rede/operadora/8/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__planeja_arquisicao__lista(self):
        url = self.sistema_url + '/admin/rede/planejaaquisicaorecurso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__planeja_arquisicao__busca(self):
        url = self.sistema_url + '/admin/rede/planejaaquisicaorecurso/?q=bandwidth'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__planeja_arquisicao__registro(self):
        url = self.sistema_url + '/admin/rede/planejaaquisicaorecurso/135/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__planeja_arquisicao__registro__save(self):
        url = self.sistema_url + '/admin/rede/planejaaquisicaorecurso/119/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__projeto__lista(self):
        url = self.sistema_url + '/admin/rede/projeto/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__projeto__registro(self):
        url = self.sistema_url + '/admin/rede/projeto/10/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__projeto__registro__save(self):
        url = self.sistema_url + '/admin/rede/projeto/10/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__recursos__lista(self):
        url = self.sistema_url + '/admin/rede/recurso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__recursos__registro(self):
        url = self.sistema_url + '/admin/rede/recurso/66/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__recursos__registro__save(self):
        url = self.sistema_url + '/admin/rede/recurso/66/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__rirs__lista(self):
        url = self.sistema_url + '/admin/rede/rir/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__rirs__registro(self):
        url = self.sistema_url + '/admin/rede/rir/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__rirs__registro__save(self):
        url = self.sistema_url + '/admin/rede/rir/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__segmento__lista(self):
        url = self.sistema_url + '/admin/rede/segmento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__segmento__registro(self):
        url = self.sistema_url + '/admin/rede/segmento/62/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__segmento__registro__save(self):
        url = self.sistema_url + '/admin/rede/segmento/62/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__sistema__lista(self):
        url = self.sistema_url + '/admin/rede/sistema/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_servico__lista(self):
        url = self.sistema_url + '/admin/rede/tiposervico/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_servico__registro(self):
        url = self.sistema_url + '/admin/rede/tiposervico/27/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_servico__registro__save(self):
        url = self.sistema_url + '/admin/rede/tiposervico/27/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__unidade__lista(self):
        url = self.sistema_url + '/admin/rede/unidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__unidade__registro(self):
        url = self.sistema_url + '/admin/rede/unidade/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__unidade__registro__save(self):
        url = self.sistema_url + '/admin/rede/unidade/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__uso__lista(self):
        url = self.sistema_url + '/admin/rede/uso/'
        self.browser.get(url)
        self.assertLoadPage(url)


class SitesTest(SeleniumServerTestCase):

    def setUp(self):
        super(SitesTest, self).setUp()

    def tearDown(self):
        super(SitesTest, self).tearDown()

    def test__sites__lista(self):
        url = self.sistema_url + '/admin/sites/site/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sites__busca(self):
        url = self.sistema_url + '/admin/sites/site/?q=intranet'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sites__registro(self):
        url = self.sistema_url + '/admin/sites/site/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__sites__registro__save(self):
        url = self.sistema_url + '/admin/sites/site/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class ProcessoTest(SeleniumServerTestCase):

    def setUp(self):
        super(ProcessoTest, self).setUp()

    def tearDown(self):
        super(ProcessoTest, self).tearDown()

    def test__relatorio_gerencial__processos__lista(self):
        url = self.sistema_url + '/processo/processos'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__atribuicoes__lista(self):
        url = self.sistema_url + '/admin/processo/atribuicao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__atribuicoes__registro(self):
        url = self.sistema_url + '/admin/processo/atribuicao/107/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__atribuicoes__registro__save(self):
        url = self.sistema_url + '/admin/processo/atribuicao/107/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__equipes__lista(self):
        url = self.sistema_url + '/admin/processo/equipe/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipes__registro(self):
        url = self.sistema_url + '/admin/processo/equipe/6/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipes__registro__save(self):
        url = self.sistema_url + '/admin/processo/equipe/6/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__grupos__lista(self):
        url = self.sistema_url + '/admin/processo/equipe/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__macroprocesso__lista(self):
        url = self.sistema_url + '/admin/processo/macroprocesso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__macroprocesso__registro(self):
        url = self.sistema_url + '/admin/processo/macroprocesso/9/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__macroprocesso__registro__save(self):
        url = self.sistema_url + '/admin/processo/macroprocesso/9/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__natureza__lista(self):
        url = self.sistema_url + '/admin/processo/natureza/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__natureza__registro(self):
        url = self.sistema_url + '/admin/processo/natureza/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__natureza__registro__save(self):
        url = self.sistema_url + '/admin/processo/natureza/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__norma__lista(self):
        url = self.sistema_url + '/admin/processo/norma/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__norma__registro(self):
        url = self.sistema_url + '/admin/processo/norma/3/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__norma__registro__save(self):
        url = self.sistema_url + '/admin/processo/norma/3/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__otrs__lista(self):
        url = self.sistema_url + '/admin/processo/otrs/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__papel__lista(self):
        url = self.sistema_url + '/admin/processo/papel/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__procedimentos__lista(self):
        url = self.sistema_url + '/admin/processo/procedimento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__lista(self):
        url = self.sistema_url + '/admin/processo/processo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__busca_area(self):
        url = self.sistema_url + '/admin/processo/processo/?q=eaa'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__busca_grupo(self):
        url = self.sistema_url + '/admin/processo/processo/?q=grupo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__busca_macroprocesso(self):
        url = self.sistema_url + '/admin/processo/processo/?q=atividades'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__registro(self):
        url = self.sistema_url + '/admin/processo/processo/115/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__processo__registro__save(self):
        url = self.sistema_url + '/admin/processo/processo/115/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__recursos__lista(self):
        url = self.sistema_url + '/admin/processo/recurso/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__recursos__registro(self):
        url = self.sistema_url + '/admin/processo/recurso/3/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__recursos__registro__save(self):
        url = self.sistema_url + '/admin/processo/recurso/3/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__visao__lista(self):
        url = self.sistema_url + '/admin/processo/visao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__visao__registro(self):
        url = self.sistema_url + '/admin/processo/visao/4/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__visao__registro__save(self):
        url = self.sistema_url + '/admin/processo/visao/4/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__area__lista(self):
        url = self.sistema_url + '/admin/processo/area/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__area__registro(self):
        url = self.sistema_url + '/admin/processo/area/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__area__registro__save(self):
        url = self.sistema_url + '/admin/processo/area/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class ProtocoloTest(SeleniumServerTestCase):

    def setUp(self):
        super(ProtocoloTest, self).setUp()

    def tearDown(self):
        super(ProtocoloTest, self).tearDown()

    def test__arquivo__lista(self):
        url = self.sistema_url + '/admin/protocolo/arquivo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__arquivo__busca(self):
        url = self.sistema_url + '/admin/protocolo/arquivo/?q=52885'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__lista(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__busca(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/?q=dl380'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__lista_filtro_estado(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/?estado__id__exact=9'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__lista_filtro_vencimento(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/?data_vencimento__gte=2014-01-01&data_vencimento__lt=2015-01-01'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__registro(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/5842/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__cotacao__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/cotacao/5842/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__descricao__lista(self):
        url = self.sistema_url + '/admin/protocolo/descricao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__descricao__busca(self):
        url = self.sistema_url + '/admin/protocolo/descricao/?q=agv'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__descricao__registro(self):
        url = self.sistema_url + '/admin/protocolo/descricao/7/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__descricao__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/descricao/7/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__estado__lista(self):
        url = self.sistema_url + '/admin/protocolo/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estado__registro(self):
        url = self.sistema_url + '/admin/protocolo/estado/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estado__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/estado/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__feriado__lista(self):
        url = self.sistema_url + '/admin/protocolo/feriado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__feriado__busca(self):
        url = self.sistema_url + '/admin/protocolo/feriado/?q=finados'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__feriado__filtro_tipo(self):
        url = self.sistema_url + '/admin/protocolo/feriado/?tipo__id__exact=1'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__feriado__registro(self):
        url = self.sistema_url + '/admin/protocolo/feriado/11/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__feriado__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/feriado/3/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__origem__lista(self):
        url = self.sistema_url + '/admin/protocolo/origem/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__origem__registro(self):
        url = self.sistema_url + '/admin/protocolo/origem/2/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__origem__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/origem/2/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__protocolo__lista(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__busca_nf(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/?q=12260'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__busca_desc(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/?q=administrativa'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__lista_filtro_termo(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/?termo__id__exact=17'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__lista_filtro_estado(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/?estado__id__exact=7'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__registro(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/2594/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__protocolo__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/protocolo/2594/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_feriado__lista(self):
        url = self.sistema_url + '/admin/protocolo/tipoferiado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_feriado__registro(self):
        url = self.sistema_url + '/admin/protocolo/tipoferiado/16/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_feriado__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/tipoferiado/15/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_documento__lista(self):
        url = self.sistema_url + '/admin/protocolo/tipodocumento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_documento__registro(self):
        url = self.sistema_url + '/admin/protocolo/tipodocumento/12/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_documento__registro__save(self):
        url = self.sistema_url + '/admin/protocolo/tipodocumento/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class QuestionarioTest(SeleniumServerTestCase):

    def setUp(self):
        super(QuestionarioTest, self).setUp()

    def tearDown(self):
        super(QuestionarioTest, self).tearDown()

    def test__questionario__lista(self):
        url = self.sistema_url + '/admin/questionario/questionario/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__questionario__registro(self):
        url = self.sistema_url + '/admin/questionario/questionario/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__questionario__registro__save(self):
        url = self.sistema_url + '/admin/questionario/questionario/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class PatrimonioTest(SeleniumServerTestCase):

    def setUp(self):
        super(PatrimonioTest, self).setUp()

    def tearDown(self):
        super(PatrimonioTest, self).tearDown()

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_todos(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=0&estado=0&partnumber=0'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento_busca_por_tipo_estado(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=1&estado=22&partnumber=0'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_por_tipo(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=1&estado=0&partnumber=0'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__busca_por_tipo_de_equpamento__busca_partnumber(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento?tipo=0&estado=0&partnumber=0350WYC%2F0+CN'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_estado_do_item__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_estado'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_localizacao__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_local'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_localizacao__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_local?entidade=1&endereco=60&detalhe=24&detalhe1=&detalhe2='
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_marca__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_marca'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_marca__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_marca?marca=3Com'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_tipo__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_tipo__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo?tipo=42'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__patrimonio_por_tipo_de_equipamento__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_tipo_equipamento2'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__racks__filtro_inicial(self):
        url = self.sistema_url + '/patrimonio/racks'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_tecnico__racks__lista(self):
        url = self.sistema_url + '/patrimonio/racks?dc=13'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__pagamentos_por_termo_de_outorga__filtro(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_termo'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__pagamentos_por_termo_de_outorga__lista(self):
        url = self.sistema_url + '/patrimonio/relatorio/por_termo?termo=6&modalidade=1&agilis=1&doado=2&localizado=2&numero_fmusp=0'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__dimensao__lista(self):
        url = self.sistema_url + '/admin/patrimonio/dimensao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__dimensao__registro(self):
        url = self.sistema_url + '/admin/patrimonio/dimensao/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__dimensao__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/dimensao/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__direcoes__lista(self):
        url = self.sistema_url + '/admin/patrimonio/direcao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__direcoes__registro(self):
        url = self.sistema_url + '/admin/patrimonio/direcao/10/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__direcoes__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/direcao/10/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__distribuica_unidade__lista(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicaounidade/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__distribuica_unidade__registro(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicaounidade/3/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__distribuica_unidade__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicaounidade/3/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__distribuicao__lista(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__distribuicao__registro(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicao/5/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__distribuicao__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/distribuicao/5/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__equipamento__lista(self):
        url = self.sistema_url + '/admin/patrimonio/equipamento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipamento__busca_descricao(self):
        url = self.sistema_url + '/admin/patrimonio/equipamento/?q=camera'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipamento__busca_partnumber(self):
        url = self.sistema_url + '/admin/patrimonio/equipamento/?q=mpp2i'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipamento__registro(self):
        url = self.sistema_url + '/admin/patrimonio/equipamento/6/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__equipamento__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/equipamento/6/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__estados__lista(self):
        url = self.sistema_url + '/admin/patrimonio/estado/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro(self):
        url = self.sistema_url + '/admin/patrimonio/estado/22/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__estados__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/estado/22/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__patrimonio__lista(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__busca_descricao(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/?q=monitor'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__busca_nf(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/?q=682'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__busca_ns(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/?q=7c5038'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__filtro_tipo(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/?q=&tipo__id__exact=42'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__filtro_termo(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/?pagamento__protocolo__termo__id__exact=17'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__registro(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/6096/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__patrimonio__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/patrimonio/6096/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__historico_local__lista(self):
        url = self.sistema_url + '/admin/patrimonio/historicolocal/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__historico_local__busca(self):
        url = self.sistema_url + '/admin/patrimonio/historicolocal/?q=monitor'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__historico_local__registro(self):
        url = self.sistema_url + '/admin/patrimonio/historicolocal/6758/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__historico_local__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/historicolocal/6758/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipo_equipamentos__lista(self):
        url = self.sistema_url + '/admin/patrimonio/tipoequipamento/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_equipamentos__registro(self):
        url = self.sistema_url + '/admin/patrimonio/tipoequipamento/31/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipo_equipamentos__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/tipoequipamento/31/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__tipos__lista(self):
        url = self.sistema_url + '/admin/patrimonio/tipo/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipos__registro(self):
        url = self.sistema_url + '/admin/patrimonio/tipo/44/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__tipos__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/tipo/44/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)

    def test__unidade_dimensao__lista(self):
        url = self.sistema_url + '/admin/patrimonio/unidadedimensao/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__unidade_dimensao__registro(self):
        url = self.sistema_url + '/admin/patrimonio/unidadedimensao/1/'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__unidade_dimensao__registro__save(self):
        url = self.sistema_url + '/admin/patrimonio/unidadedimensao/1/'
        self.browser.get(url)
        self.assertLoadPageAndSaveEdit(url)


class LogsTest(SeleniumServerTestCase):

    def setUp(self):
        super(LogsTest, self).setUp()

    def tearDown(self):
        super(LogsTest, self).tearDown()

    def test__relatorio_administrativos__registro_de_uso_do_sistema__filtro(self):
        url = self.sistema_url + '/logs'
        self.browser.get(url)
        self.assertLoadPage(url)

    def test__relatorio_administrativos__registro_de_uso_do_sistema__filtro_por_ano(self):
        url = self.sistema_url + '/logs?inicial=2008&final=2008'
        self.browser.get(url)
        self.assertLoadPage(url)
