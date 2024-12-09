# -*- coding: utf-8 -*-

from __future__ import unicode_literals

#para trabajar con el módulo de administración
from django.contrib import admin
from django.urls import path, include, re_path
from appportfolio import views
from appportfolio.views import *

# Ficheros estáticos durante el desarrollo
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# Ficheros estáticos durante el servidor
from django.views.static import serve

urlpatterns = [
    #el que dirige a admin
    re_path('admin/', admin.site.urls),
    #la raíz
    #significa que cuando dé enter lleva directamente a home, mediante la función home que está es views
    re_path(r'^$', views.home,name = 'home'),
    re_path('habilidades/', views.habilidades,name = 'habilidades'),
    re_path('sobremi/', views.sobremi,name = 'sobremi'),
    re_path('categorias/', views.categorias,name = 'categorias'),
    re_path('estudios/', views.estudios,name = 'estudios'),
    re_path('experiencias/', views.experiencias,name = 'experiencias'),
    re_path(r'^(?P<id>\d+)/ver_experiencia$', views.ver_experiencia,name='ver_experiencia'),
    path('eliminarExperiencia/<int:pk>/', views.eliminarExperiencia, name='eliminarExperiencia'),
    re_path(r'^(?P<id>\d+)/ver_habilidad$', views.ver_habilidad,name='ver_habilidad'),
    path('eliminarHabilidad/<int:pk>/', views.eliminarHabilidad, name='eliminarHabilidad'),
    path('crear_habilidad/', views.crear_habilidad, name='crear_habilidad'),
    path('editar_habilidad/<int:habi_id>/', views.editar_habilidad, name='editar_habilidad'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('entrevistadores/', views.entrevistadores, name='entrevistadores'),
    path('subir_imagenes/', views.subir_imagenes, name='subir_imagenes'),
    path('subir_videos/', views.subir_videos, name='subir_videos'),
    path('imagen/editar/<int:imagen_id>/', views.editar_imagen, name='editar_imagen'),
    path('imagen/eliminar/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('video/editar/<int:video_id>/', views.editar_video, name='editar_video'),
    path('video/eliminar/<int:video_id>/', views.eliminar_video, name='eliminar_video'),
    path('contacto/', views.contacto, name='contacto'),
    path('generar_pdf/<int:entre>/', views.generar_pdf, name='generar_pdf'),
    path('listar_entrevistadores/', views.listar_entrevistadores, name='listar_entrevistadores'),
    path('generar_curriculum/', views.generar_curriculum, name='generar_curriculum'),
    path('ver_curriculum/<int:id>/', views.ver_curriculum, name='ver_curriculum'),
    path('generar_pdfCV/<int:id>/', views.generar_pdfCV, name='generar_pdfCV'),
    path('lista_noticias/', views.lista_noticias, name='lista_noticias'),
    path('crear_noticia/', views.crear_noticia, name='crear_noticia'),
    path('listar_valoraciones/', views.listar_valoraciones, name='listar_valoraciones'),
    path('actualizar_valoracion/<int:pk>/edit/', views.actualizar_valoracion, name='actualizar_valoracion'),
    path('añadir_valoracion/add/', views.añadir_valoracion, name='añadir_valoracion'),
    path('chat_view/<int:entrevistador_id>/', views.chat_view, name='chat_view'),
    path('chat/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('seleccionar_entrevistadores/', views.seleccionar_entrevistadores, name='seleccionar_entrevistadores'),
    path('listar_tareas/', views.listar_tareas, name='listar_tareas'),
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('listar_proyectos', views.listar_proyectos, name='listar_proyectos'),
    path('crear_proyecto/', views.crear_proyecto, name='crear_proyecto'),
    path('editar_proyecto/<int:proyecto_id>/', views.editar_proyecto, name='editar_proyecto'),
    path('eliminar_proyecto/<int:id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    })
]