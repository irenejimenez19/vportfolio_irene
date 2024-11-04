# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

################################################
# TABLA 1 - Habilidades                        
################################################

#                herencia
#               paquete.clase
class Habilidad(models.Model): 
    id = models.AutoField(primary_key=True)
    #                   varchar        etiqueta             para permitir nulos, para permitir dejarlo en blanco
    habilidad = models.CharField("Nombre de habilidad",max_length=25, null=True, blank=True) #para que no explote la base de datos
    #                  int
    nivel= models.IntegerField("Nivel", null=True, blank=True) # 1 al 10
    comentario = models.CharField("Comentario: ", max_length=255, null=True, blank=True)
	
    class Meta:
        verbose_name = "Habilidad"  #puede ser otro nombre
        verbose_name_plural = "Habilidades"
        ordering = ['habilidad']
		
	#   toString
    #           this
    def __str__(self):
        return '%s,%s,%s' % (self.habilidad, self.nivel, self.comentario)
        
################################################
# TABLA 2 - Personal                        
################################################

class Personal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre",max_length=25, null=True, blank=True)
    apellido1 = models.CharField("Primer apellido",max_length=25, null=True, blank=True)
    apellido2 = models.CharField("Segundo apellido",max_length=25, null=True, blank=True)
    edad = models.IntegerField("Edad", null=True, blank=True)

    usuario = models.ForeignKey(User, related_name='datos_usuario', null=True, blank=True, on_delete= models.PROTECT)
    #                                                                                      Proteger para que no haya borrado en cascada
    
    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personales"
        ordering = ['nombre']
        
    def __str__(self):
        return '%s,%s,%s,%s,%s,%s' % (self.id, self.nombre, self.apellido1, self.apellido2, self.edad, self.usuario)


################################################
# TABLA 3 - Categoría
################################################

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField("Puesto de trabajo", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nombre_categoria']

    def __str__(self):
        return '%s,%s' % (self.id, self.nombre_categoria)

################################################
# TABLA 4 - Estudios
################################################

class Estudio(models.Model):
    id = models.AutoField(primary_key=True)
    titulacion = models.CharField("Nombre de titulación: ", max_length=50, null=True, blank=True)
    fechaInicio = models.DateField("Fecha de inicio: ", null = True, blank = True)
    fechaFin = models.DateField("Fecha de fin: ", null=True, blank=True)
    notaMedia = models.IntegerField("Nota media: ", null=True, blank=True)
    lugarEstudio = models.CharField("Lugar de estudio: ", max_length=50, null=True, blank=True)
    nombreLugar = models.CharField("Nombre de lugar: ", max_length=50, null=True, blank=True)
    ciudad = models.CharField("Ciudad: ", max_length=50, null=True, blank=True)
    presencial = models.BooleanField("Modalidad presencial: ", max_length=50, null=True, blank=True)
    observaciones = models.CharField("Observaciones: ", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Estudio"
        verbose_name_plural = "Estudios"
        ordering = ['-id']

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (self.id, self.titulacion, self.fechaInicio, self.fechaFin, self.notaMedia, self.lugarEstudio, self.nombreLugar, self.ciudad, self.presencial, self.observaciones)

################################################
# TABLA 5 - Experiencias
################################################

class Experiencia(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField('Empresa',max_length=50,null=True, blank=True)
    fecha_inicio= models.DateField('Fecha de Inicio',null=True, blank=True)
    fecha_fin = models.DateField('Fecha de Finalización', null=True, blank=True)
    observaciones = models.CharField('Funciones', max_length=50, null=True, blank=True)
    categoria = models.CharField('Categoría', max_length=50,null=True, blank=True)

    class Meta:
        verbose_name = 'Experiencia' #puede ser otro nombre
        verbose_name_plural = 'Experiencias'
        ordering = ['empresa']

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s' % (self.id,self.empresa,self.fecha_inicio,self.fecha_fin,self.observaciones,self.categoria)

################################################
# TABLA 6 - Imágenes
################################################

class Imagen(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to="media/")
    comentario = models.CharField("Comentario", max_length=100, null=True, blank=True)

    #estudio = models.ForeignKey(Estudio, related_name='estudio_imagen', null=True, blank=True, on_delete=models.PROTECT)
    #                                                                                          Proteger para que no haya borrado en cascada

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"
        ordering = ['id']

    def __str__(self):
        return '%s,%s,%s' % (self.id, self.imagen, self.comentario)

################################################
# TABLA 7 - Entrevistadores
################################################

class Entrevistador(models.Model):
    id = models.AutoField(primary_key=True)
    avatar = models.ImageField("Avatar", null=True, blank=True, upload_to="media/")
    empresa = models.CharField("Empresa", max_length=30, null=True, blank=True)
    fecha_entrevista = models.DateField("Fecha entrevista", null=True, blank=True)
    conectado = models.BooleanField("Conectado", null=True, blank=True)
    seleccionado = models.BooleanField("Seleccionado", null=True, blank=True)

    user = models.ForeignKey(User, related_name='entrevistador_usuario', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Entrevistador' #puede ser otro nombre
        verbose_name_plural = 'Entrevistadores'
        ordering = ['empresa']

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s' % (self.id,self.empresa,self.fecha_entrevista,self.conectado,self.seleccionado,self.user)

################################################
# TABLA 8 - Vídeos
################################################

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField("Video", null=True, blank=True, upload_to="videos/")
    comentario = models.CharField("Comentario", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        ordering = ['id']

    def __str__(self):
        return '%s,%s,%s' % (self.id, self.video, self.comentario)
