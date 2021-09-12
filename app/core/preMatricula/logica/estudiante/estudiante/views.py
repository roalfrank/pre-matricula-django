import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from core.preMatricula.models import Estudiante
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import UserCrearAutomaticoForm, EstudianteForm
from core.login.form import UserPerfilRegistrationForm


class EstudianteView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "estudiante/estudiante/list.html"
    permiso_vista = 'view_estudiante'
    permiso_crud = {
        'add': 'add_estudiante',
        'change': 'change_estudiante',
        'delete': 'delete_estudiante',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_user = UserCrearAutomaticoForm(request.POST)
                form_perfil = UserPerfilRegistrationForm(request.POST)
                form_estudiante = EstudianteForm(request.POST)
                if all([form_user.is_valid(), form_estudiante.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        user = form_user.save(commit=False)
                        user.save()
                        grupo_estudiante = Group.objects.filter(
                            name='Estudiante')[0]
                        user.groups.add(grupo_estudiante)
                        perfil = form_perfil.save(commit=False)
                        perfil.user = user
                        perfil.save()
                        estudiante = form_estudiante.save(commit=False)
                        estudiante.usuario = user
                        estudiante.creado_por = request.user
                        estudiante.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    data['error'] = form_perfil.errors.as_json()

            elif action == "cargarDatos":
                data = [i.toJson() for i in Estudiante.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                estudiante = Estudiante.objects.get(
                    pk=int(request.POST['id_edit']))
                user_instancia = User.objects.get(
                    pk=estudiante.usuario.pk)
                perfil_instancia = Perfil.objects.get(
                    pk=estudiante.usuario.perfil.pk)

                form_user = UserCrearAutomaticoForm(
                    request.POST, instance=user_instancia)
                form_perfil = UserPerfilRegistrationForm(
                    request.POST, instance=perfil_instancia)
                form_estudiante = EstudianteForm(
                    request.POST, instance=estudiante)
                if all([form_user.is_valid(), form_estudiante.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        form_user.save()
                        perfil = form_perfil.save()
                        form_estudiante.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_user.is_valid():
                        error.update(form_user.errors.get_json_data())
                    elif not form_estudiante.is_valid():
                        error.update(form_estudiante.errors.get_json_data())
                    elif not form_perfil.is_valid():
                        error.update(form_perfil.errors.get_json_data())
                    print(error)
                    data['error'] = json.dumps(error)

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
                    print('id usuarios a borrar', id_deletes)
                    delet_registro = User.objects.filter(
                        pk__in=id_deletes)
                    print('enditades usarios a borrar', delet_registro)
                    for registro in delet_registro:
                        try:
                            registro.delete()
                        except Exception as e:
                            print('error borrar', e)
                            error.append(f"{registro.username}")
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
            data['enviado'] = False
            data['error'] = 'Error en las operaciones con los registros'
        print(data)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Estudiantes"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_estudiante'] = EstudianteForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context
