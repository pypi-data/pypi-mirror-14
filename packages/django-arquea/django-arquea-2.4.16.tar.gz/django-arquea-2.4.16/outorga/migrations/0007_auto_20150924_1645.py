# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outorga', '0006_auto_20150924_1641'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('natureza_gasto__termo', 'descricao'), 'verbose_name': 'Item do Or\xe7amento', 'verbose_name_plural': 'Itens do Or\xe7amento'},
        ),
    ]
