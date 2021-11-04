import json
import datetime
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.contrib.auth.models import User, Group
from django.db.models import Q, F
from core.preMatricula.models import Estudiante, PreMatriculaEstudiante
from core.user.models import Perfil
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import UserCrearAutomaticoForm, EstudianteForm
from core.login.form import UserPerfilRegistrationForm
from core.preMatricula.utils.general import listado_matricula_estudiante


# class EstudianteView(ListView):
#     model = Estudiante
#     template_name = "estudiante/estudiante/list.html"
#     paginate_by = 2

#     # def get_queryset(self):
#     #     datos = self.model.objects.all()
#     #     return datos

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(context)
#         # return context
class EstudianteDetailCargarFormAddView(TemplateView):
    template_name = "estudiante/estudiante/form_add.html"

    def get_context_data(self, **kwargs):
        print(self.request.GET.get('next'))
        context = super().get_context_data(**kwargs)
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_estudiante'] = EstudianteForm()
        context['form_user'] = UserCrearAutomaticoForm()
        print('estoy en add form estudiante')
        return context


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = "estudiante/estudiante/detailEstudiante.html"

    def get_context_data(self, **kwargs):
        print(self.request.GET.get('next'))
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        context['matriculados'] = self.get_object(
        ).prematriculaestudiante_set.all()
        print(context['matriculados'])
        context['interes'] = self.get_object(
        ).estudiantecursointeres_set.all()
        print('curso interes', context['interes'])
        return context


class EstudianteView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    # model = Estudiante
    template_name = "estudiante/estudiante/estudiante_list.html"
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

                print(request.POST)
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

                    estudiantes = Estudiante.objects.filter(condicion)
                else:
                    estudiantes = Estudiante.objects.filter(
                        Q(usuario__perfil__nombre__icontains=busqueda) | Q(
                            usuario__username__icontains=busqueda) | Q(usuario__perfil__ci__icontains=busqueda) | Q(usuario__perfil__correo__icontains=busqueda)
                    )

                lista = [i.toJson()
                         for i in estudiantes[inicio:inicio+limite]]
                data = {
                    'total': estudiantes.count(),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                print(request.POST)
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
                        form_user.save(edit=True)
                        perfil = form_perfil.save()
                        form_estudiante.save()
                        data['enviado'] = True
                        data['nombre'] = perfil.nombre
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_user.is_valid():
                        print('error formulario user')
                        error.update(form_user.errors.get_json_data())
                    elif not form_estudiante.is_valid():
                        print('error formulario estudiante')
                        error.update(form_estudiante.errors.get_json_data())
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
        context['title'] = "Lista de Estudiantes"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_perfil'] = UserPerfilRegistrationForm()
        context['form_estudiante'] = EstudianteForm()
        context['form_user'] = UserCrearAutomaticoForm()
        return context

# metodos utiles


def cantEstudiantes():
    cant = Estudiante.objects.all().count()
    return cant


def cant_estudiantes_no_matriculados():
    cant = Estudiante.objects.exclude(
        prematriculaestudiante__estudiante__pk=F('pk')).count()
    hace_una_semana = datetime.datetime.now() - datetime.timedelta(days=7)
    print(hace_una_semana)
    print(Estudiante.objects.exclude(
        Q(prematriculaestudiante__estudiante__pk=F('pk'))).filter(Q(usuario__date_joined__lt=hace_una_semana)))
    return cant


def reporte_estudiante_semana_actual():
    result = {}
    date = datetime.datetime.today()
    dia_semana = date.weekday()+1
    week = int(date.strftime("%V"))
    lista_estudiante_semana_actual = Estudiante.objects.filter(
        usuario__date_joined__week=week)
    lista_estudiante_semana_pasada = Estudiante.objects.filter(
        usuario__date_joined__week=week-1)
    result['cantidad_estudiantes_semana_actual'] = lista_estudiante_semana_actual.count()
    result['cantidad_estudiantes_semana_pasada'] = lista_estudiante_semana_pasada.count()
    lista_cantidad_estudiantes_dias_actual = []
    lista_cantidad_estudiantes_dias_pasado = []
    for dia in range(1, 8):
        if dia <= dia_semana:
            lista_cantidad_estudiantes_dias_actual.append(lista_estudiante_semana_actual.filter(
                usuario__date_joined__iso_week_day=dia).count())
        lista_cantidad_estudiantes_dias_pasado.append(lista_estudiante_semana_pasada.filter(
            usuario__date_joined__iso_week_day=dia).count())
    result['lista_cantidad_estudiantes_dias_actual'] = lista_cantidad_estudiantes_dias_actual
    result['lista_cantidad_estudiantes_dias_pasado'] = lista_cantidad_estudiantes_dias_pasado
    return result


def matriculados_en_la_semana_actual():
    result = {}
    date = datetime.datetime.today()
    dia_semana = date.weekday()+1
    week = int(date.strftime("%V"))
    lista_estudiante_semana_matriculado_actual = PreMatriculaEstudiante.objects.filter(
        fecha_creado__week=week)
    lista_estudiante_semana_matriculado_pasada = PreMatriculaEstudiante.objects.filter(
        fecha_creado__week=week-1)
    # para que funcione el distint es necesario extraer por values()
    result['cantidad_estudiantes_semana_matriculado_actual'] = lista_estudiante_semana_matriculado_actual.count()
    result['cantidad_estudiantes_semana_matriculado_pasada'] = lista_estudiante_semana_matriculado_pasada.count()
    lista_cantidad_estudiantes_dias_matriculado_actual = []
    lista_cantidad_estudiantes_dias_matriculado_pasado = []
    for dia in range(1, 8):
        if dia <= dia_semana:
            lista_cantidad_estudiantes_dias_matriculado_actual.append(lista_estudiante_semana_matriculado_actual.filter(
                fecha_creado__iso_week_day=dia).count())
        lista_cantidad_estudiantes_dias_matriculado_pasado.append(lista_estudiante_semana_matriculado_pasada.filter(
            fecha_creado__iso_week_day=dia).count())
    result['lista_cantidad_estudiantes_dias_matriculado_actual'] = lista_cantidad_estudiantes_dias_matriculado_actual
    result['lista_cantidad_estudiantes_dias_matriculado_pasado'] = lista_cantidad_estudiantes_dias_matriculado_pasado
    return result


def estudiantes_no_matriculados_7dias_registrado():
    pass
