# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

__author__ = 'antonio'


def login_required_or_403(function=None):

    def test_auth(user):
        if not user.is_authenticated():
            raise PermissionDenied

        return True

    actual_decorator = user_passes_test(test_auth)
    if function:
        return actual_decorator(function)

    return actual_decorator
