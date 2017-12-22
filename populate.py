#encoding:utf-8
import csv

from django.core.management import call_command

from principal.models import Libro, Usuario, Puntuacion


lim=50
libF = "csv/BX-Books.csv"
userF = "csv/BX-Users.csv"
ratF = "csv/BX-Book-Ratings.csv"


def populateBBDD():
    call_command('flush',interactive=False)
    call_command('syncdb',interactive=False)
    
    populateLibros()
    populateUsers()
    populateRatings()
 
 
def populateLibros():
    with open(libF) as f:
        reader = csv.reader(f,delimiter=";")
        print "Creando Libros..."
        i = 0
        for row in reader:
            try:
                for a in row: a=a.decode('utf-8')
                if i>lim:
                    break
                i+=1
            
                Libro.objects.create(isbn=row[0], titulo=row[1], autor=row[2], ano=row[3]
                                 ,editor=row[4], urlS=row[5], urlM=row[6], urlL=row[7])
            except:
                pass

def populateUsers():     
    with open(userF) as f:
        reader = csv.reader(f,delimiter=";")
        print "Creando usuario..."
        i = 0
        for row in reader:
            try:
                if i >lim:
                    break
                if row[2] is not "NULL":
                    Usuario.objects.create(idUsuario=row[0],edad=row[2],localizacion=row[1])
                
                i+=1
            except:
                pass

def populateRatings():
    with open(ratF) as f:
        reader = csv.reader(f,delimiter=";")
        print "Creando ratings..."        
        i = 0
        for row in reader:
            try:
                if i<=lim:
                    Puntuacion.objects.create(idUsuario=row[0],isbn=row[1],puntuacion=row[2])
                i+=1
            except:
                pass    
            
if __name__ == '__main__':
    populateBBDD()
    print "Done!"