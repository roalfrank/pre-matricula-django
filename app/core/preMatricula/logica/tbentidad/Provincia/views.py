from django.shortcuts import render


def createProvincia(request):
    data ={}
    return render(request,"tbentidad/provincia/list.html",data)