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
from protocolo.models import Protocolo, Estado as EstadoP
import time
import re
import getpass

TIPOS = {'STB': 'STC',
         'DET': 'STR',
         'MCN': 'MCS',
         'STB_OUT': 'STC',
         'DIA': 'MNT'}


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

        pagamentos = Pagamento.objects.filter(protocolo__termo=termo)
        pagtos = pagamentos

        for p in pagamentos:
            if p.auditoria_set.filter(parcial=parcial).count() <= 0:
                pagtos = pagtos.exclude(id=p.id)

        pagamentos = pagtos
        mods = []
        for m in pagamentos.values_list('origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla',
                                        flat=True).distinct():
            if not m in mods:
                mods.append(m)

        if 'MPN' in mods:
            mods.remove('MPN')

        if 'STE' in mods:
            mods.remove('STE')

        ha = EstadoP.objects.get(nome__contains='Agilis')
        protocolos_agilis = []
        for m in mods:
            data = urllib.urlencode([('processo', args[0]), ('parcial', parcial), ('tipoPrestacao', 'PRN'), ('tipoDespesa', TIPOS[m]), ('Prosseguir', 'Prosseguir')])
            req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar', data=data)
            resp = urllib2.urlopen(req)

            pgs = pagamentos.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla=m)

            dt = []
            pa = []
            for pg in pgs:
                try:
                    inte, dec = str(pg.valor_fapesp).split('.')
                except:
                    inte = str(pg.valor_fapesp)
                    dec = 0

                pa.append(pg.protocolo.pk)
                nf = pg.protocolo.num_documento
                if pg.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
                    nf = '%s %s' % (pg.protocolo.tipo_documento.nome, nf)

                try:
                    data_nota = pg.protocolo.data_vencimento.strftime('%d/%m/%Y')
                except:
                    data_nota = pg.protocolo.data_chegada.strftime('%d/%m/%Y')

                dt += [('notaFiscal', nf), ('dataNotaFiscal', data_nota), ('cheque', pg.conta_corrente.cod_oper),
                       ('pagina', pg.auditoria_set.filter(parcial=parcial).values_list('pagina', flat=True)[0]),
                       ('valorItem', '%s,%s' % (inte, dec))]

            for k in range(0, 4):
                dt += [('notaFiscal', ''), ('dataNotaFiscal', ''), ('cheque', ''), ('pagina', ''), ('valorItem', '')]

            i = 0
            erros = []
            while i < pgs.count():
                data = urllib.urlencode(dt[5*i:5*i+25]+[('method', 'Incluir')])
                req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiOud.do?method=Incluir', data=data)
                p2 = urllib2.urlopen(req)
                txt = p2.read()

                time.sleep(60)
                if txt.find('Erros') >= 0:
                    self.stderr.write(u'Erro encontrado na inserção dos itens abaixo')
                    self.stderr.write('%s' % dt[5*i:5*i+25])
                    erros.append(i)

                i += 5

            for l in range(len(erros)-1, -1, -1):
                pa = pa[:erros[l]] + pa[erros[l]+5:]

            protocolos_agilis += pa

        Protocolo.objects.filter(id__in=protocolos_agilis).update(estado=ha)
