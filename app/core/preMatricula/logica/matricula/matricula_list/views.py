from typing import List
from django.contrib.auth.decorators import permission_required, login_required
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.db.models.deletion import RestrictedError
from django.db.models import Q
from core.preMatricula.models import PreMatricula, Maestro, PreMatriculaMaestro
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin
from .form import PreMatriculaForm


class MatriculaDetailCargarFormAddView(TemplateView):
    template_name = "matricula/matricula_list/form_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_matricula'] = PreMatriculaForm()
        return context


class MatriculaView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "matricula/matricula_list/matricula_list.html"
    permiso_vista = 'view_prematricula'
    permiso_crud = {
        'add': 'add_prematricula',
        'change': 'change_prematricula',
        'delete': 'delete_prematricula',
    }

    def post(self, request, *args, **kwargs):

        data = {}
        try:
            action = request.POST['action']
            # action addd para adicionar registro
            if action == 'add':
                print(request.POST)
                form_matricula = PreMatriculaForm(request.POST)
                profesores = request.POST.getlist('profesor')
                print('primer profesor', profesores[0])
                if all([form_matricula.is_valid()]):
                    with transaction.atomic():
                        matricula = form_matricula.save()
                        error_creando_relacion = False
                        for profesor in profesores:
                            profe = Maestro.objects.filter(pk=profesor).first()
                            if profe:
                                PreMatriculaMaestro.objects.create(
                                    maestro=profe, preMatricula=matricula)
                            else:
                                error_creando_relacion = True
                        if error_creando_relacion:
                            data['enviado'] = False
                            data['error'] = 'Error creando relacion con matricula, buscando a profesor no encontrado.'
                        else:
                            data['enviado'] = True
                            data['nombre'] = matricula.curso.__str__()
                else:
                    data['enviado'] = False
                    data['error'] = form_matricula.errors.as_json()

            elif action == "cargarDatos":
                limite = int(request.POST['limite'])
                inicio = int(request.POST['inicio'])
                busqueda = request.POST['busqueda']
                lista_id_maestros = []
                print(busqueda)
                if busqueda != '':
                    lista_filtro = {
                        'curso': 'curso__pk',
                        'jcp': 'jcb__jcm__region__jcp__pk',
                        'region': 'jcb__jcm__region__pk',
                        'jcm': 'jcb__jcm__pk',
                        'jcb': 'jcb__pk',
                        'horas': 'curso__duracion',
                        'rango': 'fecha_inicio__range',
                        'estado': 'estado',
                        'profesor': 'prematriculamaestro__maestro__pk__in'}
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    # contador para limitar el for, solo se ejecute una ves si encuentra desde o hasta.
                    contador_solo_desde = 0
                    for key, value in filtros.items():
                        # si uno de los valores de busqueda es desde o hasta
                        if (key == 'desde' or key == 'hasta'):
                            # si contador es 0 - solo se hace una sola busqueda de fecha , asi evitamos volver a buscar
                            if contador_solo_desde == 0:
                                # rango de fecha en una lista para pasarla como parametro a la consulta
                                rango_fecha = [
                                    filtros['desde'], filtros['hasta']]
                                # se realiza la condicion de busqueda para el rangp se  fecha con el atributo de  range
                                condicion.add(
                                    Q(**{lista_filtro['rango']: rango_fecha}), Q.AND)
                                # cambio el contador para que no se realize mas, esto es solo una vez
                                contador_solo_desde = 1
                        else:
                            # tengo que chequear el parametro de busqueda estado para condicionarlo
                            if key == 'estado':
                                # si es diferente a todos , pues realizo la busqueda
                                if value != 'TD':
                                    condicion.add(
                                        Q(**{lista_filtro[key]: value}), Q.AND)
                            elif key == 'profesor':
                                lista_id_maestros = []
                                if type(value) == list:
                                    lista_id_maestros = [int(n) for n in value]
                                else:
                                    lista_id_maestros.append(int(value))
                                # condicion.add(
                                #     Q(**{'prematriculamaestro__maestro__pk__in': lista_id_maestros}), Q.AND)
                            else:
                                # aqui ya realizo las condiciones normales para todos los parametros de busquedas
                                condicion.add(
                                    Q(**{lista_filtro[key]: value}), Q.AND)
                    # si no esta estado como parametro de busqueda , entonces filtro por abierto
                    try:
                        filtros['estado']
                    except:
                        condicion.add(
                            Q(**{lista_filtro['estado']: 'AB'}), Q.AND)

                    matriculas = PreMatricula.objects.filter(condicion)
                else:
                    matriculas = PreMatricula.objects.filter(estado='AB')
                # lista que tiene ya formateados a json los datos a buscar
                lista = []
                for m in matriculas[inicio:inicio+limite]:
                    if len(lista_id_maestros) >= 1:
                        lista_pk_profesores_m = [
                            maestro['maestro__pk'] for maestro in m.prematriculamaestro_set.all().values('maestro__pk')]
                        if lista_pk_profesores_m == lista_id_maestros:
                            lista.append(m.toJson(request.user.pk))
                    else:
                        lista.append(m.toJson(request.user.pk))
                # formatos que es necesario para el datatble
                data = {
                    'total': len(lista),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            # action edit - editando una entidad.
            elif action == 'edit':
                matricula = PreMatricula.objects.get(
                    pk=int(request.POST['id_edit']))
                form_matricula = PreMatriculaForm(
                    request.POST, instance=matricula)
                profesores = request.POST.getlist('profesor')
                if all([form_matricula.is_valid()]):
                    with transaction.atomic():
                        matricula = form_matricula.save()
                        relacion_anterior = PreMatriculaMaestro.objects.filter(
                            preMatricula=matricula)
                        lista_no_editar = []
                        # recorrido por la relacion anterior para chequear quien se edito
                        for relacion in relacion_anterior:
                            # si la relacion esta en la lista nueva no borrarla
                            if relacion.pk in profesores:
                                # agrego a la lista que posteriormente utilizo para comparar
                                lista_no_editar.append(relacion.pk)
                            else:
                                # elimino la relacion porque no esta en la lista nueva
                                relacion.delete()
                        error_creando_relacion = False
                        if not len(lista_no_editar) == len(profesores):
                            lista_add_relacion = [
                                n for n in profesores if n not in lista_no_editar]
                            for maestro in lista_add_relacion:
                                profe = Maestro.objects.filter(
                                    pk=maestro).first()
                                if profe:
                                    PreMatriculaMaestro.objects.create(
                                        maestro=profe, preMatricula=matricula)
                                else:
                                    error_creando_relacion = True
                        if error_creando_relacion:
                            data['enviado'] = False
                            data['error'] = 'Error creando relacion con matricula, buscando a profesor no encontrado.'
                        else:
                            data['enviado'] = True
                            data['nombre'] = matricula.curso.__str__()
                else:
                    data['enviado'] = False
                    error = {}
                    if not form_matricula.is_valid():
                        error.update(form_matricula.errors.get_json_data())
                    print(error)
                    data['error'] = json.dumps(error)

            # action delete, eliminar una registro
            elif action == "delete":
                print(request.POST)
                try:
                    id_deletes = []
                    error = []
                    id = json.loads(request.POST["id"])
                    if type(id) == int:
                        id_deletes.append(id)
                    else:
                        id_deletes.extend(id)
                    delet_registro = PreMatricula.objects.filter(
                        pk__in=id_deletes)
                    for registro in delet_registro:
                        try:
                            registro.delete()
                        except Exception as e:
                            print('error borrar', e)
                            error.append(f"{registro.curso.__str__()}")
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
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de curso a matricular"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_matricula'] = PreMatriculaForm()
        return context


@ login_required
@ permission_required('preMatricula.view_prematricula', raise_exception=True)
def buscarMatricula(request):
    if request.method == 'POST':
        id_matricula = int(request.POST['id_matricula'])
        matricula = PreMatricula.objects.filter(pk=id_matricula).first()
        datos = matricula.toJsonForm()
        datos['enviado'] = True
        return JsonResponse(datos, safe=False)
    return JsonResponse([], safe=False)


@ login_required
@ permission_required('preMatricula.add_prematricula', raise_exception=True)
def buscarMaestro(request):
    if request.method == 'POST':
        busqueda = request.POST['busqueda']
        cantidad = int(request.POST['cantidad'])
        print(request.POST)
        maestros = Maestro.objects.filter(
            Q(instructor__usuario__perfil__nombre__icontains=busqueda) | Q(instructor__usuario__perfil__ci__icontains=busqueda) | Q(instructor__usuario__username__icontains=busqueda))[0:cantidad]
        print(maestros)
        resultado = [{
            'id': maestro.pk,
            'nombre': maestro.instructor.usuario.perfil.get_nombre(),
            'ci': maestro.instructor.usuario.perfil.ci,
            'foto': maestro.instructor.usuario.perfil.get_image(),
            'jcp': maestro.instructor.jcb.jcm.region.jcp.entidad.nombre,
            'jcm': maestro.instructor.jcb.jcm.entidad.nombre,
            'username': maestro.instructor.usuario.username,
            'jcb': maestro.instructor.jcb.entidad.nombre, } for maestro in maestros]
        print(resultado)

        return JsonResponse(resultado, safe=False)
    return JsonResponse([], safe=False)
