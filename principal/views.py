#encoding:utf-8
import operator
import shelve

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404, \
    get_object_or_404
from django.template import RequestContext

from populate import populateBBDD
from principal.forms import SearchForm
from principal.models import *
from principal.recommendations import transformPrefs, calculateSimilarUsers, \
    topMatches


Prefs={}   # matriz de usuarios y puntuaciones a cada a items
ItemsPrefs={}   # matriz de items y puntuaciones de cada usuario. Inversa de Prefs
SimItems=[]  # matriz de similitudes entre los items

def loadDict():
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.usuario.id)
        isbn = int(ra.libro.isbn)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[isbn][user] = rating
    shelf['Prefs']=Prefs
    shelf['UserPrefs']=transformPrefs(Prefs)
    shelf['SimUser']=calculateSimilarUsers(Prefs, n=10)
    shelf.close()

def loadRS(request):
    loadDict()
    return render_to_response('populate.html')
     


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
    
    for row in punts:
        libro = row.libro.isbn
        puntuados[libro]/=Puntuacion.objects.filter(libro=Libro.objects.get(isbn=libro)).count()
    
    libros=[]
    
    for i in range(3):
        if puntuados:
            masP = max(puntuados.iteritems(), key=operator.itemgetter(1))[0]
            libros.append(Libro.objects.get(isbn=masP))
            del puntuados[masP]
    
    return render_to_response('b.html',{'libros':libros})


def similarBooks(request):
    user = None
    if request.method == 'POST':
            formulario = SearchForm(request.POST)
            if formulario.is_valid():
                idUsuario = formulario.cleaned_data['Id del usuario']
                user = get_object_or_404(Usuario, pk=idUsuario)
                shelf = shelve.open("dataRS.dat")
                ItemsPrefs = shelf['ItemsPrefs']
                shelf.close()
                recommended = topMatches(ItemsPrefs, int(idUsuario),n=3)
                print recommended
                items=[]
                for re in recommended:
                    item = Libro.objects.get(pk=int(re[1]))
                    items.append(item)
            else:
                formulario = SearchForm()
            return render_to_response('search2.html',{'formulario':formulario}, context_instance=RequestContext(request))
        

