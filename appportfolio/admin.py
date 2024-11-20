# -*- coding: utf-8 -*-from __future__ import unicode_literalsfrom django.contrib import adminfrom appportfolio.models import *from django.contrib.auth.models import User admin.site.site_header = "Sitio web Salmantino"  #este es el títuloadmin.site.site_title = "Portal del Portfolio"admin.site.index_title = "Bienvenidos al portal de Administración"class HabilidadAdmin(admin.ModelAdmin):	list_display = [ha.name for ha in Habilidad._meta.get_fields()]	search_fields = ('id','habilidad','comentario') #siempre tienen que ser una tupla	list_filter   = ('id','habilidad','comentario') #siempre tienen que ser una tuplaadmin.site.register(Habilidad, HabilidadAdmin)class PersonalAdmin(admin.ModelAdmin):	list_display = [co.name for co in Personal._meta.get_fields()]	search_fields = ('id','nombre','apellido1','apellido2','edad') #siempre tienen que ser una tupla	list_filter   = ('id','nombre') #siempre tienen que ser una tuplaadmin.site.register(Personal, PersonalAdmin)class CategoriaAdmin(admin.ModelAdmin):	list_display = [co.name for co in Categoria._meta.get_fields()]	search_fields = ('id','nombre_categoria') #siempre tienen que ser una tupla	list_filter   = ('id','nombre_categoria') #siempre tienen que ser una tuplaadmin.site.register(Categoria, CategoriaAdmin)class EstudioAdmin(admin.ModelAdmin):	list_display = ['id','titulacion','fechaInicio','fechaFin','notaMedia','lugarEstudio','nombreLugar','ciudad','presencial','observaciones']	search_fields = ('id','titulacion','fechaInicio','fechaFin','notaMedia','lugarEstudio','nombreLugar','ciudad','presencial','observaciones') #siempre tienen que ser una tupla	list_filter   = ('id','titulacion','fechaInicio','fechaFin','notaMedia','lugarEstudio','nombreLugar','ciudad','presencial','observaciones') #siempre tienen que ser una tuplaadmin.site.register(Estudio, EstudioAdmin)class ExperienciaAdmin(admin.ModelAdmin):	list_display = [ex.name for ex in Experiencia._meta.get_fields()]	search_fields = ('id','empresa','fecha_inicio','fecha_fin','observaciones','categoria') #siempre tienen que ser una tupla	list_filter   = ('id','empresa','fecha_inicio','fecha_fin','observaciones','categoria') #siempre tienen que ser una tuplaadmin.site.register(Experiencia, ExperienciaAdmin)class ImagenAdmin(admin.ModelAdmin):	list_display = [im.name for im in Imagen._meta.get_fields() if hasattr(im, 'verbose_name')]	search_fields = ('id','imagen') #siempre tienen que ser una tupla	list_filter   = ('id','imagen') #siempre tienen que ser una tuplaadmin.site.register(Imagen, ImagenAdmin)class EntrevistadorAdmin(admin.ModelAdmin):	list_display = [en.name for en in Entrevistador._meta.get_fields() if hasattr(en, 'verbose_name')]	search_fields = ('id','empresa','fecha_entrevista','conectado','seleccionado','user') #siempre tienen que ser una tupla	list_filter   = ('id','empresa','fecha_entrevista','conectado','seleccionado','user') #siempre tienen que ser una tuplaadmin.site.register(Entrevistador, EntrevistadorAdmin)class VideoAdmin(admin.ModelAdmin):	list_display = [vi.name for vi in Video._meta.get_fields() if hasattr(vi, 'verbose_name')]	search_fields = ('id','video') #siempre tienen que ser una tupla	list_filter   = ('id','video') #siempre tienen que ser una tuplaadmin.site.register(Video, VideoAdmin)class CurriculumAdmin(admin.ModelAdmin):	list_display = [cu.name for cu in Curriculum._meta.get_fields() if hasattr(cu, 'verbose_name')]	search_fields = ('id','nombre','apellido1','apellido2','email','telefono') #siempre tienen que ser una tupla	list_filter   = ('id','nombre','apellido1','apellido2','email','telefono') #siempre tienen que ser una tuplaadmin.site.register(Curriculum, CurriculumAdmin)class DetalleCurriculumEstudioAdmin(admin.ModelAdmin):	list_display = [dces.name for dces in DetalleCurriculumEstudio._meta.get_fields() if hasattr(dces, 'verbose_name')]	search_fields = ('id','estudio','curriculum') #siempre tienen que ser una tupla	list_filter   = ('id','estudio','curriculum') #siempre tienen que ser una tuplaadmin.site.register(DetalleCurriculumEstudio, DetalleCurriculumEstudioAdmin)class DetalleCurriculumExperienciaAdmin(admin.ModelAdmin):	list_display = [dcex.name for dcex in DetalleCurriculumExperiencia._meta.get_fields() if hasattr(dcex, 'verbose_name')]	search_fields = ('id','experiencia','curriculum') #siempre tienen que ser una tupla	list_filter   = ('id','experiencia','curriculum') #siempre tienen que ser una tuplaadmin.site.register(DetalleCurriculumExperiencia, DetalleCurriculumExperienciaAdmin)class NoticiaAdmin(admin.ModelAdmin):	list_display = [no.name for no in Noticia._meta.get_fields() if hasattr(no, 'verbose_name')]	search_fields = ('id','titulo') #siempre tienen que ser una tupla	list_filter   = ('id','titulo') #siempre tienen que ser una tuplaadmin.site.register(Noticia, NoticiaAdmin)@admin.register(Valoracion)class ValoracionAdmin(admin.ModelAdmin):	list_display = ('id', 'votos_entrevista', 'votos_empresa', 'media_aspectos', 'timestamp')	readonly_fields = ('media_aspectos',)	def save_model(self, request, obj, form, change):		# Calcula automáticamente la media		if obj.votos_entrevista and obj.votos_empresa:			obj.media_aspectos = (obj.votos_entrevista + obj.votos_empresa)		super().save_model(request, obj, form, change)