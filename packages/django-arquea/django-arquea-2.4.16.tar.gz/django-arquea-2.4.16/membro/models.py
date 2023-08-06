# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import timedelta, datetime, date
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models.signals import post_save
from dateutil.rrule import rrule, DAILY
import calendar
from protocolo.models import Feriado
from utils.models import NARADateField

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CPFField(models.CharField):
    """
    """
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        models.CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        from localflavor.br.forms import BRCPFField
        defaults = {'form_class': BRCPFField}
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)
######


class TipoAssinatura(models.Model):
    """
    Uma instância dessa classe é um tipo de assinatura.

    O método '__unicode__'	Retorna o nome.
    A 'class Meta'		Define a descrição (singular e plural) do modelo e a ordenação  dos dados pelo nome.
    """

    nome = models.CharField(_(u'Nome'), max_length=20, help_text=_(u' '), unique=True)

    # Retorna o nome
    def __unicode__(self):
        return u'%s' % self.nome

    # Define a descrição do modelo e a ordenação dos dados pelo nome.
    class Meta:
        verbose_name = _(u'Tipo de Assinatura')
        verbose_name_plural = _(u'Tipos de Assinatura')
        ordering = ("nome", )


class SindicatoArquivo(models.Model):
    """
    Uma instância dessa classe é arquivo de sindicato de um mebro.
    O arquivo deve ser enviado anualmente.

    O método '__unicode__'    Retorna o nome.
    A 'class Meta'        Define a descrição (singular e plural) do modelo e a ordenação  dos dados pelo nome.
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'),
                               limit_choices_to=Q(historico__funcionario=True) & Q(historico__termino__isnull=True))
    arquivo = models.FileField(upload_to='membro__sindicatoarquivo', null=True, blank=True)
    ano = models.IntegerField(verbose_name=_(u'Ano'), blank=True, null=True)

    # Retorna o nome
    def __unicode__(self):
        return u'%s - %s' % (self.ano, self.arquivo)

    # Define a descrição do modelo e a ordenação dos dados pelo nome.
    class Meta:
        verbose_name = _(u'Arquivo do Sindicato')
        verbose_name_plural = _(u'Arquivos do Sindicato')
        ordering = ("ano", )


class Membro(models.Model):
    CACHE_KEY__CARGO_ATUAL = 'model_membro__cargo_atual_%d'

    """
    Uma instância dessa classe representa um membro de uma equipe.

    O método '__unicode__'	Retorna os campos 'nome' e 'cargo'.
    O método 'existe_ramal' 	Retorna o campo 'ramal' se estiver preenchido.
    O método 'existe_curriculo' Retorna um ícone com link para o currículo lattes se o campo 'url_lattes'
    se estiver preenchido.
    A class 'Meta' 		Define a ordenação dos dados pelos campos 'equipe' e 'membro' e define que um membro deve ser
    único pelos campos 'equipe', 'nome' e 'funcao'.
    """
    nome = models.CharField(_(u'Nome'), max_length=50, help_text=_(u'ex. Caio Andrade'))
    rg = models.CharField(_(u'RG'), max_length=12, help_text=_(u'ex. 00.000.000-0'), blank=True, null=True)
    cpf = CPFField(_(u'CPF'), blank=True, null=True, help_text=_(u'ex. 000.000.000-00'))
    email = models.CharField(_(u'E-mail'), max_length=50, blank=True, help_text=_(u'ex. nome@empresa.br'))
    ramal = models.IntegerField(_(u'Ramal'), blank=True, null=True)
    obs = models.TextField(_(u'Observação'), blank=True)
    url_lattes = models.URLField(_(u'Currículo Lattes'), blank=True, help_text=_(u'URL do Currículo Lattes'))
    foto = models.ImageField(upload_to='membro', blank=True, null=True)
    data_nascimento = NARADateField(_(u'Nascimento'), help_text=_(u'Data de nascimento'), blank=True, null=True)
    site = models.BooleanField(_(u'Exibir no site?'), default=False)
    contato = models.ForeignKey('identificacao.Contato', null=True, blank=True)

    # Retorna o nome e o cargo.
    def __unicode__(self):
        cargo = self.cargo_atual
        if cargo:
            return u'%s (%s)' % (self.nome, cargo)
        return u'%s' % self.nome

    # Verifica se o campo ramal está preenchido.
    def existe_ramal(self):
        if self.ramal:
            return self.ramal
        return ''
    existe_ramal.short_description = _(u'Ramal')

    # Retorna um ícone com o link para o currículo lattes.
    def existe_curriculo(self):
        if self.url_lattes:
            a = '<center><a href="%s">%s</a></center>' % (self.url_lattes, self.url_lattes)
            return a
        return ''
    existe_curriculo.allow_tags = True
    existe_curriculo.short_description = _(u'Currículo Lattes')

    # cargo atual do membro, caso exista, a partir do histórico
    @property
    def cargo_atual(self):
        retorno = cache.get(Membro.CACHE_KEY__CARGO_ATUAL % self.id)
        if retorno is None:
            cargos = []
            for h in self.historico_set.all():
                if h.termino is None:
                    cargos.append(h.cargo.nome)
            retorno = ' - '.join(cargos)

            cache.set(Membro.CACHE_KEY__CARGO_ATUAL % self.id, retorno, 600)

        return retorno

    # se o membro é atualmente funcionario
    @property
    def funcionario(self):
        return Historico.ativos.filter(membro=self, funcionario=True).count() > 0

    @property
    def ativo(self):
        return Historico.ativos.filter(membro=self).count() > 0

    @cached_property
    def data_inicio(self):
        return Historico.objects.filter(membro=self).order_by('inicio').values_list('inicio')[0][0]

    # Define a ordenação e unicidade dos dados.
    class Meta:
        ordering = ('nome', )


class Usuario(models.Model):
    """
    Uma instância dessa classe representa um usuário de um sistema.

    O método '__unicode__'		Retorna o campo 'username'.
    A classmethod 'usuarios_sistema'	Retorna os usuários de um sistema.
    A class 'Meta' 			Define a descrição do modelo (singuar e plural), ordena os dados pelos campos 'username' e
    a unicidade de um usuário pelos campos 'membro', 'username' e 'sistema'.
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'))  # , limit_choices_to=Q(funcionario=True))
    username = models.CharField(_(u'Usuário'), max_length=20, help_text=_(u'Nome de usuário no sistema'))
    sistema = models.CharField(_(u'Sistema'), max_length=50, help_text=_(u'Nome do Sistema'))

    # Retorna o usuário.
    def __unicode__(self):
        return u'%s' % self.username

    # Define a descrição do modelo, a ordenação e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')
        ordering = ('username', )
        unique_together = (('membro', 'username', 'sistema'),)


class Assinatura(models.Model):

    """
    Uma instância dessa classe representa uma assinatura de um membro.

    O método '__unicode__'		Retorna os campos 'membro' e 'tipo_assinatura'.
    A classmethod 'assinaturas_membro'	Retorna as assinaturas de um membro específico.
    A class 'Meta'		Define a ordenação dos dados pelo 'nome' e unicidade pelos campos 'tipo_assinatura' e 'membro'.
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'))  # , limit_choices_to=Q(funcionario=True))
    tipo_assinatura = models.ForeignKey('membro.TipoAssinatura', verbose_name=_(u'Tipo de Assinatura'))

    # Retorna o membro e o tipo de assinatura.
    def __unicode__(self):
        return u'%s | %s' % (self.membro.nome, self.tipo_assinatura)

    # Define a ordenação e a unicidade dos dados.
    class Meta:
        ordering = ('membro', )
        unique_together = (('membro', 'tipo_assinatura'),)


class Ferias(models.Model):
    """
    Controle de período aquisitivo para as férias
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'),
                               limit_choices_to=Q(historico__funcionario=True) & Q(historico__termino__isnull=True))
    inicio = NARADateField(_(u'Início do período aquisitivo'), help_text=_(u'Início do período de trabalho'))
    realizado = models.BooleanField(_(u'Férias já tiradas?'), default=False)

    def save(self, *args, **kwargs):
        self.inicio_ferias = self.inicio + timedelta(365)
        self.fim_ferias = self.inicio_ferias + timedelta(365)
        super(Ferias, self).save(*args, **kwargs)

    # Retorna o membro e o período de férias.
    def __unicode__(self):
        if self.inicio:
            inicio = self.inicio.strftime('%d/%m/%Y')
        else:
            inicio = ''
        return u'%s | Início período: %s' % (self.membro, inicio)

    def inicio_ferias(self):
        if self.inicio is not None:
            return (self.inicio + timedelta(365)).strftime('%d/%m/%Y')
        return ''
    inicio_ferias.short_description = u'Início do período para férias'

    def fim_ferias(self):
        if self.inicio is not None:
            return (self.inicio + timedelta(730)).strftime('%d/%m/%Y')
        return ''
    fim_ferias.short_description = u'Final do período para férias'

    def link_edit(self):
        if not self.id:
            return ''
        return '<a href="%s?" target="_blank">Detalhes</a>' % reverse('admin:membro_ferias_change', args=[self.id])
    link_edit.allow_tags = True
    link_edit.short_description = u'Detalhes do período de férias'

    @property
    def trab_termino(self):
        return self.trab_inicio+timedelta(365)

    # Retorna quantos dias de férias foi solicitado.
    def qtde_dias(self):
        if self.periodo_escolha_inic and self.periodo_escolha_term:
            dias = self.periodo_escolha_term - self.periodo_escolha_inic
            dias = dias.days + 1
            return '%s dias' % dias
        return ''
    qtde_dias.short_description = _(u'Dias solicitados')

    # Diz se o prazo de aquisição das férias já foi completado
    def completo(self):
        umano = date(self.inicio.year+1, self.inicio.month, self.inicio.day)
        return umano <= datetime.now().date()
    completo.boolean = True

    @classmethod
    def total_dias_uteis_aberto(self, membro_id):
        # Retorna o total de dias em aberto para o membro, em segundos
        total_dias_uteis_aberto = 0

        ferias = Ferias.objects.filter(membro=membro_id)

        for f in ferias:
            controles = ControleFerias.objects.filter(ferias=f).select_related().order_by('inicio')

            for c in controles:
                if c.dias_uteis_aberto and c.dias_uteis_aberto > 0:
                    total_dias_uteis_aberto = total_dias_uteis_aberto + c.dias_uteis_aberto

                if c.dias_uteis_fato:
                    total_dias_uteis_aberto = total_dias_uteis_aberto - c.dias_uteis_fato

        return total_dias_uteis_aberto * 8 * 60 * 60

    # Define a descrição do modelo, ordenação e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Férias')
        verbose_name_plural = _(u'Férias')
        unique_together = (('membro', 'inicio'),)
        ordering = ('inicio',)


class ControleFerias(models.Model):
    """
    Controle efetivo das férias, com as datas reais de saída e retorno
    """
    ferias = models.ForeignKey('membro.Ferias')
    inicio = NARADateField()
    termino = NARADateField()
    oficial = models.BooleanField(_(u'Oficial?'), default=False)
    obs = models.TextField(null=True, blank=True)
    vendeu10 = models.BooleanField(_(u'Vendeu 10 dias?'), default=False)
    antecipa13 = models.BooleanField(_(u'Antecipação de 13º salário?'), default=False)
    dias_uteis_fato = models.IntegerField(_(u'Dias úteis tirados de fato'))
    dias_uteis_aberto = models.IntegerField(_(u'Dias úteis em aberto'))
    arquivo_oficial = models.FileField(upload_to='controleferias__arquivooficial', null=True, blank=True)

    def dia_ferias(self, dia):
        # verifica se tem algum período de férias com dias úteis tirados de fato
        # não deve entrar na conta se forem período de férias com venda de dias, ou somente marcação de vencimento
        # de férias
        is_ferias = False
        if self.dias_uteis_fato > 0:
            is_ferias = is_ferias or (self.inicio <= dia <= self.termino)
        return is_ferias

    def __unicode__(self):
        return u"%s - %s" % (self.inicio, self.termino)

    class Meta:
        verbose_name = _(u'Controle de férias')
        verbose_name_plural = _(u'Controles de férias')


class TipoDispensa(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return u'%s' % self.nome


class DispensaLegal(models.Model):
    """
    Dispensas legais, como por exemplo dispensa médica, para trabalho em eleição, luto, casamento, etc
    """
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'),
                               limit_choices_to=Q(historico__funcionario=True) & Q(historico__termino__isnull=True))
    tipo = models.ForeignKey('membro.TipoDispensa', verbose_name=_('Tipo de dispensa'))
    justificativa = models.TextField()
    inicio_direito = NARADateField(_(u'Início do direito'))
    dias_uteis = models.IntegerField(_(u'Dias úteis.'), help_text='*mover para dias corridos', null=True, default=0)
    inicio_realizada = NARADateField(_(u'Início da realização da dispensa'), blank=True, null=True)
    realizada = models.BooleanField(_(u'Já realizada?'), default=False)
    atestado = models.BooleanField(_(u'Há atestado?'), default=False)
    arquivo = models.FileField(upload_to='dispensas/', null=True, blank=True)

    dias_corridos = models.IntegerField(_(u'Duração em dias corridos'), null=True, default=0)
    horas = models.IntegerField(_(u'Horas'), null=True, default=0)
    minutos = models.IntegerField(_(u'Minutos'), null=True, default=0)

    def __unicode__(self):
        return u"%s - %s" % (self.membro, self.justificativa)

    @cached_property
    def termino_realizada(self):
        """
        Calcula a data de termino da dispensa, descontado o sábado e o domingo
        Leva em conta os feriados.
        """
        soma_dias = 0

        if self.realizada and self.inicio_realizada:

            if self.dias_corridos:
                soma_dias += self.dias_corridos
            if self.horas:
                soma_dias += self.horas / 8.0
            if self.minutos:
                soma_dias += self.minutos / 60.0

            if self.dias_corridos >= 1:
                return self.inicio_realizada + timedelta(soma_dias - 1)

        return self.inicio_realizada

    def dia_dispensa(self, dia):
        is_dispensa = False
        horas_dispensa = 0

        if self.realizada and self.inicio_realizada:

            is_dispensa = self.inicio_realizada <= dia <= self.termino_realizada

            if is_dispensa:
                if self.termino_realizada == dia:
                    if self.horas or self.minutos:
                        if self.horas:
                            horas_dispensa += self.horas % 8.0
                        if self.minutos:
                            horas_dispensa += (self.minutos % 60.0)/60
                    elif self.dias_corridos:
                        horas_dispensa = 8.0
                elif dia < self.termino_realizada:
                    horas_dispensa = 8.0
                elif dia > self.termino_realizada:
                    horas_dispensa = 0

        return {'is_dispensa': is_dispensa, 'horas': horas_dispensa}

    class Meta:
        verbose_name = _(u'Dispensa')
        verbose_name_plural = _(u'Dispensas')


class Banco(models.Model):
    """
    Tabela para guardar os números e nomes dos bancos, com atualização automática periódica.

    O método '__unicode__'	Retorna o nome e o número do banco.
    A class 'Meta'		Define a ordenação dos dados pelo nome do banco.

    >>> b = Banco(numero=151, nome='Nossa Caixa')
    >>> b.save()

    >>> b.__unicode__()
    u'Nossa Caixa (151)'
    """

    numero = models.IntegerField()
    nome = models.CharField(max_length=100)

    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('nome',)

    # Retorna o nome e o número do banco.
    def __unicode__(self):
        return u'%s (%03d)' % (self.nome, self.numero)


class DadoBancario(models.Model):
    """
    Uma instância dessa classe representa os dados bancários de uma entidade ou um contato.

    O método '__unicode__'	Retorna os dados bancários (banco + agência + conta).
    O método 'agencia_digito'	Retorna o número da agência + o dígito.
    O método 'conta_digito'	Retorna o número da conta + o dígito.
    A class 'Meta'		Define a descrição do modelo (singular e plural), a ordenação dos dados pelo 'banco' e a
    unicidade dos dados pelos campos 'banco', 'agencia', 'ag_digito', 'conta', 'cc_digito'.
    """
    membro = models.OneToOneField('membro.Membro', verbose_name=_(u'Membro'))
    banco = models.ForeignKey('membro.Banco', verbose_name=_(u'Banco'))
    agencia = models.IntegerField(_(u'Ag.'), help_text=_(u'ex. 0909'))
    ag_digito = models.IntegerField(' ', blank=True, null=True, help_text=_(u'ex. 9'))
    conta = models.IntegerField(_(u'CC'), help_text=_(u'ex. 01222222'))
    cc_digito = models.CharField(' ', max_length=1, blank=True, help_text=_(u'ex. x'))

    # Retorna o banco, a agência e o número da conta.
    def __unicode__(self):
        if self.ag_digito:
            ag = u'%s-%s' % (self.agencia, self.ag_digito)
        else:
            ag = u'%s' % self.agencia
        if self.cc_digito:
            cc = u'%s-%s' % (self.conta, self.cc_digito)
        else:
            cc = u'%s' % self.conta
        return u'%s AG. %s CC %s' % (self.banco, ag, cc)

    # Define a descrição do modelo, a ordenação dos dados pelo banco e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Dados bancários')
        verbose_name_plural = _(u'Dados bancários')
        ordering = ('banco', )
        unique_together = (('banco', 'agencia', 'ag_digito', 'conta', 'cc_digito'),)

    # Retorna o número da agência completo (agência + dígito)
    def agencia_digito(self):
        if self.agencia or self.ag_digito:
            if self.ag_digito:
                return '%s-%s' % (self.agencia, self.ag_digito)
            else:
                return self.agencia
        return ' '
    agencia_digito.short_description = _(u'Agência')

    # Retorna o número da conta completo (conta + dígito)
    def conta_digito(self):
        if self.conta or self.cc_digito:
            if self.cc_digito:
                return '%s-%s' % (self.conta, self.cc_digito)
            else:
                return self.conta
        return ' '
    conta_digito.short_description = _(u'Conta')


class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    hierarquia = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class AtivoManager(models.Manager):
    def get_queryset(self):
        return super(AtivoManager, self).get_queryset().filter(termino__isnull=True)


class Historico(models.Model):
    inicio = models.DateField(_(u'Início'))
    termino = models.DateField(_(u'Término'), null=True, blank=True)
    funcionario = models.BooleanField(_(u'Funcionário'), default=False)
    obs = models.TextField(null=True, blank=True)
    cargo = models.ForeignKey('membro.Cargo')
    membro = models.ForeignKey('membro.Membro')

    objects = models.Manager()
    ativos = AtivoManager()

    def __unicode__(self):
        return u'%s - %s' % (self.membro.nome, self.cargo.nome)

    def ativo(self):
        return self.termino is None

    class Meta:
        ordering = ('-inicio',)
        verbose_name = _(u'Histórico')
        verbose_name_plural = _(u'Históricos')


def historico_post_save_signal(sender, instance, **kwargs):
    # Post-save signal do Historico do Membro para limpar o cache do Membro.cargo_atual
    cache.delete(Membro.CACHE_KEY__CARGO_ATUAL % instance.membro_id)

# Registrando o sinal
post_save.connect(historico_post_save_signal, sender=Historico, dispatch_uid="historico_post_save")


class Arquivo(models.Model):
    membro = models.ForeignKey('membro.Membro')
    arquivo = models.FileField(upload_to='membro')

    def __unicode__(self):
        return u'%s - %s' % (self.membro.nome, self.arquivo.name)


class Controle(models.Model):
    membro = models.ForeignKey('membro.Membro', verbose_name=_(u'Membro'),
                               limit_choices_to=Q(historico__funcionario=True) & Q(historico__termino__isnull=True))
    entrada = models.DateTimeField()
    saida = models.DateTimeField(null=True, blank=True)
    obs = models.TextField(_(u'Comentários'), blank=True, null=True)
    almoco_devido = models.BooleanField(_(u'Hora de almoço devida?'), default=True)
    almoco = models.IntegerField(_(u'Tempo de almoço em minutos'), null=True, blank=True, default=60)

    def __unicode__(self):
        entrada = timezone.localtime(self.entrada) if timezone.is_aware(self.entrada) else self.entrada
        if self.saida:
            saida = timezone.localtime(self.saida) if timezone.is_aware(self.saida) else self.saida
            return u'%s - de %s a %s' % (self.membro, entrada, saida)
        else:
            return u'%s - %s' % (self.membro, entrada)

    @cached_property
    def segundos(self):
        if not self.saida:
            return 0
        delta = self.saida-self.entrada

        try:
            # PYTHON 2.7
            segundos_trabalhados = delta.total_seconds()
        except AttributeError:
            # AJUSTE PARA O PYTHON < 2.7
            segundos_trabalhados = delta.seconds + delta.days * 24 * 3600.0

        if self.almoco_devido and self.almoco:
            segundos_trabalhados -= self.almoco * 60

        return round(segundos_trabalhados)

    @cached_property
    def hora_almoco(self):
        if self.almoco:
            return self.almoco * 60
        else:
            return 0

    def total_analitico_horas(self, ano, mes):
        controles = Controle.objects.filter(membro=self.membro_id).order_by('entrada')

        primeiroDiaFiltro = None
        if ano and ano.isdigit() and int(ano) > 0:
            controles = controles.filter(entrada__year=ano)

        primeiroControle = controles[:1].get()
        if mes and mes.isdigit() and int(mes) > 0:
            controles = controles.filter(entrada__month=mes)
            primeiroDiaFiltro = datetime(primeiroControle.entrada.year, int(mes), 01)
        else:
            primeiroDiaFiltro = datetime(primeiroControle.entrada.year, primeiroControle.entrada.month, 01)

        meses = []
        if controles.exists():
            ultimoControle = controles.order_by('-entrada')[:1].get()
            ultimoDiaFiltro = datetime(ultimoControle.entrada.year, ultimoControle.entrada.month,
                                       calendar.monthrange(ultimoControle.entrada.year,
                                                           ultimoControle.entrada.month)[1], 23, 59, 59)

            controles = controles.order_by('-entrada')

            mes_anterior = date(1979, 01, 01)
            if controles.count() > 0:

                for dt in rrule(DAILY, dtstart=primeiroDiaFiltro, until=ultimoDiaFiltro):

                    if dt.month != mes_anterior.month or dt.year != mes_anterior.year:
                        dias = []
                        meses.insert(0, ({'mes': dt.month, 'ano': dt.year, 'dias': dias, 'total': 0}))
                        mes_anterior = dt

                    itemControle = ItemControle()
                    itemControle.dia = date(dt.year, dt.month, dt.day)
                    itemControle.controles = controles.filter(entrada__year=dt.year,
                                                              entrada__month=dt.month,
                                                              entrada__day=dt.day)
    #                 dias.append(itemControle)
                    dias.insert(0, itemControle)

            total_banco_horas = 0
            ferias = ControleFerias.objects.filter(ferias__membro=self.membro_id)
            dispensas = DispensaLegal.objects.filter(membro=self.membro_id)

            for m in meses:
                total_segundos_trabalhos_mes = 0
                # total de horas de dispensas
                total_horas_dispensa = 0
                # total de horas de ferias
                total_horas_ferias = 0

                # ferias_ini < mes_ini < ferias_fim  OR  mes_ini < ferias_ini < mes_fim
                mes_corrente_ini = date(m['ano'], m['mes'], 01)
                mes_corrente_fim = mes_corrente_ini + timedelta(calendar.monthrange(m['ano'], m['mes'], )[1])

                for d in m['dias']:
                    # total de horas trabalhadas
                    total_segundos_trabalhos_mes = total_segundos_trabalhos_mes + sum([c.segundos for c in d.controles])
                    # verifica se tem algum período de férias com dias úteis tirados de fato
                    # não deve entrar na conta se forem período de férias com venda de dias, ou somente marcação de
                    # vencimento de férias
                    for data_ferias in ferias:
                        d.is_ferias = data_ferias.dia_ferias(d.dia)
                        if d.is_ferias:
                            d.obs = u'%s Férias' % d.obs
                            break

                    # é final de semana?
                    d.is_final_de_semana = d.dia.weekday() >= 5
                    if d.is_final_de_semana:
                        if d.dia.weekday() == 5:
                            d.obs = u'%s Sábado' % d.obs
                        elif d.dia.weekday() == 6:
                            d.obs = u'%s Domingo' % d.obs

                    # é feriado?
                    diaFeriado = Feriado.get_dia_de_feriado(d.dia)
                    if diaFeriado is not None:
                        d.obs = u'%s %s' % (d.obs, diaFeriado.tipo.nome)
                        # este feriado é facultativo ou não?
                        if not diaFeriado.tipo.subtrai_banco_hrs:
                            d.is_feriado = True

                    # é dispensa?
                    d.is_dispensa = False
                    horas_dispensa = 0
                    for dispensa in dispensas:
                        dia_dispensa = dispensa.dia_dispensa(d.dia)
                        if dia_dispensa['is_dispensa']:
                            d.is_dispensa = dia_dispensa['is_dispensa']
                            horas_dispensa = dia_dispensa['horas']
                            d.obs = u'%s Dispensa %s' % (d.obs, dispensa.tipo.nome)
                            break

                    # soma os dias de trabalho
                    if not d.is_final_de_semana and not d.is_feriado:
                        # conta as horas de dispensas
                        if d.is_dispensa:
                            total_horas_dispensa += horas_dispensa * 3600
                        # conta as horas de ferias
                        if d.is_ferias:
                            # soma 8h
                            total_horas_ferias += 28800

                m.update({'total': total_segundos_trabalhos_mes})
                if self.membro.data_inicio > mes_corrente_ini:
                    # Leva em conta a data de admissão do membro para a contagem das horas úteis do período
                    total_horas_periodo = self.total_horas_uteis(self.membro.data_inicio, mes_corrente_fim)
                else:
                    # as horas totais do período são as horas do total de dias do mes menos os finais de semana,
                    # ferias e dispensas
                    total_horas_periodo = self.total_horas_uteis(mes_corrente_ini, mes_corrente_fim)
                m.update({'total_horas_periodo': total_horas_periodo})

                total_horas_restante = total_horas_periodo - total_horas_dispensa - total_horas_ferias - \
                    total_segundos_trabalhos_mes

                m.update({'total_horas_restante': total_horas_restante})
                m.update({'total_horas_dispensa': total_horas_dispensa})
                m.update({'total_horas_ferias': total_horas_ferias})

                # soma horas extras somente dos meses que não forem o mês em andamento
                total_banco_horas = 0
                if datetime.now().year != c.entrada.year or datetime.now().month != c.entrada.month:
                    total_banco_horas = -total_horas_restante
                m.update({'total_banco_horas': total_banco_horas})

        return meses

    @classmethod
    def total_horas_uteis(self, data_ini, data_fim):
        soma_dias_de_trabalho = 0

        d = data_ini
        while d < data_fim:
            # é final de semana?
            is_final_de_semana = d.weekday() >= 5

            # é feriado?
            is_feriado = False
            diaFeriado = Feriado.get_dia_de_feriado(d)

            # verifica se o feriado é facultativo, ou seja, com desconto de banco de horas.
            if diaFeriado is not None and not diaFeriado.tipo.subtrai_banco_hrs:
                is_feriado = True

            # soma os dias de trabalho
            if not is_final_de_semana and not is_feriado:
                soma_dias_de_trabalho += 1

            d += timedelta(days=1)

        # as horas totais do período são as horas do total de dias do mes menos os finais de semana, ferias e dispensas
        total_horas_periodo = (soma_dias_de_trabalho * 8 * 60 * 60)

        return total_horas_periodo

    class Meta:
        ordering = ('-entrada',)

    def permanencia(self):
        return '%2dh%2dmin' % (self.segundos/3600, self.segundos/60 % 60)


class ItemControle:
    dia = date(1979, 12, 12)
    controles = []
    obs = ''
    is_final_de_semana = False
    is_feriado = False
    is_dispensa = False
    is_ferias = False

    def almoco(self):
        return 0

    def __unicode__(self):
        return u'%s' % (self.dia)


# Classe para definição de permissões de views e relatórios da app Membro
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_adm_logs", "Rel. Adm. - Registro de uso do sistema por ano"),     # /logs
            ("rel_adm_mensalf", "Rel. Adm. - Controle de horário mensal"),     # /membro/mensalf
        )
