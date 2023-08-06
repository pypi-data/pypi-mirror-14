/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
// filters a select by hiding all non-matching items - only works in FF so far.
//
// select          -  the id of the select control to filter
// filter_by_ctrl  -  a reference to an input object with the text to filter by
function abc(select_ctrl, filter_by_ctrl)
{
sel = document.getElementById(select_ctrl);
alert(sel);
}

function membro_select(eq, tr, mb)
{
    var filter2 = new Array();
    eq_ctrl = document.getElementById(eq);
    tr_ctrl = document.getElementById(tr);
    mb_ctrl = document.getElementById(mb);

    filter1 = eq_ctrl.options[eq_ctrl.selectedIndex].text;

    for(i=0;i<tr_ctrl.options.length;i++)
    {
        txt = tr_ctrl.options[i].text;
        mem_eq = txt.split(' - ');
        equipe = mem_eq[1]

        if (equipe && equipe.search(filter1, "i")!=-1)
        {
            filter2.push(mem_eq[0]);
        }
    }

    for(i=0;i<mb_ctrl.options.length;i++)
    {
        var existe = false;
        txt = mb_ctrl.options[i].text;
        for (j=0;j<filter2.length;j++)
        {
            if (txt.search(filter2[j], "i")!=-1)
            {
                existe = true;
            }
        }
        do_show = (!filter1 ||
                   mb_ctrl.options[i].value=="" ||
                   existe)
        mb_ctrl.options[i].style.display = do_show ? ' block':' none';
     }
}
        
function filter_select(sel, filter_by)
{
    select_ctrl = document.getElementById(sel);
    filter_by_ctrl = document.getElementById(filter_by);
    filter_text = filter_by_ctrl.options[filter_by_ctrl.selectedIndex].text.replace(/^\s+|\s+$/g,"");
    //if (filter_by_ctrl.value == filter_by_ctrl.old_value) return false;    
    sel_found = false;
    
    for(i=0;i<select_ctrl.options.length;i++)
    {
        txt = select_ctrl.options[i].text;
        do_show = (!filter_text ||
                   select_ctrl.options[i].value=="" ||
                   txt.search(filter_text, "i")!=-1)
        select_ctrl.options[i].style.display = do_show ? ' block':' none';
        // preselect the first item, and try to be smart about it
        if (!sel_found && do_show) {
            if (
                (select_ctrl.options[i].value=="" && !filter_text) ||
                (select_ctrl.options[i].value!="")
               )
            {
                if (!select_ctrl.options[i].selected)
                {
                    select_ctrl.options[i].selected = true;
                    // we need to call a possible onchange manually, because it doesn't
                    // happen by itself. unfortunately, there is also an old but as-of-yet
                    // unfixed bug in firefox that requires the setTimeout() workaround,
                    // see:
                    //  * https://bugzilla.mozilla.org/show_bug.cgi?id=317600
                    //  * https://bugzilla.mozilla.org/show_bug.cgi?id=246518
                    //if (select_ctrl.onchange) window.setTimeout(function(){select_ctrl.onchange()}, 0);
                }
                sel_found = true; 
            }
        }
    }
    // do some work of our own to determine one the value has changed, for
    // performance reaonns, but e.g. we also don't want to change the selection
    // unless the filter changed at least, and definitely not on control keys
    // such as arrow up or arrow down.
    //filter_by_ctrl.old_value = filter_by_ctrl.value;
}

function filter_select2(sel, filter1, filter2)
{
    select_ctrl = document.getElementById(sel);
    filter1_by_ctrl = document.getElementById(filter1);
    filter2_by_ctrl = document.getElementById(filter2);
    filter2_text = filter2_by_ctrl.options[filter2_by_ctrl.selectedIndex].text.replace(/^\s+|\s+$/g,"");
    filter1_text = filter1_by_ctrl.options[filter1_by_ctrl.selectedIndex].text.split(" - ")[0]
    filter1_text = filter1_text.replace(/^\s+|\s+$/g,"");
    for(i=0;i<select_ctrl.options.length;i++)
    {
        txt = select_ctrl.options[i].text;
        do_show = ((!filter1_text && !filter2_text) ||
                   select_ctrl.options[i].value=="" ||
                   (txt.search(filter1_text)!=-1 && txt.search(filter2_text, "i")!=-1))
        select_ctrl.options[i].style.display = do_show ? ' block':' none';
    }
    select_ctrl.options[0].selected = true;
}

function soma_dados(id_dados, id_total)
{
    dados = document.getElementById(id_dados);
    total = document.getElementById(id_total);
    t = 0.0;
    for(i=0;i<dados.options.length;i++)
    {
        if (dados.options[i].selected)
        {
           d = dados.options[i].text.split("-");
           v = d[d.length-1];
           t += Number(v);
        }
    }
    total.value = t.toFixed(2);
    
}