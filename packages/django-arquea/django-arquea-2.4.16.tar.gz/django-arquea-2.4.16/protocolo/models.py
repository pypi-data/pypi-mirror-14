# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.templatetags.static import static

from identificacao.models import Entidade
from utils.functions import formata_moeda

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class TipoDocumento(models.Model):
    """
    Uma instância dessa classe representa um tipo de protocolo que pode ser: nota fiscal, fatura, cotação, entre outros.

    O método '__unicode__'	Retorna o nome quando um objeto dessa classe for solicitado.
    A class 'Meta' 		Define a descrição do modelo (singular e plural) e a ordenação da visualização dos dados pelo
    nome.
    """

    nome = models.CharField(_('Nome'), max_length=100, help_text='ex. Nota Fiscal', unique=True)
    sigla = models.CharField(max_length=10)

    # Define a descrição do modelo (singular e plural) e a ordenação dos dados.
    class Meta:
        verbose_name = _('Tipo de documento')
        verbose_name_plural = _('Tipos de documento')
        ordering = ('nome', )

    # Retorna o nome
    def __unicode__(self):
        return self.nome


class Estado(models.Model):
    """
    Uma instância dessa classe representa um estado de um objeto que pode ser: pago, pendente, arquivado entre outros.

    O método '__unicode__'	Retorna o nome quando um objeto dessa classe for solicitado.
    A classe 'Meta' 		Define a ordenação da visualização dos dados pelo campo 'nome'.
    """

    nome = models.CharField(_('Nome'), max_length=30, help_text='ex. Pendente', unique=True)

    # Retorna o nome.
    def __unicode__(self):
        return self.nome

    # Define a ordenação dos dados.
    class Meta:
        ordering = ('-nome', )


class Origem(models.Model):

    """
    Uma instância dessa classe representa uma origem do protocolo que pode ser: correio, e-mail entre outros.

    O método '__unicode__'	Retorna o nome quando um objeto dessa classe for solicitado.
    A classe 'Meta'		Define a descrição do modelo (singular e plural) e a ordenação da visualização dos dados pelo nome.

    >>> og, created = Origem.objects.get_or_create(nome='E-mail')

    >>> og.__unicode__()
    'E-mail'
    """
    nome = models.CharField(_('Nome'), max_length=20, help_text='ex. Correio', unique=True)

    # Retorna o nome.
    def __unicode__(self):
        return self.nome

    # Define a descrição do modelo (singular e plural) e a ordenação dos dados.
    class Meta:
        ordering = ('nome', )
        verbose_name = _('Origem')
        verbose_name_plural = _('Origens')


class TipoFeriado(models.Model):
    nome = models.CharField(max_length=45)
    movel = models.BooleanField(u'Móvel', default=False)
    dia = models.IntegerField(_(u'Dia'), null=True, blank=True)
    mes = models.IntegerField(_(u'Mes'), null=True, blank=True)
    subtrai_banco_hrs = models.BooleanField(_(u'Subtrai do banco de horas?'), default=False)

    def __unicode__(self):
        return self.nome


class Feriado(models.Model):

    CACHE_KEY_FERIADOS = 'model_protocolo__feriados'

    """
    Uma instância desta classe diz que essa data é um feriado. Caso seja móvel,
    vale apenas para o ano colocado, caso não seja, essa data é feriado em todos
    os anos.

    O método '__unicode__' 		Retorna a data do feriado nos formatos dd/mm/aa ou dd/mm dependendo do campo 'movel'.
    O método da classe 'dia_de_feriado'	Verifica se uma data é feriado.
    A classe 'Meta' 			Define a ordenação dos dados pelo campo 'feriado'.
    """
    feriado = models.DateField(_('Feriado'), unique=True)
    obs = models.CharField(_(u'Observação'), max_length=100, blank=True)
    tipo = models.ForeignKey('protocolo.TipoFeriado', null=True, blank=True)
    # movel = models.BooleanField(_(u'Este feriado é móvel?'))

    # Retorna a data do feriado de acordo com sua classificação.
    def __unicode__(self):
        return self.feriado.strftime("%d/%m/%y")

    # Define um método da classe que verifica se uma data é feriado.
    @staticmethod
    def dia_de_feriado(data):
        feriados = cache.get(Feriado.CACHE_KEY_FERIADOS)
        if feriados is None:
            feriados = []
            for f in Feriado.objects.all():
                feriados.append(f.feriado)
            cache.set(Feriado.CACHE_KEY_FERIADOS, feriados, 600)

        return data in feriados

    @staticmethod
    def get_dia_de_feriado(data):
        feriado_existe = Feriado.dia_de_feriado(data)

        if feriado_existe:
            dm = Feriado.objects.filter(feriado=data).select_related('tipo')
            if len(dm) > 1:
                raise ValueError("Há mais de um feriado em um único dia.")

            if len(dm) == 1:
                return dm.filter()[:1].get()
        else:
            return None

    def get_movel(self):
        return self.tipo.movel
    get_movel.short_description = 'Móvel?'
    get_movel.admin_order_field = 'tipo__movel'
    get_movel.boolean = True

    def get_subtrai(self):
        return self.tipo.subtrai_banco_hrs
    get_subtrai.short_description = 'Subtrai horas?'
    get_subtrai.admin_order_field = 'tipo__subtrai_banco_hrs'
    get_subtrai.boolean = True

    # Define a ordenação da visualização dos dados.
    class Meta:
        ordering = ('feriado', )


def feriado_post_save_signal(sender, instance, **kwargs):
    # Post-save signal do Feriado para limpar o cache dos Feriados
    cache.delete(Feriado.CACHE_KEY_FERIADOS)

# Registrando o sinal
post_save.connect(feriado_post_save_signal, sender=Feriado, dispatch_uid="feriado_post_save")


class Protocolo(models.Model):

    """
    Uma instância dessa classe representa um documento cadastrado no sistema como nota fiscal,
    fatura, cotação, contrato, entre outros.

    O valor total do protocolo sera calculado através da soma de seus itens, que são instâncias da
    classe ItemProtocolo e será mostrado no formato da moeda correspondente.

    Será feita uma consulta dos pagamentos do próximo dia útil.

    O método '__unicode__' 		Retorna os campos 'termo', 'descricao', 'estado' e a data de vencimento formatada.
    O método 'mostra_termo'		Retorna o termo do protocolo.
    O método 'mostra_categoria'		Retorna a categoria do protocolo.
    O método 'mostra_estado'		Retorna o estado do protocolo.
    O método 'doc_num' 			Retorna o tipo e o número do documento.
    O método 'entidade' 		Retorna a entidade da identificação.
    O método 'recebimento' 		Retorna a data de recebimento no formato 'dd/mm/aa hh:mm'.
    O método 'validade' 		Retorna a data de validade no formato 'dd/mm/aa'.
    O método 'vencimento' 		Retorna a data de vencimento no formato 'dd/mm/aa'
    O método 'colorir' 			Marca em verde o estado dos protocolos diferentes de 'concluído'.
    O método 'pagamentos_amanhã'	Verifica se o protocolo (diferente de contrato e cotação) com estado diferente de
                                    concluído possui data de vencimento até o próximo dia útil.
    O atributo 'valor' 			Calcula a soma de todos os itens do protocolo.
    O método 'mostra valor' 		Formata o atributo 'valor' no formato de moeda conforme o campo 'moeda_estrangeira'.
    O método 'existe_arquivo' 		Retorna um ícone indicando que existe arquivo para o protocolo.
    O método 'Meta' 			Define a ordenação da visualização dos dados pelos campos 'descricao' e 'data_chegada'.
    """
    tipo_documento = models.ForeignKey('protocolo.TipoDocumento', verbose_name=_(u'Documento'),
                                       limit_choices_to=~Q(nome=u'Contrato') & ~Q(nome=u'Cotação') &
                                                        ~Q(nome=u'Ordem de Serviço'))
    origem = models.ForeignKey('protocolo.Origem', verbose_name=_(u'Origem'), null=True, blank=True)
    estado = models.ForeignKey('protocolo.Estado', verbose_name=_(u'Estado'),
                               limit_choices_to=~Q(nome=u'Anterior a vigência') & ~Q(nome=u'Expirado') &
                                                ~Q(nome=u'Prazo estourado') & ~Q(nome=u'Vigente'))
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=_(u'Identificação'), null=True)
    descricao2 = models.ForeignKey('protocolo.Descricao', verbose_name=_(u'Descrição'), null=True)
    termo = models.ForeignKey('outorga.Termo', verbose_name=_(u'Termo'))
    protocolo = models.ForeignKey('protocolo.Protocolo', verbose_name=_(u'Protocolo anterior'), related_name='anterior',
                                  null=True, blank=True)
    responsavel = models.ForeignKey(User, verbose_name=_(u'Responsável'), null=True, blank=True,
                                    help_text=_(u'Técnico responsável pelas cotações'),
                                    limit_choices_to={'groups__name': 'tecnico'})

    num_documento = models.CharField(_(u'Número'), max_length=50, blank=True,
                                     help_text=_(u'ex. 11000-69.356/10/08-00002/00003'))
    data_chegada = models.DateTimeField(_(u'Recebido em'))
    data_vencimento = models.DateField(_(u'Data de vencimento'), blank=True, null=True)
    data_validade = models.DateField(_(u'Data de validade'), blank=True, null=True,
                                     help_text=_(u'ex. Data da validade de uma cotação/contrato'))
    descricao = models.CharField(_(u'Descrição antiga'), max_length=200,
                                 help_text=_(u'ex. Conta telefônica da linha 3087-1500'), default='x-x-x')
    obs = models.TextField(_(u'Observação'), blank=True)
    moeda_estrangeira = models.BooleanField(_(u'Dólar?'), help_text=_(u'O valor do documento está em dolar?'),
                                            default=False)
    valor_total = models.DecimalField(_(u'Valor total'), max_digits=12, decimal_places=2, blank=True, null=True,
                                      help_text=_(u'É a soma dos valores dos documentos tratados por este protocolo.'))
    referente = models.CharField(_(u'Referente'), max_length=100, blank=True, null=True)
    procedencia = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Procedência'), null=True, blank=True)

    # Retorna os campos termo, descrição, estado e data de vencimento.
    def __unicode__(self):
        dt = self.data_vencimento or self.data_chegada
        return u'%s - %s %s - %s' % (dt.strftime("%d/%m"), self.tipo_documento, self.num_documento, self.mostra_valor())

    # Caso seja um pedido, exibe um link para as cotações
    def cotacoes(self):
        if self.tipo_documento.nome == 'Pedido':
            return u'<a href="/protocolo/%s/cotacoes">Cotações</a>' % self.pk
        return ''
    cotacoes.allow_tags = True
    cotacoes.short_description = _(u'Cotações')

    # Retorna a entidade.
    def entidade(self):
        if self.descricao2:
            return self.descricao2.entidade.sigla
        else:
            return ''
    entidade.short_description = _(u'Entidade')
    entidade.admin_order_field = 'descricao2'

    # Retorna o termo.
    def mostra_termo(self):
        return self.termo
    mostra_termo.short_description = _(u'Termo')

    # Retorna a categoria.
    def mostra_categoria(self):
        return self.categoria.nome
    mostra_categoria.short_description = _(u'Categoria')

    # Retorna o estado.
    def mostra_estado(self):
        return self.estado.nome
    mostra_estado.short_description = _(u'Estado')

    # Retorna o tipo e o número do documento.
    def doc_num(self):
        try:
            self.cotacao
        except Cotacao.DoesNotExist:
            return u'%s %s' % (self.tipo_documento.nome, self.num_documento)
        return ''
    doc_num.short_description = _(u'Documento')

    # Retorna a data de recebimento formatada.
    def recebimento(self):
        if timezone.is_aware(self.data_chegada):
            data_chegada = timezone.localtime(self.data_chegada)
        else:
            data_chegada = self.data_chegada
        return data_chegada.strftime("%d/%m/%y %H:%M")
    recebimento.short_description = _(u'Recebido em')

    # Retorna a data de validade formatada.
    def validade(self):
        if self.data_validade:
            return self.data_validade.strftime("%d/%m/%y")
        return ''
    validade.short_description = _(u'Validade')

    # Retorna a data de vencimento formatada.
    def vencimento(self):
        if self.data_vencimento:
            return self.data_vencimento.strftime("%d/%m/%y")
        return ''
    vencimento.short_description = _(u'Vencimento')
    vencimento.admin_order_field = 'data_vencimento'

    # Retorna a data de recebimento formatada.
    def chegada(self):
        if timezone.is_aware(self.data_chegada):
            data_chegada = timezone.localtime(self.data_chegada)
        else:
            data_chegada = self.data_chegada
        return data_chegada.strftime("%d/%m/%y")
    vencimento.short_description = _(u'Recebimento')
    vencimento.admin_order_field = 'data_chegada'

    # Marca em vermelho o estado 'pendente'.
    def colorir(self):
        if self.estado.nome.lower().startswith(u'concluído'):
            return '<span style="color: green">%s</span>' % self.estado.nome
        else:
            return self.estado.nome
    colorir.allow_tags = True
    colorir.short_description = _(u'Estado')
    colorir.admin_order_field = 'estado'

    # Verifica se a data de vencimento do protocolo diferente de 'Contrato' e 'Cotação' e com estado diferente de
    # 'concluído' será no próximo dia útil.
    def pagamentos_amanha(self):
        try:
            self.cotacao
        except Cotacao.DoesNotExist:
            if self.estado.nome.lower() != u'concluído':
                today = datetime.date.today()
                nextday = today + relativedelta(days=+1)
                while Feriado.dia_de_feriado(nextday) or nextday.weekday() > 4:
                    nextday = nextday + relativedelta(days=+1)
                if self.data_vencimento and self.data_vencimento <= nextday:
                    return True
                return False
            return False

    # Define um atributo que calcula a soma de todos os itens do protocolo.
    @property
    def valor(self):
        if self.valor_total is not None:
            return self.valor_total
        total = Decimal('0.00')
        if self.itemprotocolo_set.exists():
            for item in self.itemprotocolo_set.all():
                total += item.valor
        return total

    # Formata o atributo 'valor' conforme o campo 'moeda_estrangeira'.
    def mostra_valor(self):
        valor = self.valor

        if valor == 0:
            return '-'

        if self.moeda_estrangeira is False:
            moeda = 'R$'
            sep_decimal = ','
        else:
            moeda = '$'
            sep_decimal = '.'
        return moeda + ' ' + formata_moeda(valor, sep_decimal)
    mostra_valor.short_description = _(u'Valor')
    mostra_valor.admin_order_field = 'valor_total'

    # Retorna um ícone se o protocolo tiver arquivos.
    def existe_arquivo(self):
        a = '<center><a href="/protocolo/arquivo/?protocolo__id__exact=%s"><img src="%s" /></a></center>' % \
            (self.id, static('img/arquivo.png'))
        if self.arquivo_set.all():
            return a
        else:
            return ' '
    existe_arquivo.allow_tags = True
    existe_arquivo.short_description = _(u'Arquivo')

    # Retorna os protocolos diferentes de 'Contrato', 'Cotação' que não estão relacionadas ao modelo 'Despesa'.
    @classmethod
    def protocolos_em_aberto(cls, fp=None):
        if fp:
            prot = cls.objects.filter(~Q(estado__nome='Pago') & ~Q(estado__nome="Concluído") | Q(pk=fp.protocolo.id))
            protocolos = [p for p in prot if p != fp.protocolo]
        else:
            prot = cls.objects.exclude(estado__nome__in=['Pago', 'Concluído'])
            protocolos = [p for p in prot]

        for p in protocolos:
            fp = p.fontepagadora_set.all()
            total = Decimal('0.0')
            for f in fp:
                total += f.valor
            if p.valor <= total:
                prot = prot.exclude(pk=p.id)

        return prot

    # Retorna os protocolos diferentes de 'Contrato', 'Cotação' que não estão relacionadas ao modelo 'Despesa'.
    @classmethod
    def protocolos_termo(cls, t):
        return cls.objects.filter(Q(cotacao=None) &
                                  (Q(tipo_documento__nome='Patrimônio Herdado') | Q(tipo_documento__nome='Nota Fiscal')
                                   | Q(tipo_documento__nome='Cupom Fiscal') | Q(tipo_documento__nome='Fatura')) &
                                  Q(termo=t))

    # Define a ordenação dos dados.
    class Meta:
        ordering = ('descricao', '-data_chegada', 'data_vencimento')


class Cotacao(Protocolo):
    """
    Subclasse de protocolo, com espaço para que seja colocado o parecer técnico para a aceitação ou
    rejeição da cotação.

    O método '__unicode__' 	Retorna a entidade e a descrição.
    O método 'existe_entrega'	Retorna o campo 'entrega' se ele estiver preenchido.
    A classe 'Meta' 		Define a descrição do modelo (singular e plural) a ordenação dos dados pela data de chegada.
    """
    parecer = models.TextField(_(u'Parecer Técnico'),
                               help_text=_(u'Justificativa para aceitar ou rejeitar esta cotação'), blank=True)
    aceito = models.BooleanField(_(u'Aceito?'), help_text=_(u'Essa cotação foi aceita?'), default=False)
    entrega = models.CharField(_(u'Entrega'), max_length=20, help_text=_(u' '), blank=True)

    # Retorna a entidade e a descrição.
    def __unicode__(self):
        return u'%s - %s' % (self.identificacao.endereco.entidade, self.descricao)

    # Retorna o campo 'entrega' se existir.
    def existe_entrega(self):
        if self.entrega:
            return self.entrega
        else:
            return ' '
    existe_entrega.short_description = _(u'Entrega')

    # Define a descrição do modelo e a ordenação dos dados.
    class Meta:
        verbose_name = _(u'Cotação')
        verbose_name_plural = _(u'Cotações')
        ordering = ('-data_chegada', )


class ItemProtocolo(models.Model):
    """
    Uma instância dessa classe representa um item de um protocolo.

    Será retornado o valor total do item: quantidade * valor unitario.

    A classe 'Meta' 		Define a descrição do modelo (singular e plural) e a ordenação dos dados pelo 'id'.
    O método '__unicode__'	Retorna o protocolo e a descrição.
    O atributo 'valor' 		Calcula o valor de cada item (quantidade * valor unitário).
    """

    protocolo = models.ForeignKey('protocolo.Protocolo', verbose_name=_(u'Protocolo'))
    descricao = models.TextField(_(u'Descrição'), help_text=_(u'ex. Despesas da linha 3087-1500 ref. 10/2008'))
    quantidade = models.IntegerField(_(u'Quantidade'), help_text=_(u'ex. 1'), default=1)
    valor_unitario = models.DecimalField(_(u'Valor unitário'), max_digits=12, decimal_places=2,
                                         help_text=_(u'ex. 286.50'))
    ordem_servico = models.ForeignKey('outorga.OrdemDeServico', verbose_name=_(u'Ordem de Serviço'), null=True,
                                      blank=True)

    # Define a descrição do modelo e a ordenação dos dados.
    class Meta:
        verbose_name = _('Item do protocolo')
        verbose_name_plural = _('Itens do protocolo')
        ordering = ('id', )

    # Retorna o protocolo e a descrição
    def __unicode__(self):
        if self.descricao:
            return u'%s | %s' % (self.protocolo, self.descricao)

    # Define um atributo que calcula o valor total do item.
    @property
    def valor(self):
        return self.quantidade * Decimal(self.valor_unitario)

    # Formata o atributo 'valor' conforme o campo 'moeda_estrangeira'.
    def mostra_valor(self):
        if self.valor == 0:
            return '-'

        if self.protocolo.moeda_estrangeira is False:
            moeda = 'R$'
            sep_decimal = ','
        else:
            moeda = '$'
            sep_decimal = '.'
        return moeda + ' ' + formata_moeda(self.valor, sep_decimal)
    mostra_valor.short_description = _(u'Valor')


# class Contrato(Protocolo):
#
#     """
#     Uma subclasse de Protocolo com alguns campos específicos como datas de início e término.
#
#     O método '__unicode__'	Retorna a sigla da entidade da indentificação e o número da OS.
#     O método 'formata_inicio'	Retorna a data de início no formato dd/mm/aa.
#     A classe 'Meta' 		Define a ordenação dos dados pelo campo 'data_vencimento'.
#     O método 'estado_contrato' 	Define o estado do contrato e marca em vermelho se for diferente de 'Vigente'.
#     O método 'formata_recisao' 	Retorna o campo 'limite_recisao' formatado em meses.
#     O método 'formata_periodo' 	Retorna o campo 'periodo_renova' formatado em meses.
#
#     >>> from identificacao.models import Contato, Entidade, Identificacao
#     >>> from membro.models import Membro
#     >>> from outorga.models import Termo
#
#     >>> import datetime
#
#     >>> td, created = TipoDocumento.objects.get_or_create(nome='Nota fiscal')
#
#     >>> e, created = Estado.objects.get_or_create(nome='Aprovado')
#
#     >>> c, created = Contato.objects.get_or_create(nome='Joao', defaults={'email': 'joao@joao.com.br', 'tel': ''})
#
#     >>> og, created = Origem.objects.get_or_create(nome='Fax')
#
#     >>> mb, created = Membro.objects.get_or_create(nome='Gerson Gomes', funcionario=True,
#         defaults={'cargo': 'Outorgado', 'email': 'gerson@gomes.com', 'cpf': '000.000.000-00'})
#
#     >>> t, created = Termo.objects.get_or_create(ano=2008, processo=52885, digito=8,
#         defaults={'data_concessao': datetime.date(2008,1,1), 'data_assinatura': datetime.date(2009,1,15),
#                   'membro': mb})
#
#     >>> ent, created = Entidade.objects.get_or_create(sigla='SAC',
#         defaults={'nome': 'Global Crossing', 'ativo':False, 'fisco':True, 'cnpj': '',
#                   'url': 'www.globalcrossing.com', 'asn': 123})
#
#     >>> iden, created = Identificacao.objects.get_or_create(entidade=ent, contato=c,
#         defaults={'funcao': 'Tecnico', 'area': '', 'ativo': True})
#
#     >>> cont = Contrato(termo=t, tipo_documento=td, num_documento=2008, estado=e, identificacao=iden,
#         data_chegada=datetime.datetime(2008,9,30,10,10), data_validade=datetime.date(2009,8,25),
#         data_vencimento=datetime.date(2008,9,30), descricao="Link internacional", origem=og, valor_total=None,
#         data_inicio=datetime.date(2008,01,01), limite_recisao=3, auto_renova=True, periodo_renova=12)
#     >>> cont.save()
#
#     >>> cont.__unicode__()
#     'SAC'
#
#     >>> cont.formata_inicio()
#     '01/01/08'
#
#     >>> cont.estado_contrato()
#     '<span style="color: red">Expirado</span>'
#
#     >>> cont.data_vencimento = datetime.date.today()
#     >>> cont.save()
#
#     >>> cont.estado_contrato()
#     '<span style="color: red">Prazo estourado</span>'
#
#     >>> cont.formata_periodo()
#     '12 meses'
#
#     >>> cont.formata_recisao()
#     '3 meses'
#
#     >>> cont.estado_contrato()
#     '<span style="color: red">Prazo estourado</span>'
#     """
#
#
#     data_inicio = models.DateField(_(u'Data de início'))
#     limite_recisao = models.IntegerField(_(u'Recisão'), help_text=_(u'Tempo limite para recisão, em meses'))
#     os =  models.CharField(_(u'OS'), max_length=20, help_text=_(u'Número da Ordem de Serviço'), blank=True)
#     auto_renova = models.BooleanField(_(u'Renovação automática?'))
#     periodo_renova = models.IntegerField(_(u'Vigência'), help_text=_(u'Período de vigência do contrato, em meses.'))
#     categoria =  models.CharField(_(u'Categoria'), max_length=20, help_text=_(u' '), blank=True)
#
#
#     # Retorna os campos descrição e entidade/contato.
#     def __unicode__(self):
#         if self.tipo_documento.nome == 'Ordem de Serviço':
#             return '%s_OS %s' % (self.identificacao.entidade.sigla, self.os)
#         else:
#             return '%s' % (self.identificacao.entidade.sigla)
#
#
#     # Retorna a data de início formatada.
#     def formata_inicio(self):
#         return self.data_inicio.strftime("%d/%m/%y")
#     formata_inicio.short_description = _(u'Início')
#
#
#     # Retorna o campo 'limite_recisao' formatado.
#     def formata_recisao(self):
#         if self.limite_recisao > 1:
#             return "%s meses" % (self.limite_recisao)
#         return "%s mês" % (self.limite_recisao)
#     formata_recisao.short_description = _(u'Recisão')
#
#
#     # Retorna o campo 'periodo_renova' formatado.
#     def formata_periodo(self):
#         if self.periodo_renova > 1:
#             return "%s meses" % (self.periodo_renova)
#         return "%s mês" % (self.periodo_renova)
#     formata_periodo.short_description = _(u'Vigência')
#
#
#     # Define a ordenação dos dados.
#     class Meta:
#         ordering = ('-data_vencimento', )
#
#
#     # Define o estado de acordo com as datas de início e termino
#     def estado_contrato(self):
#         hoje = datetime.date.today()
#
#         if hoje < self.data_inicio:
#             e = u'Anterior a vigência'
#         elif hoje > self.data_vencimento:
#             e = u'Expirado'
#         elif hoje > self.data_vencimento + relativedelta(months=-self.limite_recisao):
#             e = u'Prazo estourado'
#         else:
#             e = u'Vigente'
#
#         est, created = Estado.objects.get_or_create(nome=e)
#
#         self.estado = est
#         self.save()
#
#         if self.estado.nome != u'Vigente':
#             return '<span style="color: red">%s</span>' % (self.estado)
#         else:
#             return self.estado.nome
#     estado_contrato.allow_tags = True
#     estado_contrato.short_description = _(u'Estado')


# Retorna o caminho para onde o arquivo será feito upload.
def upload_dir(instance, filename):
    return "protocolo/%s/%s" % (str(instance.protocolo.id), filename)


class Arquivo(models.Model):

    """
    Uma instância dessa classe representa um arquivo de um protocolo.

    O método '__unicode__'	Retorna a o nome do arquivo.
    A class 'Meta'		Define a ordenação dos dados pelo 'id' e a unicidade dos dados pelos campos 'arquivo' e 'protocolo'.
    """
    arquivo = models.FileField(upload_to=upload_dir)
    protocolo = models.ForeignKey('protocolo.Protocolo')

    # Retorna o nome do arquivo.
    def __unicode__(self):
        if not self.arquivo.name:
            return ''
        if self.arquivo.name.find('/') == -1:
            return self.arquivo.name
        else:
            return self.arquivo.name.split('/')[-1]

    # Retorna o termo.
    def mostra_termo(self):
        return self.protocolo.termo
    mostra_termo.short_description = _(u'Termo')

    # Retorna a sigla da entidade.
    def mostra_entidade(self):
        if self.protocolo.identificacao_id:
            return self.protocolo.identificacao.entidade.sigla
        else:
            return ''
    mostra_entidade.short_description = _(u'Entidade')

    # Retorna a descrição do protocolo.
    def mostra_descricao(self):
        return self.protocolo.descricao
    mostra_descricao.short_description = _(u'Descrição')

    # Define a ordenação dos dados e a unicidade dos dados.
    class Meta:
        ordering = ('id', )
        unique_together = ('arquivo', 'protocolo')


class Descricao(models.Model):
    descricao = models.CharField(max_length=200)
    entidade = models.ForeignKey(Entidade)

    class Meta:
        verbose_name = u'Descrição'
        verbose_name_plural = u'Descrições'
        ordering = ('entidade', 'descricao')

    def __unicode__(self):
        return "%s - %s" % (self.entidade.__unicode__(), self.descricao)


# Classe para definição de permissões de views e relatórios da app Protocolo
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_adm_descricao", u"Rel. Adm. - Protocolos por descrição"),     # /protocolo/descricao
        )
