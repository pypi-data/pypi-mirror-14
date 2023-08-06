# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from configuracao.models import LayoutPagina, LayoutLinkHeader, LayoutLinkFooter

site = admin.site


def static_root(request):
    """
    Adds STATIC_ROOT settings to the context.
    """
    return {'STATIC_ROOT': settings.STATIC_ROOT}


def debug(context):
    """
    Disponibiliza a variável de DEBUG para o template
    """
    return {'DEBUG': settings.DEBUG}


def _applist(request):
    app_dict = {}
    user = request.user
    for model, model_admin in site._registry.items():
        app_label = model._meta.app_label
        try:
            app = __import__(app_label)
            app_verbose_name = app.verbose_name
        except:
            app_verbose_name = app_label.title()
        has_module_perms = user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            if True in perms.values():
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'admin_url': mark_safe('/admin/%s/%s/' % (app_label, model.__name__.lower())),
                    'perms': perms,
                }
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': app_label.title(),
                        'verbose_name': app_verbose_name,
                        'app_url': app_label + '/',
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    app_list = app_dict.values()
    app_list.sort(lambda x, y: cmp(x['name'], y['name']))
    for app in app_list:
        app['models'].sort(lambda x, y: cmp(x['name'], y['name']))
    return {'adm_app_list': app_list}


def _papelaria(context):
    """
    Disponibiliza o acesso aos arquivos de papel timbrado para o template django.
    Ver as opções disponíveis em: configuracao.models.papelaria
    Utilizar:

    no PisaPdF
    {% load static %}
    <img src="{% get_media_prefix %}{{papelaria.papel_timbrado_retrato_a4}}">

    no WeasyPDF utilizar
    <img src="media:{{papelaria.papel_timbrado_retrato_a4}}">
    """
    from configuracao.models import Papelaria

    arquivos = Papelaria.objects.all()

    for a in arquivos:
        if a.valido:
            return {'papelaria': a}
    return {'papelaria': ''}


def _layoutPagina(context):
    """
    """
    layoutPagina = LayoutPagina.objects.all().first()

    logoHeader = ''
    if layoutPagina and layoutPagina.logo_cabecalho and layoutPagina.logo_cabecalho.logo:
        logoHeader = layoutPagina.logo_cabecalho

    logoFooter = ''
    if layoutPagina and layoutPagina.logo_rodape and layoutPagina.logo_rodape.logo:
        logoFooter = layoutPagina.logo_rodape

    linksHeader = None
    if layoutPagina:
        linksHeader = LayoutLinkHeader.objects.all().filter(pagina=layoutPagina).order_by('ordem')

    linksFooter = None
    if layoutPagina:
        linksFooter = LayoutLinkFooter.objects.all().filter(pagina=layoutPagina).order_by('ordem')

    return {'layoutPagina': layoutPagina,
            'logoHeader': logoHeader,
            'linksHeader': linksHeader,
            'logoFooter': logoFooter,
            'linksFooter': linksFooter}


def sistema(context):
    # Agrega
    new_context_values = {}
    new_context_values.update(_applist(context))
    new_context_values.update(_papelaria(context))
    new_context_values.update(_layoutPagina(context))

    return new_context_values
