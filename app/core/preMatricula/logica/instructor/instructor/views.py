from django.contrib.auth.decorators import permission_required, login_required
import json
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q
from core.preMatricula.models import Instructor
from core.preMatricula.logica.estudiante.estudiante.form import UserCrearAutomaticoForm
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import InstructorForm
#from core.preMatricula.logica.instructor.form import UserCrearAutomaticoForm
from core.login.form import UserPerfilRegistrationForm


class InstructorDetailCargarFormAddView(TemplateView):
    template_name = "instructor/instructor/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_instructor'] = InstructorForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context


class InstructorDetailView(DetailView):
    model = Instructor
    template_name = "instructor/instructor/detailInstructor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')

        return context


class InstructorView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    #model = Instructor
    template_name = "instructor/instructor/instructor_list.html"
    permiso_vista = 'view_intructor'
    permiso_crud = {
        'add': 'add_intructor',
        'change': 'change_intructor',
        'delete': 'delete_intructor',
    }

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                form_user = UserCrearAutomaticoForm(request.POST)
                form_perfil = UserPerfilRegistrationForm(request.POST)
                form_instructor = InstructorForm(request.POST)
                if all([form_user.is_valid(), form_instructor.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        user = form_user.save(commit=False)
                        user.save()
                        grupo_instructor = Group.objects.filter(
                            name='Instructor')[0]
                        user.groups.add(grupo_instructor)
                        perfil = form_perfil.save(commit=False)
                        perfil.user = user
                        perfil.save()
                        instructor = form_instructor.save(commit=False)
                        instructor.usuario = user
                        instructor.save()
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
                        'provincia': 'usuario__perfil__municipio__provincia__pk'
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    for key, value in filtros.items():
                        condicion.add(Q(**{lista_filtro[key]: value}), Q.AND)

                    instructors = Instructor.objects.filter(condicion)
                else:
                    instructors = Instructor.objects.filter(
                        Q(usuario__perfil__nombre__icontains=busqueda) | Q(
                            usuario__username__icontains=busqueda) | Q(usuario__perfil__ci__icontains=busqueda) | Q(usuario__perfil__correo__icontains=busqueda)
                    )

                lista = [i.toJson()
                         for i in instructors[inicio:inicio+limite]]
                data = {
                    'total': instructors.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                instructor = Instructor.objects.get(
                    pk=int(request.POST['id_edit']))
                user_instancia = User.objects.get(
                    pk=instructor.usuario.pk)
                perfil_instancia = Perfil.objects.get(
                    pk=instructor.usuario.perfil.pk)

                form_user = UserCrearAutomaticoForm(
                    request.POST, instance=user_instancia)
                form_perfil = UserPerfilRegistrationForm(
                    request.POST, instance=perfil_instancia)
                form_instructor = InstructorForm(
                    request.POST, instance=instructor)
                if all([form_user.is_valid(), form_instructor.is_valid(), form_perfil.is_valid()]):
                    with transaction.atomic():
                        form_user.save(edit=True)
                        perfil = form_perfil.save()
                        form_instructor.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_user.is_valid():
                        print('error formulario user')
                        error.update(form_user.errors.get_json_data())
                    elif not form_instructor.is_valid():
                        print('error formulario instructor')
                        error.update(form_instructor.errors.get_json_data())
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
                    delet_registro = User.objects.filter(
                        pk__in=id_deletes)
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
        context['title'] = "Lista de instructors"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_instructor'] = InstructorForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context


@ login_required
@ permission_required('preMatricula.view_instructor', raise_exception=True)
def buscarInstructor(request):
    if request.method == 'POST':
        id_instructor = int(request.POST['id_instructor'])
        instructor = Instructor.objects.filter(pk=id_instructor)[0]
        datos = instructor.datosAllJson()
        datos['enviado'] = True
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)
