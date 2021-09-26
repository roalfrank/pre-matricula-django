from core.preMatricula.models import PreMatriculaEstudiante
from core.preMatricula.models import Estudiante
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from core.preMatricula.models import PreMatricula, Curso
from core.preMatricula.views import esta_matriculado


def lista_curso_relacionado(id_matricula, cantidad):
    matricula = PreMatricula.objects.filter(pk=id_matricula).first()
    nexCurso = matricula.curso
    lista_relacionado = []
    for m in range(0, cantidad):
        proximo = nexCurso.nextCurso
        if proximo:
            lista_relacionado.append(proximo)
            nexCurso = proximo
    cantidad_buscado = len(lista_relacionado)
    lista_faltante = []
    if cantidad_buscado < cantidad:
        faltan = cantidad-cantidad_buscado
        lista_faltante = [m for m in Curso.objects.filter(
            ~Q(pk__in=[encontrado.pk for encontrado in lista_relacionado]))[0:faltan]]
    if len(lista_faltante) != 0:
        lista_relacionado.extend(lista_faltante)
    lista_matricula_relacionado = [
        matricula for matricula in PreMatricula.objects.filter(~Q(pk=id_matricula), curso__in=lista_relacionado)]
    return lista_matricula_relacionado


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
                    respuesta['cant_estudiante'] = PreMatriculaEstudiante.objects.filter(
                        preMatricula=matricula).count()
                    respuesta['estado'] = matricula.estado.nombre
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
                respuesta['cant_estudiante'] = PreMatriculaEstudiante.objects.filter(
                    preMatricula=matricula).count()
                matricula.actualizad_estado()
                respuesta['estado'] = matricula.estado.nombre
            except Exception as e:
                respuesta['error'] = True
                print(e)
        return JsonResponse(respuesta, safe=False)


@login_required
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
        context['next'] = self.request.GET.get('next')
        lista_estudiante = self.object.prematriculaestudiante_set.all()
        context['cantAlumnos'] = lista_estudiante.count()
        n = 4
        lista = [lista_estudiante[i:i + n]
                 for i in range(0, len(lista_estudiante), n)]
        context['listaAlumnos'] = lista
        context['base_url'] = "{0}://{1}{2}".format(
            self.request.scheme, self.request.get_host(), self.request.path)
        context['promedioCantidad'] = round(
            (context['cantAlumnos']*100)/self.object.capacidad, 2)
        is_liked = False
        if self.get_object().likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context['is_liked'] = is_liked
        context['listaRelacionado'] = lista_curso_relacionado(
            self.object.pk, 3)
        context['matriculado'] = esta_matriculado(
            self.request.user, self.object.pk)
        context['total_likes'] = self.get_object().likes.all().count()
        context['lista_comentarios'] = self.get_object(
        ).comentario_set.filter(respuestaA=None, aprobado=True).order_by('-fecha_comentario',)

        return context
