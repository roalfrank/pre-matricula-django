from django.shortcuts import render
from django.views.generic import TemplateView
from core.preMatricula.models import Provincia
from .form import ProvinciaForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


class ProvinciaListView(TemplateView):
    template_name = "tbentidad/provincia/list.html"
    
    @method_decorator(login_required)
    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request,*args,**kwargs):
        #print('Hola estoy en crear provincia principio')
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'add':
                print('Hola estoy en crear provincia dentro')
                form = ProvinciaForm(request.POST)
                print(form)
                if form.is_valid():
                    form.save()
                    data['enviado']=True
                    data['nombre'] = request.POST['nombre']
                else:    
                    data['enviado']= False
            elif action == 'chequearProvincia':
                #print(request.POST['nombre'][0])
                try:
                    provincia = Provincia.objects.filter(nombre__iexact=request.POST['nombre'])
                    print(provincia)
                    if len(provincia) < 1:
                        return JsonResponse(True, safe=False)
                    return JsonResponse(False,safe=False)
                except:
                    return JsonResponse(False,safe=False)
            elif action == "cargarDatos":
                data = [i.toJson()  for i in Provincia.objects.all()]
                print(data)
                return JsonResponse(data,safe=False)
        except Exception as e:
            print(e)
            data['error'] = 'Ha ocurrido un error '
        return JsonResponse(data)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Provincia"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form'] = ProvinciaForm()
        return context



