from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from core.preMatricula.models import PreMatricula


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
        context['promedioCantidad'] = round(
            (context['cantAlumnos']*100)/self.object.capacidad, 2)
        is_liked = False
        if self.get_object().likes.filter(id=self.request.user.id).exists():
            is_liked = True
        context['is_liked'] = is_liked
        context['total_likes'] = self.get_object().likes.all().count()
        context['lista_comentarios'] = self.get_object(
        ).comentario_set.filter(respuestaA=None, aprobado=True).order_by('-fecha_comentario',)
        print('lista de comentarios', context['lista_comentarios'])

        return context
