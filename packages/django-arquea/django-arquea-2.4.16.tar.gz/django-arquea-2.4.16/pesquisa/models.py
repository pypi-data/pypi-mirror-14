# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


REDES = (
    ('Kyatera', 'Kyatera'),
    ('Ae', 'Ae'),
    ('Cinapce', 'Cinapce'),
    ('Grid Unesp', 'Grid Unesp'),
)

ESTADO_EQUIPAMENTO = (
    ('nao adquirido', u'ainda não foi adquirido'),
    ('nao instalado', u'foi orçado ou adquirido e não está instalado'),
    ('instalado', u'está instalado'),
)

EQUIPAMENTO = (
    ('switch', 'Switch'),
    ('roteador', 'Roteador'),
    ('pc', 'PC adaptado'),
)


class L2(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('id',)


class L3(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('id',)


class Pesquisa(models.Model):
    """
    """

    usuario = models.ForeignKey(User, editable=False)
    rede = models.CharField(max_length=30, choices=REDES, verbose_name=u'Rede de Pesquisa',
                            help_text=u'Indicar a qual programa Fapesp de pesquisa o laboratório pertence')
    laboratorio = models.CharField(max_length=255, verbose_name=u'Qual é o seu laboratório, centro ou grupo?')
    endereco = models.CharField(max_length=255, verbose_name=u'Endereço', blank=True)
    cidade = models.CharField(max_length=50, verbose_name=u'Cidade')
    instituicao = models.CharField(max_length=200, verbose_name=u'Instituição', blank=True,
                                   help_text=u'Exemplo: FMUSP, IFGW-Unicamp, ITA')
    responsavel1 = models.CharField(max_length=100, verbose_name=u'Pesquisador responsável 1',
                                    help_text=u'Pesquisador cujo nome consta no processo Fapesp correspondente ao projeto')
    emailresp1 = models.EmailField(verbose_name=u'E-mail do pesquisador responsável 1', blank=True)
    responsavel2 = models.CharField(max_length=100, verbose_name=u'Pesquisador responsável 2',
                                    help_text=u'Pesquisador ou coordenador co-responsável pelo projeto, caso existir, juntamente com o pesquisador principal', blank=True)
    emailresp2 = models.EmailField(verbose_name=u'E-mail do pesquisador responsável 2', blank=True)
    contato1 = models.CharField(max_length=100, verbose_name=u'Contato técnico 1',
                                help_text=u'Analista de suporte, pesquisador, responsável pela rede do laboratório e da conexão com a rede KyaTera')
    emailcontato1 = models.EmailField(verbose_name=u'E-mail do contato técnico 1')
    telefone1 = models.CharField(max_length=14, verbose_name=u'Telefone do contato técnico 1',
                                 help_text=u'Telefone no formato: (xx) xxxx-xxxx', blank=True)
    contato2 = models.CharField(max_length=100, verbose_name=u'Contato técnico 2',
                                help_text=u'Segunto contato técnico, no caso do "Contato técnico 1" não ser encontrado', blank=True)
    emailcontato2 = models.EmailField(verbose_name=u'E-mail do contato técnico 2', blank=True)
    telefone2 = models.CharField(max_length=14, verbose_name=u'Telefone do contato técnico 2',
                                 help_text=u'Telefone no formato: (xx) xxxx-xxxx', blank=True)

    estado_equipamento = models.CharField(max_length=100, choices=ESTADO_EQUIPAMENTO,
                                          verbose_name=u'Quanto ao equipamento de conexão à rede KyaTera')

    equipamento = models.CharField(max_length=50, choices=EQUIPAMENTO,
                                   verbose_name=u'Equipamento de conexão')
    fabricante = models.CharField(max_length=100, blank=True, verbose_name=u'Fabricante ou marca',
                                  help_text=u'Exemplos: Cisco, Foundry, 3Com, Nortel')
    modelo = models.CharField(max_length=200, blank=True, help_text=u'Exemplos: Catalyst, XMR')
    cobre = models.CharField(max_length=200, blank=True, verbose_name=u'Interfaces de cobre (quantidade, velocidade)', help_text='Exemplo: 24 portas UTP 100/1000')
    otica = models.CharField(max_length=200, blank=True, verbose_name=u'Interfaces óticas',
                             help_text=u'Exemplos: 2 portas LX 1 GigaE, 1 SFP LH 10 GigaE')

    l2 = models.ManyToManyField(L2, blank=True)
    l2_outro = models.CharField(max_length=100, blank=True, verbose_name=u'Outro relevante?')
    l3 = models.ManyToManyField(L3, blank=True)
    l3_outro = models.CharField(max_length=100, blank=True, verbose_name=u'Outro relevante?')

    obs = models.TextField(blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.rede, self.laboratorio)

    class Meta:
        verbose_name = 'Rede Kyatera'
        verbose_name_plural = 'Rede Kyatera'

    def format_lab(self):
        return self.laboratorio
    format_lab.short_description = _(u'Laboratório')

    def format_estado(self):
        return self.estado_equipamento
    format_estado.short_description = _(u'Estado do equipamento')

    def format_contato(self):
        return self.contato1
    format_contato.short_description = _(u'Contato técnico')
