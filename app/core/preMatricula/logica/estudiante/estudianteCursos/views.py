import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q, F
from core.preMatricula.models import PreMatricula
from .form import EstudianteCursosForm


class EstudianteCursosView(LoginRequiredMixin, TemplateView):
    template_name = "estudiante/estudiante-cursos/estudiante_cursos_list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == "cargarDatos":
                limite = int(request.POST['limite'])
                inicio = int(request.POST['inicio'])
                busqueda = request.POST['busqueda']
                if busqueda != '':
                    lista_filtro = {
                        'estado': 'estado',
                        'cursos': 'curso__pk',
                        'horas': 'curso__duracion',
                    }
                    busqueda_json = json.loads(busqueda)
                    filtros = busqueda_json['filtro']
                    condicion = Q()
                    pk_usuario = request.user.pk
                    condicion.add(
                        Q(**{'prematriculaestudiante__estudiante__usuario__pk': pk_usuario}), Q.AND)
                    for key, value in filtros.items():
                        if key == 'estado':
                            # si es diferente a todos , pues realizo la busqueda
                            if value != 'TD':
                                condicion.add(
                                    Q(**{lista_filtro[key]: value}), Q.AND)
                        else:
                            condicion.add(
                                Q(**{lista_filtro[key]: value}), Q.AND)
                    try:
                        filtros['estado']
                    except:
                        condicion.add(
                            Q(**{lista_filtro['estado']: 'AB'}), Q.AND)
                    matriculas = PreMatricula.objects.filter(condicion)
                else:
                    matriculas = PreMatricula.objects.filter(
                        prematriculaestudiante__estudiante__usuario__pk=request.user.pk)
                lista = []
                for m in matriculas[inicio:inicio+limite]:
                    lista.append(m.toJson())
                # formatos que es necesario para el datatble
                data = {
                    'total': len(lista),
                    'lista': lista
                }
                respuesta = JsonResponse(data, safe=False)
                return respuesta
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
        context['title'] = "Mis Cursos"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form_estudiante_curso'] = EstudianteCursosForm()

        return context

# metodos utiles
