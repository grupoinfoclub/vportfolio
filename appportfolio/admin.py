# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from appportfolio.models import *
from django.contrib.auth.models import User

#este es el título del encabezado superior   
admin.site.site_header = "SITIO DE ADMINISTRACIÓN DE PORTFOLIO"  
#El título de la pestaña del navegador (etiqueta HTML <title>).
admin.site.site_title = "ADMINISTRACIÓN DE PORTFOLIO"
#Subtítulo de la página 
admin.site.index_title = "Bienvenidos al portal de Administración"

class CategoriaAdmin(admin.ModelAdmin):
	#list_display = [c.name for c in Categoria._meta.get_fields()]
	list_display = ['id','nombre_categoria']
	search_fields = ('id','nombre_categoria')
	list_filter   = ('id','nombre_categoria')
admin.site.register(Categoria, CategoriaAdmin)

class ExperienciaAdmin(admin.ModelAdmin):
	list_display = [c.name for c in Experiencia._meta.get_fields()]
	#list_display = ['id', 'empresa','fecha_inicio','fecha_fin','observaciones','categoria']
	search_fields = ('id','empresa')
	list_filter   = ('id','empresa')
admin.site.register(Experiencia, ExperienciaAdmin)

class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'titulo',
        'fecha',
        'tecnologias',
        'precio'
    )
    search_fields = ('titulo', 'tecnologias')
    list_filter = ('fecha', 'tecnologias')
    ordering = ('titulo',)
admin.site.register(Proyecto, ProyectoAdmin)    

class PostAdmin(admin.ModelAdmin):
	list_display = [c.name for c in Post._meta.get_fields()]
	#list_display = ['id', 'empresa','fecha_inicio','fecha_fin','observaciones','categoria']
	search_fields = ('id','titulo')
	list_filter   = ('id','titulo')
admin.site.register(Post, PostAdmin)