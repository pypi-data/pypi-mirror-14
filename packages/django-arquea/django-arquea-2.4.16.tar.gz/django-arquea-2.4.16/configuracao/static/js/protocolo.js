/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
 
function referente(sel, field)
{
select_ctrl = document.getElementById(sel);
field_ctrl = document.getElementById(field);

txt = select_ctrl.options[select_ctrl.selectedIndex].text
field_ctrl.value = txt;
}
