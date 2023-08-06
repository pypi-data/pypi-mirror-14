# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.management import BaseCommand
from protocolo.models import Protocolo, Feriado
import datetime
from django.core.mail import send_mail
from django.conf import settings

__author__ = 'antonio'


class Command(BaseCommand):
    help = 'Send mails warning about payments for the next 3 days'

    def handle(self, *args, **options):
        today = datetime.date.today()
        one_day = datetime.timedelta(days=1)

        next_day = today + one_day
        while Feriado.dia_de_feriado(next_day) or next_day.weekday() > 4:
            next_day += one_day

        prots = [p for p in Protocolo.objects.filter(data_vencimento__range=(today, next_day + 2*one_day))
                 .exclude(estado__nome='Pago')]

        if len(prots) > 0:
            if len(prots) == 1:
                subject = u"Protocolo a vencer nos próximos 3 dias"
                txt = u"O protocolo %s deve ser pago nos próximos 3 dias."
            else:
                subject = u"Protocolos a vencer nos próximos 3 dias"
                txt = u"Os protocolos %s devem ser pagos nos próximos 3 dias."

            msg = ', '.join(['http://%s%s' %
                             (Site.objects.get_current().domain,
                              reverse('admin:protocolo_protocolo_change', args=(p.id,))) for p in prots])
            send_mail(subject, txt % msg, "sistema@ansp.br", settings.PROTO_MAILS)
