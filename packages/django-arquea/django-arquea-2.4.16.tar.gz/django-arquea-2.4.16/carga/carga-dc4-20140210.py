# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# from django.core.management import setup_environ
# import settings
# setup_environ(settings)

# from django.db import transaction
from patrimonio.models import HistoricoLocal, Tipo, Patrimonio, Equipamento, Estado
from identificacao.models import EnderecoDetalhe
import csv
import datetime


class ImportError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def cargaDC4_20140207(item):
    # 289 - DC4
    endDet = EnderecoDetalhe.objects.get(pk=289)
    # 22 - Ativo
    # 30 - Inativo
    est = Estado.objects.get(pk=22)

    # 46 - Carga
    tipoPatr = Tipo.objects.get(pk=46)

    # Rack em que está contido

    patrRack = Patrimonio.objects.get(apelido=item['rack'])
    equipamento = Equipamento.objects.get(pk=item['equipamento_id'])

    patrimonio = Patrimonio(ns=item['ns'], apelido=item['apelido'], descricao=item['descricao'], tipo=tipoPatr,
                            patrimonio=patrRack, equipamento=equipamento, modelo=equipamento.modelo,
                            tamanho=equipamento.tamanho, agilis=False)

    patrimonio.save()

    historicoPai = HistoricoLocal(posicao=item['posicao'], descricao='Verificado novo equipamento em visita ao NAP.',
                                  data=datetime.date(2014, 1, 29), patrimonio=patrimonio, endereco=endDet, estado=est)

    historicoPai.save()

    print patrimonio.id


def loadInventario(file):
    planilha = csv.reader(file, delimiter=';', quotechar='"')

    inventario = []

    count = 0
    for item in planilha:
        try:
            # serial
            # apelido
            # descricao
            # rack
            # posicao
            # equipamento_id

            ns = str(item[0]) if item[0] is not "" else None
            apelido = str(item[1]) if item[1] is not "" else None
            descricao = str(item[2]) if item[2] is not "" else None
            rack = "Rack " + str(item[3]) if item[3] is not "" else None
            posicao = str(item[4]) if item[4] is not "" else None
            equipamento_id = str(item[5]) if item[5] is not "" else None

            inventario.append({'ns': ns, 'apelido': apelido, 'descricao': descricao, 'rack': rack, 'posicao': posicao,
                               'equipamento_id': equipamento_id
                               })

        # inventario.save()
        except (UnicodeDecodeError, ImportError):
            print item

    for item in inventario:
        count += 1
        print 'count %s' % count
        cargaDC4_20140207(item)


def loadCSV():
    loadInventario(open('/share/carga_dc4_2.csv', 'rb'))

# Disparo de carga do CSV
loadCSV()