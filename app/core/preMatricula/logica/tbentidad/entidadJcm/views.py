import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.db.models.deletion import RestrictedError
from core.preMatricula.models import Entidad, JCM
from .form import JcmForm
from core.preMatricula.logica.tbentidad.entidadJcp.form import EntidadForm
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin


def buscarJCM(request):
    if request.method == "POST":
        try:
            id_region = int(request.POST['id_region'])
        except:
            return JsonResponse([], safe=False)
        jcms = [{'id': i.id, 'text': i.__str__()}
                for i in JCM.objects.filter(region__id=id_region)]
        return JsonResponse(jcms, safe=False)

    return JsonResponse([], safe=False)


class JcmView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "tbentidad/entidad-jcm/list.html"
    permiso_vista = 'view_jcm'
    permiso_crud = {
        'add': 'add_jcm',
        'change': 'change_jcm',
        'delete': 'delete_jcm',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_entidad = EntidadForm(request.POST)
                form_jcm = JcmForm(request.POST)
                print(form_jcm)
                print(request.POST)
                if all([form_entidad.is_valid(), form_jcm.is_valid()]):
                    entidad = form_entidad.save(commit=False)
                    entidad.save()
                    jcm = form_jcm.save(commit=False)
                    jcm.entidad = entidad
                    jcm.save()
                    data['enviado'] = True
                    data['nombre'] = entidad.nombre
                else:
                    data['enviado'] = False
                    data['error'] = form_jcm.errors.as_json()

            elif action == "cargarDatos":
                data = [i.toJson() for i in JCM.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                print(request.POST)
                registro = JCM.objects.get(
                    pk=int(request.POST['id_edit']))
                entidad_instancia = Entidad.objects.get(pk=registro.entidad.pk)
                form_entidad = EntidadForm(
                    request.POST, instance=entidad_instancia)
                form_jcm = JcmForm(
                    request.POST, instance=registro)
                if all([form_entidad.is_valid(), form_jcm.is_valid()]):
                    entidad = form_entidad.save()
                    form_jcm.save()
                    data['enviado'] = True
                    data['nombre'] = entidad.nombre
                else:
                    data['enviado'] = False
                    data['error'] = form_jcm.errors.as_json()

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
        context['title'] = "Lista de Joven Club Municipal"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_entidad'] = EntidadForm()
        context['form_jcm'] = JcmForm()
        return context
