# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, Http404

import os
import logging
import magic
import urllib

# Get an instance of a logger
logger = logging.getLogger(__name__)


def verifica(request):
    return HttpResponse('Ok')


@login_required
def serve_files(request, filename):

    # evita que o usuario tente acessar qualquer arquivo do sistema
    filename = filename.replace('..', '')

    path = '%s/%s' % (settings.MEDIA_ROOT, filename)

    # descobre o mime type
    try:
        mime = magic.from_file(path, mime=True)
    except:
        raise Http404

    # monta a resposta sem conteúdo, apenas com o header do x-sendfile
    response = HttpResponse(content_type=mime)
    response['X-Sendfile-encoding'] = 'url'
    response['X-Sendfile'] = urllib.quote(path.encode('utf-8'))
    response['Content-length'] = os.path.getsize(path)

    return response
