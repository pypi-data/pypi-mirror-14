# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models


class Tipo(models.Model):
    """
    Tipo de ocorrência
    """
    entidade = models.ForeignKey('identificacao.Entidade')
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s - %s' % (self.entidade, self.nome)

    class Meta:
        ordering = ('entidade__sigla', 'nome',)


class Estado(models.Model):
    """
    Estado da ocorrência
    """
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Natureza(models.Model):
    """
    Natureza do ocorrido
    """
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Servico(models.Model):
    """
    Serviços envolvidos
    """
    nome = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.nome

    class Meta:
        ordering = ('nome',)


class Ticket(models.Model):
    """
    Tickets do OTRS
    """
    ticket = models.IntegerField()
    repositorio = models.ForeignKey('repositorio.Repositorio')

    def __unicode__(self):
        return '%s' % self.ticket


class Repositorio(models.Model):
    """
    Repositório de informações da ANSP, projetado para guardar todas
    as informações de ocorrências
    """

    # o número é gerado automaticamente
    numero = models.IntegerField(editable=False)

    # data também gerada automaticamente
    data = models.DateField(u'Data de registro', auto_now_add=True)
    data_ocorrencia = models.DateField(u'Data da ocorrência')
    tipo = models.ForeignKey('repositorio.Tipo', help_text=u'Diário de bordo, manutenção, etc.')
    estado = models.ForeignKey('repositorio.Estado', help_text=u'Pendente, resolvido, etc.')
    natureza = models.ForeignKey('repositorio.Natureza', help_text=u'Problema, incidente, etc.')
    servicos = models.ManyToManyField('repositorio.Servico', help_text=u'Serviços envolvidos', verbose_name=u'Serviços',
                                      null=True, blank=True)
    ocorrencia = models.TextField(u'Ocorrência')
    obs = models.TextField(u'Observação', null=True, blank=True)

    anterior = models.ForeignKey('repositorio.Repositorio', help_text=u'Item do repositório ao qual este se refere',
                                 null=True, blank=True)
    memorandos = models.ManyToManyField('memorando.MemorandoSimples', null=True, blank=True)
    patrimonios = models.ManyToManyField('patrimonio.Patrimonio', verbose_name='Patrimônios', null=True, blank=True)
    responsavel = models.ForeignKey('membro.Membro', limit_choices_to={'historico__funcionario': True,
                                                                       'historico__termino__isnull': True},
                                    verbose_name='Responsável')
    demais = models.ManyToManyField('membro.Membro', verbose_name='Demais envolvidos', related_name='outros', null=True,
                                    blank=True)

    def __unicode__(self):
        return u'%s - %s - %s' % (self.num_rep(), self.tipo, self.responsavel)

    def num_rep(self):
        return '%s/%s' % (self.data.year, self.numero)

    num_rep.short_description = u'Número'
    num_rep.admin_order_field = 'numero'

    def proximo_numero(self):
        from datetime import datetime
        from django.db.models import Max

        agora = datetime.now()
        n = Repositorio.objects.filter(data__year=agora.year).aggregate(Max('numero'))
        n = n['numero__max'] or 0
        return n + 1

    def save(self, *args, **kwargs):
        if self.id is None:
            self.numero = self.proximo_numero()
        super(Repositorio, self).save(*args, **kwargs)

    def servicos_display(self):
        return ', '.join([unicode(s) for s in self.servicos.all()])
    servicos_display.short_description = u'Serviços'

    class Meta:
        verbose_name = u'Repositório'
        verbose_name_plural = u'Repositórios'


class Anexo(models.Model):
    """
    Arquivos anexos ao repositório
    """
    arquivo = models.FileField(upload_to='repositorio')
    palavras_chave = models.TextField(u'Palavras chave')
    repositorio = models.ForeignKey('repositorio.Repositorio')

    def lista_palavras_chave(self):
        return self.palavras_chave.split()


# Classe para definição de permissões de views e relatórios da app repositorio
class Permission(models.Model):
    class Meta:
        # remover as permissões padrões, pois essa é uma classe para configurar permissões customizadas
        default_permissions = ()
        permissions = (
            ("rel_ger_repositorio", "Rel. admin. - Repositório"),  # /repositorio/relatorios/repositorio
        )
