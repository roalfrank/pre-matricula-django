from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse


class ValidatePermissionRequiredCrudSimpleMixin(object):
    permiso_vista = ''
    permiso_crud = {}
    url_redirect = None

    def get_permiso_vista(self):
        perms = []
        if isinstance(self.permiso_vista, str):
            perms.append(self.permiso_vista)
        else:
            perms = list(self.permiso_vista)
        return perms

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('sitio:listar')
        return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        group = request.user.groups.all()[0]
        perms = self.get_permiso_vista()
        for p in perms:
            if not group.permissions.filter(codename=p).exists():
                return HttpResponseRedirect(self.get_url_redirect())
        if request.is_ajax() and request.method == "POST":
            action = request.POST['action']
            print(f'esto es lo que llegua al dispach :{action}')
            if (action == 'add' and not group.permissions.filter(codename=self.permiso_crud['add']).exists()) or (action == 'edit' and not group.permissions.filter(codename=self.permiso_crud['change']).exists()) or (action == 'delete' and not group.permissions.filter(codename=self.permiso_crud['delete']).exists()):
                data = {}
                data['enviado'] = False
                data['error'] = "No tiene acceso a esta opcion"
                return JsonResponse(data)
            print("paso la prueba de verificacion")
        return super().dispatch(request, *args, **kwargs)
