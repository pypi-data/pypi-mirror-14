# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#@PydevCodeAnalysisIgnore

# from django.test import LiveServerTestCase
from django_selenium.testcases import SeleniumTestCase
from django.conf import settings
from selenium import webdriver, selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SeleniumServerTestCase(SeleniumTestCase):
    """
    Classe para utilização em testes de Selenium.
    Possui setup para conectar em um Selenium Server, e fazer login no Sistema via CAS.

A configuração deve ser feita no settings-selenium

    Exemplo:
        class HomeTest(SeleniumServerTestCase):

            def setUp(self):
                super(HomeTest, self).setUp()

            def tearDown(self):
                super(HomeTest, self).tearDown()

            def test_controle_500(self):
                req = self.browser.get(self.sistema_url + '/pagina/')
                self.assertTrue(self.is_http_500(), u'Requisicao retornou HTTP (500)')
                self.assertFalse(self.is_http_404(), u'Requisicao retornou HTTP (404)')

                #get html contet
                #browser.page_source
    """
    def __init__(self, *args, **kwargs):
        SeleniumTestCase.__init__(self, *args, **kwargs)

    @classmethod
    def setUpClass(cls):
        # Only display possible problems
        selenium_logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARNING)

        # configura a url do sistema que vai ser testada
        cls.sistema_url = 'http://' + settings.SELENIUM_SISTEMA_HOST + ''

        # iniciando conexão com o Selenium Server no modo HTMLUNIT
        # server_url = "http://%s:%s/wd/hub" % (settings.SELENIUM_HOST , settings.SELENIUM_PORT)
        # dc = DesiredCapabilities.HTMLUNITWITHJS
        # options = webdriver.ChromeOptions()
        # cls.browser = webdriver.Remote(server_url, dc)

        # iniciando conexão com o Selenium Server no modo FIREFOX
        server_url = "http://%s:%d/wd/hub" % (settings.SELENIUM_HOST, settings.SELENIUM_PORT)
        fp = webdriver.FirefoxProfile()
        cls.browser = webdriver.Remote(server_url, desired_capabilities=webdriver.DesiredCapabilities.FIREFOX, browser_profile=fp)
        cls.login()

    @classmethod
    def tearDownClass(cls):
        cls.logout()
        cls.browser.quit()

    @classmethod
    def login(cls):
        """
        Faz o handshake com o CAS para fazer o login no Sistema
        """
        _request = cls.browser.get('https://cas.ansp.br/cas/login?service=http%3A%2F%2F' +
                                   settings.SELENIUM_SISTEMA_HOST + '%2Faccounts%2Flogin%2F%3Fnext%3D%252Fadmin%252F')

        # She sees the familiar 'Django administration' heading
        cls.browser.find_element_by_tag_name('body')

        cls.browser.find_element_by_id("id_username").send_keys(settings.SELENIUM_SISTEMA_USERNAME)
        cls.browser.find_element_by_id("id_password").send_keys(settings.SELENIUM_SISTEMA_PASS)

        cls.browser.find_element_by_id("login-form").submit()

    @classmethod
    def logout(cls):
        cls.browser.get('http://' + settings.SELENIUM_SISTEMA_HOST + '/accounts/logout/')

    def is_http_404(self):
        elemHeader = None

        try:
            # DESENVOLVIMENTO
            elemHeader = self.browser.find_element_by_css_selector('div#summary h1')
        except:
            try:
                # PRODUCAO
                elemHeader = self.browser.find_element_by_css_selector('div#content.colM h2')
            except:
                print

        # Teste de 404 para ambientes de desenvolvimento
        if elemHeader and elemHeader.text.find('Page not found') >= 0:
            return True
        # Teste de 404 para ambientes de produção
        elif elemHeader and elemHeader.text.find(u"não existe no sistema.") >= 0:
            return True

    def is_http_500(self):
        elemHeaderDesenv = None
        elemHeaderProd = None

        try:
            # DESENVOLVIMENTO
            elemHeaderDesenv = self.browser.find_element_by_css_selector('div#traceback')
        except:
            try:
                # PRODUCAO
                elemHeaderProd = self.browser.find_element_by_css_selector('div#content.colM')
            except:
                print

        # Teste de 500 para ambientes de desenvolvimento
        if elemHeaderDesenv:
            return True
        # Teste de 500 para ambientes de produção
        elif elemHeaderProd and elemHeaderProd.text.find('Ocorreu um erro no sistema') >= 0:
            return True

    def is_http_403(self):
        return(u"403 Forbidden" in self.browser.page_source)

    def assertLoadPage(self, url):
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)' % url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)' % url)
        self.assertFalse(self.is_http_403(), u'Requisicao %s retornou HTTP (403) Forbidden' % url)

    def assertLoadPageAndSaveEdit(self, url):
        btnSaveEdit = self.browser.find_element_by_name('_continue')
        btnSaveEdit.click()
        self.assertFalse(self.is_http_404(), u'Requisicao %s retornou HTTP (404)' % url)
        self.assertFalse(self.is_http_500(), u'Requisicao %s retornou HTTP (500)' % url)
        self.assertTrue(u"modificado com sucesso. Você pode editá-lo novamente abaixo" in self.browser.page_source,
                        'Falha ao identificar mensagem de modificado com sucesso. url=%s' % url)

