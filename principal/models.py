from django.core import validators
from django.core.validators import MinValueValidator, MaxValueValidator,URLValidator
from django.db import models
from numpy import unique


# Create your models here.
# from django.contrib.auth.models import User
# class profesor(models.Model):
# usuario = models.ForeignKey(User)

class Usuario(models.Model):
    idUsuario = models.IntegerField(null=False, blank=False, max_length=50, unique=True)
    edad = models.IntegerField(null=False, blank=False, max_length=50)
    localizacion = models.CharField(null=False, blank=False, max_length=100)
    def __unicode__(self):
        return self.idUsuario


class Libro(models.Model):
    isbn = models.CharField(max_length=30, null=False, blank=False, unique=True)
    titulo = models.CharField(max_length=30, null=False, blank=False)
    autor = models.CharField(max_length=30, null=False, blank=False)
    ano = models.IntegerField()
    editor=models.CharField(max_length=30, null=False, blank=False)
    urlS = models.URLField(validators=[URLValidator()])
    urlM = models.URLField(validators=[URLValidator()])
    urlL = models.URLField(validators=[URLValidator()])
    
    def __unicode__(self):
        return self.titulo

    
class Puntuacion(models.Model):
    libro = models.ForeignKey(Libro)
    idUsuario = models.IntegerField(null=False, blank=False, max_length=50, unique=True)
    isbn = models.CharField(max_length=30, null=False, blank=False, unique=True)
    puntuacion = models.IntegerField(null=False, blank=False, max_length=2, validators=[MinValueValidator(1), MaxValueValidator(10)])
    def __unicode__(self):
        return self.puntuacion
    