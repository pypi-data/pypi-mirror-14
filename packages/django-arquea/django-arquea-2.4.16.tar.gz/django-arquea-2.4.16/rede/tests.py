# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.urlresolvers import reverse
from django.test import TestCase

from identificacao.models import ASN, Entidade
from rede.models import RIR, BlocoIP


class BlocoIPModelTest(TestCase):
    def setUp(self):
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN', nome='nome ANSP_ASN', cnpj='', fisco=True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")

        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP', nome='nome ANSP_PROP', cnpj='', fisco=True,
                                                        url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")

        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO', nome='nome ANSPP_DESIGNADO', cnpj='', fisco=True,
                                            url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO', nome='nome ANSP_USUARIO', cnpj='', fisco=True, url='')

        rir = RIR.objects.create(nome="RIR1")

        ipv4 = BlocoIP.objects.create(ip='192.168.1.0', mask='20',  # @UnusedVariable
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv4 - n1", transito=True)

        ipv6 = BlocoIP.objects.create(ip='2001:0db8::7344', mask='20',  # @UnusedVariable
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv6 - n1", transito=True)

    def test_unicode(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('192.168.1.0/20', p.__unicode__())

    def test_cidr(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('192.168.1.0/20', p.cidr())

    def test_netmask(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('255.255.240.0', p.netmask())

    def test_ipv4(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertTrue(p.is_IPV4())
        self.assertFalse(p.is_IPV6())

    def test_ipv6(self):
        p = BlocoIP.objects.get(ip='2001:0db8::7344')
        self.assertTrue(p.is_IPV6())
        self.assertFalse(p.is_IPV4())

    def test_AS(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual(1234, p.AS())

    def test_prop(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('ANSP_PROP', p.prop().entidade.sigla)

    def test_usu(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('ANSP_USUARIO', p.usu())

    def test_desig(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertEqual('ANSP_DESIGNADO', p.desig())

    def test_leaf(self):
        p = BlocoIP.objects.get(ip='192.168.1.0')
        self.assertTrue(p.leaf())

    def test_superbloco(self):
        asn_entidade = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_ASN', nome='nome ANSP_ASN', cnpj='', fisco=True,
                                               url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")

        proprietario_entidade = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_PROP', nome='nome ANSP_PROP', cnpj='',
                                                        fisco=True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")

        designado = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_DESIGNADO', nome='nome ANSPP_DESIGNADO', cnpj='',
                                            fisco=True, url='')
        usuario = Entidade.objects.create(sigla='SUPERBLOCO_ANSP_USUARIO', nome='nome ANSP_USUARIO', cnpj='',
                                          fisco=True, url='')

        rir = RIR.objects.create(nome="SUPERBLOCO_RIR1")

        ipv4_superbloco = BlocoIP.objects.create(ip='192.168.0.0', mask='20', asn=asn, proprietario=proprietario,
                                                 superbloco=None, designado=designado, usuario=usuario, rir=rir,
                                                 obs="OBS ipv4 - superbloco", transito=True)

        p = BlocoIP.objects.get(ip='192.168.1.0')
        p.superbloco = ipv4_superbloco
        p.save()

        ipv4_superbloco = BlocoIP.objects.get(ip='192.168.0.0')
        self.assertFalse(ipv4_superbloco.leaf())


class ViewPermissionDeniedTest(TestCase):
    """
    Teste das permissões das views. Utilizando um usuário sem permissão de superusuário.
    """
    fixtures = ['auth_user.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewPermissionDeniedTest, self).setUp()
        self.response = self.client.login(username='john', password='123456')

    def test_planejamento(self):
        url = reverse("rede.views.planejamento")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_planilha_informacoes_gerais(self):
        url = reverse("rede.views.planilha_informacoes_gerais")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_planejamento2(self):
        url = reverse("rede.views.planejamento2")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip(self):
        url = reverse("rede.views.blocosip")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_ansp(self):
        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_transito(self):
        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_inst_transito(self):
        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_blocosip_inst_ansp(self):
        url = reverse("rede.views.blocosip_inst_ansp")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_custo_terremark(self):
        url = reverse("rede.views.custo_terremark")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)

    def test_relatorio_recursos_operacional(self):
        url = reverse("rede.views.relatorio_recursos_operacional")
        response = self.client.get(url)
        self.assertContains(response, u'403 Forbidden', status_code=403)


class ViewBlocoIPTest(TestCase):

    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewBlocoIPTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpBlocoIP(self):
        # Registro 1
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN_1', nome='nome ANSP_ASN_1', cnpj='', fisco=True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")

        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP_1', nome='nome ANSP_PROP_1', cnpj='',
                                                        fisco=True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")

        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO_1', nome='nome ANSP_DESIGNADO_1', cnpj='', fisco=True,
                                            url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO_1', nome='nome ANSP_USUARIO_1', cnpj='', fisco=True,
                                          url='')

        rir = RIR.objects.create(nome="RIR_1")

        ipv4 = BlocoIP.objects.create(ip='192.168.1.0', mask='20',  # @UnusedVariable
                                      asn=asn, proprietario=proprietario, superbloco=None,
                                      designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv4 - n1", transito=True)
        # Registro 2
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN_2', nome='nome ANSP_ASN_2', cnpj='', fisco=True, url='')
        asn = ASN.objects.create(numero=1234, entidade=asn_entidade, pais="BR")

        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP_2', nome='nome ANSP_PROP_2', cnpj='',
                                                        fisco=True, url='')
        proprietario = ASN.objects.create(numero=4321, entidade=proprietario_entidade, pais="BR")

        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO_2', nome='nome ANSPP_DESIGNADO_2', cnpj='',
                                            fisco=True, url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO_2', nome='nome ANSP_USUARIO_2', cnpj='', fisco=True,
                                          url='')

        rir = RIR.objects.create(nome="RIR_2")

        ipv6 = BlocoIP.objects.create(ip='2001:0db8::7344', mask='20', asn=asn, proprietario=proprietario,  # @UnusedVariable
                                      superbloco=None, designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv6 - n1", transito=True)

    def _test_view__blocosip__breadcrumb(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<a href="/rede/relatorios/blocosip/">Lista de Blocos IP</a>')

    def _test_view__blocosip__filtros__cabecalhos(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<select name="anunciante" id="id_anunciante">')
        self.assertContains(response, u'<select name="proprietario" id="id_proprietario">')
        self.assertContains(response, u'<select name="usuario" id="id_usuario">')
        self.assertContains(response, u'<select name="designado" id="id_designado">')
        self.assertContains(response, u'<select name="designado" id="id_designado">')
        self.assertContains(response, u'<input type="checkbox" id="id_porusuario" name="porusuario">')

    def test_view__blocosip(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)

    def test_view__blocosip__resultado_sem_filtro(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0', 'usuario': '0', 'designado': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)

        # asssert dos dados do relatório. Verificação dos cabeçalhos das colunas.
        self.assertContains(response, u'<div class="colunas">AS anunciante</div>')
        self.assertContains(response, u'<div class="colunas">AS proprietário</div>')
        self.assertContains(response, u'<div class="colunas">Usado por</div>')
        self.assertContains(response, u'<div class="colunas">Designado para</div>')
        self.assertContains(response, u'<div class="colunas">RIR</div>')
        self.assertContains(response, u'<div class="obs">Obs</div>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'<div class="col1"><a href="%s"'
                            % reverse('admin:rede_blocoip_change', args=(1,)))
        self.assertContains(response, u'192.168.1.0/20')
        self.assertContains(response, u'<div class="colunas">1234 - ANSP_ASN_1</div>')
        self.assertContains(response, u'<div class="colunas">4321 - ANSP_PROP_1</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_USUARIO_1</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_DESIGNADO_1</div>')
        self.assertContains(response, u'<div class="colunas">RIR_1</div>')
        self.assertContains(response, u'<div class="obs">OBS ipv4 - n1</div>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'<div class="col1"><a href="%s"'
                            % reverse('admin:rede_blocoip_change', args=(2,)))
        self.assertContains(response, u'2001:db8::7344/20')
        self.assertContains(response, u'<div class="colunas">1234 - ANSP_ASN_2</div>')
        self.assertContains(response, u'<div class="colunas">4321 - ANSP_PROP_2</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_USUARIO_2</div>')
        self.assertContains(response, u'<div class="colunas">ANSP_DESIGNADO_2</div>')
        self.assertContains(response, u'<div class="colunas">RIR_2</div>')
        self.assertContains(response, u'<div class="obs">OBS ipv6 - n1</div>')

    def test_view__blocosip__filtro_anunciante(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por anunciante.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante': '1', 'proprietario': '0', 'usuario': '0', 'designado': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="1" selected>1234 - ANSP_ASN_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')

    def test_view__blocosip__filtro_proprietario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por proprietario.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '2', 'usuario': '0', 'designado': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="2" selected>4321 - ANSP_PROP_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')

    def test_view__blocosip__filtro_usuario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por usuario.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0', 'usuario': '4', 'designado': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="4" selected>ANSP_USUARIO_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')

    def test_view__blocosip__filtro_designado(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por designado.
        """
        self.setUpBlocoIP()

        url = reverse("rede.views.blocosip")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0', 'usuario': '0', 'designado': '3'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="3" selected>ANSP_DESIGNADO_1</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertNotContains(response, u'2001:db8::7344/20')


class ViewBlocoIPANSPTest(TestCase):

    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewBlocoIPANSPTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpBlocoIP_ANSP(self):
        # Registro 1
        entidade_ansp = Entidade.objects.create(sigla='ANSP', nome='nome ANSP_ASN_1', cnpj='', fisco=True, url='')

        asn = ASN.objects.create(numero=1234, entidade=entidade_ansp, pais="BR")
        proprietario = ASN.objects.create(numero=4321, entidade=entidade_ansp, pais="BR")
        designado = entidade_ansp
        usuario = entidade_ansp
        rir = RIR.objects.create(nome="RIR_1")

        ipv4_1 = BlocoIP.objects.create(ip='192.168.1.0', mask='20', asn=asn, proprietario=proprietario,
                                        superbloco=None, designado=designado, usuario=usuario, rir=rir,
                                        obs="OBS ipv4 - n1", transito=True)

        proprietario_2 = ASN.objects.create(numero=4322, entidade=entidade_ansp, pais="BR")

        ipv4_2 = BlocoIP.objects.create(ip='192.168.1.1', mask='20', asn=asn, proprietario=proprietario_2,  # @UnusedVariable
                                        superbloco=ipv4_1, designado=designado, usuario=usuario, rir=rir,
                                        obs="OBS ipv4 - n1_1", transito=True)

        # Registro 2
        asn_entidade = Entidade.objects.create(sigla='ANSP_ASN_2', nome='nome ANSP_ASN_2', cnpj='', fisco=True, url='')
        asn = ASN.objects.create(numero=12345, entidade=asn_entidade, pais="BR")

        proprietario_entidade = Entidade.objects.create(sigla='ANSP_PROP_2', nome='nome ANSP_PROP_2', cnpj='',
                                                        fisco=True, url='')
        proprietario = ASN.objects.create(numero=54321, entidade=proprietario_entidade, pais="BR")

        designado = Entidade.objects.create(sigla='ANSP_DESIGNADO_2', nome='nome ANSPP_DESIGNADO_2', cnpj='',
                                            fisco=True, url='')
        usuario = Entidade.objects.create(sigla='ANSP_USUARIO_2', nome='nome ANSP_USUARIO_2', cnpj='', fisco=True,
                                          url='')

        rir = RIR.objects.create(nome="RIR_2")

        ipv6 = BlocoIP.objects.create(ip='2001:0db8::7344', mask='20', asn=asn, proprietario=proprietario,  # @UnusedVariable
                                      superbloco=None, designado=designado, usuario=usuario, rir=rir,
                                      obs="OBS ipv6 - n1", transito=True)

    def _test_view__blocosip_ansp__breadcrumb(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<a href="/rede/relatorios/blocosip_ansp/">Lista de Blocos IP - Blocos ANSP</a>')

    def _test_view__blocosip_ansp__filtros__cabecalhos(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<select name="anunciante" id="id_anunciante">')
        self.assertContains(response, u'<select name="proprietario" id="id_proprietario">')

    def test_view__blocosip_ansp(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_ANSP()

        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_ansp__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_ansp__filtros__cabecalhos(response)

    def test_view__blocosip_ansp__resultado_sem_filtro(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_ANSP()

        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_ansp__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_ansp__filtros__cabecalhos(response)

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'<h4>Bloco <a href="%s" >192.168.1.0/20 - 255.255.240.0</a></h4>'
                            % reverse('admin:rede_blocoip_change', args=(1,)))
        self.assertContains(response, u'<td class="col1 td_titulo">Prefixo</td>')
        self.assertContains(response, u'<td class="colunas td_titulo">Máscara IP</td>')
        self.assertContains(response, u'<td class="colunas td_titulo">ASN Anunciante</td>')
        self.assertContains(response, u'<td class="colunas td_titulo">Usuário</td>')
        self.assertContains(response, u'<td class="obs td_titulo">Obs</td>')

        self.assertContains(response, u'<td class="col1"><a href="%s">192.168.1.1/20</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(2,)))
        self.assertContains(response, u'<td class="colunas">255.255.240.0</td>')
        self.assertContains(response, u'<td class="colunas">1234</td>')
        self.assertContains(response, u'<td class="colunas">ANSP</td>')
        self.assertContains(response, u'<td class="obs">OBS ipv4 - n1_1</td>')

    def test_view__blocosip_ansp__filtro_anunciante(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por anunciante.
        """
        self.setUpBlocoIP_ANSP()

        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url, {'anunciante': '1', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_ansp__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_ansp__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="1" selected>1234 - ANSP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertContains(response, u'192.168.1.1/20')
        self.assertNotContains(response, u'2001:db8::7344/20')

    def test_view__blocosip_ansp__filtro_proprietario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por proprietario.
        """
        self.setUpBlocoIP_ANSP()

        url = reverse("rede.views.blocosip_ansp")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '3', 'usuario': '0', 'designado': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_ansp__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_ansp__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="3" selected>4322 - ANSP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'192.168.1.0/20')
        self.assertContains(response, u'192.168.1.1/20')
        self.assertNotContains(response, u'2001:db8::7344/20')


class ViewBlocoIPTransitoTest(TestCase):

    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewBlocoIPTransitoTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpBlocoIP_Transito(self):
        rir = RIR.objects.create(nome="RIR_1")

        # Registro 1
        entidade_uninove = Entidade.objects.create(sigla='UNINOVE', nome='', cnpj='', fisco=True, url='')
        asn_uninove = ASN.objects.create(numero=52914, entidade=entidade_uninove, pais="BR")
        ipv4_uninove = BlocoIP.objects.create(ip='186.251.39.0', mask='24', asn=asn_uninove, proprietario=asn_uninove,  # @UnusedVariable
                                              superbloco=None, designado=entidade_uninove, usuario=entidade_uninove,
                                              rir=rir, obs="", transito=True)

        # Registro 2
        entidade_unicamp = Entidade.objects.create(sigla='UNICAMP', nome='', cnpj='', fisco=True, url='')
        asn_unicamp = ASN.objects.create(numero=53187, entidade=entidade_unicamp, pais="BR")
        ipv4_unicamp1 = BlocoIP.objects.create(ip='143.106.0.0', mask='16', asn=asn_unicamp, proprietario=asn_unicamp,  # @UnusedVariable
                                               superbloco=None, designado=entidade_unicamp, usuario=entidade_unicamp,
                                               rir=rir, obs="", transito=True)

        # Registro 3
        ipv4_unicamp2 = BlocoIP.objects.create(ip='177.8.96.0', mask='20', asn=asn_unicamp, proprietario=asn_unicamp,  # @UnusedVariable
                                               superbloco=None, designado=entidade_unicamp, usuario=entidade_unicamp,
                                               rir=rir, obs="", transito=True)

        # Registro 4
        entidade_unesp = Entidade.objects.create(sigla='UNESP', nome='', cnpj='', fisco=True, url='')
        asn_unesp = ASN.objects.create(numero=53166, entidade=entidade_unesp, pais="BR")
        ipv4_unesp = BlocoIP.objects.create(ip='186.217.0.0', mask='16', asn=asn_unesp, proprietario=asn_unesp,  # @UnusedVariable
                                            superbloco=None, designado=entidade_unesp, usuario=entidade_unesp,
                                            rir=rir, obs="", transito=True)

        # Registro 5
        entidade_inpe = Entidade.objects.create(sigla='INPE', nome='', cnpj='', fisco=True, url='')
        asn_inpe = ASN.objects.create(numero=53166, entidade=entidade_inpe, pais="BR")
        ipv4_unesp = BlocoIP.objects.create(ip='150.163.0.0', mask='17', asn=asn_inpe, proprietario=asn_inpe,  # @UnusedVariable
                                            superbloco=None, designado=entidade_inpe, usuario=entidade_inpe,
                                            rir=rir, obs="", transito=True)

    def _test_view__blocosip_transito__breadcrumb(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<a href="/rede/relatorios/blocosip_transito/">'
                                      u'Lista de Blocos IP - Trânsito</a>')

    def _test_view__blocosip_transito__filtros__cabecalhos(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<select name="anunciante" id="id_anunciante">')
        self.assertContains(response, u'<select name="proprietario" id="id_proprietario">')

    def test_view__blocosip_transito(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_Transito()

        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_transito__filtros__cabecalhos(response)

    def test_view__blocosip_transito__resultado_sem_filtro(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_Transito()

        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_transito__filtros__cabecalhos(response)

        # asssert dos dados do relatório. Verificação dos cabeçalhos dos dados
        self.assertContains(response, u'<h1>Blocos IP - Trânsito</h1>')
        self.assertContains(response, u'<th class="colunas">Bloco IP</th>')
        self.assertContains(response, u'<th class="colunas">Máscara IP</th>')
        self.assertContains(response, u'<th class="colunas">ASN Anunciante</th>')
        self.assertContains(response, u'<th class="colunas">Anunciante</th>')
        self.assertContains(response, u'<th class="colunas">ASN Proprietário</th>')
        self.assertContains(response, u'<th class="colunas">Proprietário</th>')
        self.assertContains(response, u'<th class="obs">Obs</th>')

        self.assertContains(response, u'<td id="td_blocos_1_col1" class="col1"><a href="%s" >143.106.0.0/16</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(2,)))
        self.assertContains(response, u'<td id="td_blocos_1_col2" class="colunas">255.255.0.0</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col3" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col4" class="colunas">UNICAMP</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col5" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col6" class="colunas">UNICAMP</td>')

        self.assertContains(response, u'<td id="td_blocos_2_col1" class="col1"><a href="%s" >150.163.0.0/17</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(5,)))
        self.assertContains(response, u'<td id="td_blocos_2_col2" class="colunas">255.255.128.0</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col3" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col4" class="colunas">INPE</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col5" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col6" class="colunas">INPE</td>')

        self.assertContains(response, u'<td id="td_blocos_3_col1" class="col1"><a href="%s" >177.8.96.0/20</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(3,)))
        self.assertContains(response, u'<td id="td_blocos_3_col2" class="colunas">255.255.240.0</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col3" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col4" class="colunas">UNICAMP</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col5" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col6" class="colunas">UNICAMP</td>')

        self.assertContains(response, u'<td id="td_blocos_4_col1" class="col1"><a href="%s" >186.217.0.0/16</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(4,)))
        self.assertContains(response, u'<td id="td_blocos_4_col2" class="colunas">255.255.0.0</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col3" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col4" class="colunas">UNESP</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col5" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col6" class="colunas">UNESP</td>')

        self.assertContains(response, u'<td id="td_blocos_5_col1" class="col1"><a href="%s" >186.251.39.0/24</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(1,)))
        self.assertContains(response, u'<td id="td_blocos_5_col2" class="colunas">255.255.255.0</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col3" class="colunas">52914</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col4" class="colunas">UNINOVE</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col5" class="colunas">52914</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col6" class="colunas">UNINOVE</td>')

    def test_view__blocosip_transito__filtro_anunciante(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por anunciante.
        """
        self.setUpBlocoIP_Transito()

        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url, {'anunciante': '2', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_transito__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="2" selected>53187 - UNICAMP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'143.106.0.0/16')
        self.assertContains(response, u'177.8.96.0/20')
        self.assertNotContains(response, u'186.251.39.0')
        self.assertNotContains(response, u'186.217.0.0')
        self.assertNotContains(response, u'150.163.0.0')

    def test_view__blocosip_transito__filtro_proprietario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por proprietario.
        """
        self.setUpBlocoIP_Transito()

        url = reverse("rede.views.blocosip_transito")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '3'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_transito__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="3" selected>53166 - UNESP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'186.217.0.0')
        self.assertNotContains(response, u'143.106.0.0/16')
        self.assertNotContains(response, u'177.8.96.0/20')
        self.assertNotContains(response, u'186.251.39.0')
        self.assertNotContains(response, u'150.163.0.0')


class ViewBlocoIPInstTransitoTest(TestCase):

    # Fixture para carregar dados de autenticação de usuário
    fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml']

    def setUp(self):
        super(ViewBlocoIPInstTransitoTest, self).setUp()
        # Comando de login para passar pelo decorator @login_required
        self.response = self.client.login(username='john', password='123456')

    def setUpBlocoIP_InstTransito(self):
        rir = RIR.objects.create(nome="RIR_1")

        # Registro 1
        entidade_uninove = Entidade.objects.create(sigla='UNINOVE', nome='', cnpj='', fisco=True, url='')
        asn_uninove = ASN.objects.create(numero=52914, entidade=entidade_uninove, pais="BR")
        ipv4_uninove = BlocoIP.objects.create(ip='186.251.39.0', mask='24', asn=asn_uninove, proprietario=asn_uninove,  # @UnusedVariable
                                              superbloco=None, designado=entidade_uninove, usuario=entidade_uninove,
                                              rir=rir, obs="", transito=True)

        # Registro 2
        entidade_unicamp = Entidade.objects.create(sigla='UNICAMP', nome='', cnpj='', fisco=True, url='')
        asn_unicamp = ASN.objects.create(numero=53187, entidade=entidade_unicamp, pais="BR")
        ipv4_unicamp1 = BlocoIP.objects.create(ip='143.106.0.0', mask='16', asn=asn_unicamp, proprietario=asn_unicamp,  # @UnusedVariable
                                               superbloco=None, designado=entidade_unicamp, usuario=entidade_unicamp,
                                               rir=rir, obs="", transito=True)
        # Registro 3
        ipv4_unicamp2 = BlocoIP.objects.create(ip='177.8.96.0', mask='20', asn=asn_unicamp, proprietario=asn_unicamp,  # @UnusedVariable
                                               superbloco=None, designado=entidade_unicamp, usuario=entidade_unicamp,
                                               rir=rir, obs="", transito=True)

        # Registro 4
        entidade_unesp = Entidade.objects.create(sigla='UNESP', nome='', cnpj='', fisco=True, url='')
        asn_unesp = ASN.objects.create(numero=53166, entidade=entidade_unesp, pais="BR")
        ipv4_unesp = BlocoIP.objects.create(ip='186.217.0.0', mask='16', asn=asn_unesp, proprietario=asn_unesp,  # @UnusedVariable
                                            superbloco=None, designado=entidade_unesp, usuario=entidade_unesp, rir=rir,
                                            obs="", transito=True)

        # Registro 5
        entidade_inpe = Entidade.objects.create(sigla='INPE', nome='', cnpj='', fisco=True, url='')
        asn_inpe = ASN.objects.create(numero=53166, entidade=entidade_inpe, pais="BR")
        ipv4_unesp = BlocoIP.objects.create(ip='150.163.0.0', mask='17', asn=asn_inpe, proprietario=asn_inpe,  # @UnusedVariable
                                            superbloco=None, designado=entidade_inpe, usuario=entidade_inpe, rir=rir,
                                            obs="", transito=True)

    def _test_view__blocosip_inst_transito__breadcrumb(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<a href="/rede/relatorios/blocosip_inst_transito/">'
                                      u'Lista de Blocos IP - Instituição Trânsito</a>')

    def _test_view__blocosip_inst_transito__filtros__cabecalhos(self, response):
        # assert breadcrumb
        self.assertContains(response, u'<select name="anunciante" id="id_anunciante">')
        self.assertContains(response, u'<select name="proprietario" id="id_proprietario">')

    def test_view__blocosip_inst_transito(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_InstTransito()

        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url, {})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_inst_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_inst_transito__filtros__cabecalhos(response)

    def test_view__blocosip_inst_transito__resultado_sem_filtro(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica.
        """
        self.setUpBlocoIP_InstTransito()

        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_inst_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_inst_transito__filtros__cabecalhos(response)

        # asssert dos dados do relatório. Verificação dos cabeçalhos dos dados
        self.assertContains(response, u'<h1>Blocos IP - Instituições Trânsito</h1>')
        self.assertContains(response, u'<th class="colunas">ASN Proprietário</th>')
        self.assertContains(response, u'<th class="colunas">Proprietário</th>')
        self.assertContains(response, u'<th class="colunas">Bloco IP</th>')
        self.assertContains(response, u'<th class="colunas">Máscara IP</th>')
        self.assertContains(response, u'<th class="colunas">ASN Anunciante</th>')
        self.assertContains(response, u'<th class="colunas">Anunciante</th>')
        self.assertContains(response, u'<th class="obs">Obs</th>')

        self.assertContains(response, u'<td id="td_blocos_1_col1" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col2" class="colunas">INPE</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col3" class="col1"><a href="%s" >150.163.0.0/17</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(5,)))
        self.assertContains(response, u'<td id="td_blocos_1_col4" class="colunas">255.255.128.0</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col5" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_1_col6" class="colunas">INPE</td>')

        self.assertContains(response, u'<td id="td_blocos_2_col1" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col2" class="colunas">UNESP</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col3" class="col1"><a href="%s" >186.217.0.0/16</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(4,)))
        self.assertContains(response, u'<td id="td_blocos_2_col4" class="colunas">255.255.0.0</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col5" class="colunas">53166</td>')
        self.assertContains(response, u'<td id="td_blocos_2_col6" class="colunas">UNESP</td>')

        self.assertContains(response, u'<td id="td_blocos_3_col1" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col2" class="colunas">UNICAMP</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col3" class="col1"><a href="%s" >143.106.0.0/16</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(2,)))
        self.assertContains(response, u'<td id="td_blocos_3_col4" class="colunas">255.255.0.0</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col5" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_3_col6" class="colunas">UNICAMP</td>')

        self.assertContains(response, u'<td id="td_blocos_4_col1" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col2" class="colunas">UNICAMP</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col3" class="col1"><a href="%s" >177.8.96.0/20</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(3,)))
        self.assertContains(response, u'<td id="td_blocos_4_col4" class="colunas">255.255.240.0</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col5" class="colunas">53187</td>')
        self.assertContains(response, u'<td id="td_blocos_4_col6" class="colunas">UNICAMP</td>')

        self.assertContains(response, u'<td id="td_blocos_5_col1" class="colunas">52914</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col2" class="colunas">UNINOVE</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col3" class="col1"><a href="%s" >186.251.39.0/24</a></td>'
                            % reverse('admin:rede_blocoip_change', args=(1,)))
        self.assertContains(response, u'<td id="td_blocos_5_col4" class="colunas">255.255.255.0</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col5" class="colunas">52914</td>')
        self.assertContains(response, u'<td id="td_blocos_5_col6" class="colunas">UNINOVE</td>')

    def test_view__blocosip_inst_transito__filtro_anunciante(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por anunciante.
        """
        self.setUpBlocoIP_InstTransito()

        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url, {'anunciante': '2', 'proprietario': '0'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_inst_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_inst_transito__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="2" selected>53187 - UNICAMP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'143.106.0.0/16')
        self.assertContains(response, u'177.8.96.0/20')
        self.assertNotContains(response, u'186.251.39.0')
        self.assertNotContains(response, u'186.217.0.0')
        self.assertNotContains(response, u'150.163.0.0')

    def test_view__blocosip_inst_transito__filtro_proprietario(self):
        """
        View do relatório de Blocos IP, com visão de árvore hierárquica. Filtro por proprietario.
        """
        self.setUpBlocoIP_InstTransito()

        url = reverse("rede.views.blocosip_inst_transito")
        response = self.client.get(url, {'anunciante': '0', 'proprietario': '3'})

        self.assertEqual(200, response.status_code)

        # assert breadcrumb
        self._test_view__blocosip_inst_transito__breadcrumb(response)

        # asssert dos filtros
        self._test_view__blocosip_inst_transito__filtros__cabecalhos(response)
        self.assertContains(response, u'<option value="3" selected>53166 - UNESP</option>')

        # asssert dos dados do relatório. Verificação dos dados
        self.assertContains(response, u'186.217.0.0')
        self.assertNotContains(response, u'143.106.0.0/16')
        self.assertNotContains(response, u'177.8.96.0/20')
        self.assertNotContains(response, u'186.251.39.0')
        self.assertNotContains(response, u'150.163.0.0')


# class ViewCrossConnectionTest(TestCase):
#
#     # Fixture para carregar dados de autenticação de usuário
#     fixtures = ['auth_user_superuser.yaml', 'initial_data.yaml',]
#
#     def setUp(self):
#         super(ViewCrossConnectionTest, self).setUp()
#         # Comando de login para passar pelo decorator @login_required
#         self.response = self.client.login(username='john', password='123456')
#
#     def setUpCrossConnection(self):
#         ent= Entidade.objects.create(sigla='TERREMARK', nome='', cnpj='', fisco=True, url='')
#         end = Endereco.objects.create(entidade=ent, rua='', num=215, bairro='', cep='', estado='', pais='')
#         tipoDetalhe = TipoDetalhe.objects.create(nome='Rack')
#         rack1 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.CP073",
# mostra_bayface=True)
#         rack2 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S039",
# mostra_bayface=True)
#         rack3 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S040",
# mostra_bayface=True)
#         rack4 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S041",
#  mostra_bayface=True)
#         rack5 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S042",
#  mostra_bayface=True)
#         rack6 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S043",
#  mostra_bayface=True)
#         rack7 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S044",
#  mostra_bayface=True)
#         rack8 = EnderecoDetalhe.objects.create(endereco=end, tipo=tipoDetalhe, complemento="NAPSAO.01.S045",
#  mostra_bayface=True)
#
#         t1 = TipoConector.objects.create(sigla='RJ45', obs='',)
#         origem = IFCConector.objects.create(rack=rack1, shelf='shelf1', porta='1-2', tipoConector=t1, ativo=True,
#  obs='')
#         destino = IFCConector.objects.create(rack=rack2, shelf='shelf2', porta='3-4', tipoConector=t1, ativo=True,
# obs='')
#         cross = CrossConnection.objects.create(origem=origem, destino=destino, circuito='CIRCUITO1',
# ordemDeServico='OS1', obs='', ativo=True)
#
#         t2 = TipoConector.objects.create(sigla='PC SM', obs='',)
#         origem = IFCConector.objects.create(rack=rack3, shelf='shelf3', porta='1-2', tipoConector=t2, ativo=True,
# obs='')
#         destino = IFCConector.objects.create(rack=rack4, shelf='shelf4', porta='3-4', tipoConector=t2, ativo=True,
# obs='')
#         cross = CrossConnection.objects.create(origem=origem, destino=destino, circuito='CIRCUITO2',
# ordemDeServico='OS2', obs='', ativo=True)
#
#         origem = IFCConector.objects.create(rack=rack5, shelf='shelf5', porta='1-2', tipoConector=t2, ativo=True,
#  obs='')
#         destino = IFCConector.objects.create(rack=rack6, shelf='shelf6', porta='3-4', tipoConector=t2, ativo=True,
# obs='')
#         cross = CrossConnection.objects.create(origem=origem, destino=destino, circuito='CIRCUITO3',
#  ordemDeServico='OS3', obs='', ativo=True)
#
#         t3 = TipoConector.objects.create(sigla='PC MM', obs='',)
#         origem = IFCConector.objects.create(rack=rack7, shelf='shelf7', porta='1-2', tipoConector=t3, ativo=True,
# obs='')
#         destino = IFCConector.objects.create(rack=rack8, shelf='shelf8', porta='3-4', tipoConector=t3, ativo=True,
# obs='')
#         cross = CrossConnection.objects.create(origem=origem, destino=destino, circuito='CIRCUITO4',
# ordemDeServico='OS3', obs='', ativo=True)
#
#
#     def _test_view__cross_connection__breadcrumb(self, response):
#         # assert breadcrumb
#         self.assertContains(response, u'<a href="/rede/relatorios/crossconnection/">Lista de Cross Conexões</a>')
#
#
#     def _test_view__cross_connection__filtros__cabecalhos(self, response):
#         # assert breadcrumb
#         self.assertContains(response, u'<select name="rack" id="id_rack">')
#         self.assertContains(response, u'<select name="shelf" id="id_shelf">')
#         self.assertContains(response, u'<select name="conector" id="id_conector">')
#         self.assertContains(response, u'<select name="projeto" id="id_projeto">')
#
#
#     def test_view__cross_connection(self):
#         """
#         View do relatório de Blocos IP, com visão de árvore hierárquica.
#         """
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#
#     def test_view__cross_connection__resultado_sem_filtro(self):
#         """
#         View do relatório de Blocos IP, com visão de árvore hierárquica.
#         """
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {'rack':'0', 'shelf':'0', 'conector':'0', 'projeto':'0'})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#         # asssert dos dados do relatório. Verificação dos cabeçalhos dos dados
#         self.assertContains(response, u'<h1>Cross Conexões</h1>')
#
#         self.assertContains(response, u'<td class="col1 td_titulo">Rack 1</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Shelf</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Porta</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Conector</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Rack 2</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Shelf</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Porta</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Conector</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">Circuito</td>')
#         self.assertContains(response, u'<td class="colunas td_titulo">OS/Projeto</td>')
#         self.assertContains(response, u'<td class="obs td_titulo">Obs</td>')
#
#         self.assertContains(response, u'<td id="td_blocos_1_col1" class="">rack1</td>')
#         self.assertContains(response, u'<td id="td_blocos_1_col5" class="">rack2</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col1" class="">rack3</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col5" class="">rack4</td>')
#         self.assertContains(response, u'<td id="td_blocos_3_col1" class="">rack5</td>')
#         self.assertContains(response, u'<td id="td_blocos_3_col5" class="">rack6</td>')
#         self.assertContains(response, u'<td id="td_blocos_4_col1" class="">rack7</td>')
#         self.assertContains(response, u'<td id="td_blocos_4_col5" class="">rack8</td>')
#
#
#     def test_view__crossconnection__filtro_rack(self):
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {'rack':'rack1', 'shelf':'0', 'conector':'0', 'projeto':'0'})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#
#         # asssert dos dados do relatório. Verificação dos dados
#         self.assertContains(response, u'<td id="td_blocos_1_col1" class="">rack1</td>')
#         self.assertContains(response, u'<td id="td_blocos_1_col5" class="">rack2</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack3</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack4</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack5</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack6</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack7</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack8</td>')
#
#
#     def test_view__crossconnection__filtro_rack_shelf(self):
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {'rack':'rack1', 'shelf':'shelf1', 'conector':'0', 'projeto':'0'})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#
#         # asssert dos dados do relatório. Verificação dos dados
#         self.assertContains(response, u'<td id="td_blocos_1_col1" class="">rack1</td>')
#         self.assertContains(response, u'<td id="td_blocos_1_col5" class="">rack2</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack3</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack4</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack5</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack6</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col1" class="">rack7</td>')
#         self.assertNotContains(response, u'<td id="td_blocos_1_col5" class="">rack8</td>')
#
#
#     def test_view__crossconnection__filtro_conector(self):
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {'rack':'0', 'shelf':'0', 'conector':'PC SM', 'projeto':'0'})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#         # asssert dos dados do relatório. Verificação dos dados
#         self.assertContains(response, u'<td id="td_blocos_1_col1" class="">rack3</td>')
#         self.assertContains(response, u'<td id="td_blocos_1_col5" class="">rack4</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col1" class="">rack5</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col5" class="">rack6</td>')
#
#
#     def test_view__crossconnection__filtro_projeto(self):
#         self.setUpCrossConnection()
#
#         url = reverse("rede.views.crossconnection")
#         response = self.client.get(url, {'rack':'0', 'shelf':'0', 'conector':'0', 'projeto':'OS3'})
#
#         self.assertEqual(200, response.status_code)
#
#         # assert breadcrumb
#         self._test_view__cross_connection__breadcrumb(response)
#
#         # asssert dos filtros
#         self._test_view__cross_connection__filtros__cabecalhos(response)
#
#         # asssert dos dados do relatório. Verificação dos dados
#         print response.content
#         self.assertContains(response, u'<td id="td_blocos_1_col1" class="">rack5</td>')
#         self.assertContains(response, u'<td id="td_blocos_1_col5" class="">rack6</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col1" class="">rack7</td>')
#         self.assertContains(response, u'<td id="td_blocos_2_col5" class="">rack8</td>')
#
