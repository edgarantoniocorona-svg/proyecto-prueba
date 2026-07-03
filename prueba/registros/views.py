from django.shortcuts import render
from .models import Alumnos, ComentarioContacto
from .forms import ComentarioContactoForm

# Create your views here.

def registros(request):
    alumnos = Alumnos.objects.all()
    return render(request, "registros/principal.html", {'alumnos': alumnos})


def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): 
            form.save() # Guarda los datos en la base de datos
            
            # Recuperamos los datos actualizados usando el Modelo y enviando la clave exacta
            comentarios = ComentarioContacto.objects.all()
            return render(request, 'registros/comentariosregistro.html', {'comentariocontactos': comentarios})
    else:
        form = ComentarioContactoForm()
        
    return render(request, 'registros/contacto.html', {'form': form})


def contacto(request):
    # 👈 Devolvemos la función que faltaba para revivir el servidor
    return render(request, "registros/contacto.html")


def comentariosregistro(request):
    # Consulta impecable que mapea con tu tabla HTML
    datos_comentarios = ComentarioContacto.objects.all() 
    return render(request, 'registros/comentariosregistro.html', {'comentariocontactos': datos_comentarios})