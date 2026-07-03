from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto
# Register your models here.

class AdministradorModelo(admin.ModelAdmin):
    readonly_fields = ('created','updated')
    list_display = ('matricula','nombre','carrera','turno')
    search_fields = ('matricula','nombre','carrera','turno')
    date_hierarchy = 'created'
    list_filter = ('carrera','turno')

class ComentarioModelo(admin.ModelAdmin):
    list_display = ('id','alumno','coment')
    search_fields = ('id','alumno','coment')
    date_hierarchy = 'created'
    readonly_fields = ('created','id')
    list_display_links = ('id', 'alumno')
    list_select_related = ('alumno',)
    #exclude = ('id',)
    list_editable = ('coment',)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id', 'mensaje')
    search_fields = ('id','created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')




admin.site.register(Alumnos, AdministradorModelo)
admin.site.register(Comentario,ComentarioModelo)
admin.site.register(ComentarioContacto, AdministrarComentariosContacto)