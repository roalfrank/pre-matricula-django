from django.shortcuts import render
from django.views.generic import TemplateView
from core.preMatricula.models import Provincia
from .form import ProvinciaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import  Q
import time


class ProvinciaListView(TemplateView):
    template_name = "tbentidad/provincia/list.html"
    
    @method_decorator(login_required)
    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = ProvinciaForm(request.POST)
                if form.is_valid():
                    form.save()
                    data['enviado']=True
                    data['nombre'] = request.POST['nombre']
                else:    
                    data['enviado']= False
                    data['error']="Error insertando dato"
            elif action == 'chequearProvincia':
                try:
                    
                    id_edit = request.POST['edit_id']
                    if id_edit == "":
                        id_edit = None

                    provincia = Provincia.objects.filter(
                        ~Q(id=id_edit), nombre__iexact=request.POST['nombre'])
                    print(provincia)
                    if len(provincia) < 1:
                        return JsonResponse(True, safe=False)
                    return JsonResponse(False,safe=False)
                except:
                    return JsonResponse(False,safe=False)
            elif action == "cargarDatos":
                # for n in range(31, 300):
                #     nombre = f"roal-{n}"
                #     provincia = Provincia(nombre=nombre)
                #     provincia.save()
                tiempo_inicial = time.time()
                data = [i.toJson()  for i in Provincia.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                tiempo = time.time() - tiempo_inicial
                print(tiempo)
                return respuesta
            elif action=='edit':
                print(request.POST)
                provincia=Provincia.objects.get(pk=int(request.POST['id_edit']))
                print(provincia)
                form = ProvinciaForm(request.POST,instance=provincia)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado']= False
                    data['error'] = "Error editando datos"
        except Exception as e:
            print(e)
            print(e.args)
            print(type(e))
            data['error'] = 'Ha ocurrido un error '
        return JsonResponse(data)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Provincia"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form'] = ProvinciaForm()
        return context



