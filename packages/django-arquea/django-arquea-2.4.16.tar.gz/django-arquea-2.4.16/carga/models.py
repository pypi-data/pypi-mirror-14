# -*- coding:utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.models import NARADateField


class Carga_inventario(models.Model):
    # [0]
    local = models.CharField(_(u'local'), null=True, blank=True, max_length=100)
    # [1] Patrimonio modelo
    model_number = models.CharField(_(u'model_number'), null=True, blank=True, max_length=100)
    # [2] Patrimonio part_number
    part_number = models.CharField(_(u'part_number'), null=True, blank=True, max_length=50)
    # [3]
    revision = models.CharField(_(u'revision'), null=True, blank=True, max_length=50)
    # [4]
    version = models.CharField(_(u'version'), null=True, blank=True, max_length=50)
    # [5] Patrimonio ean
    ean = models.CharField(_(u'EAN'), max_length=45, null=True, blank=True)
    # [6] Patrimonio ns
    serial_number = models.CharField(_(u'Número de série'), null=True, blank=True, max_length=50)
    # [7]
    service_tag = models.CharField(_(u'Service tag'), null=True, blank=True, max_length=50)
    # [8] Patrimonio marca
    fabricante = models.CharField(_(u'Marca/Editora'), null=True, blank=True, max_length=100)
    # [9] Protocolo num_documento
    nota_fiscal = models.CharField(_(u'Número'), null=True, max_length=50, blank=True)
    # [10]
    data = NARADateField(_(u'Data'), null=True, blank=True)
    # [11] Patrimonio ncm
    ncm_sh = models.CharField(_(u'NCM/SH'), null=True, blank=True, max_length=30)
    # [12]
    o_cst = models.CharField(_(u'o_cst'), null=True, blank=True, max_length=30)
    # [13]
    cfop = models.CharField(_(u'cfop'), null=True, blank=True, max_length=30)
    # [14]
    unidade = models.CharField(_(u'Unidade'), null=True, blank=True, max_length=10)
    # [15]
    quantidade = models.DecimalField(_(u'quantidade'), max_digits=6, decimal_places=0, null=True, blank=True)
    # [16]
    volume = models.CharField(_(u'Volume'), null=True, blank=True, max_length=50)
    # [17]
    processo_fapesp = models.CharField(_(u'Processo Fapesp'), null=True, max_length=50)
    # [18]
    garantia = models.CharField(_(u'Garantia'), null=True, blank=True, max_length=50)
    # [19]
    termino_garantia = models.CharField(_(u'Termino de Garantia'), null=True, blank=True, max_length=50)
    # [20] Patrimonio descricao
    descricao = models.TextField(_(u'Descrição NF'), null=True, blank=True, max_length=350)
    # [21]
    propriedade = models.TextField(_(u'propriedade'), null=True, blank=True)
    # [22]
    patrimonio = models.TextField(_(u'patrimonio'), null=True, blank=True)
    # [23]
    estado = models.CharField(_(u'estado'), null=True, blank=True, max_length=20)
    # [24]
    enviado = models.CharField(_(u'enviado'), null=True, blank=True, max_length=30)
    # [25]
    instalado = models.CharField(_(u'instalado'), null=True, blank=True, max_length=40)
    # [26]
    site = models.CharField(_(u'site - localizacao'), null=True, blank=True, max_length=50)
    # [27] Patrimonio
    localizacao = models.CharField(_(u'localizacao'), null=True, blank=True, max_length=100)
    # [28]
    cage = models.CharField(_(u'cage'), null=True, blank=True, max_length=30)
    # [29]
    rack = models.CharField(_(u'rack'), null=True, blank=True, max_length=10)
    # [30]
    furo = models.CharField(_(u'furo'), null=True, blank=True, max_length=10)
    # [31]
    posicao = models.CharField(_(u'posicao'), null=True, blank=True, max_length=10)
    # [32]
    inventariado = NARADateField(_(u'inventariado'), null=True, blank=True)
    # [33]
    observacao = models.CharField(_(u'observacao'), null=True, blank=True, max_length=350)
    # [34]
    atualizado = NARADateField(_(u'atualizado'), null=True, blank=True)
    # [35]
    # id do patrimonio
    # [36]
    # id do patrimonio pai
    # [37]
    url_equipamento = models.CharField(_(u'url_equipamento'), null=True, blank=True, max_length=200)

    #     website_part_number = models.CharField(u'website_part_number', null=True, blank=True, max_length=200)
    #     # [36]
    #     website_fabricante = models.CharField(u'website_fabricante', null=True, blank=True, max_length=200)

    planilha_aba = models.CharField(_(u'planilha_aba'), null=True, blank=True, max_length=50)
    planilha_linha = models.DecimalField(_(u'planilha_linha'), max_digits=5, decimal_places=0, null=True, blank=True)

    # [35]
    patrimonio_model = models.ForeignKey('patrimonio.Patrimonio', null=True, blank=True)
    equipamento_model = models.ForeignKey('patrimonio.Equipamento', null=True, blank=True)

    #     chk_posicao = models.BooleanField(_(u'Posicao ok?'), null=True, blank=True)
    #     chk_sn = models.BooleanField(_(u'Serial ok?'), null=True, blank=True)
    #     chk_pn = models.BooleanField(_(u'Part Number ok?'), null=True, blank=True)
    #     chk_model = models.BooleanField(_(u'Modelo ok?'), null=True, blank=True)

    tipo_carga = models.DecimalField(_(u'tipo_carga'), max_digits=2, decimal_places=0, null=True, blank=True)

    def __unicode__(self):
        if self.serial_number:
            return self.serial_number
        else:
            return u''
