# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.contrib import admin
from treemenus.admin import MenuAdmin, MenuItemAdmin
from treemenus.models import Menu

from models import MenuItemExtension


class MenuItemExtensionInline(admin.StackedInline):
    model = MenuItemExtension
    max_num = 1


class CustomMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtensionInline, ]


class CustomMenuAdmin(MenuAdmin):
    menu_item_admin_class = CustomMenuItemAdmin

admin.site.unregister(Menu)   # Unregister the standard admin options
admin.site.register(Menu, CustomMenuAdmin)   # Register the new, customized, admin options
