from core.preMatricula.models import PreMatriculaEstudiante
from core.preMatricula.models import Estudiante
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, request
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.preMatricula.models import PreMatricula, Curso
from core.preMatricula.views import esta_matriculado

# metodo para saber si un estudiante esta matriculado


def estudianteEstaMatriculado(request):
    if request.method == 'POST':
        id_matricula = int(request.POST['id_matricula'])
        esta = esta_matriculado(request.user, id_matricula)
        print('esta Matriculado?', esta)
        return JsonResponse(esta, safe=False)

# metodo que devuelve los cursos relacionados a una matricula


def lista_curso_relacionado(id_matricula, cantidad):
    matricula = PreMatricula.objects.filter(pk=id_matricula).first()
    nexCurso = matricula.curso
    lista_relacionado = []
    # itero hasta la cantidad para ir agregando los nextcursos
    for m in range(0, cantidad):
        proximo = nexCurso.nextCurso
        if proximo:
            lista_relacionado.append(proximo)
            nexCurso = proximo
        # si no tiene proximo salgo
        else:
            break
    # cantidad de elementos en la lista de relacionados
    cantidad_buscado = len(lista_relacionado)
    lista_faltante = []
    # compruebo si estan la canrtidad que se necesitan
    if cantidad_buscado < cantidad:
        # faltan cursos para completar lo  que se pide
        faltan = cantidad-cantidad_buscado
        # rellenamos con cursos de la tabla general
        lista_faltante = [m for m in Curso.objects.filter(
            ~Q(pk__in=[encontrado.pk for encontrado in lista_relacionado]))[0:faltan]]
    if len(lista_faltante) != 0:
        lista_relacionado.extend(lista_faltante)
    # con el listado de los cursos ya completados, procedemos a listar las matriculas de esos cursos
    lista_matricula_relacionado = [
        matricula for matricula in PreMatricula.objects.filter(~Q(pk=id_matricula), curso__in=lista_relacionado)]
    return lista_matricula_relacionado

# analizar este metodo mas tarde para comprobar si esta vigente


@login_required
def listar_estudiante_matriculado_carrucel(request, id_matricula):
    template_name = "matricula/matricula/lista_estudiantes_matriculado_carrucel.html"
    respuesta = {}
    matricula = PreMatricula.objects.filter(pk=id_matricula).first()
    lista_estudiante = matricula.listadoEstudiante()
    n = 4
    lista = [lista_estudiante[i:i + n]
             for i in range(0, len(lista_estudiante), n)]
    respuesta['listaAlumnos'] = lista
    return render(request, template_name, respuesta)

# analizar este metodo mas tarde para comprobar si esta vigente


@login_required
def likeMatricula(request):
    context = {}

    if request.method == "POST":

        matricula = get_object_or_404(
            PreMatricula, id=request.POST.get('id_matricula'))
        is_liked = False
        if matricula.likes.filter(id=request.user.id).exists():
            matricula.likes.remove(request.user)
            is_liked = False

        else:
            matricula.likes.add(request.user)
            is_liked = True

        context['is_liked'] = is_liked
        context['total_likes'] = matricula.likes.all().count()
        context['error'] = False
    else:
        context['error'] = True
    return JsonResponse(context, safe=False)


@login_required
def addEstudianteMatricula(request):
    if request.method == 'POST':
        action = request.POST['action']
        respuesta = {}
        if action == 'add':
            try:
                id_matricula = int(request.POST['id_matricula'])
                estudiante = Estudiante.objects.filter(
                    usuario=request.user).first()
                matricula = PreMatricula.objects.filter(
                    pk=id_matricula).first()
                matriculado_ya = PreMatriculaEstudiante.objects.filter(
                    preMatricula=matricula, estudiante=estudiante).count()
                if matriculado_ya >= 1:
                    respuesta['error'] = True
                else:

                    matriculado = PreMatriculaEstudiante(
                        preMatricula=matricula, estudiante=estudiante)
                    matriculado.save()
                    respuesta['error'] = False
            except Exception as e:
                respuesta['error'] = True
                print(e)

        elif action == 'delete':
            try:
                id_matricula = int(request.POST['id_matricula'])
                estudiante = Estudiante.objects.filter(
                    usuario=request.user).first()
                matricula = PreMatricula.objects.filter(
                    pk=id_matricula).first()
                matriculado_ya = PreMatriculaEstudiante.objects.filter(
                    preMatricula=matricula, estudiante=estudiante).first()
                matriculado_ya.delete()
                respuesta['error'] = False

            except Exception as e:
                respuesta['error'] = True
                print(e)
        return JsonResponse(respuesta, safe=False)


def getDetallePageMatricula(request, id):
    template_name = "matricula/matricula/detalle_matricula_page.html"
    context = {}
    context['id_matricula'] = id
    return render(request, template_name, context)


class MatriculaDetailView(DetailView):
    model = PreMatricula
    template_name = "matricula/matricula/detalle_matricula.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # next es la direccion  a donde tenemos que direccionar una vez terminado
        context['next'] = self.request.GET.get('next')
        # cantidad y listado de alumnos de esta matricula
        lista_estudiante = self.object.prematriculaestudiante_set.all()
        context['cantAlumnos'] = lista_estudiante.count()
        context['listaAlumnos'] = lista_estudiante
        # base_url empleado en le generador de qr
        context['base_url'] = "{0}://{1}{2}".format(
            self.request.scheme, self.request.get_host(), '/sistema/matricula-pagina/')
        # promedio en pociento de los estudiantes contra capacidad
        context['promedioCantidad'] = round(
            (context['cantAlumnos']*100)/self.object.capacidad, 2)
        # esto activa el boton de like si el usuario ha dado like
        is_liked = False
        if self.get_object().likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context['is_liked'] = is_liked
        # listado de los cursos relacionados a esta matricula
        context['listaRelacionado'] = lista_curso_relacionado(
            self.object.pk, 3)
        # comprobar si la se esta mirando aurenticado para mandar la variable matriculado
        if self.request.user.is_authenticated:
            context['matriculado'] = esta_matriculado(
                self.request.user, self.object.pk)
        # mandar el estado  de la matricula
        if self.object.estado == 'CE':
            context['cerrado'] = True
        else:
            context['cerrado'] = False
        # total de likes
        context['total_likes'] = self.get_object().likes.all().count()
        # listado de los comentarios
        context['lista_comentarios'] = self.get_object(
        ).comentario_set.filter(respuestaA=None, aprobado=True).order_by('fecha_comentario',)

        return context
