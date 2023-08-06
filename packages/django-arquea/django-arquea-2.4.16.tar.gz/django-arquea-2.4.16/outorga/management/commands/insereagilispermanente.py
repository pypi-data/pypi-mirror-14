# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib2
import urllib
import cookielib
from django.core.management.base import BaseCommand, CommandError
from outorga.models import Termo
from patrimonio.models import Patrimonio
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

        data = urllib.urlencode([('processo', args[0]), ('parcial', parcial), ('tipoPrestacao', 'PRN'),
                                 ('tipoDespesa', 'MPE'), ('Prosseguir', 'Prosseguir')])
        req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineSelecao.do?method=pesquisar',
                              data=data)
        resp = urllib2.urlopen(req)

        eqs = {}
        patrimonios = Patrimonio.objects.filter(pagamento__protocolo__termo=termo,
                                                pagamento__origem_fapesp__item_outorga__natureza_gasto__modalidade__sigla='MPN')
        for e in patrimonios.filter(agilis=True):
            texto = '%s - %s - %s' % (e.equipamento.modelo, e.pagamento.id, e.equipamento.entidade_fabricante.sigla)
            if e.pagamento.auditoria_set.filter(parcial=parcial).count() == 0:
                continue
            if texto in eqs.keys():
                eqs[texto].append(e)
            else:
                eqs[texto] = [e]

        incluir = [('method', 'Incluir')]
        for eq in eqs.keys():
            qtd = len(eqs[eq])
            e = eqs[eq][0]
            pg = e.pagamento

            try:
                inte, dec = str(e.valor).split('.')
            except:
                inte = str(e.valor)
                dec = 0

            nf = pg.protocolo.num_documento
            sn = ','.join([pt.ns for pt in eqs[eq]])
            modelo, pgto, marca = eq.split(' - ')
            for pt in patrimonios.filter(agilis=False, equipamento__modelo=modelo, pagamento__id=pgto,
                                         equipamento__entidade_fabricante__sigla=marca):
                sn += ',%s' % pt.ns
            if len(sn) > 170:
                sn = sn[:170]

            if pg.protocolo.tipo_documento.nome.lower().find('anexo') == 0:
                nf = '%s %s' % (pg.protocolo.tipo_documento.nome, nf)
            dt = [('notaFiscal', nf), ('dataNotaFiscal', pg.protocolo.data_vencimento.strftime('%d/%m/%Y')),
                  ('cheque', pg.conta_corrente.cod_oper),
                  ('pagina', pg.auditoria_set.filter(parcial=parcial).values_list('pagina', flat=True)[0]),
                  ('valorItem', '%s,%s' % (inte, dec)), ('descricao', e.equipamento.descricao), ('quantidade', qtd),
                  ('marca', e.marca or ''), ('modelo', e.modelo or ''), ('observacao', sn),
                  ('procedencia', e.procedencia or '')]

            data = urllib.urlencode(dt+incluir)
            req = urllib2.Request(url='http://internet.aquila.fapesp.br/agilis/PconlineIncluiOuAlteraMpe.do', data=data)
            p2 = urllib2.urlopen(req)
            txt = p2.read()

            # pausa entre requisições para não sobrecarregar
            time.sleep(30)
            if txt.find('Erros') >= 0:
                print u'Erro encontrado na inserção dos itens abaixo'
                print dt
