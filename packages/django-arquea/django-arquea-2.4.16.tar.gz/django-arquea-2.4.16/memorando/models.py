# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _


def proximo_numero():
    from datetime import datetime
    from django.db.models import Max
    agora = datetime.now()
    n1 = MemorandoSimples.objects.filter(data__year=agora.year).aggregate(Max('numero'))
    n2 = MemorandoResposta.objects.filter(data__year=agora.year).aggregate(Max('numero'))
    n1 = n1['numero__max'] or 0
    n2 = n2['numero__max'] or 0

    return max(n1, n2) + 1


class Estado(models.Model):

    """
    Uma instância dessa classe é um estado (ex. Aguardando assinatura).
    O método '__unicode__'	Retorna o nome.
    A class 'Meta'		Define a ordem de apresentação dos dados pelo nome.

    >>> e, created = Estado.objects.get_or_create(nome='Aguardando assinatura')

    >>> e.__unicode__()
    'Aguardando assinatura'
    """
    nome = models.CharField(_(u'Nome'), max_length=30, help_text=_(u'ex. Aguardando assinatura'), unique=True)

    # Retorna o nome.
    def __unicode__(self):
        return self.nome

    # Define a ordenação dos dados pelo nome.
    class Meta:
        ordering = ("nome", )


class Assunto(models.Model):
    descricao = models.CharField(max_length=100)

    def __unicode__(self):
        return self.descricao


class MemorandoFAPESP(models.Model):
    termo = models.ForeignKey('outorga.Termo')
    numero = models.CharField(_(u'Número do memorando'), max_length=15)
    arquivo = models.FileField(upload_to='memorando', null=True, blank=True)

    def __unicode__(self):
        return self.numero

    class Meta:
        verbose_name = _(u'Memorando da FAPESP')
        verbose_name_plural = _(u'Memorandos da FAPESP')


class Pergunta(models.Model):
    memorando = models.ForeignKey('memorando.MemorandoFAPESP')
    numero = models.CharField(_(u'Número da pergunta'), max_length=10)
    questao = models.TextField(_(u'Questão'))

    def __unicode__(self):
        return u'%s - pergunta %s' % (self.memorando, self.numero)

    class Meta:
        ordering = ('numero',)


class MemorandoResposta(models.Model):
    memorando = models.ForeignKey('memorando.MemorandoFAPESP')
    estado = models.ForeignKey('memorando.Estado')
    assunto = models.ForeignKey('memorando.Assunto')
    assinatura = models.ForeignKey('membro.Assinatura')
    numero = models.IntegerField(editable=False)
    anexa_relatorio = models.BooleanField(u'Anexar relatório de inventário?', default=False)
    identificacao = models.ForeignKey('identificacao.Identificacao', verbose_name=_(u'Identificação'))
    data = models.DateField()
    arquivo = models.FileField('Documento assinado', upload_to='memorando', null=True, blank=True)
    protocolo = models.FileField(upload_to='memorando', null=True, blank=True)
    obs = models.TextField(null=True, blank=True)
    introducao = models.TextField(_(u'Introdução'), null=True, blank=True)
    conclusao = models.TextField(_(u'Conclusão'), null=True, blank=True)
    # classificacao = models.ForeignKey('financeiro.TipoComprovante', verbose_name=_(u'Classificação'))

    def __unicode__(self):
        return u'%s/%s' % (self.data.year, self.numero)

    '''
    O método para salvar uma instância é sobrescrito para que o número sequencial
    do memorando seja gerado automaticamente para cada ano.
    '''
    def save(self, *args, **kwargs):
        if self.id is None:
            self.numero = proximo_numero()
        super(MemorandoResposta, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'Memorando de resposta à FAPESP')
        verbose_name_plural = _(u'Memorandos de resposta à FAPESP')
        ordering = ('data',)

    def termo(self):
        return self.memorando.termo


class Corpo(models.Model):
    """
    Cada item de um memorando da FAPESP
    """
    memorando = models.ForeignKey('memorando.MemorandoResposta')
    pergunta = models.ForeignKey('memorando.Pergunta')
    resposta = models.TextField()
    anexo = models.FileField(u'Anexo (em pdf)', upload_to='memorando', null=True, blank=True)
    concluido = models.BooleanField('Ok', default=False)

    def __unicode__(self):
        return u'%s' % self.pergunta.numero

    class Meta:
        ordering = ('pergunta__numero', 'memorando__data')


class MemorandoSimples(models.Model):
    superior = models.IntegerField(default=3)
    inferior = models.IntegerField(default=2)
    esquerda = models.IntegerField(default=3)
    direita = models.IntegerField(default=3)
    data = models.DateField(auto_now_add=True)
    destinatario = models.TextField(u'Destinatário')
    numero = models.IntegerField(editable=False)
    assunto = models.ForeignKey('memorando.Assunto', null=True)
    corpo = models.TextField()
    equipamento = models.BooleanField('Equipamento?', default=False)
    envio = models.BooleanField('Envio?', default=False)
    assinatura = models.ForeignKey('membro.Membro')
    assinado = models.FileField(_(u'Memorando assinado'), upload_to='memorandos', null=True, blank=True)
    pai = models.ForeignKey('memorando.MemorandoSimples', verbose_name=u'Memorando pai', null=True, blank=True)

    def __unicode__(self):
        if self.assunto_id is not None:
            return u'%s/%s - %s' % (self.data.year, self.numero, self.assunto.__unicode__())
        else:
            return u'%s/%s' % (self.data.year, self.numero)

    def num_memo(self):
        return u'%s/%s' % (self.data.year, self.numero)
    num_memo.admin_order_field = 'data'
    num_memo.short_description = u'Número'

    class Meta:
        verbose_name_plural = u'Memorandos Simples'
        ordering = ('-data', '-numero')

    '''
    O método para salvar uma instância é sobrescrito para que o número sequencial
    do memorando seja gerado automaticamente para cada ano.
    '''
    def save(self, *args, **kwargs):
        if self.id is None:
            self.numero = proximo_numero()
        super(MemorandoSimples, self).save(*args, **kwargs)

    def destino(self):
        dest = self.destinatario.split('\n')
        return '<br />'.join(dest)


class Arquivo(models.Model):
    arquivo = models.FileField(upload_to='memorando')
    memorando = models.ForeignKey('memorando.MemorandoSimples')

    def __unicode__(self):
        return self.arquivo.name


# Classe para definição de permissões de views e relatórios da app Memorando
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_adm_memorando", "Rel. Adm. - Memorandos FAPESP"),   # /memorando/relatorio
        )
