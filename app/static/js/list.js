
//guardamos en modal_title el elemento del titulo para poder editarlo segun la vista en que estemos.
var modal_title = $('.modal-title');
var tooltip = function () { $('[data-toggle="tooltip"]').tooltip() };
//variable global para saber si estamos en editar
var id_edit = null;
//me permite cargar el formulario si se ha utilizado la opcion de ver detalles
var cargar_extra_on_hide_modal = false;
//funcion global para utilizarlo en abrir el modal.
var abrir_modal_nuevo = function (titulo) {
        
        $('input[name="action"]').val("add");
        modal_title.find('span').html(titulo);
        modal_title.find('i').removeClass().addClass('fa fa-plus');
        document.getElementById('formRegistro').reset();
        $("#modal-nuevo").modal("show");
}

var funcion_vincular_select = null;


