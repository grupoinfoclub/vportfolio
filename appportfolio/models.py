# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

################################################
# 1 - Categoria
################################################
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField('Puesto de Trabajo',max_length=30, null=True, blank=True)
    prueba= models.CharField('Prueba',max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria' #puede ser otro nombre
        verbose_name_plural = 'Categorias'
        ordering = ['nombre_categoria']

    def __str__(self):
        return "%s,%s,%s" % (self.id,self.nombre_categoria,self.prueba)

################################################
# 2 - Experiencias
################################################
class Experiencia(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField('Empresa',max_length=50,null=True, blank=True)
    fecha_inicio= models.DateField('Fecha de Inicio',null=True, blank=True)
    fecha_fin = models.DateField('Fecha de Finalización', null=True, blank=True)
    observaciones = models.CharField('Funciones', max_length=50, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, related_name='expe_categoria', null=True, blank=True, on_delete=models.PROTECT)
    logro_destacado = models.TextField('Logro Destacado', null=True, blank=True)
    sueldo = models.DecimalField('Sueldo', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Experiencia' #puede ser otro nombre
        verbose_name_plural = 'Experiencias'
        ordering = ['empresa']

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s,%s,%s" % (self.id,self.empresa,self.fecha_inicio,
        self.fecha_fin,self.observaciones,self.categoria,self.logro_destacado,self.sueldo)

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField('Título del Proyecto', max_length=50)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    fecha = models.DateField('Fecha del Proyecto', null=True, blank=True)
    tecnologias = models.CharField('Tecnologías usadas', max_length=150, null=True, blank=True)
    precio = models.DecimalField('Precio del Proyecto', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['titulo']

    def __str__(self):
        return f"{self.id} - {self.titulo}"

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField('titulo',max_length=200, null=True, blank=True)
    contenido = models.TextField('contenido', null=True, blank=True)
    fecha = models.DateField('Fecha',auto_now_add=True, null=True, blank=True)
    imagen = models.ImageField('Imagen',upload_to="posts/", null=True, blank=True)    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['titulo']

    def __str__(self):
        return f"{self.id} - {self.titulo} {self.contenido} {self.fecha}"
    