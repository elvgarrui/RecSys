#encoding:utf-8
from principal.models import *
from django.shortcuts import render_to_response, get_list_or_404
# Para autenticacion
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
# from django.core.mail import EmailMessage# Create your views here.


def inicio(request):
    return render_to_response('inicio.html')