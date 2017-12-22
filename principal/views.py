#encoding:utf-8
import operator

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext

from principal.models import *


# Para autenticacion
# from django.core.mail import EmailMessage# Create your views here.
def inicio(request):
    return render_to_response('inicio.html')

def mejorPuntuados(request):
    puntuados={}
    punts = Puntuacion.objects.all()
    for row in punts:
        libro = row.isbn
        puntos = row.puntuacion
        if libro in puntuados:
            aux=puntuados[libro]
            puntuados[libro]=aux+puntos
        else:
            puntuados[libro] = puntos
    
    libros=[]
    
    for i in range(3):
        if puntuados:
            masP = max(puntuados.iteritems(), key=operator.itemgetter(1))[0]
            libros.append(Libro.objects.get(isbn=masP))
            del puntuados[masP]
    
    return render_to_response('b.html',{'libros':libros})