# -*- encoding:utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone
from ipaddress import IPv4Address, IPv6Address
from django.utils.translation import ugettext_lazy as _

import ipaddress


class BlocoIP(models.Model):
    ip = models.GenericIPAddressField(verbose_name='Bloco IP')
    mask = models.IntegerField()
    asn = models.ForeignKey('identificacao.ASN', verbose_name='AS anunciante')
    proprietario = models.ForeignKey('identificacao.ASN', help_text=u'Preencher caso seja diferente do dono do AS.',
                                     null=True, blank=True, related_name='possui', verbose_name=u'AS Proprietário')
    superbloco = models.ForeignKey('rede.BlocoIP', null=True, blank=True, verbose_name='Super bloco')
    designado = models.ForeignKey('identificacao.Entidade', null=True, blank=True, related_name='designa',
                                  verbose_name='Designado para')
    usuario = models.ForeignKey('identificacao.Entidade', help_text=u'Preencher caso seja diferente do designado.',
                                null=True, blank=True, related_name='usa', verbose_name=u'Usado por')
    rir = models.ForeignKey('rede.RIR', null=True, blank=True, verbose_name='RIR')
    obs = models.TextField(null=True, blank=True)
    transito = models.BooleanField(u'Bloco de trânsito?', default=False)

    def __unicode__(self):
        return u'%s/%s' % (self.ip, self.mask)

    def cidr(self):
        return self.__unicode__()
    cidr.admin_order_field = 'ip'
    cidr.allow_tags = True
    cidr.short_description = 'Bloco IP'

    def netmask(self):
        # ip = IPv4Network(u'%s/%s' % (self.ip, self.mask), strict=False)
        ip = ipaddress.ip_network(u'%s/%s' % (self.ip, self.mask), strict=False)
        return '%s' % ip.netmask

    def is_IPV4(self):
        return isinstance(ipaddress.ip_address(u'%s' % self.ip), IPv4Address)

    def is_IPV6(self):
        return isinstance(ipaddress.ip_address(u'%s' % self.ip), IPv6Address)

    def AS(self):
        return self.asn.numero
    AS.admin_order_field = 'asn__numero'
    AS.short_description = 'ASN'

    def prop(self):
        return self.proprietario
    prop.admin_order_field = 'proprietario__sigla'
    prop.short_description = u'Proprietário'

    def usu(self):
        if self.usuario:
            return self.usuario.sigla
        else:
            return None
    usu.admin_order_field = 'usuario__sigla'
    usu.short_description = u'Usado por'

    def desig(self):
        return self.designado.sigla
    desig.admin_order_field = 'designado__sigla'
    desig.short_description = 'Designado para'

    def save(self, *args, **kwargs):
        if self.superbloco:
            self.rir = self.superbloco.rir
        super(BlocoIP, self).save(*args, **kwargs)

    def leaf(self):
        if self.blocoip_set.count() == 0:
            return True
        return False

    class Meta:
        verbose_name = u'Bloco IP'
        verbose_name_plural = u'Blocos IP'
        ordering = ('ip',)
        unique_together = ('ip', 'mask')


class RIR(models.Model):
    nome = models.CharField(max_length=40)

    def __unicode__(self):
        return self.nome


class Provedor(models.Model):
    ip = models.GenericIPAddressField()
    mask = models.IntegerField()
    provedor = models.CharField(max_length=40)

    def __unicode__(self):
        return self.provedor


class Rota(models.Model):
    aspath = models.CharField(u'AS path', max_length=255)
    blocoip = models.ForeignKey('rede.BlocoIP', verbose_name='Bloco IP')
    nexthop = models.GenericIPAddressField()
    provedor = models.ForeignKey('rede.Provedor')
    preferencial = models.BooleanField(default=False)
    local_pref = models.IntegerField(null=True, blank=True)
    historico = models.ForeignKey('rede.Historico')

    def __unicode__(self):
        return u'%s %s' % (self.historico, self.blocoip)


class Historico(models.Model):
    arquivo = models.FileField(upload_to='rede')
    horario = models.DateTimeField(auto_now=True)
    equipamento = models.ForeignKey('patrimonio.Patrimonio', null=True, blank=True)

    def __unicode__(self):
        return timezone.localtime(self.horario) if timezone.is_aware(self.horario) else self.horario


UNIDADES = (
    (1, 'bps'),
    (1000, 'kbps'),
    (1000000, 'Mbps'),
    (1000000000, 'Gbps'),
    (1000000000000, 'Tbps'),
)


class Banda(models.Model):
    velocidade = models.IntegerField()
    unidade = models.IntegerField(choices=UNIDADES)

    def __unicode__(self):
        return u'%s %s' % (self.velocidade, self.get_unidade_display())

    class Meta:
        ordering = ('unidade', 'velocidade')


class Operadora(models.Model):
    nome = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class IPBorda(models.Model):
    ip = models.GenericIPAddressField('IP de borda')

    def __unicode__(self):
        return u'%s' % self.ip


class Enlace(models.Model):
    participante = models.ForeignKey('identificacao.Endereco')
    entrada_ansp = models.ForeignKey('identificacao.Endereco', verbose_name='Ponto de entrada na ANSP',
                                     related_name='entrada')
    operadora = models.ManyToManyField('rede.Operadora', through='EnlaceOperadora')
    obs = models.TextField(null=True, blank=True)

    def participante_display(self):
        return u'%s' % self.participante.entidade.sigla
    participante_display.short_description = u'Participante'

    def entrada_display(self):
        return u'%s' % self.entrada_ansp.entidade.sigla
    entrada_display.short_description = u'Ponto de entrada na ANSP'

    def __unicode__(self):
        return self.participante_display()

    class Meta:
        ordering = ('participante',)


class EnlaceOperadora(models.Model):
    enlace = models.ForeignKey('rede.Enlace')
    operadora = models.ForeignKey('rede.Operadora')
    banda = models.ForeignKey('rede.Banda')
    ip_borda = models.ManyToManyField('rede.IPBorda')
    data_ativacao = models.DateField(null=True, blank=True)
    data_desativacao = models.DateField(null=True, blank=True)
    link_redundante = models.BooleanField(default=False)
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - (Operadora %s)' % (self.enlace, self.operadora)

    class Meta:
        ordering = ('enlace', 'operadora',)


class Segmento(models.Model):
    enlace = models.ForeignKey('rede.Enlace')
    operadora = models.ForeignKey('rede.Operadora')
    banda = models.ForeignKey('rede.Banda')
    # ip_borda = models.ManyToManyField('rede.IPBorda')
    data_ativacao = models.DateField(u'Data de ativação', null=True, blank=True)
    data_desativacao = models.DateField(u'Data de desativação', null=True, blank=True)
    link_redundante = models.BooleanField(u'Link redundante?', default=False)
    obs = models.TextField(null=True, blank=True)
    canal = models.ForeignKey('rede.Canal', null=True, blank=True)
    uso = models.ForeignKey('rede.Uso', null=True, blank=True)
    sistema = models.ForeignKey('rede.Sistema', null=True, blank=True)
    designacao = models.CharField(u'Designação', max_length=50, null=True, blank=True)
    interfaces = models.ManyToManyField('rede.Interface', null=True, blank=True)

    def __unicode__(self):
        return u'%s - (Operadora %s)' % (self.enlace, self.operadora)

    class Meta:
        ordering = ('enlace', 'operadora',)


class Interface(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey('rede.TipoInterface')
    midia = models.ForeignKey('rede.Midia')

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class TipoInterface(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Midia(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Canal(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Uso(models.Model):
    nome = models.CharField(max_length=20)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Sistema(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class TipoServico(models.Model):
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Projeto(models.Model):
    nome = models.CharField(max_length=200)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Unidade(models.Model):
    nome = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class PlanejaAquisicaoRecurso(models.Model):
    os = models.ForeignKey('outorga.OrdemDeServico', null=True, blank=True, verbose_name=u'Alteração de contrato')
    # contrato = models.ForeignKey('outorga.Contrato', null=True, blank=True)
    quantidade = models.FloatField()
    valor_unitario = models.DecimalField(u'Valor unitário sem imposto', max_digits=12, decimal_places=2)
    tipo = models.ForeignKey('rede.TipoServico', verbose_name=u'Tipo de descrição')
    referente = models.CharField(max_length=150, null=True, blank=True)
    projeto = models.ForeignKey('rede.Projeto')
    unidade = models.ForeignKey('rede.Unidade')
    instalacao = models.BooleanField(u'Instalação', default=False)
    obs = models.TextField(null=True, blank=True)
    ano = models.IntegerField()
    beneficiados = models.ManyToManyField('identificacao.Entidade', through='Beneficiado')
    banda = models.ForeignKey('rede.Banda', null=True, blank=True)

    def __unicode__(self):
        inst = ''
        if self.instalacao:
            inst = u'Instalação - '
        return u'%s - %s%s - %s - %s - %s (%s)' % (self.os, inst, self.projeto, self.tipo, self.quantidade,
                                                   self.valor_unitario, self.referente)

    @property
    def valor_total(self):
        q = Decimal(str(self.quantidade))
        return q * self.valor_unitario

    class Meta:
        verbose_name = u'Planeja Aquisição de Recursos'
        verbose_name_plural = u'Planeja Aquisição de Recursos'
        ordering = ('os__numero', 'instalacao', 'tipo')


class Beneficiado(models.Model):
    planejamento = models.ForeignKey('rede.PlanejaAquisicaoRecurso')
    entidade = models.ForeignKey('identificacao.Entidade')
    estado = models.ForeignKey('rede.Estado', null=True)
    quantidade = models.FloatField()

    def __unicode__(self):
        return u'%s' % self.entidade

    def porcentagem(self):
        if not self.quantidade:
            return 100.0
        return self.quantidade*100/self.planejamento.quantidade


class Recurso(models.Model):
    planejamento = models.ForeignKey('rede.PlanejaAquisicaoRecurso')
    quantidade = models.FloatField(u'Quantidade (meses pagos)')
    valor_mensal_sem_imposto = models.DecimalField(u'Valor mensal sem imposto', max_digits=12, decimal_places=2,
                                                   null=True, blank=True)
    valor_imposto_mensal = models.DecimalField(u'Valor mensal com imposto', max_digits=12, decimal_places=2)
    pagamento = models.ForeignKey('financeiro.Pagamento', null=True, blank=True)

    mes_referencia = models.DecimalField(u'Mês inicial de referência', max_digits=2, decimal_places=0,
                                         validators=[MaxValueValidator(12), MinValueValidator(1)], null=True,
                                         blank=True)
    ano_referencia = models.DecimalField(u'Ano inicial de referência', max_digits=4, decimal_places=0,
                                         validators=[MinValueValidator(1950)], null=True, blank=True)

    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.planejamento.os, self.planejamento.tipo, self.quantidade)

    def save(self, *args, **kwargs):
        if self.valor_mensal_sem_imposto is None:
            self.valor_mensal_sem_imposto = self.planejamento.valor_total
        super(Recurso, self).save(*args, **kwargs)

    def total_geral(self):
        q = Decimal(str(self.quantidade))
        return q*self.valor_imposto_mensal

    def total_sem_imposto(self):
        q = Decimal(str(self.quantidade))
        return q*self.valor_mensal_sem_imposto


# class Projeto(models.Model):
#     nome = models.CharField(max_length=200)
#
#     def __unicode__(self):
#         return '%s' % self.nome
#
# class Unidade(models.Model):
#     nome = models.CharField(max_length=30)
#
#     def __unicode__(self):
# 	return '%s' % self.nome
#
# class PrestaServico(models.Model):
#     referente = models.CharField(max_length=45, null=True, blank=True)
#     quantidade = models.FloatField()
#     valor_unitario = models.DecimalField(u'Valor unitário sem imposto', max_digits=12, decimal_places=2)
#     os = models.ForeignKey('outorga.OrdemDeServico')
#     tipo = models.ForeignKey('rede.TipoServico', verbose_name=u'Tipo de descrição')
#     pagamento = models.ManyToManyField('financeiro.Pagamento', null=True, blank=True)
#     projeto = models.ForeignKey('rede.Projeto')
#     unidade = models.ForeignKey('rede.Unidade')
#     instalacao = models.BooleanField(u'Instalação')
#     obs = models.TextField(null=True, blank=True)
#
#     def __unicode__(self):
#         return '%s - %s' % (self.os, self.tipo)
#
#     class Meta:
#         verbose_name = u'Presta Serviço'
#         verbose_name_plural = u'Presta Serviços'


class Estado(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        ordering = ('nome',)


class TipoConector(models.Model):
    """
    Representa um tipo de conector utilizado nas IFCs.
    """
    sigla = models.CharField(_(u'Sigla'), max_length=20, unique=True)
    obs = models.TextField(_(u'Observação'), null=True, blank=True)
    imagem = models.ImageField(upload_to='conector', null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.sigla

    class Meta:
        verbose_name = u'Tipo de Conector'
        verbose_name_plural = u'Tipos de Conectores'
        ordering = ('sigla',)


class IFCConector(models.Model):
    """
    Representa um conector de IFCs para a cross conexão.
    """
    rack = models.ForeignKey('identificacao.EnderecoDetalhe')
    shelf = models.CharField(_(u'Shelf'), max_length=5, )  # patrimonio
    porta = models.CharField(_(u'Porta'), max_length=10, )  # novo  porta
    tipoConector = models.ForeignKey('rede.TipoConector')
    ativo = models.BooleanField(u'Conector ativo?', default=True)
    obs = models.TextField(null=True, blank=True)

    def __unicode__(self):
        if self.tipoConector:
            return u'%s | Shelf: %s | Porta: %s | %s' % (self.rack.complemento, self.shelf, self.porta,
                                                         self.tipoConector.sigla)
        return u'%s | Shelf: %s | Porta: %s | -' % (self.rack.complemento, self.shelf, self.porta)

    class Meta:
        verbose_name = u'IFC Conector'
        verbose_name_plural = u'IFC Conectores'
        ordering = ('rack__complemento', 'shelf', 'porta')
        unique_together = ('rack', 'shelf', 'porta')


class CrossConnection(models.Model):
    """
    Representa uma cross conexão.
    """
    origem = models.ForeignKey('rede.IFCConector', related_name='%(class)s_origem')
    destino = models.ForeignKey('rede.IFCConector', related_name='%(class)s_destino')
    circuito = models.CharField(_(u'Circuito'), max_length=40, null=True, blank=True)
    ordemDeServico = models.CharField(_(u'OS/Projeto'), max_length=30, null=True, blank=True)
    obs = models.TextField(_(u'Observação'), null=True, blank=True)
    ativo = models.BooleanField(u'Conector ativo?', default=True)

    def __unicode__(self):
        retorno = ''
        if self.origem:
            retorno += u'%s | %s | %s _X_ ' % (self.origem.rack.complemento, self.origem.shelf, self.origem.porta)
        if self.destino:
            retorno += u'%s | %s | %s' % (self.destino.rack.complemento, self.destino.shelf, self.destino.porta)
        return retorno

    class Meta:
        verbose_name = u'Cross Connection'
        verbose_name_plural = u'Cross Connections'


class CrossConnectionHistorico(models.Model):
    """
    Uma instância dessa classe representa o histórico de uma cross conexão.
    """
    crossConnection = models.ForeignKey(CrossConnection, verbose_name=_(u'Cross Connection'))
    obs = models.TextField(_(u'Observação'), )
    data = models.DateField(_(u'Data'))

    # Define a descrição do modelo e a ordenação dos dados pelo campo 'nome'.
    class Meta:
        verbose_name = _(u'Histórico Local')
        verbose_name_plural = _(u'Histórico Local')
        ordering = ('-data', 'id')


# Classe para definição de permissões de views e relatórios da app rede
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_tec_blocosip", u"Rel. Téc. - Lista de blocos IP"),     # /rede/blocosip
            ("rel_ger_custo_terremark", u"Rel. Ger. - Custos dos recursos contratados"),     # /rede/custo_terremark
            ("rel_tec_info", u"Rel. Téc. - Dados cadastrais dos participantes"),     # /rede/info
            ("rel_tec_planejamento", u"Rel. Téc. - Planejamento por ano"),     # /rede/planejamento
            ("rel_tec_servico_processo", u"Rel. Téc. - Serviços contratados por processo"),     # /rede/planejamento2
            ("rel_tec_recursos_operacional", u"Rel. Téc. - Relatório de recursos"),  # /rede/relatorio_recursos_operacional
            ("rel_tec_blocosip_ansp", u"Rel. Téc. - Blocos IP - ANSP"),     # /rede/blocosip_ansp
            ("rel_tec_blocosip_transito", u"Rel. Téc. - Blocos IP - Trânsito"),     # /rede/blocosip_transito
            ("rel_tec_blocosip_inst_transito", u"Rel. Téc. - Blocos IP - Inst. Trânsito"),  # /rede/blocosip_inst_transito
            ("rel_tec_blocosip_inst_ansp", u"Rel. Téc. - Blocos IP - Inst. ANSP"),     # /rede/blocosip_inst_ansp
            ("rel_tec_crossconnection", u"Lista de Cross Connections"),     # /rede/crossconnection
        )
