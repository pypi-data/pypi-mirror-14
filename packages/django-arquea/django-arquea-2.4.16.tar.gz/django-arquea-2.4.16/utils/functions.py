# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import date, timedelta
import calendar
import httplib
import json as simplejson
import os
import cgi
import cStringIO as StringIO
import csv
import codecs
import cStringIO

import weasyprint

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, loader, RequestContext

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


#
# Funções para uso da biblioteca PisaPDF
#
def fetch_resources(uri, rel):
    """
    Utilizado para resolver o acesso a imagens relativas.
    Ele resolve automaticamente, se for utilizado os prefixos definidos em STATIC_URL e MEDIA_URL

    Ex. de uso no template:
    {% load static %}
    url('{% get_media_prefix %}{{papelaria.papel_timbrado_retrato_a4}}');
    """
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        path = uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))

    return path


#
# Funções para uso da biblioteca WeasyPrint
#
def weasy_fetcher(url, **kwargs):
    """
    Definição de URLs relativas;
    Para acessar imagens do MEDIA, utilizar media:
    Para os do STATIC, utilizar static:

    Ex:
    url('media:{{papelaria.papel_timbrado_paisagem_a4}}');

    """
    if url.startswith('static:'):
        url = url[len('static:'):]
        file_path = os.path.join(settings.STATIC_ROOT, url)
        if isReadableFile(file_path):
            return weasyprint.default_url_fetcher('file://' + file_path)
    elif url.startswith('media:'):
        url = url[len('media:'):]
        # Normalizando a URL;
        # Removendo o sufixo de MEDIA_URL
        url_path = os.path.normpath(url.replace(settings.MEDIA_URL, '', 1)).split(os.sep)
        # Normalizando o MEDIA_ROOT para path absoluto e juntando com a URL
        file_path = os.path.join(os.path.abspath(settings.MEDIA_ROOT), *url_path)

        if isReadableFile(file_path):
            return weasyprint.default_url_fetcher('file:///' + file_path.replace(os.sep, '/'))

    return weasyprint.default_url_fetcher(url)


def render_to_pdf_weasy(template_src, context_dict, request=None, filename='file.pdf', zoom=1.0):
    """
    Grava o template HTML em um objeto HttpResponse em PDF
    utilizando a biblioteca WeasyPrint.

    @param template_src Template HTML a ser renderizado
    @param context_dict Dicionário de contexto
    @param request      Objeto Request
    @param filename     Nome do arquivo a ser gerado no Response
    @param zoom         Zoom para redimensionar a visualização do PDF, por exemplo, nos casos de impressão em uma página
    """
    if list(template_src) != template_src:
        template_src = [template_src]

    docs = []
    if request:
        context = RequestContext(request)
    else:
        context = Context()

    context.update(context_dict)

    for t_src in template_src:
        # Renderiza o HTML
        template = loader.get_template(t_src)
        html = template.render(context)
        docs.append(weasyprint.HTML(string=html, url_fetcher=weasy_fetcher).render())

    all_pages = []
    for doc in docs:
        all_pages += doc.pages

    response = HttpResponse(content_type="application/pdf")

    # Necessário passar o base_url para poder resolver os caminhos relativos de imagens
    docs[0].copy(all_pages).write_pdf(response, zoom=zoom)
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def render_to_pdfxhtml2pdf(template_src, context_dict, request=None, context_instance=None, filename='file.pdf',
                           attachments=[]):
    from xhtml2pdf import pisa
    from xhtml2pdf.pdf import pisaPDF
    # Renderiza o HTML
    template = loader.get_template(template_src)
    if request:
        context = RequestContext(request)
    else:
        context = Context()

    context.update(context_dict)
    html = template.render(context)

    # Removendo CSS microsoft que causam erro no XHTML2PDF
    html = html.replace('-moz-use-text-color', '')
    html = html.replace('border: medium none;', 'border-width: medium 0 0 0;')

    pdf = pisaPDF()
    pdf_princ = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8")), link_callback=fetch_resources)
    pdf.addDocument(pdf_princ)
    a = 0
    for f, d, t in attachments:
        a += 1
        pdf.addDocument(pisa.pisaDocument(
            StringIO.StringIO((u'<div style="text-align:center; font-size:22px; padding-top:12cm;">'
                               u'<strong>Anexo %s<br />%s</strong></div>' % (a, d)).encode('utf-8'))))
        if t == 1:
            pdf.addFromFile(f)
        elif t == 2:
            pdf.addFromString(f)

    if not pdf_princ.err:
        response = HttpResponse(content_type='application/pdf')
        response.write(pdf.getvalue())
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    return HttpResponse('We  had some errors<pre>%s</pre>' % cgi.escape(html))


def formata_moeda(n, s_d):
    """
    Formata um número n no formato de moeda, sendo s_d o ponto de sinal do decimal.
    Ex:
        n = 10000
        s_d = ,

        retorno: 1.000,00

    Caso n seja vazio ou nulo, retorna 0.00 ou 0,00

    @param n    Número a ser formatado
    @param s_d  Caracter separador de decimal
    """
    if s_d == '.':
        s_i = ','
    else:
        s_i = '.'

    if n:
        f = str(n)
    else:
        f = "0"

    num = f.split('.')
    i = num[0]
    if len(num) > 1:
        d = num[1]
    else:
        d = '0'
    if len(d) == 1:
        d += '0'
    ii = list(i)
    j = 3
    while len(ii) > j:
        ii.insert(-j, s_i)
        j += 4
    r = ''.join(ii)
    return s_d.join((r, d))


def pega_bancos():
    conn = httplib.HTTPConnection('www.febraban.org.br')
    conn.request('GET', '/bancos.asp')
    dados = conn.getresponse().read()
    conn.close()
    p1 = dados.find('table')
    bancos = []
    numero = None
    dados = dados[p1:]
    dados = dados.split('blank">\r\n')
    for l in dados[1:]:
        n = l.find('\r')
        m = l[:n]
        if numero is not None:
            try:
                bancos.append((int(numero), m.strip().decode('iso-8859-1').encode('utf-8')))
            except:
                pass
            numero = None
        else:
            numero = m.strip()

    return bancos


def pega_lista(request, obj, filtro):
    if request.method == 'POST':
        filtro_id = request.POST.get('id')
        kwargs = {filtro: filtro_id}
        lista = obj.objects.filter(**kwargs)
        retorno = []
        for o in lista:
            retorno.append({'pk': o.pk, 'valor': o.__unicode__()})
        if lista.count() > 0:
            json = simplejson.dumps(retorno)
        else:
            retorno = [{"pk": "0", "valor": "Nenhum registro"}]
            json = simplejson.dumps(retorno)
    return json


def working_days(year, month):
    fromdate = date(year, month, 1)
    dias_mes = calendar.monthrange(year, month)[1]
    daygenerator = (fromdate + timedelta(x + 1) for x in range(dias_mes))
    return sum(day.weekday() < 5 for day in daygenerator)


def clone_objects(objects):
    def clone(from_object):
        args = dict([(fld.name, getattr(from_object, fld.name))
                     for fld in from_object._meta.fields
                     if fld is not from_object._meta.pk])

        return from_object.__class__.objects.create(**args)

    if not hasattr(objects, '__iter__'):
        objects = [objects]

    # We always have the objects in a list now
    objs = []
    for o in objects:
        obj = clone(o)
        obj.save()
        objs.append(obj)


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def month_range(start_date, end_date):
    """
    Returns all months (with the same day when possible) between
    start_date and end_date (including both)

    @param start_date   Date of the beggining
    @param end_date     Date of the ending
    """
    current_date = start_date

    while current_date <= end_date:
        yield current_date
        carry, new_month = divmod(current_date.month, 12)
        new_month += 1
        current_date = current_date.replace(year=current_date.year + carry, month=new_month, day=1)


def isReadableFile(full_path):
    try:
        if not os.path.isfile(full_path):
            # print u"File does not exist: %s" % full_path
            return False
        elif not os.access(full_path, os.R_OK):
            # print u"File cannot be read: %s" % full_path
            return False
        else:
            # print "File can be read."
            return True
    except IOError as ex:
        print "I/O error({0}): {1}".format(ex.errno, ex.strerror)
        return False
