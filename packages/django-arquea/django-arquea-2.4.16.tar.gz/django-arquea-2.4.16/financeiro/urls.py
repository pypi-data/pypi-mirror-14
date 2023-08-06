# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns

urlpatterns = patterns('financeiro.views',
                       (r'pagamento_termo$', 'ajax_termo_escolhido'),
                       (r'pagamento_numero$', 'ajax_numero_escolhido'),
                       (r'pagamento_cc$', 'ajax_codigo_escolhido'),
                       (r'parcial_pagina_termo$', 'ajax_parcial_pagina'),
                       (r'nova_pagina$', 'ajax_nova_pagina'),
                       (r'relatorios/pagamentos_mes$', 'pagamentos_mensais'),
                       (r'relatorios/pagamentos_mes/(?P<pdf>\d)$', 'pagamentos_mensais'),
                       (r'relatorios/pagamentos_parcial$', 'pagamentos_parciais'),
                       (r'relatorios/pagamentos_parcial/(?P<pdf>\d)$', 'pagamentos_parciais'),
                       (r'relatorios/gerencial$', 'relatorio_gerencial'),
                       (r'relatorios/gerencial/(?P<pdf>\d)$', 'relatorio_gerencial'),
                       (r'relatorios/gerencial_anual$', 'gerencial_anual'),
                       (r'relatorios/gerencial_anual/(?P<pdf>\d)$', 'gerencial_anual'),
                       (r'relatorios/acordos$', 'relatorio_acordos'),
                       (r'relatorios/acordos/(?P<pdf>\d)$', 'relatorio_acordos'),
                       (r'relatorios/parciais$', 'parciais'),
                       (r'relatorios/caixa$', 'caixa'),
                       (r'relatorios/prestacao$', 'presta_contas'),
                       (r'relatorios/prestacao/(?P<pdf>\d)$', 'presta_contas'),
                       (r'relatorios/tipos$', 'tipos_documentos'),
                       (r'cheque/(?P<cc>\d+)$', 'cheque'),
                       (r'^extrato$', 'extrato'),
                       (r'^extrato/(?P<pdf>\d)$', 'extrato'),
                       (r'extrato_tarifas$', 'extrato_tarifas'),
                       (r'extrato_mes$', 'extrato_mes'),
                       (r'^extrato_mes/(?P<pdf>\d)$', 'extrato_mes'),
                       (r'extrato_financeiro$', 'extrato_financeiro'),
                       (r'extrato_financeiro_parciais$', 'financeiro_parciais'),
                       (r'sel_extrato$', 'ajax_escolhe_extrato'),
                       (r'extrato_financeiro_parciais/(?P<pdf>\d+)$', 'financeiro_parciais'),
                       (r'ajax_get_recursos_vigentes$', 'ajax_get_recursos_vigentes'),
                       (r'ajax_insere_extrato_cc$', 'ajax_insere_extrato_cc')
                       )
