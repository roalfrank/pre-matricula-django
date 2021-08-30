
var modal_title = $('.modal-title');
var tooltip = function () { $('[data-toggle="tooltip"]').tooltip() };
var id_edit = null;
var delete_select = function (tabla,url_deletes=window.location.pathname) {
        var select_item = new Array();
        $('#data input[type="checkbox"]:checked').each(function(){
            var tr = tabla.cell($(this).closest('td,li')).index();
            var data = tabla.row(tr.row).data();
            select_item.push(data.id);
            });
        if(select_item.length == 0){ mensaje("info",'No hay registros seleccionados.');}
        else{
        var contexto = {
            id:JSON.stringify(select_item),
            action:"delete",
            csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
            }
        console.log(contexto);
        with_ajax(url_deletes,"Eliminando","Estas seguro de eliminar los registro seleccionados",contexto,function(data){
            if (data.hasOwnProperty('error')){
                mensaje("error","Estos registros están Restringido:  - "+data.error );
            }
            else{
            mensaje("success","Registro eliminado correctamente");
            }
            id_edit=null;
            tabla.ajax.reload();
        });
        }
}
var abrir_modal_nuevo = function (titulo) {
        console.log(titulo)
        $('input[name="action"]').val("add");
        modal_title.find('span').html(titulo);
        modal_title.find('i').removeClass().addClass('fa fa-plus');
        document.getElementById('formRegistro').reset();
        $("#modal-nuevo").modal("show");
}

var delete_registro=function(tabla,element,url_delete=window.location.pathname) {
    var tr = tabla.cell($(element).closest('td,li')).index();
    var data = tabla.row(tr.row).data();
    contexto = {
        id:data.id,
        action:"delete",
        csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()
        }
    with_ajax(url_delete,"Eliminando","Estas seguro de eliminar este registro",contexto,function(data){
        if (data.hasOwnProperty('error')){
            mensaje("error","Error Guardando el Registro - "+data.error );
        }
        else{
            $("#modal-nuevo").modal("hide");
            tabla.ajax.reload();
            mensaje("success","Registro eliminado correctamente");
        }
        id_edit=null;
        });
}
