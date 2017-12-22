#encoding:utf-8
import operator

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext

from principal.forms import SearchForm
from principal.models import *
from populate import populateBBDD


# Para autenticacion
# from django.core.mail import EmailMessage# Create your views here.
def inicio(request):
    return render_to_response('inicio.html')

def populateDB(request):
    populateBBDD()
    return render_to_response('populate.html')

def buscarPorUsuario(request):
    if request.method == 'POST':
        formulario = SearchForm(request.POST)
        if formulario.is_valid():
            usuarioLibros = Puntuacion.objects.filter(usuario=Usuario.objects.get(idUsuario=formulario.cleaned_data['idUsuario']))
            return render_to_response('a.html',{'libros':usuarioLibros})
    else:
        formulario = SearchForm()
    return render_to_response('search.html',{'formulario':formulario}, context_instance=RequestContext(request))


def mejorPuntuados(request):
    puntuados={}
    punts = Puntuacion.objects.all()
    for row in punts:
        libro = row.libro.isbn
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