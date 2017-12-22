import csv
from datetime import time
import datetime

from django.core.management import call_command

from main.models import Artista, Etiqueta, UsuarioArtista, UsuarioEtiquetaArtista, UsuarioAmigo


lim=500
userL=50
artistF = "carga/artists.dat"
tagF = "carga/tags.dat"
usartF = "carga/user_artists.dat"
UsfriF = "carga/user_friends.dat"
UstagF = "carga/user_taggedartists.dat"


def populateBBDD():
    call_command('flush',interactive=False)
    call_command('syncdb',interactive=False)
    
    populateArtistas()
    populateEtiquetas()
    populateUserArtists()
    populateUserFriend()
    populateUserTagArtists()
 
 
def populateArtistas():
    with open(artistF) as f:
        reader = csv.reader(f,delimiter="|")
        print "Creando artistas..."
        for row in reader:
            if int(row[0])>lim:
                break
            Artista.objects.get_or_create(idArtista=int(row[0]),nombre=row[1], url=row[2], pictureUrl=row[3])


def populateEtiquetas():     
    with open(tagF) as f:
        reader = csv.reader(f,delimiter="|")
        print "Creando etiquetas..."
        for row in reader:
            if int(row[0])>lim:
                break
            Etiqueta.objects.get_or_create(idTag=int(row[0]),tagValue=row[1])
            
            
def populateUserArtists():           
    with open(usartF) as f:
        reader = csv.reader(f,delimiter="|")
        print "Creando relaciones usuario-artista..."
#         i=0
        for row in reader:
            if int(row[1])<=lim and int(row[0])<=userL:
                try:
                    usuarioId = row[0]
                    artista = Artista.objects.get(idArtista=int(row[1]))
                    t = row[2]
                    UsuarioArtista.objects.get_or_create(usuarioId=usuarioId,artista=artista,tiempoEscucha=t)
                except:
                    pass
            

def populateUserFriend():
    with open(UstagF) as f:
        reader = csv.reader(f,delimiter="|")                
        print "Creando amistades..."
        for row in reader:
            if int(row[0])<=userL and int(row[1])<=userL:
                usuarioId=row[0]
                amigoId=row[1]
                UsuarioAmigo.objects.get_or_create(usuarioId=usuarioId,amigoId=amigoId)
    
    
def populateUserTagArtists():
    with open(UstagF) as f:
        reader = csv.reader(f,delimiter="|")
        print "Creando relaciones userartisttag..."        
#         i=0
        for row in reader:
            if int(row[1])<=lim and int(row[2])<=lim and int(row[0])<=userL:
                try:
                    userid=row[0]
                    artista=Artista.objects.get(idArtista=int(row[1]))
                    tag = Etiqueta.objects.get(idTag=int(row[2]))
                    fecha = datetime.date(int(row[5]), int(row[4]), int(row[3]))
                    UsuarioEtiquetaArtista.objects.get_or_create(usuarioId=userid,artista=artista,fecha=fecha,tag=tag)
                except:
                    pass
            
            
if __name__ == '__main__':
    populateBBDD()
    print "Done!"