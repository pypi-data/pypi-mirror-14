/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
 
$(function(){

   $("*[rel=tooltip]").hover(function(e){
         $("body").append('<div class="tooltip">'+$(this).attr('title')+'</div>');
         
         $('.tooltip').css({
                     top : e.pageY - 50,
                     left : e.pageX + 20
                     }).fadeIn();

   }, function(){
      $('.tooltip').remove();
      
   }).mousemove(function(e){
      $('.tooltip').css({
                     top : e.pageY - 50,
                     left : e.pageX + 20
                     })
   })

   /**
    * Eventos para abrir ou esconder a tabela de conflito de equipamentos
    */
   $(".conflitos-title").click(function(){
	   $(this).siblings(".conflitos-content").toggle(); 
   });
   
   /**
    * Habilita/desabilita o targetSel
    * Check/uncheck o chkSel
    * Atualiza a URL da geração do PDF com o parametro urlSel
    */
   function _chk_toogle(targetSel, chkSel, urlSel) {
	   $(targetSel).toggle();
	   
	   var showOrHide = ($(chkSel).prop('checked'));
	   var newUrl = updateQueryString(urlSel, showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   }
   function _chk_span_toogle(targetSel, chkSel, urlSel) {
	   
	   
	   var showOrHide = !($(chkSel).prop('checked'));
	   
	   $(targetSel).toggle(showOrHide);
	   $(chkSel).prop('checked', showOrHide);
	   
	   var newUrl = updateQueryString(urlSel, showOrHide?1:0, $('#icons a').attr('href'));
	   $('#icons a').attr('href', newUrl);
   }
   
   /**
    * Exibe ou esconde as imagens dos stencils dos equipamentos
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_stencil").change(function(e){
	   _chk_toogle(".interno a img", '#chk_stencil', 'chk_stencil');
   });
   $("#chk_stencil + span").click(function(e){
	   _chk_span_toogle(".interno a img", '#chk_stencil', 'chk_stencil');
   });
   
   /**
    * Exibe ou esconde as legendas dos equipamentos.
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_legenda").click(function(e){
	   _chk_toogle(".equip div div:nth-child(1)", '#chk_legenda', 'chk_legenda');
   });
   $("#chk_legenda + span").click(function(e){
	   _chk_span_toogle(".equip div div:nth-child(1)", '#chk_legenda', 'chk_legenda');
   });
   
   /**
    * Exibe ou esconde as legendas dos equipamentos.
    * Os disparos ocorrem no checkbox e no label do checkbox
    */
   $("#chk_legenda_desc").click(function(e){
	   _chk_toogle(".equip div div:nth-child(2)", '#chk_legenda_desc', 'chk_legenda_desc');
   });
   $("#chk_legenda_desc + span").click(function(e){
	   _chk_span_toogle(".equip div div:nth-child(2)", '#chk_legenda_desc', 'chk_legenda_desc');
   });
   
   $("#chk_outros").click(function(e){
	   _chk_toogle(".outros-content", '#chk_outros', 'chk_outros');
   });
   $("#chk_outros + span").click(function(e){
	   _chk_span_toogle(".outros-content", '#chk_outros', 'chk_outros');
   });
   
   $("#chk_traseira").click(function(e){
	   _chk_toogle(".rack_traseiro", '#chk_traseira', 'chk_traseira');''
   });
   $("#chk_traseira + span").click(function(e){
	   _chk_span_toogle(".rack_traseiro", '#chk_traseira', 'chk_traseira');
   });
   
   $("#chk_avisos").click(function(e){
	   _chk_toogle(".conflitos", '#chk_avisos', 'chk_avisos');
   });
   $("#chk_avisos + span").click(function(e){
	   _chk_span_toogle(".conflitos", '#chk_avisos', 'chk_avisos');
   });
 
   
   /**
    * Function para alterar a queryString de um parametro href
    */
   function updateQueryString(key, value, url) {
	    if (!url) url = window.location.href;
	    var re = new RegExp("([?|&])" + key + "=.*?(&|#|$)(.*)", "gi");

	    if (re.test(url)) {
	        if (typeof value !== 'undefined' && value !== null)
	            return url.replace(re, '$1' + key + "=" + value + '$2$3');
	        else {
	            var hash = url.split('#');
	            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
	            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
	                url += '#' + hash[1];
	            return url;
	        }
	    }
	    else {
	        if (typeof value !== 'undefined' && value !== null) {
	            var separator = url.indexOf('?') !== -1 ? '&' : '?',
	                hash = url.split('#');
	            url = hash[0] + separator + key + '=' + value;
	            if (typeof hash[1] !== 'undefined' && hash[1] !== null) 
	                url += '#' + hash[1];
	            return url;
	        }
	        else
	            return url;
	    }
	}
   
});
