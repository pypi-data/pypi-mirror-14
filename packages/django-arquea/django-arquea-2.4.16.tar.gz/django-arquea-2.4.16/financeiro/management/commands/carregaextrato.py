# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand
from datetime import date
import re
from decimal import Decimal
from financeiro.models import ExtratoCC


class Command(BaseCommand):
    args = u'<arquivo_extrato cc/ct >'
    help = 'Carrega um extrato de conta corrente'

    def handle(self, *args, **options):
        if len(args) < 2:
            self.stdout.write('Nome de arquivo faltando')
            return

        arq = open(args[0])
        seq = 1
        codigo_anterior = 0
        for l in arq:
            dados = l.split()
            if args[1] == 'cc':
                data = dados.pop(0)
                sinal = dados.pop()
                valor = dados.pop()
                codigo = dados.pop()
                historico = ' '.join(dados)
                cartao = False
                codigo = re.sub('\.', '', codigo)
                (d, m, y) = map(int, data.split('/'))
            else:
                data = dados[0]
                valor = dados[-6]
                sinal = dados[-5]
                historico = ' '.join(dados[1:-7])
                cartao = True
                (d, m, y) = map(int, data.split('/'))
                codigo_data = '%s%02d%02d' % (y, m, d)
                if codigo_data > codigo_anterior:
                    seq = 1
                    codigo_anterior = codigo_data
                codigo = '%s%s' % (codigo_data, seq)
                seq += 1

            data = date(y, m, d)

            valor = re.sub('\.', '', valor)
            valor = re.sub(',', '.', valor)
            sinal = '' if sinal == 'C' else '-'
            ExtratoCC.objects.create(data_oper=data, cod_oper=codigo, valor=Decimal('%s%s' % (sinal, valor)),
                                     historico=historico, despesa_caixa=False, cartao=cartao)

        self.stdout.write('Extrato inserido')
