# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tipo(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome


class Evento(models.Model):
    acordo = models.ForeignKey('outorga.Acordo', null=True, blank=True)
    tipo = models.ForeignKey('evento.Tipo')
    local = models.CharField(max_length=100)
    descricao = models.CharField(_(u'Descrição'), max_length=200)
    inicio = models.DateTimeField(_(u'Início'))
    termino = models.DateTimeField(_(u'Término'))
    url = models.URLField(u'URL', null=True, blank=True)
    obs = models.TextField(_(u'Observação'), null=True, blank=True)

    def __unicode__(self):
        return self.descricao


class AreaPrograma(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Área do programa')
        verbose_name_plural = _(u'Áreas dos programas')


class Sessao(models.Model):
    area = models.ForeignKey('evento.AreaPrograma', verbose_name=_(u'Área'))
    evento = models.ForeignKey('evento.Evento')
    descricao = models.CharField(_(u'Descrição'), max_length=100)
    local = models.CharField(max_length=100)
    inicio = models.DateTimeField(_(u'Início'))
    termino = models.DateTimeField(_(u'Término'))
    arquivo = models.FileField(upload_to='sessao', null=True, blank=True)
    obs = models.TextField(_(u'Observação'), null=True, blank=True)

    def __unicode__(self):
        return u'%s - %s' % (self.area, self.descricao)

    class Meta:
        verbose_name = _(u'Sessão')
        verbose_name_plural = _(u'Sessões')


class Atribuicao(models.Model):
    membro = models.ForeignKey('membro.Membro')
    relatorio = models.FileField(u'Relatório', upload_to='evento', null=True, blank=True)
    area = models.ForeignKey('evento.AreaOperacional', verbose_name=_(u'Área operacional'))
    sessao = models.ForeignKey('evento.Sessao', verbose_name=_(u'Sessão'))

    def __unicode__(self):
        return u'%s tem a função %s no evento %s' % (self.membro.nome, self.area.nome, self.sessao.descricao)

    class Meta:
        verbose_name = _(u'Atribuição')
        verbose_name_plural = _(u'Atribuições')


class AreaOperacional(models.Model):
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Área operacional')
        verbose_name_plural = _(u'Áreas operacionais')
