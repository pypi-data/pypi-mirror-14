# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class Papelaria(models.Model):
    """
    Classe parar configuração da imagem de fundo utilizado na geração de PDFs com papel timbrado.
    """
    papel_timbrado_retrato_a4 = models.FileField(upload_to='papel_timbrado_retrato_a4', null=True, blank=True)
    retrato_a4_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2,
                                                     null=True, blank=True)
    retrato_a4_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2,
                                                     null=True, blank=True)

    papel_timbrado_paisagem_a4 = models.FileField(upload_to='papel_timbrado_paisagem_a4', null=True, blank=True)
    paisagem_a4_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2,
                                                      null=True, blank=True)
    paisagem_a4_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2,
                                                      null=True, blank=True)

    papel_timbrado_retrato_a3 = models.FileField(upload_to='papel_timbrado_retrato_a3', null=True, blank=True)
    retrato_a3_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2,
                                                     null=True, blank=True)
    retrato_a3_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2,
                                                     null=True, blank=True)

    papel_timbrado_paisagem_a3 = models.FileField(upload_to='papel_timbrado_paisagem_a3', null=True, blank=True)
    paisagem_a3_margem_superior = models.DecimalField(_(u'Margem superior em cm'), max_digits=3, decimal_places=2,
                                                      null=True, blank=True)
    paisagem_a3_margem_inferior = models.DecimalField(_(u'Margem inferior em cm'), max_digits=3, decimal_places=2,
                                                      null=True, blank=True)

    valido = models.BooleanField(u'Template válido?', default=True)

    def has_files(self):
        import os.path

        return self.papel_timbrado_retrato_a4 is not None and self.papel_timbrado_retrato_a4.name and \
            os.path.isfile(self.papel_timbrado_retrato_a4.name) and self.papel_timbrado_paisagem_a4 is not None and \
            self.papel_timbrado_paisagem_a4.name and os.path.isfile(self.papel_timbrado_paisagem_a4.name) and \
            self.papel_timbrado_retrato_a3 is not None and self.papel_timbrado_retrato_a3.name and \
            os.path.isfile(self.papel_timbrado_retrato_a3.name) and self.papel_timbrado_paisagem_a3 is not None and \
            self.papel_timbrado_paisagem_a3.name and os.path.isfile(self.papel_timbrado_paisagem_a3.name)


class Cheque(models.Model):
    """
    Objeto de configuração da imagem de fundo utilizado na geração de PDFs com papel timbrado.
    """
    nome_assinatura = models.CharField(_(u'Assinatura'), max_length=150)


class Variavel(models.Model):
    # Nome da variável. É utilizada nos outros models para identificar a variável.
    DATACENTER_IDS = 'DATACENTER_IDS'
    TERMO_EXCLUIDO_IDS = 'TERMO_EXCLUIDO_IDS'

    # Nome das variáveis e suas descrições que devem ser exibidas na tela do Administrador
    _NOMES = (
        (DATACENTER_IDS, 'ID da Entidade do Datacenter principal.'),
        (TERMO_EXCLUIDO_IDS, 'IDs de Termos a serem excluídos da visão de relatórios, '
                             'como o de Patrimônio por Termo. Ex: 1,2,3'),
    )

    nome = models.CharField(_(u'Nome da variável'), max_length=60, unique=True, choices=_NOMES)
    valor = models.CharField(_(u'Valor'), max_length=60, help_text=u'', )
    obs = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _(u'Variável')
        verbose_name_plural = _(u'Variáveis')
        ordering = ('nome',)


class ClassesExtra(models.Model):
    content_type = models.ForeignKey(ContentType)
    help = models.TextField()

    def __unicode__(self):
        return '%s/%s - extra' % (self.content_type.app_label, self.content_type.model)

    class Meta:
        ordering = ('content_type__app_label', 'content_type__model')
        verbose_name = u'Ajuda dos modelos'
        verbose_name_plural = u'Ajudas dos modelos'


class FieldsHelp(models.Model):
    model = models.ForeignKey(ClassesExtra)
    field = models.CharField(max_length=30)
    help = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s/%s - %s' % (self.model.content_type.app_label, self.model.content_type.model, self.field)

    class Meta:
        verbose_name = u'Ajuda dos campos'
        verbose_name_plural = u'Ajudas dos campos'


class LayoutPagina(models.Model):
    logo_cabecalho = models.ForeignKey('configuracao.LayoutLogo', related_name="+")
    logo_rodape = models.ForeignKey('configuracao.LayoutLogo', related_name="+")

    class Meta:
        verbose_name = u'Layout da página'
        verbose_name_plural = u'Layout das páginas'


class LayoutLogo(models.Model):
    logo = models.ImageField(null=True, blank=True)
    titulo = models.CharField(_(u'Título do logo'), max_length=200)
    url = models.CharField(_(u'URL do logo'), max_length=400, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.titulo

    class Meta:
        verbose_name = u'Logotipo do layout'
        verbose_name_plural = u'Logotipos do layout'


class LayoutLink(models.Model):
    titulo = models.CharField(max_length=200)
    url = models.URLField(max_length=400)
    ordem = models.PositiveSmallIntegerField(help_text=u"Ordem de exibição do link.")

    def __unicode__(self):
        return '%s' % self.titulo

    class Meta:
        ordering = ('ordem', 'titulo')
        verbose_name = u'Link do layout'
        verbose_name_plural = u'Links do layout'


class LayoutLinkHeader(LayoutLink):
    pagina = models.ForeignKey('configuracao.LayoutPagina')

    class Meta:
        verbose_name = u'Link do cabeçalho'
        verbose_name_plural = u'Links do cabeçalho'


class LayoutLinkFooter(LayoutLink):
    pagina = models.ForeignKey('configuracao.LayoutPagina')

    class Meta:
        verbose_name = u'Link do rodapé'
        verbose_name_plural = u'Links do rodapé'
