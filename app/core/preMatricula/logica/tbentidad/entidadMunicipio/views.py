import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.deletion import RestrictedError
from core.preMatricula.models import Municipio
from .form import MunicipioForm
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin


class MunicipioView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "tbentidad/entidad-municipio/list.html"
    permiso_vista = 'view_municipio'
    permiso_crud = {
        'add': 'add_municipio',
        'change': 'change_municipio',
        'delete': 'delete_municipio',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form = MunicipioForm(request.POST)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado'] = False
                    data['error'] = "Error insertando dato"
            # action chequear , esto es para comprobar rapido si ya hay otra  con el Mismo Nombre
            elif action == 'chequear':
                try:
                    print(request.POST)
                    # chequeamos si estamos en editar o add . si es editar hacemos la consulta con NONe
                    # edit_id no se incluye en la consulta
                    id_edit = request.POST['edit_id']
                    print("estoy en chequear")
                    if id_edit == "":
                        id_edit = None
                    # consulta a la base dato chequear el nombre de la provincia.
                    estado = Municipio.objects.filter(
                        ~Q(id=id_edit), nombre__iexact=request.POST['nombre'])
                    if len(estado) < 1:
                        # si no hay resultado en la busqueda , se devuelve True, dando lus verde a esa estado.
                        return JsonResponse(True, safe=False)
                    # si hay resultado se retorna Fasle para impedir que se cree la discapacidad con nombres repetidos.
                    return JsonResponse(False, safe=False)
                except:
                    return JsonResponse(False, safe=False)
            # Action  cargarDatos - para cargar la datatable de mi vista.
            elif action == "cargarDatos":
                data = [i.toJson() for i in Municipio.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                registro = Municipio.objects.get(
                    pk=int(request.POST['id_edit']))
                form = MunicipioForm(
                    request.POST, instance=registro)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado'] = False
                    data['error'] = "Error editando datos"

            # action delete, eliminar una registro
            elif action == "delete":
                try:
                    id_deletes = []
                    error = []
                    id = json.loads(request.POST["id"])
                    if type(id) == int:
                        id_deletes.append(id)
                    else:
                        id_deletes.extend(id)
                    delet_registro = Municipio.objects.filter(
                        pk__in=id_deletes)
                    for registro in delet_registro:
                        try:
                            registro.delete()
                        except:
                            error.append(f"{registro.nombre}")
                    if len(error) > 0:
                        data['error'] = error
                except Exception as e:
                    if type(e) == RestrictedError:
                        data['error'] = "Esta estado tiene registro vinculados, no se puede borrar."
                    else:
                        print(type(e))
                        data['error'] = e
        except Exception as e:
            # comprobar los errores , esto despues solo dejar a data['error']
            print(e)
            print(e.args)
            print(type(e))
            print('type(e) ver si es aqui')

            data['error'] = 'Error en las operaciones con los registros'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Municipio"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form'] = MunicipioForm()
        return context
