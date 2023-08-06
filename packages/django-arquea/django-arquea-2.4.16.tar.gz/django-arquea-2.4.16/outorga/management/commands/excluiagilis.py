# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib2
import urllib
import cookielib
from django.core.management.base import BaseCommand, CommandError
from outorga.models import Termo
import time
import re
import getpass

TIPOS = {'STB': 'STC',
         'DET': 'STR',
         'MCN': 'MCS',
         'MPN': 'MPE',
         'DIA': 'MNT',
         'REL': 'REL'}

mods = ['STB', 'DET', 'MCN', 'MPN', 'REL', 'DIA']


class Command(BaseCommand):
    args = '<processo parcial usuario>'
    help = u'Envia as informações de prestação de contas para o sistema Agilis'

    def handle(self, *args, **options):
        if len(args) < 3:
            raise CommandError(u'Parâmetros faltando')

        try:
            parcial = int(args[1])
        except ValueError:
            raise CommandError(u'Parcial deve ser inteiro')

        try:
            (ano, numero, digito) = re.findall(r"[\d]+", args[0])
        except ValueError:
            raise CommandError(u'Processo deve ter o fomato aa/nnnnn-d')

        try:
            termo = Termo.objects.get(processo=numero, digito=digito)
        except Termo.DoesNotExist:
            raise CommandError(u'Processo %s não existe' % args[0])

        password = getpass.getpass(prompt="Entre com a senha do agilis:")

        # Com o Cookie Jar, os cookies são recebidos e enviados a cada requisição, fazendo com que a sessão seja mantida
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        # Faz o login e acessa páginas intermediárias necessárias
        urllib2.install_opener(opener)
        data = urllib.urlencode([('username', args[2]), ('password', password)])
        req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
        urllib2.urlopen(req)
        urllib2.urlopen('http://internet.aquila.fapesp.br/agilis/Solicitacao.do?'
                        'method=prepararAcao&processo=%s&redirectPC=redirectPC' % args[0])
        urllib2.urlopen('http://internet.aquila.fapesp.br/agilis/Pconline.do?'
                        'method=iniciar&solicitacao=49&processo=%s' % args[0])

        vezes = 0
        for m in mods:

            params = [('processo', args[0]), ('parcial', parcial), ('Prosseguir', 'Prosseguir')]
            if m == 'REL':
                params += [('tipoPrestacao', 'REL')]
            else:
                params += [('tipoPrestacao', 'PRN'), ('tipoDespesa', TIPOS[m])]
            data = urllib.urlencode(params)
            req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar',
                                  data=data)
            p = urllib2.urlopen(req)

            data = urllib.urlencode([('method', 'Excluir')])
            req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineResumo.do', data=data)
            p2 = urllib2.urlopen(req)

            txt = p2.read()
            x = txt.split('<a href="PconlineResumo.do?id=')
            for t in x[1:]:
                (n, lixo) = t.split('method=Excluir">')
                r = n.split('&')
                n = r[0]

                if m == 'REL':
                    tp = 'Vld'
                elif m == 'MPN':
                    tp = 'Mpe'
                else:
                    tp = 'Oud'
                req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineExclui%s.do?'
                                          'method=Excluir&id=%s' % (tp, n))
                p3 = urllib2.urlopen(req)
                vezes += 1
                if vezes % 10 == 0:
                    print ('Esperando...')
                    time.sleep(60)
