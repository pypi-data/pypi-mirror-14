# -* coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.db import connection
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect

import csv
import datetime

from carga.forms import UploadFileForm
from patrimonio.models import Equipamento, Patrimonio

import logging
from carga.models import Carga_inventario

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def list_planilha_patrimonio(request):
    chk_patrimonio_vazio = request.GET.get('chk_patrimonio_vazio')

    if chk_patrimonio_vazio == '1':
        inventario = Carga_inventario.objects.filter(patrimonio_model__isnull=True) \
            .select_related('patrimonio_model', 'patrimonio_model__equipamento',
                            'patrimonio_model__equipamento__especificacao',
                            'patrimonio_model__equipamento__entidade_fabricante')
    elif chk_patrimonio_vazio == '0':
        inventario = Carga_inventario.objects.filter(patrimonio_model__isnull=False) \
            .select_related('patrimonio_model', 'patrimonio_model__equipamento',
                            'patrimonio_model__equipamento__especificacao',
                            'patrimonio_model__equipamento__entidade_fabricante')
    else:
        inventario = Carga_inventario.objects.all() \
            .select_related('patrimonio_model', 'patrimonio_model__entidade_procedencia',
                            'patrimonio_model__equipamento', 'patrimonio_model__equipamento__especificacao',
                            'patrimonio_model__equipamento__entidade_fabricante')

    ordenacao = request.GET.get('ord')
    if ordenacao == 'rack':
        inventario = inventario.order_by('rack', 'furo', )
    elif ordenacao == 'patrimonio':
        inventario = inventario.order_by('patrimonio_model', 'planilha_linha')
    else:
        inventario = inventario.order_by('planilha_linha')

    c = {'inventario': inventario}
    c.update({'chk_patrimonio_vazio': chk_patrimonio_vazio})
    c.update({'com_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=False).count()})
    c.update({'sem_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=True).count()})

    return TemplateResponse(request, 'admin/carga/patrimonio/lista_carga_patrimonio.html', c)


@login_required
def add_patrimonio(request):
    chk_patrimonio_vazio = request.GET.get('chk_patrimonio_vazio')

    if chk_patrimonio_vazio == '1':
        inventario = Carga_inventario.objects.filter(patrimonio_model__isnull=True)
    elif chk_patrimonio_vazio == '0':
        inventario = Carga_inventario.objects.filter(patrimonio_model__isnull=False)
    else:
        inventario = Carga_inventario.objects.all()

    ordenacao = request.GET.get('ord')
    if ordenacao == 'rack':
        inventario = inventario.order_by('rack', 'furo', )
    elif ordenacao == 'patrimonio':
        inventario = inventario.order_by('patrimonio_model', 'planilha_linha')
    else:
        inventario = inventario.order_by('planilha_linha')

    c = {'inventario': inventario}
    c.update({'chk_patrimonio_vazio': chk_patrimonio_vazio})
    c.update({'com_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=False).count()})
    c.update({'sem_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=True).count()})

    return TemplateResponse(request, 'admin/carga/patrimonio/lista_carga_patrimonio.html', c)


@login_required
@csrf_protect
def upload_planilha_patrimonio(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        c.update({'form': form})

        handle_uploaded_file(request.FILES['file'])

        retornoCheckPatrimonio = checkPatrimonio()

        c.update({'success': True})
        c.update({'novos_patrimonios': retornoCheckPatrimonio['count']})
        c.update({'com_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=False).count()})
        c.update({'sem_patrimonio': Carga_inventario.objects.filter(patrimonio_model__isnull=True).count()})

        return TemplateResponse(request, 'admin/carga/patrimonio/carga_patrimonio.html', c)
    else:
        form = UploadFileForm()
        c.update({'form': form})

    return TemplateResponse(request, 'admin/carga/patrimonio/carga_patrimonio.html', c)


def handle_uploaded_file(f):
    planilha = csv.reader(f, delimiter=';', quotechar='"')

    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE "{0}"'.format(Carga_inventario._meta.db_table))  # @UndefinedVariable

    count = 0
    for item in planilha:
        count += 1
        if count > 1:
            inventario = Carga_inventario()
            inventario.planilha_linha = count
            for ch in ['\x99', '\xae', '\xc2']:
                if item[1] is not None:
                    item[1] = item[1].replace(ch, "")
                if item[2] is not None:
                    item[2] = item[2].replace(ch, "")
                if item[8] is not None:
                    item[8] = item[8].replace(ch, "")
                if item[20] is not None:
                    item[20] = item[20].replace(ch, "")
                if item[33] is not None:
                    item[33] = item[33].replace(ch, "")

            inventario.model_number = item[1].decode('iso-8859-1').encode('utf-8').strip() \
                if item[1] is not "" else None
            inventario.part_number = item[2].decode('iso-8859-1').encode('utf-8').strip(' ') \
                if item[2] is not "" else None
            inventario.revision = str(item[3]).strip() if item[3] is not "" else None

            inventario.version = str(item[4]).strip() if item[4] is not "" else None
            inventario.ean = str(item[5]).strip() if item[5] is not "" else None

            item[6] = item[6].strip(' *')
            inventario.serial_number = item[6].decode('iso-8859-1').encode('utf-8') if item[6] is not "" else None
            inventario.service_tag = str(item[7]).strip() if item[7] is not "" else None
            inventario.fabricante = item[8].decode('iso-8859-1').encode('utf-8').strip() if item[8] is not "" else None
            inventario.nota_fiscal = str(item[9]).strip() if item[9] is not "" else None

            if item[10].isdigit():
                item[10] = minimalist_xldate_as_datetime(int(item[10]), 0)
            else:
                item[10] = None

            inventario.data = item[10]
            inventario.ncm_sh = str(item[11]).strip() if item[11] is not "" else None
            inventario.o_cst = item[12].strip() if item[12] is not "" else None
            inventario.cfop = str(item[13]).strip() if item[13] is not "" else None
            inventario.unidade = str(item[14]).strip() if item[14] is not "" else None
            inventario.quantidade = str(item[15]).strip() if item[15] is not "" else None
            inventario.volume = str(item[16]).strip() if item[16] is not "" else None
            inventario.processo_fapesp = item[17].decode('iso-8859-1').encode('utf-8').strip() \
                if item[17] is not "" else None
            inventario.garantia = str(item[18]).strip() if item[18] is not "" else None
            inventario.termino_garantia = str(item[19]).strip() if item[19] is not "" else None
            inventario.descricao = item[20].decode('iso-8859-1').encode('utf-8').strip() if item[20] is not "" else None
            inventario.propriedade = item[21].decode('iso-8859-1').encode('utf-8').strip() \
                if item[21] is not "" else None
            inventario.patrimonio = str(item[22]).strip() if item[22] is not "" else None
            inventario.estado = item[23].decode('iso-8859-1').encode('utf-8').strip() if item[23] is not "" else None
            inventario.enviado = item[24].decode('iso-8859-1').encode('utf-8').strip() if item[24] is not "" else None
            inventario.instalado = item[25].decode('iso-8859-1').encode('utf-8').strip() if item[25] is not "" else None
            inventario.site = item[26].decode('iso-8859-1').encode('utf-8').strip() if item[26] is not "" else None
            inventario.localizacao = item[27].decode('iso-8859-1').encode('utf-8').strip() \
                if item[27] is not "" else None
            inventario.cage = item[28].decode('iso-8859-1').encode('utf-8').strip() if item[28] is not "" else None
            inventario.rack = str(item[29]).strip() if item[29] is not "" else None
            inventario.furo = str(item[30]).strip() if item[30] is not "" else None
            inventario.posicao = str(item[31]).strip() if item[31] is not "" else None

            if item[32].isdigit():
                item[32] = minimalist_xldate_as_datetime(int(item[32]), 0)
            else:
                item[32] = None

            inventario.inventariado = item[32] if item[32] is not "" else None
            inventario.observacao = item[33].decode('iso-8859-1').encode('utf-8').strip() \
                if item[33] is not "" else None

            if item[34].isdigit():
                item[34] = minimalist_xldate_as_datetime(int(item[34]), 0)
            else:
                item[34] = None

            inventario.atualizado = item[34]
            if item[35].isdigit():

                try:
                    p = Patrimonio.objects.get(pk=int(item[35]))
                except Patrimonio.DoesNotExist:
                    raise Exception("Patrimonio.DoesNotExist. Lookup id = %s ." % int(item[35]))

                inventario.patrimonio_model = p
                # website_part_number = item[34].decode('iso-8859-1').encode('utf-8')
                #     website_fabricante =  item[35].decode('iso-8859-1').encode('utf-8')

            # if inventario.quantidade and inventario.quantidade != 1:
            #                     raise Exception('Quantidade deve ser 1. Verificar dados de importação.')

            inventario.url_equipamento = item[37]

            inventario.save()


def buscaPatrimonioPorSN(item):
    patr = None
    # Verificar o match pelo serial number.
    if item.serial_number and item.serial_number != '' and item.serial_number != ' ':
        p = Patrimonio.objects.filter(ns=item.serial_number)

        if len(p) == 1:
            patr = p.filter()[:1].get()
            patr.tipo_carga = 1
    return patr


def buscaPatrimonioPorServiceTag(item):
    patr = None

    # Verificar o match pelo service tag
    if item.service_tag and item.service_tag != '' and item.service_tag != ' ':
        p = Patrimonio.objects.filter(ns=('(Serv TAG ' + item.service_tag + ')'))

        if len(p) == 1:
            patr = p.filter()[:1].get()
            patr.tipo_carga = 5
    return patr


def buscaPatrimonioPorModeloPNPosicao(item):
    patr = None

    if item.model_number and item.model_number != '' and item.model_number != ' ' and item.part_number \
            and item.part_number != '' and item.part_number != ' ' and item.cage and item.rack:

        pts_pn = Patrimonio.objects.filter(part_number=item.part_number, modelo=item.model_number,
                                           historicolocal__endereco__ordena__contains=item.cage,
                                           historicolocal__posicao__startswith=item.rack)

        if item.furo and item.furo.isdigit():
            pts_pn = pts_pn.filter(historicolocal__posicao__contains=item.furo)

    return patr


def buscaPatrimonioSemSNPorPosicao(item):
    patr = None

    if (item.rack and item.cage) and item.quantidade == 1:

        pts_pn = Patrimonio.objects.filter(historicolocal__endereco__ordena__contains=item.cage,
                                           historicolocal__posicao__startswith=item.rack)

        if item.furo and item.furo.isdigit():
            pts_pn = pts_pn.filter(historicolocal__posicao__contains=item.furo)

    return patr


def checkPatrimonio():
    count = 0

    inventario = Carga_inventario.objects.all()
    for item in inventario:
        if not item.patrimonio_model:
            patr = buscaPatrimonioPorSN(item)

            if not patr:
                patr = buscaPatrimonioPorServiceTag(item)

            if not patr:
                patr = buscaPatrimonioPorModeloPNPosicao(item)

            if not patr:
                patr = buscaPatrimonioSemSNPorPosicao(item)

            if patr:
                item.patrimonio_model = patr
                count = count + 1
                if patr.equipamento:
                    item.equipamento_model = patr.equipamento
                else:
                    item.equipamento_model = checkEquipamento(item)
                item.save()
    return {'count': count}


def checkEquipamento(item):
    e = Equipamento.objects.filter(part_number=item.part_number)
    if len(e) == 1:
        return e.filter()[:1].get()
    return None


def checkPatrimonioPosicao():
    inventario = Carga_inventario.objects.filter(patrimonio_model__isnull=False)
    for item in inventario:
        # rack = item.patrimonio_model.historico_atual.posicao_rack
        # furo = item.patrimonio_model.historico_atual.posicao_furo
        # posicao = item.patrimonio_model.historico_atual.posicao_colocacao

        # chk_rack = False
        #         if rack or item.rack:
        #             chk_rack = item.rack == rack
        #
        #         chk_furo = False
        #         if furo or item.furo:
        #             chk_furo = item.furo == furo
        #
        #         chk_posicao = False
        #         if posicao or item.posicao:
        #             chk_posicao = item.posicao == posicao
        #
        #         item.chk_posicao = chk_rack and chk_furo and chk_posicao
        item.save()


def minimalist_xldate_as_datetime(xldate, datemode):
    # datemode: 0 for 1900-based, 1 for 1904-based
    return (
        datetime.datetime(1899, 12, 30)
        + datetime.timedelta(days=xldate + 1462 * datemode)
    )
