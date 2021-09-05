import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from core.preMatricula.models import Region
from .form import RegionForm
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin


class RegionListView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "tbentidad/entidad-region/list.html"
    permiso_vista = 'view_region'
    permiso_crud = {
        'add': 'add_region',
        'change': 'change_region',
        'delete': 'delete_region', }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = RegionForm(request.POST)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado'] = False
                    data['error'] = "Error insertando dato"
            # Action  cargarDatos - para cargar la datatable de mi vista.
            elif action == "cargarDatos":
                data = [i.toJson() for i in Region.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una region.
            elif action == 'edit':
                region = Region.objects.get(
                    pk=int(request.POST['id_edit']))
                form = RegionForm(request.POST, instance=region)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado'] = False
                    data['error'] = "Error editando datos"
            # action delete, eliminar una region
            elif action == "delete":
                try:
                    id_deletes = []
                    error = []
                    id = json.loads(request.POST["id"])
                    if type(id) == int:
                        id_deletes.append(id)
                    else:
                        id_deletes.extend(id)
                    delet_region = Region.objects.filter(
                        pk__in=id_deletes)
                    for region in delet_region:
                        try:
                            region.delete()
                        except:
                            error.append(f"{region.nombre}")
                    if len(error) > 0:
                        data['error'] = error
                except Exception as e:
                    if type(e) == RestrictedError:
                        data['error'] = "Esta region, no se puede borrar."
                    else:
                        print(type(e))
                        data['error'] = e
        except Exception as e:
            # comprobar los errores , esto despues solo dejar a data['error']
            print(e)
            print(e.args)
            print(type(e))
            data['error'] = 'Error en las operaciones con los registros'
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Región"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form'] = RegionForm()
        return context
