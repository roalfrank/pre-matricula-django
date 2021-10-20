from django.contrib.auth.decorators import permission_required, login_required
import json
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.preMatricula.models import Gestor, Instructor
from core.preMatricula.logica.estudiante.estudiante.form import UserCrearAutomaticoForm
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import GestorForm
# from core.preMatricula.logica.gestor.form import UserCrearAutomaticoForm
from core.login.form import UserPerfilRegistrationForm


class GestorDetailCargarFormAddView(TemplateView):
    template_name = "gestor/gestor/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_gestor'] = GestorForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context


class GestorCargarFormAddTrabajadorView(TemplateView):
    template_name = "gestor/gestor/form_add_trabajador.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GestorDetailView(DetailView):
    model = Gestor
    template_name = "gestor/gestor/detailGestor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        return context


class GestorView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "gestor/gestor/gestor_list.html"
    permiso_vista = 'view_gestor'
    permiso_crud = {
        'add': 'add_gestor',
        'change': 'change_gestor',
        'delete': 'delete_gestor',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                try:
                    id_usuario_trabajador = int(
                        request.POST['id_usuario_agregar_trabajador'])
                    usuario = User.objects.filter(
                        pk=id_usuario_trabajador).first()
                    Gestor.objects.create(
                        usuario=usuario, jcm=usuario.instructor.jcb.jcm)
                    print('estoy en agregar gestor desde trabajador')
                except Exception as e:
                    from django.utils.datastructures import MultiValueDictKeyError
                    if type(e) == MultiValueDictKeyError:
                        form_user = UserCrearAutomaticoForm(request.POST)
                        form_perfil = UserPerfilRegistrationForm(request.POST)
                        form_gestor = GestorForm(request.POST)
                        if all([form_user.is_valid(), form_gestor.is_valid(), form_perfil.is_valid()]):
                            with transaction.atomic():
                                user = form_user.save(commit=False)
                                user.save()
                                grupo_gestor = Group.objects.filter(
                                    name='Gestor')[0]
                                user.groups.add(grupo_gestor)
                                perfil = form_perfil.save(commit=False)
                                perfil.user = user
                                perfil.save()
                                gestor = form_gestor.save(commit=False)
                                gestor.usuario = user
                                gestor.save()
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
                        'nombre': 'usuario__perfil__nombre__icontains',
                        'ci': 'usuario__perfil__ci__icontains',
                        'username': 'usuario__username__icontains',
                        'correo': 'usuario__perfil__correo__icontains',
                        'apellido1': 'usuario__perfil__apellido1__icontains',
                        'apellido2': 'usuario__perfil__apellido2__icontains',
                        'municipio': 'usuario__perfil__municipio__pk',
                        'provincia': 'usuario__perfil__municipio__provincia__pk',
                        'jcp': 'jcm__region__jcp__pk',
                        'region': 'jcm__region__pk',
                        'jcm': 'jcm__pk'
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    for key, value in filtros.items():
                        if key == 'tipo_gestor':
                            if value != '':
                                condicion.add(
                                    Q(**{'usuario__perfil__tipo': value}), Q.AND)
                        else:
                            condicion.add(
                                Q(**{lista_filtro[key]: value}), Q.AND)

                    gestors = Gestor.objects.filter(condicion)
                else:
                    gestors = Gestor.objects.filter(
                        Q(usuario__perfil__nombre__icontains=busqueda) | Q(
                            usuario__username__icontains=busqueda) | Q(usuario__perfil__ci__icontains=busqueda) | Q(usuario__perfil__correo__icontains=busqueda)
                    )

                lista = [i.toJson()
                         for i in gestors[inicio:inicio+limite]]
                data = {
                    'total': gestors.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                gestor = Gestor.objects.get(
                    pk=int(request.POST['id_edit']))
                user_instancia = User.objects.get(
                    pk=gestor.usuario.pk)
                perfil_instancia = Perfil.objects.get(
                    pk=gestor.usuario.perfil.pk)

                form_user = UserCrearAutomaticoForm(
                    request.POST, instance=user_instancia)
                form_perfil = UserPerfilRegistrationForm(
                    request.POST, instance=perfil_instancia)
                form_gestor = GestorForm(
                    request.POST, instance=gestor)
                if all([form_user.is_valid(), form_gestor.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        user = form_user.save(edit=True)
                        perfil = form_perfil.save()
                        gestor = form_gestor.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_user.is_valid():
                        print('error formulario user')
                        error.update(form_user.errors.get_json_data())
                    elif not form_gestor.is_valid():
                        print('error formulario gestor')
                        error.update(form_gestor.errors.get_json_data())
                    elif not form_perfil.is_valid():
                        print('error formulario perfil')
                        error.update(form_perfil.errors.get_json_data())
                    print(error)
                    data['error'] = json.dumps(error)

            # action delete, eliminar una registro
            elif action == "delete":
                try:
                    id_deletes_user = []
                    id_deletes_trabajador = []
                    error = []
                    id = json.loads(request.POST["id"])
                    print('cargados los ids', id)
                    print('tipo dato id', type(id))
                    if type(id) == int:
                        id_deletes_user.append(id)
                    else:
                        if len(id['select_item_trabajadores']) > 0:
                            id_deletes_trabajador.extend(
                                id['select_item_trabajadores'])
                        if len(id['select_item_user']) > 0:
                            id_deletes_user.extend(id['select_item_user'])
                    delet_registro_user = User.objects.filter(
                        pk__in=id_deletes_user)
                    for registro in delet_registro_user:
                        try:
                            registro.delete()
                        except Exception as e:
                            print('error borrar', e)
                            error.append(f"{registro.username}")
                    delet_registro_trabajador = Gestor.objects.filter(
                        pk__in=id_deletes_trabajador)
                    for registro in delet_registro_trabajador:
                        try:
                            registro.delete()
                        except Exception as e:
                            print('error borrar', e)
                            error.append(f"{registro.usuario.username}")
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
        context['title'] = "Lista de Gestores"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_gestor'] = GestorForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context


@ login_required
@ permission_required('preMatricula.view_gestor', raise_exception=True)
def buscarGestor(request):
    if request.method == 'POST':
        id_gestor = int(request.POST['id_gestor'])
        gestor = Gestor.objects.filter(pk=id_gestor)[0]
        datos = gestor.datosAllJson()
        datos['enviado'] = True
        datos['is_active'] = gestor.usuario.is_active
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)


@ login_required
@ permission_required('preMatricula.view_gestor', raise_exception=True)
def buscarTrabajador(request):
    if request.method == 'POST':
        lista_filtro = {
            'ci': 'usuario__perfil__ci__icontains',
            'username': 'usuario__username__icontains'
        }
        busqueda_json = request.POST['filtro']
        filtros = json.loads(busqueda_json)
        condicion = Q()
        for key, value in filtros.items():
            if value != '':
                condicion.add(
                    Q(**{lista_filtro[key]: value}), Q.AND)
        instructors = Instructor.objects.filter(condicion)[0:3]
        lista_instructores = [i.toJson() for i in instructors]
        return JsonResponse(lista_instructores, safe=False)
    return JsonResponse([], safe=False)


@ login_required
@ permission_required('preMatricula.delete_gestor', raise_exception=True)
def deleteGestorTrabajador(request):
    if request.method == 'POST':
        id_gestor = int(request.POST['id_gestor'])
        gestor = Gestor.objects.filter(pk=id_gestor).first()
        gestor.delete()
        return JsonResponse(True, safe=False)
    return JsonResponse([], safe=False)
