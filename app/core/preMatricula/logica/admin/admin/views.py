import json
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import UserCrearAutomaticoFormAdmin
from core.login.form import UserPerfilRegistrationForm
from core.preMatricula.utils.general import listado_matricula_estudiante


class AdminDetailCargarFormAddView(TemplateView):
    template_name = "admin/admin/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_user'] = UserCrearAutomaticoFormAdmin()
        return context


class AdminDetailView(DetailView):
    model = User
    template_name = "admin/admin/detailAdmin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class AdminView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    #model = Estudiante
    template_name = "admin/admin/admin_list.html"
    permiso_vista = 'view_logentry'
    permiso_crud = {
        'add': 'add_logentry',
        'change': 'change_logentry',
        'delete': 'delete_logentry',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_user = UserCrearAutomaticoFormAdmin(request.POST)
                form_perfil = UserPerfilRegistrationForm(request.POST)
                if all([form_user.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        user = form_user.save(commit=False)
                        user.save()
                        grupo_admin = Group.objects.filter(
                            name='Admin')[0]
                        user.groups.add(grupo_admin)
                        perfil = form_perfil.save(commit=False)
                        perfil.user = user
                        perfil.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    data['error'] = form_perfil.errors.as_json()

            elif action == "cargarDatos":
                limite = int(request.POST['limite'])
                inicio = int(request.POST['inicio'])
                busqueda = request.POST['busqueda']
                if busqueda != '':
                    lista_filtro = {
                        'nombre': 'perfil__nombre__icontains',
                        'ci': 'perfil__ci__icontains',
                        'username': 'username__icontains',
                        'correo': 'perfil__correo__icontains',
                        'apellido1': 'perfil__apellido1__icontains',
                        'apellido2': 'perfil__apellido2__icontains',
                        'municipio': 'perfil__municipio__pk',
                        'provincia': 'perfil__municipio__provincia__pk'
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    for key, value in filtros.items():
                        condicion.add(Q(**{lista_filtro[key]: value}), Q.AND)

                    condicion.add(Q(**{'is_staff': True}), Q.AND)
                    admin = User.objects.filter(condicion)
                else:
                    admin = User.objects.filter(is_staff=True)

                lista = [i.perfil.toJsonAdmin()
                         for i in admin[inicio:inicio+limite]]
                data = {
                    'total': admin.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                user_instancia = User.objects.get(
                    pk=int(request.POST['id_edit']))
                perfil_instancia = Perfil.objects.get(
                    pk=user_instancia.perfil.pk)

                form_user = UserCrearAutomaticoFormAdmin(
                    request.POST, instance=user_instancia)
                form_perfil = UserPerfilRegistrationForm(
                    request.POST, instance=perfil_instancia)

                if all([form_user.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        form_user.save(edit=True)
                        perfil = form_perfil.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_user.is_valid():
                        print('error formulario user')
                        error.update(form_user.errors.get_json_data())
                    elif not form_perfil.is_valid():
                        print('error formulario perfil')
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
        print(context)
        context['title'] = "Lista de admin"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_user'] = UserCrearAutomaticoFormAdmin()
        return context
