# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.http import require_safe

from utils.functions import render_to_pdf_weasy
from processo.models import Area


@login_required
@permission_required('processo.rel_ger_processos', raise_exception=True)
@require_safe
def processos(request, pdf=False):
    """
     Relatório Gerencial - Relatório de processos.
    """
    areas = []
    for a in Area.objects.all():
        area = {'area': a}
        grupos = []
        for g in a.grupo_set.all():
            grupo = {'grupo': g}
            macroprocessos = []
            for m in g.macroprocesso_set.all():
                macroprocesso = {'macroprocesso': m, 'processos': m.processo_set.all()}
                macroprocessos.append(macroprocesso)
            grupo['macroprocessos'] = macroprocessos
            grupos.append(grupo)
        area['grupos'] = grupos
        areas.append(area)

    if pdf == '2':
        # Gera arquivo PDF em A3
        return render_to_pdf_weasy('processo/processos2.pdf', {'areas': areas}, request=request,
                                   filename='processos.pdf')
    elif pdf:
        # Gera arquivo PDF em A3 ou A4. O parametro pdf é o que define o tamanho.
        return render_to_pdf_weasy('processo/processos.pdf', {'areas': areas, 'tamanho': pdf}, request=request,
                                   filename='processos.pdf')
    else:
        return TemplateResponse(request, 'processo/processos.html', {'areas': areas})
