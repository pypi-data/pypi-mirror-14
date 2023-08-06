# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib2
import urllib
import cookielib
from django.core.management.base import BaseCommand, CommandError
from financeiro.models import *
from outorga.models import Termo
import time
import re
import getpass


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

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        urllib2.install_opener(opener)
        data = urllib.urlencode([('username', args[2]), ('password', password)])
        req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/Login.do', data=data)
        urllib2.urlopen(req)
        urllib2.urlopen('http://internet.aquila.fapesp.br/agilis/Solicitacao.do?'
                        'method=prepararAcao&processo=%s&redirectPC=redirectPC' % args[0])
        urllib2.urlopen('http://internet.aquila.fapesp.br/agilis/Pconline.do?'
                        'method=iniciar&solicitacao=49&processo=%s' % args[0])

        financeiros = ExtratoFinanceiro.objects.filter(termo=termo, parcial=parcial)

        data = urllib.urlencode([('processo', args[0]), ('parcial', parcial), ('tipoPrestacao', 'REL'),
                                 ('Prosseguir', 'Prosseguir')])
        req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar',
                              data=data)
        resp = urllib2.urlopen(req)

        dt = []
        for f in financeiros:
            valor = f.valor
            if valor < Decimal('0.0'):
                valor = -valor
            try:
                inte, dec = str(valor).split('.')
            except:
                inte = str(valor)
                dec = 0

            if f.cod == 'PGMP' or f.cod == 'PGRP':
                codigo = 'L'
            else:
                codigo = 'D'

            dt += [('dataOperacao', f.data_libera.strftime('%d/%m/%Y')), ('operacao', codigo),
                   ('valorOperacao', '%s,%s' % (inte, dec))]

        for k in range(0, 8):
            dt += [('dataOperacao', ''), ('operacao', ''), ('valorOperacao', '')]

        i = 0
        while i < financeiros.count():
            data = urllib.urlencode(dt[3*i:3*i+27]+[('method', 'Incluir')])
            req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiVld.do?method=Incluir',
                                  data=data)
            p2 = urllib2.urlopen(req)
            time.sleep(60)
            i += 9
