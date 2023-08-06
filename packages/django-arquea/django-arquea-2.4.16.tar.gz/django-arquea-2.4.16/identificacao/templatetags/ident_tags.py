# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.template import Library
from django.contrib.admin.templatetags.admin_list import result_list

register = Library()


def busca(ed):
    ret = [ed]
    for e in ed.enderecodetalhe_set.order_by('complemento'):
        ret = ret + busca(e)
    return ret


@register.inclusion_tag("admin/change_list_results.html")
def result_list_patrimonio(cl):
    res = result_list(cl)
    results = res['results']
    results = [r for r in results if r.endereco]
    results = sorted(results, key=lambda x: x.endereco.entidade)

    lista = []
    for r in results:
        lista = lista + busca(r)

    res.update({'results': lista})
    return res
