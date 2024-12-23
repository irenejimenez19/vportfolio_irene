# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

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

################################################
# TABLA 9 - Curriculum
################################################

class Curriculum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre", max_length=25, null=True, blank=True)
    apellido1 = models.CharField("Primer apellido", max_length=25, null=True, blank=True)
    apellido2 = models.CharField("Segundo apellido", max_length=25, null=True, blank=True)
    email = models.EmailField("Email", max_length=40, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=9, null=True, blank=True)

    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "Curriculums"
        ordering = ['id']

    def __str__(self):
        return '%s,%s,%s,%s,%s,%s' % (self.id, self.nombre, self.apellido1, self.apellido2, self.email, self.telefono)

################################################
# TABLA 10 - Detalle Curriculum Estudio
################################################

class DetalleCurriculumEstudio(models.Model):
    id = models.AutoField(primary_key=True)

    estudio = models.ForeignKey(Estudio, related_name='estudio_detalle', null=True, blank=True, on_delete=models.PROTECT)
    curriculum = models.ForeignKey(Curriculum, related_name='curriculum_detalleEst', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'DetalleCurriculumEstudio' #puede ser otro nombre
        verbose_name_plural = 'DetalleCurriculumEstudios'
        ordering = ['id']

    def __str__(self):
        return '%s,%s,%s' % (self.id, self.estudio, self.curriculum)

################################################
# TABLA 11 - Detalle Curriculum Experiencia
################################################

class DetalleCurriculumExperiencia(models.Model):
    id = models.AutoField(primary_key=True)

    experiencia = models.ForeignKey(Experiencia, related_name='experiencia_detalle', null=True, blank=True, on_delete=models.PROTECT)
    curriculum = models.ForeignKey(Curriculum, related_name='curriculum_detalleExp', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'DetalleCurriculumExperiencia' #puede ser otro nombre
        verbose_name_plural = 'DetalleCurriculumExperiencias'
        ordering = ['id']

    def __str__(self):
        return '%s,%s,%s' % (self.id, self.experiencia, self.curriculum)

################################################
# TABLA 12 - Noticias
################################################

class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField("Título", max_length=200, null=True, blank=True)
    contenido = models.TextField("Contenido", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to="media/")

    def __str__(self):
        return '%s' % (self.titulo)

################################################
# TABLA 13 - Valoraciones
################################################

class Valoracion(models.Model):
    id = models.AutoField(primary_key=True)
    votos_entrevista = models.DecimalField("Votos entrevista", max_digits=3, decimal_places=1, null=True, blank=True)
    votos_empresa = models.DecimalField("Votos empresa", max_digits=3, decimal_places=1, null=True, blank=True)
    media_aspectos = models.DecimalField("Media aspectos", max_digits=3, decimal_places=1, null=True, blank=True)
    entrevista = models.CharField("Descripción Entrevista", max_length=200, null=True, blank=True)
    empresa = models.CharField("Descripción Empresa", max_length=200, null=True, blank=True)
    num_valoraciones = models.IntegerField("Num Valoraciones", null=True, blank=True)
    timestamp = models.DateTimeField("Fecha", default=timezone.now)

    def __str__(self):
        return f"{self.id}, {self.votos_entrevista}, {self.votos_empresa}, {self.entrevista}, {self.empresa}, {self.timestamp}"

################################################
# TABLA 14 - Mensajes
################################################

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
    contenido = models.TextField('Contenido del mensaje')
    fecha_envio = models.DateTimeField(verbose_name='Fecha de envío', auto_now_add=True)
    leido = models.BooleanField(verbose_name='Leído', default=False)

    class Meta:
        ordering = ['fecha_envio']

    def __str__(self):
        return f"De: {self.remitente.username} Para: {self.destinatario.username} - {self.contenido[:30]}"

################################################
# TABLA 15 - Estados
################################################

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.TextField('Estado', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Estado'  # puede ser otro nombre
        verbose_name_plural = 'Estados'
        ordering = ['id']

    def __str__(self):
        return f"{self.id}, {self.estado}"

################################################
# TABLA 16 - Tareas
################################################

class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    tarea = models.TextField('Tarea', max_length=50, null=True, blank=True)
    fecha = models.DateField(verbose_name='Fecha', null=True, blank=True)
    estado = models.ForeignKey(Estado, related_name='estado_tarea', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Tarea'  # puede ser otro nombre
        verbose_name_plural = 'Tareas'
        ordering = ['fecha']

    def __str__(self):
        return f"{self.id}, {self.tarea}, {self.fecha}, {self.estado}"

################################################
# TABLA 17 - Proyectos
################################################

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField("Título proyecto", max_length=50, null=True, blank=True)
    lenguaje = models.CharField("Lenguaje principal", max_length=30, null=True, blank=True)
    tecnologias = models.CharField("Tecnologías", max_length=100, null=True, blank=True)
    observaciones = models.CharField('Observaciones', max_length=100, null=True, blank=True)
    fecha_publicacion = models.DateTimeField("Fecha publicación", null=True, blank=True)

    class Meta:
        verbose_name = 'Proyecto'  # puede ser otro nombre
        verbose_name_plural = 'Proyectos'
        ordering = ['id']

    def __str__(self):
        return f"{self.id}, Llamado: {self.titulo}, Usando principalmente: {self.lenguaje} y {self.tecnologias}, Observaciones: {self.observaciones}, Fecha: {self.fecha_publicacion}"
