/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
 
  /**
    * Definição dos disparos efetuados ao final da carga da página
    */
    $(function() {
        // Adiciona o comportamento de draggable para os objetos, por exemplo, racks.
        $( ".draggable" ).draggable({
            containment: "#draggable_wrapper",
            scroll: false,
            grid: [ 10, 10 ],
            start: function() {
                drag_start(this);
            },
            stop: function() {
                drag_stop(this);
            }
        });
    
        // Abre o seletor de cor
        $('.input_color_picker').ColorPicker({
            onSubmit: function(hsb, hex, rgb, el) {
                $(el).val(hex);
                $(el).ColorPickerHide();
                
                id = $(el).attr('id');
                id_split = id.split('_');
                index = id_split[id_split.length -1];
                
                // Seta a cor no objeto do desenho e no input do color_picker
                $('#obj_drag_id_' + index).css('background', '#'+hex);
                $('#color_picker_' + index).css('background', '#'+hex);
            },
            onBeforeShow: function () {
                $(this).ColorPickerSetColor(this.value);
            }
        })
        .bind('keyup', function(){
            $(this).ColorPickerSetColor(this.value);
        });
    
        // Modifica a descrição no objeto do desenho
        $('.input_desc').change(function() {
            var el_id = get_index(this);
            $('#obj_drag_desc_' + el_id).text(this.value);
        });
        
        // Spinner para aumentar e diminur a altura de objetos
        $(".spinner_height").spinner({
          step: 10,
          spin: function( event, ui ) {
                id = $(this).attr('id');
                id_split = id.split('_');
                index = id_split[id_split.length -1];
                
                return dimension_operation(index, 'height', ui.value);
          }
        });
        $(".spinner_height.disabled").spinner( "disable" );
        
        // Spinner para aumentar e diminur a largura de objetos
        $( ".spinner_width" ).spinner({
          step: 10,
          spin: function( event, ui ) {
                id = $(this).attr('id');
                id_split = id.split('_');
                index = id_split[id_split.length -1];
                
                return dimension_operation(index, 'width', ui.value);
          }
        });
        $( ".spinner_width.disabled" ).spinner( "disable" );
        
        // Spinner para aumentar e diminur a largura e altura do data center
        $( ".spinner_height_dc" ).spinner({
          step: 10,
          spin: function( event, ui ) {
                id = $(this).attr('id');
                id_split = id.split('_');
                index = id_split[id_split.length -1];
                
                return dc_dimension_operation('height', ui.value);
          }
        });
        $( ".spinner_width_dc" ).spinner({
          step: 10,
          spin: function( event, ui ) {
                id = $(this).attr('id');
                id_split = id.split('_');
                index = id_split[id_split.length -1];
                
                return dc_dimension_operation('width', ui.value);
          }
        });
    });
    
    
    // Pega o indice da lista de objetos, para poder definir os atributos interno
    var get_index = function(el) {
        id = $(el).attr('id');
        id_split = id.split('_');
        index = id_split[id_split.length -1];
        
        return index;
    }
    var drag_start = function(element) {
        element = $(element);
        var elementId = get_index(element);
        
        // Marca a linha de informação de qual objeto está sendo arrastado
        $('#li_obj_' + elementId).animate({
          backgroundColor: "#ccc",
        }, 500 );
    }
    var drag_stop = function(element) {
        element = $(element);
        var top = element.position().top;
        var left = element.position().left;
        
        var elementId = get_index(element);
        
        // Grava os valores da posição X e Y ao final do arrasto
        $('#obj_x_id_' + elementId).attr("value", left);
        $('#obj_y_id_' + elementId).attr("value", top);
        
        // Marca a linha de informação de qual objeto está sendo arrastado
        $('#li_obj_' + elementId).animate({
          backgroundColor: "#fff",
        }, 500 );
    }
    
    /**
    * Function para alterar a largura e altura de racks e outros objetos.
    */
    var dimension_operation = function(id, dimension, value) {
        if (value < 0) {
            return false;
        }
        var dim = ''
        if(dimension == 'height') { dim = 'h'; }
        else if(dimension == 'width') { dim = 'w'; }
    
        $( '#obj_drag_id_' + id ).css(dimension, value + "px");
        
        return true;
    }
    
    /**
    * Function para alterar a largura e altura do datacenter
    * Se ultrapassar o limite da página não seta o valor e retorna False.
    */
    var dc_dimension_operation = function(dimension, value) {
        if (value < 0) {
            return false;
        }
        var dim = ''
        if(dimension == 'height') { dim = 'h'; }
        else if(dimension == 'width') { dim = 'w'; }
        
        if( (dimension == 'height' && value > 500) || (dimension == 'width' && value > 930) ) {
            //var html = '<div id="div_dc_msg">Largura ou altura passaram o limite de impressão.</div>';
            if ($('#div_dc_msg').length == 0) {
                //$('#div_dc_objs').append(html);
                return false;
            }
        } else {
            $('#div_dc_msg').remove();
        }
        
        $( '#datacenter_wrapper' ).css(dimension, value + "px");
        $( '#dc_' + dim ).attr("value", value);
        
        return true;
    }
    /**
    Adiciona um objeto no desenho
    btn = botão que disparou a function
    id = id do objeto a ser criado
    titulo = titulo do objeto a ser criado, apresentado dentro do quadrado.
    */
    var add_obj = function(btn, id, titulo) {
        $(btn).removeClass("addlink").addClass("deletelink");
        $(btn).attr('onclick','').unbind('click');
        $(btn).click(function() { delete_obj(this, id, titulo); });
        var html = '<div id="obj_drag_id_' + id +'" class="draggable ui-widget-content" style="position:absolute;top:0;left:0;width:80px;height:80px;background:#eee;">' +
                '<div class="draggable-content">'+
                '  <p>' + titulo + '</p>'+
                '  <p id="obj_drag_desc_' + id +'"></p>'+
                '</div>'+
            '</div>';
        $('#draggable_wrapper').append(html);
        $( '#obj_drag_id_' + id ).draggable({
            containment: "#draggable_wrapper",
            scroll: false,
            grid: [ 10, 10 ],
            start: function() {
                drag_start(this);
            },
            stop: function() {
                drag_stop(this);
            }
        });
        // Valores iniciais
        $( '#obj_x_id_' + id ).attr("value", 0);
        $( '#obj_y_id_' + id ).attr("value", 0);
        $( '#obj_h_id_' + id ).attr("value", 80);
        $( '#obj_w_id_' + id ).attr("value", 80);
        
        // habilitando a edição dos campos.
        $('#obj_w_id_' + id).removeClass("disabled");
        $('#obj_h_id_' + id).removeClass("disabled");
        $('#icon_width_' + id).removeClass("disabled");
        $('#icon_height_' + id).removeClass("disabled");
        
        $('#obj_w_id_' + id).spinner("enable");
        $('#obj_h_id_' + id).spinner("enable");
        $('#color_picker_' + id).removeAttr("disabled");
        $('#obj_desc_' + id).removeAttr("disabled");
    }
    /**
    Remove um objeto no desenho
    btn = botão que disparou a function
    id = id do objeto a ser criado
    titulo = titulo do objeto a ser criado, apresentado dentro do quadrado.
    */
    var delete_obj = function(btn, id, titulo) {
        $(btn).removeClass("deletelink").addClass("addlink");
        $(btn).attr('onclick','').unbind('click');
        $(btn).click(function() { add_obj(this, id, titulo); });
        
        $('#obj_drag_id_' + id).remove();
        
        $( '#obj_x_id_' + id ).attr("value", '');
        $( '#obj_y_id_' + id ).attr("value", '');
        $( '#obj_h_id_' + id ).attr("value", '');
        $( '#obj_w_id_' + id ).attr("value", '');
        
        $('#color_picker_' + id).val('');
        $('#color_picker_' + id).css('background', '');
        $('#obj_desc_' + id).val('');
        
        // habilitando a edição dos campos.
        $('#obj_w_id_' + id).addClass("disabled");
        $('#obj_h_id_' + id).addClass("disabled");
        $('#icon_width_' + id).addClass("disabled");
        $('#icon_height_' + id).addClass("disabled");

        
        $('#obj_w_id_' + id).spinner("disable");
        $('#obj_h_id_' + id).spinner("disable");
        
        $('#color_picker_' + id).attr('disabled', true);
        $('#obj_desc_' + id).attr('disabled', true);
    }