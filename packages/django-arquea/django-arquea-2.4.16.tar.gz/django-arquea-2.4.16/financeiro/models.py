# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import Max, Sum
from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

from utils.functions import formata_moeda
from protocolo.models import Estado as EstadoProtocolo
from utils.models import NARADateField

CODIGO_FINANCEIRO = (
    ('COMP', 'Concessao Bens/Serv. Pais'),
    ('PGMP', 'Pgto. Bens/Serv. Pais'),
    ('DVMP', 'Devl. Bens/Serv. Pais'),
    ('SUMP', 'Supl. Bens/Serv. Pais'),
    ('ANMP', 'Anulacao'),
    ('ESMP', 'Estorno ANMP'),
    ('CAMP', 'Canc. Bens/Serv. Pais'),
    ('CORP', 'Concessao Reserva Tecnica Auxil. Pais'),
    ('PGRP', 'Pgto. Reserva Tecnica Auxil. Pais'),
    ('DVRP', 'Devl. Reserva Tecnica Auxil. Pais'),
    ('SURP', 'Supl. Reserva Tecnica Auxil. Pais'),
    ('ANRP', 'Anulacao Reserva Tecnica Auxil. Pais'),
    ('ESRP', 'Estorno ANRP'),
    ('CARP', 'Canc. Reserva Tecnica Auxil. Pais'),
)


class ExtratoCC(models.Model):
    extrato_financeiro = models.ForeignKey('financeiro.ExtratoFinanceiro', verbose_name=_(u'Extrato Financeiro'),
                                           blank=True, null=True)
    data_oper = NARADateField(_(u'Data da operação'))
    cod_oper = models.IntegerField(verbose_name=_(u'Documento'),
                                   validators=[MinValueValidator(0), MaxValueValidator(9999999999)],
                                   help_text=u'Código com máximo de 10 dígitos.')
    despesa_caixa = models.BooleanField(_(u'Despesa de caixa?'), default=False)
    valor = models.DecimalField(_(u'Valor'), max_digits=12, decimal_places=2)
    historico = models.CharField(_(u'Histórico'), max_length=30)
    cartao = models.BooleanField(_(u'Cartão?'), default=False)
    data_extrato = NARADateField(_(u'Data do extrato'), null=True, blank=True)
    imagem = models.ImageField(_(u'Imagem do cheque'), upload_to='extratocc', null=True, blank=True,
                               help_text=u'Somente imagem .jpeg',
                               validators=[RegexValidator(regex=".+((\.jpg)|.+(\.jpeg))$",
                                                          message="Enviar somente imagem jpeg. A proporção da "
                                                                  "largura / altura deve ser maior que 2."), ])
    capa = models.TextField(null=True, blank=True)
    obs = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _(u'Extrato de Conta corrente')
        verbose_name_plural = _(u'Extratos de Conta corrente')
        ordering = ('-data_oper',)

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.data_oper, self.cod_oper, self.historico, self.valor)

    @property
    def saldo(self):
        s = ExtratoCC.objects.filter(data_oper__lte=self.data_oper).aggregate(Sum('valor'))
        return s['valor__sum']

    @property
    def saldo_anterior(self):
        s = ExtratoCC.objects.filter(data_oper__lt=self.data_oper).aggregate(Sum('valor'))
        return s['valor__sum']

    def parciais(self):
        mods = {}
        for p in self.pagamento_set.all()\
                .select_related('origem_fapesp', 'origem_fapesp__item_outorga__natureza_gasto__modalidade'):
            if p.origem_fapesp:
                modalidade = p.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
                if modalidade not in mods.keys():
                    mods[modalidade] = {}
                    for a in p.auditoria_set.all():
                        if a.parcial not in mods[modalidade].keys():
                            mods[modalidade][a.parcial] = []
                            if a.pagina not in mods[modalidade][a.parcial]:
                                mods[modalidade][a.parcial].append(a.pagina)
        parc = ''
        for modalidade in mods.keys():
            parc += '%s [parcial ' % modalidade
            for p in mods[modalidade].keys():
                pags = mods[modalidade][p]
                pags.sort()
                parc += '%s (%s)' % (p, ','.join([str(k) for k in pags]))
            parc += ']  '

        return parc


class TipoComprovanteFinanceiro(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Tipo de Comprovante Financeiro')
        verbose_name_plural = _(u'Tipos de Comprovante Financeiro')
        ordering = ('nome',)


class ExtratoFinanceiro(models.Model):
    entrada_extrato_cc = models.ForeignKey('financeiro.ExtratoCC', on_delete=models.SET_NULL, null=True, blank=True)  # referencia a uma entrada no ExtratoCC  
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo de outorga'))
    data_libera = NARADateField(_(u'Data'))
    cod = models.CharField(_(u'Código'), max_length=4, choices=CODIGO_FINANCEIRO)
    historico = models.CharField(_(u'Histórico'), max_length=40)
    valor = models.DecimalField(_(u'Valor'), max_digits=12, decimal_places=2)
    comprovante = models.FileField(_(u'Comprovante da operação'), upload_to='extratofinanceiro', null=True, blank=True)
    tipo_comprovante = models.ForeignKey('financeiro.TipoComprovanteFinanceiro', null=True, blank=True)
    parcial = models.IntegerField(null=False, blank=False, default=0,
                                  validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    taxas = models.IntegerField(default=0)

    class Meta:
        verbose_name = _(u'Extrato do Financeiro')
        verbose_name_plural = _(u'Extratos do Financeiro')
        ordering = ('-data_libera',)

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.data_libera, self.cod, self.historico, self.valor)

    def save(self, *args, **kwargs):
        for (cod, hist) in CODIGO_FINANCEIRO:
            if self.cod == cod:
                self.historico = hist
                break
        super(ExtratoFinanceiro, self).save(*args, **kwargs)

    @property
    def despesa_caixa(self):
        try:
            return self.tipo_comprovante == TipoComprovanteFinanceiro.objects.get(nome=u'Despesa de caixa')
        except:
            return False

    @staticmethod
    def _insere_extrato_cc(extratoFinanceiro):
        """
        Rotina para inserir no extrato de conta corrente a liberação do financeiro para o Cartão Pesquisa BB.
        Deve receber um objeto ExtratoFinanceiro.

        if (retorno == 1) {
            "Extrato de conta corrente inserido com sucesso."
        } else if (retorno == 2) {
            "Extrato de conta corrente já existente."
        } else {
            "Extrato de conta corrente não inserido."
        }
        """
        retorno = -1

        ef = extratoFinanceiro

        if ef.entrada_extrato_cc:
            retorno = 2
        else:
            ecc1 = ExtratoCC.objects.create(data_oper=ef.data_libera,
                                            historico=u'Liberação de verba MP',
                                            valor=-ef.valor,
                                            cod_oper=ef.data_libera.strftime('%Y%m%d9'))
            # atribuindo a referencia de entrada no extratoCC
            # o save() deve ser disparado por quem chamou este método
            ef.entrada_extrato_cc = ecc1
            
            if ef.taxas > 0:
                ecc2 = ExtratoCC.objects.create(data_oper=ef.data_libera,
                                                historico=u'Liberação de verba TX',
                                                valor=ef.taxas * Decimal('1.00'),
                                                cod_oper=ef.data_libera.strftime('%Y%m%d9'))

                ecc3 = ExtratoCC.objects.create(data_oper=ef.data_libera,
                                                historico=u'Pagamento TX',
                                                valor=ef.taxas * Decimal('-1.00'),
                                                cod_oper=ef.data_libera.strftime('%Y%m%d9'))
                if not ecc2 or not ecc3:
                    retorno = -2

            if not ecc1:
                retorno = -3
            else:
                retorno = 1

        return retorno


class Pagamento(models.Model):
    patrocinio = models.ForeignKey('financeiro.ExtratoPatrocinio', verbose_name=_(u'Extrato do patrocínio'),
                                   null=True, blank=True)
    conta_corrente = models.ForeignKey('financeiro.ExtratoCC', null=True, blank=True)
    protocolo = models.ForeignKey('protocolo.Protocolo')
    valor_fapesp = models.DecimalField(_(u'Valor originário da Fapesp'), max_digits=12, decimal_places=2)
    valor_patrocinio = models.DecimalField(_(u'Valor originário de patrocínio'), max_digits=12, decimal_places=2,
                                           null=True, blank=True)
    reembolso = models.BooleanField(default=False)
    membro = models.ForeignKey('membro.Membro', null=True, blank=True)
    origem_fapesp = models.ForeignKey('outorga.OrigemFapesp', null=True, blank=True)
    pergunta = models.ManyToManyField('memorando.Pergunta', null=True, blank=True)

    def __unicode__(self):
        if self.valor_patrocinio:
            valor = self.valor_fapesp+self.valor_patrocinio
        else:
            valor = self.valor_fapesp
        mod = ''
        if self.origem_fapesp_id:
            mod = self.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
            if self.auditoria_set.exists():
                a = self.auditoria_set.only('pagamento', 'parcial', 'pagina')[:1].get()
                return u"%s - %s - %s, parcial %s, página %s    ID: %s" % \
                       (self.protocolo.num_documento, valor, mod, a.parcial, a.pagina, self.pk)
        return u"%s - %s - %s    ID: %s" % (self.protocolo.num_documento, valor, mod, self.pk)

    def unicode_para_auditoria(self):
        """
        Método para ser chamado de dentro da Auritoria.
        Retorna um valor parecido com o unicode, mas removendo os valores de Auditoria,
        pois pertencem ao objeto Auditoria que está sendo chamado
        """
        if self.valor_patrocinio:
            valor = self.valor_fapesp + self.valor_patrocinio
        else:
            valor = self.valor_fapesp
        mod = ''
        if self.origem_fapesp:
            mod = self.origem_fapesp.item_outorga.natureza_gasto.modalidade.sigla
        return u"%s - %s - %s    ID: %s" % (self.protocolo.num_documento, valor, mod, self.pk)

    def codigo_operacao(self):
        if self.conta_corrente:
            return self.conta_corrente.cod_oper
        else:
            return ''
    codigo_operacao.short_description = 'Operação Bancária'
    codigo_operacao.admin_order_field = 'conta_corrente__cod_oper'

    def anexos(self):
        retorno = u'Não'
        if self.auditoria_set.exists():
            retorno = u'Sim'
        return retorno

    def save(self, *args, **kwargs):
        e, created = EstadoProtocolo.objects.get_or_create(nome=u'Pago')
        if not self.id:
            self.protocolo.estado = e
            self.protocolo.save()

        super(Pagamento, self).save(*args, **kwargs)

    def termo(self):
        return u'%s' % self.protocolo.termo.__unicode__()

    def item(self):
        if self.origem_fapesp:
            return u'%s' % self.origem_fapesp.item_outorga.__unicode__()
        else:
            return u'Não é Fapesp'
    item.short_description = u'Item do orçamento'

    def data(self):
        return self.protocolo.data_vencimento
    data.admin_order_field = 'protocolo__data_vencimento'

    def nota(self):
        return self.protocolo.num_documento
    nota.short_description = 'NF'
    nota.admin_order_field = 'protocolo__num_documento'

    def formata_valor_fapesp(self):
        moeda = 'R$'
        if self.origem_fapesp and self.origem_fapesp.item_outorga.natureza_gasto.modalidade.moeda_nacional is False:
            moeda = 'US$'
        return u'%s %s' % (moeda, formata_moeda(self.valor_fapesp, ','))
    formata_valor_fapesp.short_description = 'Valor Fapesp'
    formata_valor_fapesp.admin_order_field = 'valor_fapesp'

    def pagina(self):
        if self.auditoria_set.exists():
            return self.auditoria_set.only('pagina', 'pagamento')[0].pagina
        return ''
    pagina.short_description = u'Página'
    pagina.admin_order_field = 'auditoria__pagina'

    def parcial(self):
        if self.auditoria_set.exists():
            return self.auditoria_set.only('parcial', 'pagamento')[0].parcial
        return ''
    parcial.admin_order_field = 'auditoria__parcial'

    class Meta:
        ordering = ('conta_corrente',)


class LocalizaPatrocinio(models.Model):
    consignado = models.CharField(max_length=50)

    class Meta:
        verbose_name = _(u'Localização do patrocínio')
        verbose_name_plural = _(u'Localização dos patrocínios')

    def __unicode__(self):
        return self.consignado


class ExtratoPatrocinio(models.Model):
    localiza = models.ForeignKey('financeiro.LocalizaPatrocinio', verbose_name=_(u'Localização do patrocínio'))
    data_oper = NARADateField(_(u'Data da operação'))
    cod_oper = models.IntegerField(_(u'Código da operação'),
                                   validators=[MinValueValidator(0), MaxValueValidator(999999999)],
                                   help_text=u'Código com máximo de 9 dígitos.')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    historico = models.CharField(max_length=30)
    obs = models.TextField()

    class Meta:
        verbose_name = _(u'Extrato do patrocínio')
        verbose_name_plural = _(u'Extratos dos patrocínios')

    def __unicode__(self):
        return u'%s - %s - %s' % (self.localiza.consignado, self.data_oper, self.valor)


class Estado(models.Model):
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


def ultimaparcial():
    from outorga.models import Termo

    t = Termo.objects.aggregate(Max('ano'))
    a = Auditoria.objects.filter(pagamento__protocolo__termo__ano=t['ano__max']).aggregate(Max('parcial'))
    return a['parcial__max']


def ultimapagina():
    from outorga.models import Termo

    t = Termo.objects.aggregate(Max('ano'))
    p = Auditoria.objects.filter(pagamento__protocolo__termo__ano=t['ano__max'],
                                 parcial=ultimaparcial()).aggregate(Max('pagina'))
    return p['pagina__max']+1


class Auditoria(models.Model):
    estado = models.ForeignKey('financeiro.Estado')
    pagamento = models.ForeignKey('financeiro.Pagamento')
    tipo = models.ForeignKey('financeiro.TipoComprovante')
    arquivo = models.FileField(upload_to='auditoria', null=True, blank=True)
    parcial = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    pagina = models.IntegerField()
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'Parcial: %s, página: %s' % (self.parcial, self.pagina)


class TipoComprovante(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = _(u'Tipo de comprovante')
        verbose_name_plural = _(u'Tipos de comprovante')
        ordering = ('nome',)

    def __unicode__(self):
        return self.nome


# Classe para definição de permissões de views e relatórios da app financeiro
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_adm_extrato", "Rel. admin. - Panorama da conta corrente"),  # /financeiro/extrato
            ("rel_adm_extrato_financeiro", "Rel. admin. - Extrato do financeiro por mês"),  # /financeiro/extrato_financeiro
            ("rel_adm_extrato_financeiro_parciais", "Rel. admin. - Extrato do financeiro por parcial"),     # /financeiro/extrato_financeiro_parciais
            ("rel_adm_extrato_mes", "Rel. admin. - Extrato da conta corrente por mês"),     # /financeiro/extrato_mes
            ("rel_adm_extrato_tarifas", "Rel. admin. - Extrato de tarifas por mês"),     # /financeiro/extrato_tarifas
            ("rel_ger_acordos", "Rel. ger. - Acordos"),     # /financeiro/relatorios/acordos
            ("rel_adm_caixa", "Rel. admin. - Diferenças de caixa"),     # /financeiro/relatorios/caixa
            ("rel_ger_gerencial",  "Rel. ger. - Gerencial"),     # /financeiro/relatorios/gerencial
            ("rel_adm_pagamentos_mes", "Rel. admin. - Pagamentos po mês"),     # /financeiro/relatorios/pagamentos_mes
            ("rel_adm_pagamentos_parcial", "Rel. admin. - Pagamentos por parcial"),     # /financeiro/relatorios/pagamentos_parcial
            ("rel_adm_parciais", "Rel. admin. - Diferenças totais"),     # /financeiro/relatorios/parciais
            ("rel_adm_prestacao", "Rel. admin. - Prestação de contas"),     # /financeiro/relatorios/prestacao
        )
