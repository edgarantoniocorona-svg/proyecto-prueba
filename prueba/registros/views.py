import datetime

from django.shortcuts import render
from .models import Alumnos, ComentarioContacto, Archivos
from .forms import ComentarioContactoForm, FormArchivos
from django.shortcuts import get_object_or_404
from django.contrib import messages

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
    # Devolvemos la función que faltaba para revivir el servidor
    return render(request, "registros/contacto.html")


def comentariosregistro(request):
    # Consulta impecable que mapea con tu tabla HTML
    datos_comentarios = ComentarioContacto.objects.all() 
    return render(request, 'registros/comentariosregistro.html', {'comentariocontactos': datos_comentarios})

def eliminarComentarioContacto(request, id,confirmacion='registros/confirmarEliminar.html'):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    if request.method == 'POST':
        comentario.delete()
        comentarios = ComentarioContacto.objects.all()
        return render(request, 'registros/comentariosregistro.html',{'comentariocontactos':comentarios})
    return render(request, confirmacion, {'object': comentario})

def ConsultarComentarioIndividual(request, id):
    comentario=ComentarioContacto.objects.get(id=id)
    #get permite establecer una condicionante a la consulta y recupera el objetos
    #del modelo que cumple la condición (registro de la tabla ComentariosContacto.
    #get se emplea cuando se sabe que solo hay un objeto que coincide con su
    #consulta.
    return render(request, 'registros/editarComentario.html', {'comentario': comentario})
    #Indicamos el lugar donde se renderizará el resultado de esta vista
    # y enviamos la lista de alumnos recuparados.
    
def editarComentarioContacto(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)
    form = ComentarioContactoForm(request.POST, instance=comentario)
    #referenciamos que el elemento del formulario pertenece al comentario ya existente
    if form.is_valid():
        form.save()#si el registro ya existe, se modifica.
        comentarios=ComentarioContacto.objects.all()
        return render(request, 'registros/comentariosregistro.html', {'comentariocontactos': comentarios})
        #Si el formulario no es valido nos regresa al formulario para verificar datos
    return render(request, 'registros/editarComentario.html', {'comentario': comentario})

def consultas(request):
    alumnos = Alumnos.objects.all()
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar1(request):
    alumnos = Alumnos.objects.filter(carrera="TI")
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar2(request):
    alumnos = Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar3(request):
    alumnos=Alumnos.objects.all().only("matricula","nombre","carrera","turno","imagen")
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar4(request):
    alumnos = Alumnos.objects.filter(matricula__startswith="UTM23")
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar5(request):
    alumnos = Alumnos.objects.filter(turno__in=["Matutino", "Vespertino"])
    return render(request, "registros/consultas.html", {'alumnos': alumnos})

def consultar6(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    fechaInicio = datetime.date(2026, 7, 1)
    fechaFin = datetime.date(2026, 8, 13)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultar8(request):
    #Consultando entre modelos
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consultasSQL(request):
    alumnos=Alumnos.objects.raw('SELECT id,  matricula,nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
    return render(request,"registros/consultas.html",{'alumnos':alumnos})

def consulta_rango_fechas(request):
    fecha_inicio = datetime.date(2026, 6, 20)
    fecha_fin = datetime.date(2026, 8, 4)
    comentarios = ComentarioContacto.objects.filter(created__range=(fecha_inicio, fecha_fin))
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_rango_fechas_sql(request):
    tabla = ComentarioContacto._meta.db_table
    comentarios = ComentarioContacto.objects.raw(
        f'''SELECT id, usuario, mensaje, created 
           FROM registros_comentariocontacto
           WHERE DATE(created) BETWEEN "2026-06-20" AND "2026-08-04"'''
    )
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})


def consulta_expresion_comentario(request):
    expresion = ";)"
    # Se usa mensaje__icontains porque el campo se llama 'mensaje'
    comentarios = ComentarioContacto.objects.filter(mensaje__icontains=expresion)
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_expresion_comentario_sql(request):
    tabla = ComentarioContacto._meta.db_table
    comentarios = ComentarioContacto.objects.raw(
        f'''SELECT id, usuario, mensaje, created 
           FROM registros_comentariocontacto
           WHERE mensaje LIKE %s''', ['%importante%']
    )
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})


def consulta_por_usuario(request):
    usuario_buscado = "lol"
    comentarios = ComentarioContacto.objects.filter(usuario=usuario_buscado)
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_por_usuario_sql(request):
    tabla = ComentarioContacto._meta.db_table
    comentarios = ComentarioContacto.objects.raw(
        f'''SELECT id, usuario, mensaje, created 
           FROM registros_comentariocontacto 
           WHERE usuario = %s''', ["edgar"]
    )
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_expresion_year(request):
    comentarios = ComentarioContacto.objects.filter(created__year=2026)
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_expresion_year_sql(request):
    tabla = ComentarioContacto._meta.db_table
    comentarios = ComentarioContacto.objects.raw(
        f'''SELECT id, usuario, mensaje, created 
           FROM registros_comentariocontacto 
           WHERE strftime("%%Y", created) = "2026"'''
    )
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_expresion_startswith(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__startswith='prueba')
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def consulta_expresion_startswith_sql(request):
    tabla = ComentarioContacto._meta.db_table
    comentarios = ComentarioContacto.objects.raw(
        f'''SELECT id, usuario, mensaje, created 
           FROM registros_comentariocontacto 
           WHERE mensaje LIKE %s''', ['pago%']
    )
    return render(request, "registros/comentariosregistro.html", {'comentariocontactos': comentarios})

def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
            insert.save()       
            return render(request, 'registros/archivos.html', {'archivos': archivos})
        else:
            messages.error(request, "Error al procesar el formulario")
    else:
        return render(request, "registros/archivos.html", {'archivos': Archivos})

