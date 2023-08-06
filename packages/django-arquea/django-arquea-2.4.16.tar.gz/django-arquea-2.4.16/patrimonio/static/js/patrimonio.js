/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

function ajax_numero_fmusp() {
    if($("#id_tem_numero_fmusp").is(':checked')) {
        $("#id_numero_fmusp").parent().show();
    }
    else {
	$("#id_numero_fmusp").parent().hide();
    }
}

$(function() {
    ajax_numero_fmusp();
});
