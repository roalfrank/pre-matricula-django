import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import  Q
from django.db.models.deletion import RestrictedError
from core.preMatricula.models import Provincia,Municipio
from .form import ProvinciaForm
from core.preMatricula.mixis import ValidatePermissionRequiredCrudSimpleMixin

def buscarMunicipios(request):
    if request.method == "POST":
        id_provincia = int(request.POST['id_provincia'])
        municipios = [{'id':i.id,'text':i.nombre} for i in Municipio.objects.filter(provincia__id=id_provincia)]
        return JsonResponse(municipios,safe=False)
    return JsonResponse([],safe=False)
    
class ProvinciaListView(LoginRequiredMixin, ValidatePermissionRequiredCrudSimpleMixin, TemplateView):
    template_name = "tbentidad/provincia/list.html"
    permiso_vista = 'view_provincia'
    permiso_crud = {
        'add': 'add_provincia',
        'change': 'change_provincia',
        'delete': 'delete_provincia',}

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
            #action chequearProvincia , esto es para comprobar rapido si ya hay otra provincia con el Mismo Nombre
            elif action == 'chequearProvincia':
                try:
                    #chequeamos si estamos en editar o add . si es editar hacemos la consulta con NONe
                    #edit_id no se incluye en la consulta 
                    id_edit = request.POST['edit_id']
                    if id_edit == "":
                        id_edit = None
                    #consulta a la base dato chequear el nombre de la provincia.
                    provincia = Provincia.objects.filter(
                        ~Q(id=id_edit), nombre__iexact=request.POST['nombre'])
                    if len(provincia) < 1:
                        #si no hay resultado en la busqueda , se devuelve True, dando lus verde a esa provincia.
                        return JsonResponse(True, safe=False)
                    #si hay resultado se retorna Fasle para impedir que se cree la provincia con nombres repetidos.
                    return JsonResponse(False,safe=False)
                except:
                    return JsonResponse(False,safe=False)
            # Action  cargarDatos - para cargar la datatable de mi vista.
            elif action == "cargarDatos":
                data = [i.toJson()  for i in Provincia.objects.all()]
                respuesta = JsonResponse(data, safe=False)
                return respuesta
            #action edit - editando una provincia.
            elif action=='edit':
                provincia=Provincia.objects.get(pk=int(request.POST['id_edit']))
                form = ProvinciaForm(request.POST,instance=provincia)
                if form.is_valid():
                    form.save()
                    data['enviado'] = True
                    data['nombre'] = request.POST['nombre']
                else:
                    data['enviado']= False
                    data['error'] = "Error editando datos"
            #action delete, eliminar una provincia
            elif action=="delete":
                try:
                    id_deletes = []
                    error = []
                    id = json.loads(request.POST["id"])
                    if type(id) == int:
                        id_deletes.append(id)
                    else:
                        id_deletes.extend(id)
                    delet_provincia = Provincia.objects.filter(pk__in=id_deletes)
                    for provincia in delet_provincia:
                        try:
                            provincia.delete()
                        except:
                            error.append(f"{provincia.nombre}")
                    if len(error)>0:
                        data['error'] = error
                except Exception as e:
                    if type(e) == RestrictedError:
                        data['error'] = "Esta provincia tiene municipios, no se puede borrar."
                    else:
                        print(type(e))
                        data['error'] = e
        except Exception as e:
            #comprobar los errores , esto despues solo dejar a data['error']
            print(e)
            print(e.args)
            print(type(e))
            data['error'] = 'Error en las operaciones con los registros'
        return JsonResponse(data)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Lista de Provincia"
        context['icono_titulo'] = "fas fa-tachometer-alt"
        context['form'] = ProvinciaForm()
        return context



