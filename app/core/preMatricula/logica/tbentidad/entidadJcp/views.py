import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.deletion import RestrictedError
from core.preMatricula.models import Entidad, JCP
from .form import EntidadForm, JcpForm
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin


class JcpView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "tbentidad/entidad-jcp/list.html"
    permiso_vista = 'view_jcp'
    permiso_crud = {
        'add': 'add_jcp',
        'change': 'change_jcp',
        'delete': 'delete_jcp',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_entidad = EntidadForm(request.POST)
                form_jcp = JcpForm(request.POST)
                if all([form_entidad.is_valid(), form_jcp.is_valid()]):
                    entidad = form_entidad.save(commit=False)
                    entidad.save()
                    jcp = form_jcp.save(commit=False)
                    jcp.entidad = entidad
                    jcp.save()
                    data['enviado'] = True
                    data['nombre'] = entidad.nombre
                else:
                    data['enviado'] = False
                    data['error'] = "Error insertando dato"

            elif action == "cargarDatos":
                data = [i.toJson() for i in JCP.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                print(request.POST)
                registro = JCP.objects.get(
                    pk=int(request.POST['id_edit']))
                entidad_instancia = Entidad.objects.get(pk=registro.entidad.pk)
                form_entidad = EntidadForm(
                    request.POST, instance=entidad_instancia)
                form_jcp = JcpForm(
                    request.POST, instance=registro)
                if all([form_entidad.is_valid(), form_jcp.is_valid()]):
                    entidad = form_entidad.save()
                    form_jcp.save()
                    data['enviado'] = True
                    data['nombre'] = entidad.nombre
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
                    delet_registro = Entidad.objects.filter(
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
        context['title'] = "Lista de Joven Club Provincial"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_entidad'] = EntidadForm()
        context['form_jcp'] = JcpForm()
        return context
