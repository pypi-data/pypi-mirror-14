#!/usr/bin/python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import transaction
from carga.models import *
from patrimonio.models import *
from financeiro.models import Pagamento
from identificacao.models import EnderecoDetalhe
import csv
import datetime

"""
Carga de CSV de invenatário
- processo de leitura e carga em tabela temporária
- gravação de dados em
    - patrimonio
    - equipamento
    - historico
    - nf
"""

class ImportError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def loadInventario(file):
    
    
    planilha = csv.reader(file, delimiter=';', quotechar='"')
    
    
    count = 0
    for item in planilha:
        try:
            count = count + 1
            if count > 1:
                
               
                inventario = Carga_inventario()
                
                #x99 = tm
                #xae = r
                for ch in ['\x99','\xae', '\xc2']:
                    if item[1] is not None:
                        item[1] = item[1].replace(ch,"")
                    if item[2] is not None:
                        item[2] = item[2].replace(ch,"")
                    if item[8] is not None:
                        item[8] = item[8].replace(ch,"")
                    if item[20] is not None:
                        item[20] = item[20].replace(ch,"")
                    if item[33] is not None:
                        item[33] = item[33].replace(ch,"")
    
    
                
                inventario.model_number =        item[1].decode('iso-8859-1').encode('utf-8') if item[1] is not "" else None
                inventario.part_number =         item[2].decode('iso-8859-1').encode('utf-8') if item[2] is not "" else None
                inventario.revision =            str(item[3]) if item[3] is not "" else None
                
                inventario.version =             str(item[4]) if item[4] is not "" else None
                inventario.ean =                 str(item[5]) if item[5] is not "" else None
                
                item[6] = item[6].replace('*', "").strip()
                inventario.serial_number =       item[6].decode('iso-8859-1').encode('utf-8')  if item[6] is not "" else None
                inventario.service_tag =         str(item[7]) if item[7] is not "" else None
                inventario.fabricante =          item[8].decode('iso-8859-1').encode('utf-8') if item[8] is not "" else None
                inventario.nota_fiscal =         str(item[9]) if item[9] is not "" else None
                
                if '/' in str(item[10]):
                    (dia, mes, ano) = (int(x) for x in item[10].split('/'))
                    item[10] = datetime.date(ano, mes, dia)
                else:
                    item[10] = None 
          
                inventario.data =                item[10]
                inventario.ncm_sh =              str(item[11]) if item[11] is not "" else None
                inventario.o_cst =               item[12].strip() if item[12] is not "" else None
                inventario.cfop =                str(item[13]) if item[13] is not "" else None
                inventario.unidade =             str(item[14]) if item[14] is not "" else None
                inventario.quantidade =          str(item[15]) if item[15] is not "" else None
                inventario.volume =              str(item[16]) if item[16] is not "" else None
                inventario.processo_fapesp =     item[17].decode('iso-8859-1').encode('utf-8') if item[17] is not "" else None
                inventario.garantia =            str(item[18]) if item[18] is not "" else None
                inventario.termino_garantia =    str(item[19]) if item[19] is not "" else None
                inventario.descricao =           item[20].decode('iso-8859-1').encode('utf-8') if item[20] is not "" else None
                inventario.propriedade =         item[21].decode('iso-8859-1').encode('utf-8') if item[21] is not "" else None
                inventario.patrimonio =          str(item[22]) if item[22] is not "" else None
                inventario.estado =              item[23].decode('iso-8859-1').encode('utf-8') if item[23] is not "" else None
                inventario.enviado =             item[24].decode('iso-8859-1').encode('utf-8') if item[24] is not "" else None
                inventario.instalado =           item[25].decode('iso-8859-1').encode('utf-8') if item[25] is not "" else None
                inventario.site =                item[26].decode('iso-8859-1').encode('utf-8') if item[26] is not "" else None
                inventario.localizacao =         item[27].decode('iso-8859-1').encode('utf-8')  if item[27] is not "" else None
                inventario.cage =                item[28].decode('iso-8859-1').encode('utf-8')  if item[28] is not "" else None
                inventario.rack =                str(item[29]) if item[29] is not "" else None
                inventario.furo =                str(item[30]) if item[30] is not "" else None
                inventario.posicao =             str(item[31]) if item[31] is not "" else None
         
                if '/' in str(item[32]):
                    (dia, mes, ano) = (int(x) for x in item[32].split('/'))
                    item[32] = datetime.date(ano, mes, dia)
                else:
                    item[32] = None
         
                inventario.inventariado =        item[32] if item[32] is not "" else None
                inventario.observacao =          item[33].decode('iso-8859-1').encode('utf-8') if item[33] is not "" else None
         
                if '/' in str(item[34]):
                    (dia, mes, ano) = (int(x) for x in item[34].split('/'))
                    item[34] = datetime.date(ano, mes, dia)
                else:
                    item[34] = None
             
                inventario.atualizado =          item[34]
            #     website_part_number = item[34].decode('iso-8859-1').encode('utf-8')
            #     website_fabricante =  item[35].decode('iso-8859-1').encode('utf-8')
    
                if inventario.quantidade and inventario.quantidade != 1:
                    raise ImportError('Quantidade deve ser 1. Verificar dados de importação.')
            
#                 inventario.save()
        except UnicodeDecodeError, ImportError:
            print item;
            
    

def checkFabricante():
    
    inventario = Carga_inventario.objects.all()
    
    count = 0
    for item in inventario:
        if not Patrimonio.objects.filter(marca=item.fabricante).exists():
            count = count +1
    
    print 'Fabricantes não encontrados: ' + str(count) + '/' + str(Carga_inventario.objects.count());
    
def checkPartNumber():
    
    inventario = Carga_inventario.objects.all()
    
    item = Carga_inventario();
    
    count = 0
    for item in inventario:
        if not Patrimonio.objects.filter(part_number=item.part_number).exists():
            count = count +1
    
    print 'Patrimonio->part_number não encontrados: ' + str(count) + '/' + str(Carga_inventario.objects.count());

def checkPatrimonio():
    
    inventario = Carga_inventario.objects.all()
    
    item = Carga_inventario();
    
    count = 0
    for item in inventario:
        if not Patrimonio.objects.filter(part_number=item.part_number, ns=item.serial_number).exists():
            count = count +1
        else:
            patrimonios = Patrimonio.objects.filter(part_number=item.part_number, ns=item.serial_number)
            if len(patrimonios) > 1:
                print 'Patrimonio duplicado ' + str(item.serial_number)
            else:
                if patrimonios[0].ns != item.nota_fiscal:
                    print 'Patrimonio com Nota fiscal diferente: ' + str(item.serial_number) +' <' + str(patrimonios[0].ns) + "> <" + str(item.nota_fiscal) + ">"
    
    print 'Patrimonio->part_number não encontrados: ' + str(count) + '/' + str(Carga_inventario.objects.count());
 
# 
#     hc = HistoricoLocal()
#     hc.endereco = e
#     hc.descricao = ocorrencia
#     (d,m,y) = map(int, data.split('/'))
#     hc.data = datetime.date(y,m,d)
#     status = Estado.objects.get(nome=estado)
#     hc.estado = status
#     hc.patrimonio = patr
# 
#     hc.save()
#     print hc


@transaction.commit_on_success
def loadCSV():
#     loadInventario()
#     loadPatrimonio()
#     checkFabricante()
#     checkPartNumber()
    checkPatrimonio(open('/tmp/Inventario-ANSP-230720130918-V15m-OBR.csv', 'rb'))

# Disparo de carga do CSV
loadCSV()