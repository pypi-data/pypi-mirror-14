# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils import timezone
from utils.models import CNPJField
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
import re


class Contato(models.Model):
    """
    Uma instância dessa classe representa um contato.

    O método '__unicode__'	Retorna o nome.
    O método 'contato_ent'	Retorna as entidades do contato.
    A 'class Meta'		Ordena os dados pelo campo 'nome'.
    """
    primeiro_nome = models.CharField(_(u'Primeiro nome'), max_length=100, help_text=_(u'ex. João Andrade'))
    ultimo_nome = models.CharField(_(u'Último nome'), max_length=45)
    email = models.CharField(_(u'E-mail'), max_length=100, blank=True, help_text=_(u'ex. joao@joao.br'))
    ativo = models.BooleanField(_(u'Ativo'), default=True)
    tel = models.CharField(_(u'Telefone'), max_length=100,
                           help_text=_(u'ex. Com. (11)2222-2222, Cel. (11)9999-9999, Fax (11)3333-3333, ...'))
    documento = models.CharField(max_length=30, null=True, blank=True)

    @property
    def nome(self):
        if self.ultimo_nome:
            return '%s %s' % (self.primeiro_nome, self.ultimo_nome or '')
        else:
            return self.primeiro_nome

    # Retorna o nome.
    def __unicode__(self):
        return self.nome

    # Retorna as entidades do contato.
    def contato_ent(self):
        ident = self.identificacao_set.all()
        ent = []
        for i in ident:
            if i.endereco.entidade not in ent:
                ent.append(i.endereco.entidade)
        l = [e.sigla for e in ent]
        e = ', '.join(l)
        return u'%s' % e
    contato_ent.short_description = _(u'Entidade')

    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ('primeiro_nome', 'ultimo_nome')


class TipoDetalhe(models.Model):
    nome = models.CharField(max_length=40)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class EnderecoDetalhe(models.Model):
    endereco = models.ForeignKey('identificacao.Endereco', limit_choices_to={'data_inatividade__isnull': True},
                                 null=True, blank=True)
    tipo = models.ForeignKey('identificacao.TipoDetalhe')
    complemento = models.TextField()
    detalhe = models.ForeignKey('identificacao.EnderecoDetalhe', verbose_name=u'ou Detalhe pai', null=True, blank=True)
    ordena = models.CharField(editable=False, max_length=1000, null=True)
    mostra_bayface = models.BooleanField(_(u'Mostra no bayface'), help_text=_(u''), default=False)

    def save(self, *args, **kwargs):
        if self.endereco is None and self.detalhe is None:
            return
        if self.endereco is not None and self.detalhe is not None:
            return
        self.ordena = self.__unicode__()
        super(EnderecoDetalhe, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.endereco_id:
            return u'%s - %s' % (self.endereco, self.complemento)
        else:
            return u'%s - %s' % (self.detalhe, self.complemento)

    def detalhes(self):
        if self.endereco:
            return self.complemento
        else:
            return u'%s - %s' % (self.detalhe.detalhes(), self.complemento)

    def entidade(self):
        """
        Busca entidade relacionada ao EnderecoDetalhe.
        Como a Entidade está relacionada ao Endereço, ele faz a busca nos pais de
            EnderecosDetalhes até encontrar um Endereco.
        """
        retorno = ''
        if self.endereco_id:
            # Se tiver endereço, retorno a entidade do endereço
            if self.endereco.entidade_id:
                retorno = self.endereco.entidade.sigla
        elif self.detalhe_id:
            # Se pertencer a outro EnderecoDetalhe, tenta navegar para pegar o endereço pai
            retorno = self.detalhe.entidade()

        return retorno

    @property
    def end(self):
        if self.endereco:
            return self.endereco
        return self.detalhe.end

    class Meta:
        ordering = ('ordena', )
    #    verbose_name = u'Detalhe do endereço'
    #    verbose_name_plural = u'Detalhes dos endereços'


class Endereco(models.Model):

    """
    Uma instância dessa classe representa um endereco de uma identificação.

    O método '__unicode__'	Retorna os campos 'rua', 'num' e 'compl' (se existir).
    A 'class Meta'		Define a descrição do modelo (singular e plural), a ordenação dos dados e a unicidade que um
    endereço pelos campos 'identificacao', 'rua', 'num', 'compl', 'bairro', 'cidade', 'cep', 'estado' e 'pais'.
    """
    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Entidade'))
    rua = models.CharField(_(u'Logradouro'), max_length=100, help_text=_(u'ex. R. Dr. Ovídio Pires de Campos'))
    num = models.IntegerField(_(u'Num.'), help_text=_(u'ex. 215'), null=True, blank=True)
    compl = models.CharField(_(u'Complemento'), max_length=100, blank=True,
                             help_text=_(u'ex. 2. andar - Prédio da PRODESP'))
    bairro = models.CharField(_(u'Bairro'), max_length=50, blank=True, help_text=_(u'ex. Cerqueira César'))
    cidade = models.CharField(_(u'Cidade'), max_length=50, blank=True, help_text=_(u'ex. São Paulo'))
    cep = models.CharField(_(u'CEP'), max_length=8, blank=True, help_text=_(u'ex. 05403010'))
    estado = models.CharField(_(u'Estado'), max_length=50, blank=True, help_text=_(u'ex. SP'))
    pais = models.CharField(_(u'País'), max_length=50, blank=True, help_text=_(u'ex. Brasil'))
    data_inatividade = models.DateField(_(u'Data de inatividade'), blank=True, null=True)

    # Retorna os campos rua, num e compl (se existir).
    def __unicode__(self):
        return u'%s - %s' % (self.entidade.sigla, self.logradouro())
    __unicode__.short_description = _(u'Logradouro')

    def logradouro(self):
        num = ', %s' % self.num if self.num else ''
        compl = ', %s' % self.compl if self.compl else ''
        return u'%s%s%s' % (self.rua, num, compl)

    # Define a descricao do modelo, a ordenação dos dados pela cidade e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Endereço')
        verbose_name_plural = _(u'Endereços')
        ordering = ('entidade', )
        unique_together = (('rua', 'num', 'compl', 'bairro', 'cidade', 'cep', 'estado', 'pais'),)


class ASN(models.Model):
    """
    Tabela com os ASs da Internet
    """
    numero = models.IntegerField(u'Número do AS')
    entidade = models.ForeignKey('identificacao.Entidade', null=True, blank=True)
    pais = models.CharField(u'País', null=True, blank=True, max_length=3)

    def __unicode__(self):
        if self.entidade:
            return u'%s - %s' % (self.numero, self.entidade)
        else:
            return self.numero

    class Meta:
        verbose_name = u'ASN'
        verbose_name_plural = u'ASNs'
        ordering = ('numero', )


class Entidade(models.Model):
    """
    Uma instância dessa classe representa uma entidade cadastrada no sistema.

    O método '__unicode__'	Retorna a sigla da entidade.
    O método 'sigla_nome'	Retorna a sigla e o nome da entidade.
    O método 'save'		Faz a validação do CNPJ e converte todos os caracteres da sigla para maiúsculo.
    A 'class Meta' 		Define a ordenação dos dados pela sigla.

    A unicidade dos dados é feita através do campo 'sigla'.
    """
    TERREMARK_ID = 1

    entidade = models.ForeignKey('identificacao.Entidade', verbose_name=_(u'Faz parte de'), null=True, blank=True,
                                 related_name='entidade_em')
    nome = models.CharField(_(u'Nome'), max_length=255,
                            help_text=_(u'Razão Social (ex. Telecomunicações de São Paulo S.A.)'))
    url = models.URLField(_(u'URL'), blank=True, help_text=_(u'ex. www.telefonica.com.br'))
    sigla = models.CharField(_(u'Sigla'), max_length=20, help_text=_(u'Nome Fantasia (ex. TELEFÔNICA)'), unique=True)
    # asn = models.IntegerField(_(u'ASN'), blank=True, null=True, help_text=_(u' '))
    cnpj = CNPJField(_(u'CNPJ'), blank=True, help_text=_(u'ex. 00.000.000/0000-00'))
    fisco = models.BooleanField(_(u'Fisco'), help_text=_(u'ex. Ativo no site da Receita Federal?'), default=False)
    recebe_doacao = models.BooleanField(_(u'Recebe doação de equipamentos?'), default=False)

    # Retorna a sigla.
    def __unicode__(self):
        return self.sigla

    def sigla_completa(self):
        if self.entidade_id:
            return u'%s - %s' % (self.entidade.sigla_completa(), self.sigla)
        else:
            return u'%s' % self.sigla
    sigla_completa.short_description = _(u'Faz parte de')

    # Retorna a sigla com 4 espaços iniciais para cada nível de entidade pai
    def sigla_tabulada(self):
        if self.entidade_id:
            entidade_pai = self.entidade.sigla_tabulada()
            # substitui qualquer string que não inicia com espaços por quatro espaços
            retorno = re.sub('[^\s]+.+', '    ', entidade_pai)
            return u'%s%s' % (retorno, self.sigla)
        else:
            return u'%s' % self.sigla
    sigla_tabulada.short_description = _(u'Faz parte de')

    # Retorna a sigla e o nome.
    def sigla_nome(self):
        return u'%s - %s' % (self.sigla, self.nome)
    sigla_nome.short_description = _(u'Entidade')

    # Grava o CNPJ no banco de dados com as devidas pontuações e converte a sigla em letras maiúsculas.
    def save(self, force_insert=False, force_update=False, using=None):
        if self.cnpj and len(self.cnpj) < 18:
            a = list(self.cnpj)
            p = [(2, '.'), (6, '.'), (10, '/'), (15, '-')]
            for i in p:
                if i[1] != a[i[0]]:
                    a.insert(i[0], i[1])
            self.cnpj = ''.join(a)
        self.sigla = self.sigla.upper()
        super(Entidade, self).save(force_insert, force_update)

    # Define a ordenação dos dados pela sigla.
    class Meta:
        ordering = ('sigla', )


class EntidadeHistorico(models.Model):
    inicio = models.DateField()
    termino = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(_(u'Ativo'), default=False)
    obs = models.TextField(_(u'Observação'), blank=True, null=True)
    entidade = models.ForeignKey('identificacao.Entidade')
    tipo = models.ForeignKey('identificacao.TipoEntidade')

    def __unicode__(self):
        return u'%s %s %s' % (self.entidade.sigla, self.tipo.nome, self.inicio)


class Identificacao(models.Model):
    """
    Uma instância dessa classe representa uma identificação de uma empresa, fornecedor ou contato.

    O método 'formata_historico'	Retorna o histórico no formato dd/mm/aa hh:mm
    O método '__unicode__'		Retorna sigla da entidade e o nome do contato.
    A 'class Meta'			Define a descrição do modelo (singular e plural), a ordenação dos dados pela entidade e a
    unicidade dosdados pelos campos contato, entidade.
    """
    # monitor = models.ForeignKey('rede.Monitor', verbose_name=_(u'Monitor'))
    # entidade = models.ForeignKey('identificacao.Entidade', null=True, blank=True)
    endereco = models.ForeignKey('identificacao.Endereco', limit_choices_to={'data_inatividade__isnull': True},
                                 verbose_name=_(u'Entidade'))
    contato = models.ForeignKey('identificacao.Contato', verbose_name=_(u'Contato'))
    historico = models.DateTimeField(_(u'Histórico'), default=datetime.now, editable=False)
    area = models.CharField(_(u'Área'), max_length=50, blank=True, help_text=_(u'ex. Administração'))
    funcao = models.CharField(_(u'Função'), max_length=50, blank=True, help_text=_(u'ex. Gerente Administrativo'))
    ativo = models.BooleanField(_(u'Ativo'), default=False)

    # Define a descrição do modelo, a ordenação dos dados pela entidade e a unicidade dos dados.
    class Meta:
        verbose_name = _(u'Identificação')
        verbose_name_plural = _(u'Identificações')
        ordering = ('endereco', 'contato')
        unique_together = (('endereco', 'contato'),)

    # Retorna a sigla da entidade e o nome do contato.
    def __unicode__(self):
        if self.area:
            return u'%s - %s - %s' % (self.endereco.entidade, self.area, self.contato.nome)
        else:
            return u'%s - %s' % (self.endereco.entidade, self.contato.nome)

    # Retorna o histórico formatado.
    def formata_historico(self):
        historico = timezone.localtime(self.historico) if timezone.is_aware(self.historico) else historico
        return historico.strftime('%d/%m/%y %H:%M')
    formata_historico.short_description = _(u'Histórico')


class TipoArquivoEntidade(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class ArquivoEntidade(models.Model):
    arquivo = models.FileField(upload_to='entidade')
    entidade = models.ForeignKey('identificacao.Entidade')
    data = models.DateField()
    tipo = models.ForeignKey('identificacao.TipoArquivoEntidade')

    def __unicode__(self):
        return u'%s - %s' % (self.entidade.sigla, self.arquivo.name)

    class Meta:
        ordering = ('tipo', '-data')


class TipoEntidade(models.Model):
    nome = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class PapelEntidade(models.Model):
    data = models.DateField()
    tipo = models.ForeignKey('identificacao.TipoEntidade')
    entidade = models.ForeignKey('identificacao.Entidade')

    def __unicode__(self):
        return u'%s - %s' % (self.entidade, self.tipo)


class Agenda(models.Model):
    nome = models.CharField(max_length=40)
    entidades = models.ManyToManyField('identificacao.Entidade', through='Agendado')

    def __unicode__(self):
        return u'%s' % self.nome


class Agendado(models.Model):
    agenda = models.ForeignKey('identificacao.Agenda')
    entidade = models.ForeignKey('identificacao.Entidade')
    ativo = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s' % (self.agenda.nome, self.entidade.sigla)


class Acesso(models.Model):
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=u'Identificação')
    niveis = models.ManyToManyField('identificacao.NivelAcesso', verbose_name=u'Níveis de acesso', null=True,
                                    blank=True)
    liberacao = models.DateTimeField(u'Liberação', null=True, blank=True)
    encerramento = models.DateTimeField(null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    detalhe = models.ManyToManyField('identificacao.EnderecoDetalhe', null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.identificacao, self.lista_niveis())

    def lista_niveis(self):
        lista = ', '.join([n.nome for n in self.niveis.all()])
        return lista
    lista_niveis.short_description = 'Nivel de acesso'


class NivelAcesso(models.Model):
    nome = models.CharField(max_length=50)
    explicacao = models.TextField('Explicação')

    def __unicode__(self):
        return u'%s' % self.nome

    class Meta:
        verbose_name = u'Nível de acesso'
        verbose_name_plural = u'Níveis de acesso'


class Ecossistema(models.Model):
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=u'Entidade/contato')
    incentivo = models.BooleanField(u'Incentivar a dar palestra?', default=False)
    monitora = models.BooleanField(u'Monitorar o convite?', default=False)
    data_envio = models.DateField(u'Data de envio do e-mail', null=True, blank=True)
    data_resposta = models.DateField(u'Data de resposta ao e-mail', null=True, blank=True)
    dar_palestra = models.BooleanField(u'Vai dar palestra?', default=False)
    palestrante = models.CharField(max_length=50, null=True, blank=True)
    tema = models.CharField(max_length=50, null=True, blank=True)
    temas_adicionais = models.TextField(u'Temas adicionais sugeridos', null=True, blank=True)
    data_envio_postal = models.DateField(u'Data de envio do material postal', null=True, blank=True)
    inscricoes_solicitadas = models.IntegerField(u'Número de inscrições solicitadas', null=True, blank=True)
    inscricoes_aceitas = models.IntegerField(u'Número de inscrições aceitas', null=True, blank=True)
    comentarios = models.TextField(u'Comentários', null=True, blank=True)
    hotel = models.BooleanField(u'Quer hotel?', default=False)

    contato_pat = models.BooleanField(u'Contato para patrocínio?', default=False)
    vip = models.BooleanField(default=False)
    chaser = models.CharField(max_length=40, null=True, blank=True)
    vai_pat = models.BooleanField(u'Vai patrocinar?', default=False)

    def __unicode__(self):
        return u'%s' % self.identificacao.endereco.entidade.sigla

    class Meta:
        ordering = ('identificacao__endereco__entidade__sigla',)


# Classe para definição de permissões de views e relatórios da app identificação
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_adm_agenda", "Rel. Adm. - Agenda"),  # /identificacao/agenda
            ("rel_adm_ecossistema", "Rel. Adm. - Ecossistema"),  # /identificacao/ecossistema/par
            # movido de relatorio tecnico para administrativo
            ("rel_tec_arquivos", "Rel. Adm. - Documentos por entidade"),  # /identificacao/relatorios/arquivos
        )
