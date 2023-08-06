# -*- coding:utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models


class Area(models.Model):
    nome = models.CharField(max_length=45)
    escopo = models.TextField()

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u'Área'
        verbose_name_plural = u'Áreas'
        ordering = ('nome',)


class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    area = models.ForeignKey('processo.Area')

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('area', 'nome')


class Macroprocesso(models.Model):
    nome = models.TextField()
    grupo = models.ForeignKey('processo.Grupo')

    def __unicode__(self):
        return u'%s - %s' % (self.grupo, self.nome)

    def area(self):
        return self.grupo.area
    area.admin_order_field = 'grupo__area'

    class Meta:
        ordering = ('grupo', 'nome')


class Norma(models.Model):
    nome = models.CharField(max_length=120)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Recurso(models.Model):
    nome = models.CharField(max_length=120)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class OTRS(models.Model):
    nome = models.CharField(max_length=120)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Processo(models.Model):
    nome = models.TextField('Processo')
    obs = models.TextField(null=True, blank=True)
    macroprocesso = models.ForeignKey('processo.Macroprocesso')
    normas = models.ManyToManyField('processo.Norma', null=True, blank=True)
    visao = models.ForeignKey('processo.Visao', verbose_name=u'Visão')
    natureza = models.ForeignKey('processo.Natureza')
    entradas = models.ManyToManyField('processo.Recurso', null=True, blank=True, related_name='entra')
    saidas = models.ManyToManyField('processo.Recurso', null=True, blank=True, related_name='sai')
    entrada_otrs = models.ManyToManyField('processo.OTRS', null=True, blank=True, related_name='entra_otrs')
    saida_otrs = models.ManyToManyField('processo.OTRS', null=True, blank=True, related_name='sai_otrs')

    def __unicode__(self):
        return self.nome

    def somacro(self):
        return self.macroprocesso.nome
    somacro.admin_order_field = 'macroprocesso'
    somacro.short_description = 'Macroprocesso'

    def grupo(self):
        return self.macroprocesso.grupo
    grupo.admin_order_field = 'macroprocesso__grupo'

    def area(self):
        return self.grupo().area
    area.admin_order_field = 'macroprocesso__grupo__area'

    def procedimentos(self):
        return u', '.join(self.procedimento_set.all())

    class Meta:
        ordering = ('macroprocesso', 'nome')


class Equipe(models.Model):
    nome = models.CharField(max_length=45)
    membros = models.ManyToManyField('membro.Membro')

    def __unicode__(self):
        return self.nome


class Papel(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name_plural = u'Papéis'


class Atribuicao(models.Model):
    processo = models.ForeignKey('processo.Processo')
    equipe = models.ForeignKey('processo.Equipe')
    papel = models.ForeignKey('processo.Papel')

    def __unicode__(self):
        return u'%s - %s' % (self.equipe, self.processo)

    class Meta:
        verbose_name = u'Atribuição'
        verbose_name_plural = u'Atribuições'


class Visao(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u'Visão'
        verbose_name_plural = u'Visões'


class Natureza(models.Model):
    nome = models.CharField(max_length=45)

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


class Procedimento(models.Model):
    nome = models.CharField(max_length=200)
    processo = models.ForeignKey('processo.Processo')

    def __unicode__(self):
        return self.nome

    class Meta:
        ordering = ('nome',)


# Classe para definição de permissões de views e relatórios da app Processo
class Permission(models.Model):

    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_ger_processos", "Rel. Ger. - Processos"),     # /processo/processos
        )
