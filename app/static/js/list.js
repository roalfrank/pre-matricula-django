
var modal_title = $('.modal-title');
var tooltip = function () { $('[data-toggle="tooltip"]').tooltip() };
var id_edit = null;
var estudiante_view = false;

var abrir_modal_nuevo = function (titulo) {
        
        $('input[name="action"]').val("add");
        modal_title.find('span').html(titulo);
        modal_title.find('i').removeClass().addClass('fa fa-plus');
        document.getElementById('formRegistro').reset();
        $("#modal-nuevo").modal("show");
}



