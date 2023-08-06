function abre_fecha(id_no, id_arvore) {
    if ($("#a-"+id_no).text().indexOf('Abrir') == 0) {
        $("#"+id_arvore).jstree('open_all', '#'+id_no);
        $("#a-"+id_no).text("Fechar tudo");
    } else {
        $("#"+id_arvore).jstree('close_all', '#'+id_no);
        $("#a-"+id_no).text("Abrir tudo");
    }
}
