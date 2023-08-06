# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.core.urlresolvers import reverse
from django.db.models import Max, Min
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_safe, require_POST
from utils.decorators import login_required_or_403
from datetime import datetime, timedelta, date
import json as simplejson
import logging
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from membro.models import Membro, Controle, Ferias
from membro.forms import ControleObs

# Get an instance of a logger
logger = logging.getLogger(__name__)


# def ferias(context):
#     now = datetime.now()
#     funcionarios = []
#     for f in [m for m in Membro.objects.all() if m.funcionario is True]:
#         func = {}
#         func['nome'] = f.nome
#         h = Historico.ativos.get(funcionario=True, membro=f)
#         func['admissao'] = h.inicio.strftime("%d/%m/%Y")
#         ferias = f.ferias_set.order_by('-inicio')
#         if ferias.count() == 0:
#             continue
#         ferias = ferias[0]
#         final = ferias.inicio - timedelta(1)
#         final = date(final.year+1, final.month, final.day)
#         func['periodo'] = '%s a %s' % (ferias.inicio.strftime("%d/%m/%Y"), final.strftime("%d/%m/%Y"))
#         try:
#             cf = ferias.controleferias_set.get(oficial=True)
#         except:
#             continue
#         func['ferias'] = '%s a %s' % (cf.inicio.strftime("%d/%m/%Y"), cf.termino.strftime("%d/%m/%Y"))
#         dias = cf.termino - cf.inicio
#         func['dias'] = dias.days + 1
#         func['decimo_terceiro'] = u'Sim' if ferias.decimo_terceiro else u'Não'
#
#         funcionarios.append(func)
#
#     return render_to_pdf('membro/ferias.pdf', {'funcionarios':funcionarios, 'ano':now.year+1})

@login_required
@require_POST
def controle(request):
    user = request.user
    membro = get_object_or_404(Membro, contato__email=user.email)

    acao = request.POST.get('acao')
    if acao == u'entrada':
        controle = Controle()
        controle.membro = membro
        controle.entrada = datetime.now()
    else:
        controle = membro.controle_set.all()[0]
        controle.saida = datetime.now()
    controle.save()
    messages.info(request, u'Sua %s foi registrada com sucesso.' % acao)
    key = make_template_fragment_key('base-html-header', [request.user.username])
    cache.delete(key)
    return HttpResponseRedirect(reverse('membro.views.observacao', kwargs={'controle_id': controle.id}))


@login_required
def mensal(request, ano=2012, mes=7):
    membro_ids = Controle.objects.filter(entrada__year=ano, entrada__month=mes).order_by('membro')\
        .values_list('membro', flat=True).distinct()
    membros = Membro.objects.filter(id__in=membro_ids)
    from calendar import monthrange
    last_day = monthrange(int(ano), int(mes))[1]
    dias = range(1, last_day+1)
    dados = []
    for m in membros:
        linha = [m.nome]
        controles = Controle.objects.filter(entrada__year=ano, entrada__month=mes, membro=m, saida__isnull=False)
        for dia in dias:
            minutes = sum([c.segundos for c in controles.filter(entrada__day=dia)], 0)/60
            linha.append('%02d:%02d' % (minutes/60, minutes % 60))
        dados.append(linha)

    return TemplateResponse(request, 'membro/mensal.html', {'dados': dados, 'dias': dias, 'ano': ano, 'mes': mes})


@login_required
def detalhes(request):
    membro = get_object_or_404(Membro, contato__email=request.user.email)
    agora = datetime.now()

    return TemplateResponse(request, 'membro/detalhes.html',
                            {'membro': membro,
                             'dados': Controle.objects.filter(membro=membro, entrada__month=agora.month)})


@login_required
@permission_required('membro.rel_adm_mensalf', raise_exception=True)
@require_safe
def mensal_func(request):
    """
     Relatório Administrativo - Relatório com o lançamento de horas dos funcionários.

    """
    funcionario = request.GET.get('funcionario')

    if request.GET.get('ano') and funcionario != "-1":
        meses = []
        membro = get_object_or_404(Membro, pk=funcionario)
        if request.user.is_superuser is False and request.user.email != membro.email:
            raise Http404

        ano = request.GET.get('ano')
        mes = request.GET.get('mes')

        try:
            c = Controle.objects.filter(membro=funcionario)[:1].get()
        except Controle.DoesNotExist:
            raise Http404

        # Contagem de total geral do funcionario
        total_meses = c.total_analitico_horas(0, 0)
        total_geral_banco_horas = 0
        for m in total_meses:
            # soma horas extras somente dos meses que não forem o mês em andamento
            total_geral_banco_horas += m['total_banco_horas']

        if total_geral_banco_horas >= 0:
            total_geral_banco_horas_str = '%2dh %02dmin' % (total_geral_banco_horas/3600,
                                                            total_geral_banco_horas/60 % 60)
        else:
            total_geral_banco_horas_str = '-%2dh %02dmin' % (-total_geral_banco_horas/3600,
                                                             -total_geral_banco_horas/60 % 60)
        total_geral_ferias = Ferias().total_dias_uteis_aberto(funcionario)
        total_geral_ferias_str = '%2dh %02dmin' % (total_geral_ferias/3600, total_geral_ferias/60 % 60)

        meses = c.total_analitico_horas(ano, mes)

        total_banco_horas = 0
        total_horas = 0
        total_horas_periodo = 0
        total_horas_restante = 0
        total_horas_dispensa = 0
        total_horas_ferias = 0

        for m in meses:

            # total de horas trabalhadas
            total_horas += m['total']
            total_str = '%2dh %02dmin' % (m['total']/3600, m['total']/60 % 60)
            m.update({'total': total_str})

            # as horas totais do período são as horas do total de dias do mes menos os finais de semana, ferias e dispensas
            total_horas_periodo += m['total_horas_periodo']
            total_horas_periodo_str = '%2dh %02dmin' % (m['total_horas_periodo']/3600, m['total_horas_periodo']/60 % 60)
            m.update({'total_horas_periodo': total_horas_periodo_str})

            total_horas_restante += m['total_horas_restante']
            if m['total_horas_restante'] >= 0:
                total_horas_restante_str = '%02dh %02dmin' % (m['total_horas_restante']/3600.0,
                                                              m['total_horas_restante']/60 % 60)
            else:
                total_horas_restante_str = '-%02dh %02dmin' % (-m['total_horas_restante']/3600.0,
                                                               -m['total_horas_restante']/60 % 60)
            m.update({'total_horas_restante': total_horas_restante_str})

            total_horas_ferias += m['total_horas_ferias']
            total_horas_ferias_str = '%2dh %02dmin' % (m['total_horas_ferias']/3600, m['total_horas_ferias']/60 % 60)
            m.update({'total_horas_ferias': total_horas_ferias_str})

            total_horas_dispensa += m['total_horas_dispensa']
            total_horas_dispensa_str = '%2dh %02dmin' % (m['total_horas_dispensa']/3600,
                                                         m['total_horas_dispensa']/60 % 60)
            m.update({'total_horas_dispensa': total_horas_dispensa_str})
            # soma horas extras somente dos meses que não forem o mês em andamento
            total_banco_horas += m['total_banco_horas']
            if m['total_banco_horas'] >= 0:
                total_banco_horas_str = '%2dh %02dmin' % (m['total_banco_horas']/3600, m['total_banco_horas']/60 % 60)
            else:
                total_banco_horas_str = '-%2dh %02dmin' % (-m['total_banco_horas']/3600,
                                                           -m['total_banco_horas']/60 % 60)
            m.update({'total_banco_horas': total_banco_horas_str})

            # if m['total_horas_periodo_ate_hoje'] >= 0:
            #     total_horas_periodo_ate_hoje_str = '%2dh %02dmin' % (m['total_horas_periodo_ate_hoje']/3600, m['total_horas_periodo_ate_hoje']/60%60)
            # else:
            #     total_horas_periodo_ate_hoje_str = '-%2dh %02dmin' % (-m['total_horas_periodo_ate_hoje']/3600, -m['total_horas_periodo_ate_hoje']/60%60)
            # m.update({'total_horas_periodo_ate_hoje': total_horas_periodo_ate_hoje_str})

        if total_horas_restante >= 0:
            total_horas_restante_str = '%2dh %02dmin' % (total_horas_restante/3600, total_horas_restante/60 % 60)
        else:
            total_horas_restante_str = '-%2dh %02dmin' % (-total_horas_restante/3600, -total_horas_restante/60 % 60)

        if total_banco_horas >= 0:
            total_banco_horas_str = '%2dh %02dmin' % (total_banco_horas/3600, total_banco_horas/60 % 60)
        else:
            total_banco_horas_str = '-%2dh %02dmin' % (-total_banco_horas/3600, -total_banco_horas/60 % 60)

        total_horas_str = '%2dh %02dmin' % (total_horas/3600, total_horas/60 % 60)
        total_horas_periodo_str = '%2dh %02dmin' % (total_horas_periodo/3600, total_horas_periodo/60 % 60)
        total_horas_dispensa_str = '%2dh %02dmin' % (total_horas_dispensa/3600, total_horas_dispensa/60 % 60)
        total_horas_ferias_str = '%2dh %02dmin' % (total_horas_ferias/3600, total_horas_ferias/60 % 60)

        return TemplateResponse(request, 'membro/detalhe.html',
                                {'meses': meses, 'membro': membro, 'total_banco_horas': total_banco_horas_str,
                                 'total_horas': total_horas_str, 'total_horas_periodo': total_horas_periodo_str,
                                 'total_horas_restante': total_horas_restante_str,
                                 'total_horas_dispensa': total_horas_dispensa_str,
                                 'total_horas_ferias': total_horas_ferias_str,
                                 'total_geral_banco_horas': total_geral_banco_horas_str,
                                 'total_geral_ferias': total_geral_ferias_str})
    else:
        hoje = datetime.now()
        anos = [0]+range(2012, hoje.year+1)
        meses = range(13)
        funcionarios = [m for m in Membro.objects.all() if m.funcionario]

        retorno = []
        for f in funcionarios:
            entrada = Controle.objects.filter(membro=f).aggregate(Max('entrada'), Min('entrada'))

            if entrada['entrada__min']:
                ano_inicio = entrada['entrada__min'].year
                mes_inicio = entrada['entrada__min'].month
                ano_fim = entrada['entrada__max'].year
                mes_fim = entrada['entrada__max'].month
                retorno.append({'funcionario': f, 'ano_inicio': ano_inicio, 'mes_inicio': mes_inicio,
                                'ano_fim': ano_fim, 'mes_fim': mes_fim})

        return TemplateResponse(request, 'membro/sel_func.html',
                                {'anos': anos, 'meses': meses, 'funcionarios': retorno})


@login_required
def observacao(request, controle_id):
    controle = get_object_or_404(Controle, pk=controle_id)

    if request.user.email != controle.membro.email:
        return HttpResponseForbidden()

    if request.method == 'POST':
        if request.POST.get('enviar'):
            f = ControleObs(request.POST, instance=controle)
            f.save()

        return HttpResponseRedirect('/')
    else:
        f = ControleObs(instance=controle)
        return TemplateResponse(request, 'membro/observacao.html', {'form': f})


@login_required
@permission_required('membro.rel_adm_logs', raise_exception=True)
@require_safe
def uso_admin(request):
    """
     Relatório Administrativo - Relatório de registro de uso do sistema por ano.

     Relatório de logs de uso da área administrativa do sistema.
     Exibe informação de quantidade de inclusões, alterações e exclusões feitas por cada usuário, por ano.

    """
    if 'inicial' not in request.GET:
        return TemplateResponse(request, 'admin/logs_escolha.html', {'anos': range(2008, datetime.now().year+1)})

    inicial = request.GET.get('inicial')
    final = request.GET.get('final')
    try:
        inicial = int(inicial)
        final = int(final)
    except:
        raise Http404

    user_ids = LogEntry.objects.filter(action_time__range=(date(inicial, 1, 1), date(final+1, 1, 1)))\
        .values_list('user', flat=True).order_by('user').distinct()
    emails = Membro.objects.values_list('email', flat=True).order_by('email').distinct()
    emails = list(emails)
    if '' in emails:
        emails.remove('')
    user_ids = list(user_ids)
    users = []
    for u in user_ids:
        user = User.objects.get(id=u)
        if user.email in emails:
            users.append(user)

    users.sort(key=lambda x: x.first_name)

    returned = []

    sem_abuse = LogEntry.objects.exclude(content_type_id=166)
    for user in users:
        log_user = sem_abuse.filter(user=user)
        user_return = {'nome': '%s %s' % (user.first_name, user.last_name)}
        dados = []
        for ano in range(inicial, final+1):
            log_ano = log_user.filter(action_time__year=ano)
            dados.append((ano, log_ano.filter(action_flag=1).count(), log_ano.filter(action_flag=2).count(),
                          log_ano.filter(action_flag=3).count()))
        user_return['dados'] = dados
        returned.append(user_return)

    return TemplateResponse(request, 'admin/logs.html', {'users': returned})
