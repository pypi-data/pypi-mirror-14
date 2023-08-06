# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings
from django.core import urlresolvers
from utils.functions import formata_moeda
from utils.models import NARADateField
from django.db.models import Sum, Q
from decimal import Decimal
import datetime
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Retorna o caminho para onde o arquivo será feito upload.
def upload_dir(instance, filename):
    return 'outorga/%s/%s' % (str(instance.id), filename)


def upload_dir_os(instance, filename):
    return 'OS/%s/%s' % (str(instance.os.id), filename)


class Modalidade(models.Model):
    """
    Uma instância dessa classe é uma das modalidades de gasto autorizadas pelo Departamento de Auditoria da FAPESP.

    O método '__unicode__' 		Retorna a sigla e o nome da modalidade.
    A classmethod 'modalidades_termo'	Retorna as modalidades de um termo que possuem itens de outorga com o campo
    'item=None'.
    A class 'Meta'			Define a ordenação dos dados pela sigla.
    """
    sigla = models.CharField(_(u'Sigla'), max_length=10, blank=True, help_text=_(u'ex. STB'), unique=True)
    nome = models.CharField(_(u'Nome'), max_length=40, blank=True, help_text=_(u'ex. Serviços de Terceiros no Brasil'))
    moeda_nacional = models.BooleanField(_(u'R$'), help_text=_(u'ex. Moeda Nacional?'), default=True)

    # Retorna a sigla e o nome da modalidade.
    def __unicode__(self):
        return u'%s - %s' % (self.sigla, self.nome)

    # Retorna as modalidades de um termo que possuem itens do pedido de outorga com o campo 'item=None'.
    @classmethod
    def modalidades_termo(cls, t=None):
        modalidades = cls.objects.all()
        if t:
            for m in modalidades:
                ng = m.natureza_gasto_set.filter(termo=t)
                if not ng:
                    modalidades = modalidades.exclude(pk=m.id)
                else:
                    for n in ng:
                        i = n.item_set.all()
                        if not i:
                            modalidades = modalidades.exclude(pk=m.id)
        return modalidades

    # Define ordenação dos dados pela sigla.
    class Meta:
        ordering = ('sigla', )


class Estado(models.Model):
    """
    Uma instância dessa classe representa um estado (ex. Quitado, Vigente).

    O método '__unicode__'	Retorna o nome do estado.
    A class 'Meta'		Define a ordenação dos dados pelo nome.
    """
    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Vigente'), unique=True)

    # Retorna o nome.
    def __unicode__(self):
        return u'%s' % self.nome

    # Define ordena dos dados pelo nome.
    class Meta:
        ordering = ('nome', )


class Termo(models.Model):
    """
    Uma instância dessa classe representa um Termo de Outorga.

    O método '__unicode__'		Retorna o número completo do processo no formato 'ano/número-digito'.
    O método 'mostra_membro'	Retorna o nome do outorgado.
    O método 'save'				Não permite que o número do termo de ortorga seja alterado.
    O atributo 'real'           Calcula a concessão total em reais de um termo somando os totalizadores das
    naturezas de gasto considerando todos os pedidos de concessão.
    O método 'termo_real'       Formata o atributo 'real' em formato moeda.
    O atributo 'dolar'          Calcula a concessão total em dolares de um termo somando os totalizadores das
    naturezas de gasto considerando todos os pedidos pedidos de concessão.
    O método 'termo_dolar'      Formata o atributo 'dolar' em formato moeda.
    O método 'duracao_meses'	Calcula em meses a vigência do termo de outorga a partir das informações dos pedidos de
    concessão.
    O atributo 'total_realizado_real'   Calcula o total das despesas realizadas em reais de um termo somando os
    totalizadores das naturezas de gasto considerando todos os pedidos de concessão.
    O método 'formata_realizado_real'   Formata o atributo 'total_realizado_real' em formato moeda.
    O atributo 'total_realizado_dolar'  Calcula o total das despesas realizadas em dolares de um termo somando os
    totalizadores das naturezas de gasto considerando todos os pedidos de concessão.
    O método 'formata_realizado_dolar'  Formata o atributo 'total_realizado_dolar' em formato moeda.
    O atributo 'vigencia'				Foi criado para retornar o método 'duracao_meses'.
    O atributo 'num_processo'			Foi criado para retornar o método '__unicode__'.
    A classmethod 'termos_auditoria_fapesp_em_aberto'   Retorna os termos que possuem fontes pagadoras (fapesp) que
    ainda não possuem registro no modelo Auditoria FAPESP.
    A classmethod 'termos_auditoria_interna_em_aberto'  Retorna os termos que possuem fontes pagadoras (interna) que
    ainda não possuem registro no modelo Auditoria Interna.
    A 'class Meta'				Define a descrição do modelo (singular e plural) e a ordenação dos dados pelo ano.
    """
    ano = models.IntegerField(_(u'Ano'), help_text=_(u'ex. 2008'), default=0)
    processo = models.IntegerField(_(u'Processo'), help_text=_(u'ex. 52885'), default=0)
    digito = models.IntegerField(_(u'Dígito'), help_text=_(u'ex. 8'), default=0)
    inicio = NARADateField(_(u'Início'), help_text=_(u'Data de início do processo'), null=True, blank=True)
    estado = models.ForeignKey('outorga.Estado', verbose_name=_(u'Estado'))
    modalidade = models.ManyToManyField('outorga.Modalidade', through='Natureza_gasto', verbose_name=_(u'Pasta'))
    parecer = models.FileField(u'Parecer inicial', upload_to='termo', blank=True, null=True)
    parecer_final = models.FileField(u'Parecer final', upload_to='termo', blank=True, null=True)
    projeto = models.FileField(u'Projeto', upload_to='termo', blank=True, null=True)
    orcamento = models.FileField(_(u'Orçamento'), upload_to='termo', blank=True, null=True)
    quitacao = models.FileField(_(u'Quitação'), upload_to='termo', blank=True, null=True)
    doacao = models.FileField(_(u'Doação'), upload_to='termo', blank=True, null=True)
    extrato_financeiro = models.FileField(upload_to='termo', blank=True, null=True)
    relatorio_final = models.FileField(_(u'Relatório Final'), upload_to='termo', blank=True, null=True)
    # flag para indicar se o termo deve aparecer no relatório gerencial progressivo
    exibe_rel_ger_progressivo = models.BooleanField(_(u'Exibe o processo no Relatório Gerencial Progressivo?'),
                                                    default=True)
#    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Outorga'))

    # Retorna o número completo do processo (ano, número e dígito).
    def __unicode__(self):
        ano = str(self.ano)[2:]
        return '%s/%s-%s' % (ano, self.processo, self.digito)

    # Não permite fazer alteração no número do processo.
    def save(self, *args, **kwargs):
        pk = self.pk
        try:
            antigo = Termo.objects.get(pk=pk)
        except Termo.DoesNotExist:
            antigo = None

        if antigo and (antigo.ano != 0 or antigo.processo != 0 or antigo.digito != 0):
            self.ano = antigo.ano
            self.processo = antigo.processo
            self.digito = antigo.digito

        super(Termo, self).save(*args, **kwargs)

    # Retorna a soma das naturezas (moeda nacional) de um termo.
    @property
    def real(self):
        #     for ng in self.natureza_gasto_set.all():
        #         if ng.modalidade.moeda_nacional == True and ng.modalidade.sigla != 'REI':
        #             total += ng.valor_concedido
        soma = Natureza_gasto.objects.filter(termo_id=self.id) \
                                     .filter(modalidade__moeda_nacional=True) \
                                     .filter(~Q(modalidade__sigla='REI')) \
                                     .aggregate(Sum('valor_concedido'))

        total = soma['valor_concedido__sum'] or Decimal('0.00')

        return total

    # Formata o valor do atributo real.
    def termo_real(self):
        if self.real > 0:
            return '<b>R$ %s</b>' % (formata_moeda(self.real, ','))
        return '-'
    termo_real.allow_tags = True
    termo_real.short_description = _(u'Concessão  sem REI')

    # Retorna a soma das naturezas (dolar) de um termo.
    @property
    def dolar(self):
        # for ng in self.natureza_gasto_set.all():
        #     if ng.modalidade.moeda_nacional == False:
        #         total += ng.valor_concedido

        soma = Natureza_gasto.objects.filter(termo_id=self.id) \
                                     .filter(modalidade__moeda_nacional=False) \
                                     .aggregate(Sum('valor_concedido'))
        total = soma['valor_concedido__sum'] or Decimal('0.00')

        return total

    # Formata o valor do atributo tdolar.
    def termo_dolar(self):
        if self.dolar > 0:
            return '$ %s' % (formata_moeda(self.dolar, '.'))
        return '-'
    termo_dolar.short_description = _(u'Concessão')

    @cached_property
    def termino(self):
        termino = datetime.date.min

        for pedido in self.outorga_set.all():
            if pedido.termino > termino:
                termino = pedido.termino

        return termino

    # Duracao do termo como um 'timedelta'
    def duracao(self):
        if self.termino is not None and self.inicio is not None:
            return self.termino - self.inicio
        else:
            return None

    # Calcula os meses de duração do processo a partir dos dados do modelo Outorga
    def duracao_meses(self):
        dif = self.duracao()
        if dif is not None:
            meses = dif.days / 30
            if dif.days % 30 >= 28:
                meses += 1

            if meses > 0:
                if meses > 1:
                    return u"%s meses" % meses
                return u"%s mês" % meses
            return u'-'
        else:
            return u'-'
    duracao_meses.short_description = _(u'Vigência')

    # Calcula total de despesas (R$) realizadas durante a outorga
    @property
    def total_realizado_real(self):
        from financeiro.models import Pagamento
        total = Pagamento.objects.filter(origem_fapesp__item_outorga__natureza_gasto__modalidade__moeda_nacional=True,
                                         origem_fapesp__item_outorga__natureza_gasto__termo=self)\
            .aggregate(Sum('valor_fapesp'))
        return total['valor_fapesp__sum'] or Decimal('0.0')

    # Retorna o total de despesas (R$) em formato moeda.
    def formata_realizado_real(self):
        if not self.total_realizado_real:
            return '-'

        valor = formata_moeda(self.total_realizado_real, ',')
        if self.real < self.total_realizado_real:
            return '<span style="color: red"><b>R$ %s</b></span>' % valor
        return '<b>R$ %s</b>' % valor
    formata_realizado_real.allow_tags = True
    formata_realizado_real.short_description = _(u'Realizado')

    # Calcula total de despesas ($) realizadas durante o termo.
    @property
    def total_realizado_dolar(self):
        total = Decimal('0.00')
        for n in self.natureza_gasto_set.all().select_related('modalidade'):
            if not n.modalidade.moeda_nacional:
                total += n.total_realizado
        return total

    # Retorna o total de despesas ($) em formato moeda.
    def formata_realizado_dolar(self):
        if not self.total_realizado_dolar:
            return '-'

        valor = formata_moeda(self.total_realizado_dolar, '.')
        if self.dolar < self.total_realizado_dolar:
            return '<span style="color: red">$ %s</span>' % valor
        return '$ %s' % valor
    formata_realizado_dolar.allow_tags = True
    formata_realizado_dolar.short_description = _(u'Realizado')

    def saldo_real(self):
        return self.real - self.total_realizado_real

    def saldo_dolar(self):
        return self.dolar - self.total_realizado_dolar

    def formata_saldo_real(self):
        return '<b>R$ %s</b>' % formata_moeda(self.saldo_real(), ',')
    formata_saldo_real.allow_tags = True
    formata_saldo_real.short_description = _(u'Saldo')

    def formata_saldo_dolar(self):
        return '$ %s' % formata_moeda(self.saldo_dolar(), '.')
    formata_saldo_dolar.short_description = _(u'Saldo')

    # Define atributos.
    vigencia = property(duracao_meses)
    num_processo = property(__unicode__)

    # Define a descrição do modelo (singular e plural), a ordenação dos dados pelo ano.
    class Meta:
        verbose_name = _(u'Termo de Outorga')
        verbose_name_plural = _(u'Termos de Outorga')
        ordering = ("-ano", "-processo")

    @classmethod
    def termo_ativo(cls):
        hoje = datetime.datetime.now().date()
        for t in Termo.objects.order_by('-inicio'):
            if t.inicio <= hoje <= t.termino:
                return t

        return None

    def insere_itens_rt(self):
        for irt in TemplateRT.objects.all():
            (p, b) = Natureza_gasto.objects.get_or_create(termo=self, modalidade=irt.modalidade,
                                                          defaults={'valor_concedido': 0.0})
            item = Item()
            item.natureza_gasto = p
            item.descricao = irt.descricao
            item.justificativa = ' '
            item.valor = 0.0
            item.quantidade = 1
            item.rt = True
            item.save()


class Categoria(models.Model):
    """
    Uma instância dessa classe representa um tipo de categoria de um pedido de concessão.

    O método '__unicode__'	Retorna o campo 'nome'.
    A class 'Meta'		Define a ordenação dos dados pelo nome.
    """
    nome = models.CharField(_(u'Nome'), max_length=60, help_text=_(u'ex. Aditivo'), unique=True)

    # Retorna o nome da Categoria
    def __unicode__(self):
        return u'%s' % self.nome

    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('nome', )


class Outorga(models.Model):

    """
    Uma instância dessa classe representa um pedido de concessão.

    O método '__unicode__'		Retorna o termo e a categoria do pedido de concessão.
    O método 'inicio'			Retorna a data de início do termo.
    O método 'mostra_categoria'		Retorna o nome da categoria.
    O método 'mostra_termo'		Retorna o termo.
    O método 'existe_arquivo'		Retorna um ícone com link para consulta dos arquivos anexados.
    A class 'Meta'			Define a descrição do modelo (singular e plural) e a ordenação dos dados pela
    data de solicitação.
    """
    categoria = models.ForeignKey('outorga.Categoria', verbose_name=_(u'Categoria'))
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo'))
    termino = NARADateField(_(u'Término'), help_text=_(u'Término da vigência do processo'))
    obs = models.TextField(_(u'Observação'), blank=True)
    data_presta_contas = NARADateField(_(u'Prest. Contas'), blank=True, null=True,
                                       help_text=_(u'Data de Prestação de Contas'))
    data_solicitacao = NARADateField(_(u'Solicitação'), help_text=_(u'Data de Solicitação do Pedido de Concessão'))
    arquivo = models.FileField(upload_to=upload_dir, null=True, blank=True)
    protocolo = models.FileField(upload_to=upload_dir, null=True, blank=True)

    # Retorna o termo e a categoria.
    def __unicode__(self):
        return u'%s - %s' % (self.termo.num_processo, self.categoria.nome)

    # Início do processo
    @ property
    def inicio(self):
        return self.termo.inicio.strftime("%d/%m/%Y")
    # inicio.short_description = _(u'Início')

    # Retorna a categoria.
    def mostra_categoria(self):
        return self.categoria.nome
    mostra_categoria.short_description = _(u'Categoria')

    # Retorna o termo.
    def mostra_termo(self):
        return self.termo.num_processo
    mostra_termo.short_description = _(u'Termo')

    # Retorna um ícone se o pedido de concessão tiver arquivos.
    def existe_arquivo(self):
        a = '<center><a href="%s?outorga__id__exact=%s">' \
            '<img src="%simg/arquivo.png" /></a></center>' \
            % (urlresolvers.reverse('admin:outorga_arquivo_changelist'), self.id, settings.STATIC_URL)
        if self.arquivo:
            return a
        return ' '
    existe_arquivo.allow_tags = True
    existe_arquivo.short_description = _(u'Arquivo')

    # Define a descrição do modelo e a ordenação dos dados pelo termo.
    class Meta:
        verbose_name = _(u'Concessão')
        verbose_name_plural = _(u'Histórico de Concessões')
        ordering = ('data_solicitacao', )


class Natureza_gasto(models.Model):

    """
    Uma instância dessa classe representa a conexão de uma modalidade a um pedido de concessão.

    O método '__unidode__'		Retorna o termo, a categoria do pedido de concessão e o nome da modalidade.
    O método 'mostra_termo'		Retorna o termo.
    O método 'mostra_modalidade'	Retorna o nome da modalidade.
    O método 'get_absolute_url'		Retorna a URL de uma natureza de gasto.
    O método 'formata_valor'		Retorna um valor em formato moeda conforme a moeda especificada no modelo
    Modalidade.
    O atributo 'total_realizado'	Retorna o total das despesas realizadas associadas a uma modalidade e termo.
    O método 'formata_total_realizado'	Retorna o atributo 'total_realizado' em formato moeda.
    O método 'soma_itens'		Retorna a soma dos itens da natureza de gasto de um pedido de concessão e marca em
    vermelho se for diferente do valor_concedido.
    O método 'todos_itens'		Retorna os itens que não estão subordinados a outro item, considerando todos os
    pedidos de uma determinada modalidade e termo.
    O método 'v_concedido' 		Retorna o valor do campo 'valor_concedido' em formato de moeda e marca em vermelho se
    o valor concedido for diferente do total dos itens.
    A class 'Meta' 			Define a descrição do modelo (singular e plural) e a ordem de apresentação dos dados pela
    data de solicitação do pedido de concessão.
    """
    modalidade = models.ForeignKey('outorga.Modalidade', verbose_name=_(u'Modalidade'))
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo de outorga'))
    valor_concedido = models.DecimalField(_(u'Valor Concedido'), max_digits=12, decimal_places=2,
                                          help_text=_(u'ex. 150500.50'))
    obs = models.TextField(_(u'Observação'), blank=True)

    # Retorna o pedido de concessão e a sigla da modalidade.
    def __unicode__(self):
        return u'%s - %s' % (self.mostra_termo(), self.modalidade.sigla)

    # Retorna o Termo do pedido de concessão.
    def mostra_termo(self):
        return '%s' % self.termo.num_processo
    mostra_termo.short_description = _(u'Termo')

    # Retorna a modalidade da Natureza do Gasto.
    def mostra_modalidade(self):
        return u'%s' % self.modalidade.sigla
    mostra_modalidade.short_description = _(u'Modalidade')

    # Retorna a URL de uma natureza de gasto.
    def get_absolute_url(self):
        return urlresolvers.reverse('admin:outorga_natureza_gasto_change', args=(self.id,))

    # Formata um valor em formato moeda conforme campo 'moeda_nacional' do modelo 'Modalidade'.
    def formata_valor(self, v):
        if self.modalidade.moeda_nacional:
            moeda = 'R$'
            sep_decimal = ','
        else:
            moeda = '$'
            sep_decimal = '.'
        return moeda + ' ' + formata_moeda(v, sep_decimal)

    # Calcula o total de despesas realizadas de uma modalidade e termo.
    @cached_property
    def total_realizado(self):
        return self.total_realizado_rt()

    def total_realizado_rt(self, rt=None):
        total = Decimal('0.00')
        for item in self.todos_itens(rt=rt):
            total += item.valor_realizado_acumulado
        return total

    def total_realizado_parcial(self, m1, a1, m2, a2, rt=0, parcial=0):
        from financeiro.models import Pagamento

        inicio = datetime.date(a1, m1, 1)
        fim = datetime.date(a2, m2, 28)
        while True:
            try:
                fim = fim.replace(day=fim.day+1)
            except:
                break

        pagamentos = Pagamento.objects.all()
        if parcial > 0:
            pag_ids = [p.id for p in pagamentos.filter(auditoria__parcial=parcial).distinct()]
            pagamentos = pagamentos.filter(id__in=pag_ids)
        if rt == 1:
            pagamentos = pagamentos.filter(origem_fapesp__item_outorga__rt=True)
        elif rt == 2:
            pagamentos = pagamentos.filter(origem_fapesp__item_outorga__rt=False)
        if self.modalidade.moeda_nacional:
            total = pagamentos.filter(conta_corrente__data_oper__range=(inicio, fim),
                                      origem_fapesp__item_outorga__natureza_gasto=self).aggregate(Sum('valor_fapesp'))
        else:
            total = pagamentos.filter(protocolo__data_vencimento__range=(inicio, fim),
                                      origem_fapesp__item_outorga__natureza_gasto=self).aggregate(Sum('valor_fapesp'))
        return total['valor_fapesp__sum'] or Decimal('0.00')

    # Retorna o total de despesas realizadas em formato moeda.
    def formata_total_realizado(self):
        if not self.total_realizado:
            return '-'

        if self.valor_concedido < self.total_realizado:
            return '<span style="color: red">%s</span>' % self.formata_valor(self.total_realizado)
        return self.formata_valor(self.total_realizado)
    formata_total_realizado.allow_tags = True
    formata_total_realizado.short_description = _(u'Total Realizado')

    # Calcula a soma de todos os itens da natureza do gasto e marca em vermelho
    # se o valor for diferente do valor_concedido.
    def soma_itens(self):
        total = Decimal('0.00')
        for item in self.item_set.all():
            total += item.valor

        if self.valor_concedido != total != 0:
            return '<span style="color: red">%s</span>' % (self.formata_valor(total))

        if total != 0:
            return self.formata_valor(total)
        return '-'
    soma_itens.allow_tags = True
    soma_itens.short_description = _(u'Total dos Itens')

    # Retorna todos os itens de uma natureza de gasto que não estão subordinados a outro item,
    # considerando todas as concessões de um determinado Termo.
    def todos_itens(self, rt=None):
        itens = Item.objects.filter(natureza_gasto__modalidade=self.modalidade,
                                    natureza_gasto__termo=self.termo)
        if rt is not None:
            itens = itens.filter(rt=rt)
        return itens

    # Retorna a soma do valor total concedido considerando todas as naturezas de gasto de uma modalidade e Termo.
    def total_concedido_mod_termo(self):
        total = Decimal('0.00')
        for ng in Natureza_gasto.objects.filter(modalidade=self.modalidade, termo=self.termo):
            total += ng.valor_concedido
        return self.formata_valor(total)
    total_concedido_mod_termo.short_description = _(u'Total concedido para a Modalidade')

    # Formata o valor do atributo 'valor_concedido'
    def v_concedido(self):
        if self.valor_concedido or self.valor_concedido == 0:
            return self.formata_valor(self.valor_concedido)
        return '-'
    v_concedido.short_description = _(u'Valor Concedido')

    def saldo(self):
        if self.total_realizado > self.valor_concedido:
            return '<span style="color: red">%s</span>' % \
                   self.formata_valor(self.valor_concedido - self.total_realizado)
        return self.formata_valor(self.valor_concedido - self.total_realizado)
    saldo.allow_tags = True

    def valor_saldo(self):
        return self.valor_concedido - self.total_realizado

    # Define a descrição e a ordenação dos dados pelo Termo de Outorga.
    class Meta:
        verbose_name = _(u'Pasta')
        verbose_name_plural = _(u'Pastas')
        ordering = ('-termo__ano', )
        unique_together = ('modalidade', 'termo',)
        # ordering = ('-outorga__data_solicitacao', )


class TemplateRT(models.Model):
    modalidade = models.ForeignKey('outorga.Modalidade')
    descricao = models.CharField(_(u'Descrição'), max_length=255)

    def __unicode__(self):
        return u'%s - %s' % (self.modalidade, self.descricao)

    class Meta:
        verbose_name = u'Template Reserva Técnica'
        verbose_name_plural = u'Templates Reserva Técnica'


class Item(models.Model):
    """
    Uma instância dessa classe representa um item de um pedido de concessão.

    O método '__unicode__'			Retorna a descrição do item.
    O método 'mostra_termo'			Retorna o termo.
    O método 'mostra_descricao'			Retorna a descrição do item.
    O método 'mostra_concessao'			Retorna a categoria do pedido de concessão.
    O método 'mostra_modalidade'		Retorna a sigla da modalidade.
    O método 'mostra_solicitação'		Retorna a data de solicitação do pedido de concessão no formato dd/mm/aa.
    O método 'mostra_termino'			Retorna a data de término do pedido de concessão no formato dd/mm/aa.
    O atributo 'valor' 				Calcula o valor total do item (quantidade * valor unitário).
    O método 'mostra_valor'			Retorna o atributo 'valor' em formato moeda.
    O método 'mostra_valor_unit'		Retorna o campo 'valor_unit' em formato moeda.
    O método 'mostra_quantidade'		Retorna o campo 'quantidade'.
    O método 'calcula_total_despesas'		Retorna a soma das fontespagadoras 'fapesp' referentes a um item.
    O atributo 'valor_realizado_acumulado' 	Foi definido para retornar o método 'calcula_total_despesa'.
    O método 'mostra_valor_realizado'		Retorna o atributo 'valor_realizado_acumulado' em formato moeda.
    A class 'Meta'				Define a descrição do modelo (singular e plural) e a ordenação dos dados pela
     data de solicitação do pedido de concessão.
    """

    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Entidade'), null=True)
    natureza_gasto = models.ForeignKey('outorga.Natureza_gasto', verbose_name=_(u'Pasta'))
    descricao = models.CharField(_(u'Descrição'), max_length=255,
                                 help_text=_(u'ex. Locação e armazenamento especializado na Granero Tech.'))
    justificativa = models.TextField(_(u'Justificativa'))
    quantidade = models.IntegerField(_(u'Quantidade'))
    obs = models.TextField(_(u'Observação'), blank=True)
    valor = models.DecimalField(_(u'Valor Concedido'), max_digits=12, decimal_places=2, help_text=_(u'ex. 150500.50'))
    rt = models.BooleanField(u'Reserva técnica?', default=False)

    # Retorna a descrição e o termo, se existir.
    def __unicode__(self):
        return u'%s - %s' % (self.natureza_gasto.termo, self.descricao)

    # Retorna o Termo se o pedido de concessão estiver conectado a um termo.
    def mostra_termo(self):
        return u'%s' % self.natureza_gasto.mostra_termo()
    mostra_termo.short_description = _(u'Termo')

    # Retorna a descrição do item do pedido de concessão.
    def mostra_descricao(self):
        return u'%s' % self.descricao
    mostra_descricao.short_description = _(u'Descrição')

    # Retorna a modalidade do Item do Pedido de Concessão.
    def mostra_modalidade(self):
        return u'%s' % self.natureza_gasto.modalidade.sigla
    mostra_modalidade.short_description = _(u'Mod')

    # Retorna a quantidade.
    def mostra_quantidade(self):
        if self.quantidade > 0:
            return self.quantidade
        return '-'
    mostra_quantidade.short_description = _(u'Qtde')

    # Calcula o valor total realizado de um determinado item.
    def calcula_total_despesas(self):
        from financeiro.models import Pagamento

#         if hasattr(self, 'origemfapesp_set'):
#             for of in self.origemfapesp_set.all():
#                 sumFapesp = of.pagamento_set.all().aggregate(Sum('valor_fapesp'))
#                 total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')

        sumFapesp = Pagamento.objects.filter(origem_fapesp__item_outorga_id=self.id).aggregate(Sum('valor_fapesp'))
        total = sumFapesp['valor_fapesp__sum'] or Decimal('0.0')

        return total
    # Define um atributo com o valor total realizado
    valor_realizado_acumulado = property(calcula_total_despesas)

    # Valor realizado por mês
    # dt = mes/ano para o filtro inicial
    # after = flag que especifica se o dt deve levar em conta a data cheia (dia/mes/ano)
    def calcula_realizado_mes(self, dt, after=False, pagamentos=None):
        total = Decimal('0.00')
        if pagamentos:
            if after:
                if self.natureza_gasto.modalidade.moeda_nacional:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga=self, conta_corrente__data_oper__gte=dt)\
                        .aggregate(Sum('valor_fapesp'))
                else:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga=self, protocolo__data_vencimento__gte=dt)\
                        .aggregate(Sum('valor_fapesp'))
            else:
                if self.natureza_gasto.modalidade.moeda_nacional:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga=self,
                                                  conta_corrente__data_oper__month=dt.strftime('%m'),
                                                  conta_corrente__data_oper__year=dt.strftime('%Y'))\
                        .aggregate(Sum('valor_fapesp'))
                else:
                    sumFapesp = pagamentos.filter(origem_fapesp__item_outorga=self,
                                                  protocolo__data_vencimento__month=dt.strftime('%m'),
                                                  protocolo__data_vencimento__year=dt.strftime('%Y'))\
                        .aggregate(Sum('valor_fapesp'))
            total = sumFapesp['valor_fapesp__sum'] or Decimal('0.0')
        elif hasattr(self, 'origemfapesp_set'):
            for of in self.origemfapesp_set.all():
                if after:
                    if self.natureza_gasto.modalidade.moeda_nacional:
                        sumFapesp = of.pagamento_set.filter(conta_corrente__data_oper__gte=dt)\
                            .aggregate(Sum('valor_fapesp'))
                    else:
                        sumFapesp = of.pagamento_set.filter(protocolo__data_vencimento__gte=dt)\
                            .aggregate(Sum('valor_fapesp'))
                else:
                    if self.natureza_gasto.modalidade.moeda_nacional:
                        sumFapesp = of.pagamento_set.filter(conta_corrente__data_oper__month=dt.strftime('%m'),
                                                            conta_corrente__data_oper__year=dt.strftime('%Y'))\
                            .aggregate(Sum('valor_fapesp'))
                    else:
                        sumFapesp = of.pagamento_set.filter(protocolo__data_vencimento__month=dt.strftime('%m'),
                                                            protocolo__data_vencimento__year=dt.strftime('%Y'))\
                            .aggregate(Sum('valor_fapesp'))
                total += sumFapesp['valor_fapesp__sum'] or Decimal('0.0')
        return total

    # Mostra o valor realizado acumulado formatado conforme a moeda da modalidade
    def mostra_valor_realizado(self):
        if not self.valor_realizado_acumulado:
            return '-'

        total = self.natureza_gasto.formata_valor(self.valor_realizado_acumulado)
        # if self.valor_realizado_acumulado > self.valor:
        #    return '<span style="color: red">%s</span>' % (total)
        return total
    mostra_valor_realizado.allow_tags = True
    mostra_valor_realizado.short_description = _(u'Total Realizado')

    def saldo(self):
        if self.valor:
            if self.valor_realizado_acumulado:
                return self.valor - self.valor_realizado_acumulado
            else:
                return self.valor
        else:
            return - self.valor_realizado_acumulado

    # Pagina com todos os protocolos ligados a este item
    def protocolos_pagina(self):
        return '<a href="%s?fontepagadora__origem_fapesp__item_outorga__id=%s">Despesas</a>' \
               % (urlresolvers.reverse('admin:protocolo_protocolo_changelist'), self.id)
    protocolos_pagina.short_description = _(u'Lista de despesas')
    protocolos_pagina.allow_tags = True

    def pagamentos_pagina(self):
        return '<a href="%s?origem_fapesp__item_outorga=%s">Despesas</a>' \
               % (urlresolvers.reverse('admin:financeiro_pagamento_changelist'), self.id)
    pagamentos_pagina.short_description = _(u'Lista de pagamentos')
    pagamentos_pagina.allow_tags = True

    # Define a descrição (singular e plural) e a ordenação pela data de solicitação do pedido de concessão.
    class Meta:
        verbose_name = _(u'Item do Orçamento')
        verbose_name_plural = _(u'Itens do Orçamento')
        ordering = ('natureza_gasto__termo', 'descricao')


class Arquivo(models.Model):
    """
    Uma instância dessa classe representa um arquivo de um pedido de concessão.

    O método '__unicode__'	Retorna o nome do arquivo.
    O método 'concessao'	Retorna o método '__unicode__' do modelo Outorga.
    A class 'Meta'		Define a ordenação dos dados pelo 'id' e a unicidade dos dados pelos campos 'arquivo' e 'outorga'.
    """
    arquivo = models.FileField(upload_to=upload_dir)
    outorga = models.ForeignKey('outorga.Outorga', related_name='arquivos')

    # Retorna o nome do arquivo.
    def __unicode__(self):
        if self.arquivo.name.find('/') == -1:
            return u'%s' % self.arquivo.name
        else:
            return u'%s' % self.arquivo.name.split('/')[-1]

    # Retorna o pedido de concessão.
    def concessao(self):
        return self.outorga
    concessao.short_description = _(u'Pedido de Concessão')

    # Retorna o termo do pedido de concessão.
    def mostra_termo(self):
        return self.outorga.mostra_termo()
    mostra_termo.short_description = _(u'Termo')

    # Define a ordenação dos dados e a unicidade dos dados.
    class Meta:
        ordering = ('id', )
        unique_together = ('arquivo', 'outorga')


class Acordo(models.Model):
    """
    Acordos como, por exemplo, entre a ANSP e a Telefônica.

    O método '__unicode__'	Retorna a descrição do acordo.
    """
    estado = models.ForeignKey('outorga.Estado')
    descricao = models.TextField(verbose_name=_(u'Descrição'))
    itens_outorga = models.ManyToManyField('outorga.Item', through='outorga.OrigemFapesp')

    # Retorna a descrição.
    def __unicode__(self):
        return u"%s" % self.descricao

    class Meta:
        ordering = ('descricao',)


class OrigemFapesp(models.Model):
    """
    Uma instância dessa classe representa a associação de uma acordo a um item da Outorga
    """

    acordo = models.ForeignKey('outorga.Acordo')
    item_outorga = models.ForeignKey('outorga.Item', verbose_name=_(u'Item de Outorga'))

    # Retorna o acordo e o item de Outorga da Origem FAPESP.
    def __unicode__(self):
        return u"%s - %s - %s" % (self.acordo, self.item_outorga.natureza_gasto.modalidade.sigla, self.item_outorga)

    # Define a descrição do modelo.
    class Meta:
        verbose_name = _(u'Origem FAPESP')
        verbose_name_plural = _(u'Origem FAPESP')
        ordering = ('item_outorga',)

    def gasto(self):
        g = self.pagamento_set.all().aggregate(Sum('valor_fapesp'))
        return g['valor_fapesp__sum'] or Decimal('0.0')

    def termo(self):
        return self.item_outorga.natureza_gasto.termo


class Contrato(models.Model):
    """
    Uma instância dessa classe representa um contrato. (Ex. Instituto Uniemp e Telefônica)
    """
    numero = models.CharField(_(u'Número'), max_length=20)
    descricao = models.TextField(_(u'Descrição'), blank=True)
    data_inicio = NARADateField(_(u'Início'))
    auto_renova = models.BooleanField(_(u'Auto renovação?'), default=False)
    limite_rescisao = NARADateField(_(u'término'), null=True, blank=True)
    entidade = models.ForeignKey('identificacao.Entidade')
    anterior = models.ForeignKey('outorga.Contrato', verbose_name=_('Contrato anterior'), null=True, blank=True)
    arquivo = models.FileField(upload_to='contrato')

    # Retorna a entidade e a data de ínicio do Contrato.
    def __unicode__(self):
        inicio = self.data_inicio.strftime("%d/%m/%Y")
        return u"%s - %s" % (self.entidade, inicio)

    # Retorna um ícone se o contrato tiver anexo.
    def existe_arquivo(self):
        if self.arquivo and self.arquivo.name.find('/') >= 0:
            a = '<center><a href="%s"><img src="%simg/arquivo.png" /></a></center>'\
                % (self.arquivo.url, settings.STATIC_URL)
            return a
        return ' '
    existe_arquivo.allow_tags = True
    existe_arquivo.short_description = _(u'Arquivo')


class TipoContrato(models.Model):
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u'Tipo de documento'
        verbose_name_plural = u'Tipos de documento'
        ordering = ('nome',)


class EstadoOS(models.Model):
    nome = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ('nome',)
        verbose_name = 'Estado da OS'
        verbose_name_plural = 'Estados das OSs'


class OrdemDeServico(models.Model):
    """
    Uma instância dessa classe representa uma ordem de serviço de um Contrato.

    arquivos: related_name para ArquivoOS
    """
    numero = models.CharField(_(u'Número'), max_length=20)
    tipo = models.ForeignKey('outorga.TipoContrato')
    acordo = models.ForeignKey('outorga.Acordo')
    contrato = models.ForeignKey('outorga.Contrato')
    data_inicio = NARADateField(_(u'Início'))
    data_rescisao = NARADateField(_(u'Término'), null=True, blank=True)
    antes_rescisao = models.IntegerField(_(u'Prazo p/ solicitar rescisão (dias)'), null=True, blank=True)
    descricao = models.TextField(_(u'Descrição'))
    # arquivo = models.FileField(upload_to='OS', null=True, blank=True)
    estado = models.ForeignKey('outorga.EstadoOS')
    pergunta = models.ManyToManyField('memorando.Pergunta', null=True, blank=True)
    substituicoes = models.TextField(null=True, blank=True)

    # Retorna a descrição.
    def __unicode__(self):
        return u"%s %s" % (self.tipo, self.numero)

    # Retorna o prazo para solicitar recisão (campo 'antes_rescisao').
    def mostra_prazo(self):
        if self.antes_rescisao < 1:
            return '-'
        if self.antes_rescisao > 1:
            return u'%s dias' % self.antes_rescisao
        return u'%s dias' % self.antes_rescisao
    mostra_prazo.short_description = _(u'Prazo p/ rescisão')

    def entidade(self):
        return self.contrato.entidade

    def primeiro_arquivo(self):
        if self.arquivos.all().exists():
            osf = self.arquivos.all()[:1].get()
            return osf.arquivo
        return None

    class Meta:
        verbose_name = _(u'Alteração de contrato (OS)')
        verbose_name_plural = _(u'Alteração de contratos (OS)')
        ordering = ('tipo', 'numero')


class ArquivoOS(models.Model):
    """
    Arquivos de ordem de serviço
    """
    arquivo = models.FileField(upload_to=upload_dir_os)
    data = models.DateField()
    historico = models.TextField()
    os = models.ForeignKey('outorga.OrdemDeServico', related_name='arquivos')

    def __unicode__(self):
        if self.arquivo.name.find('/') == -1:
            return u'%s' % self.arquivo.name
        else:
            return u'%s' % self.arquivo.name.split('/')[-1]


# Classe para definição de permissões de views e relatórios da app patrimonio
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_ger_acordo_progressivo", "Rel. Ger. - Gerencial progressivo"),    # /outorga/relatorios/acordo_progressivo
            ("rel_ger_contratos", "Rel. Ger. - Contratos"),     # /outorga/relatorios/contratos
            ("rel_adm_item_modalidade", "Rel. Adm. - Itens do orçamento por modalidade"),    # /outorga/relatorios/item_modalidade
            ("rel_ger_lista_acordos", "Rel. Ger. - Concessões por acordo"),     # /outorga/relatorios/lista_acordos
        )
