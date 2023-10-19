from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import requests

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    return HttpResponse("Hello"#requests.get('http://127.0.0.1:8000/'))
                        )

def datos_perfil(request):
    return HttpResponse(requests.get('http://127.0.0.1:8000/DatosPerfil'))


def estado_cuenta(request):
    return HttpResponse(requests.get('http://127.0.0.1:8000/EstadoCuenta'))
