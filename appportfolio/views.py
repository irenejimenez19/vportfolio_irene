# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from appportfolio.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#paginación

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

from django.views.decorators.csrf import csrf_protect

from django.contrib.auth.models import User

from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from django.http import JsonResponse

from datetime import datetime

import urllib

# Create your views here.

'''
#crear un método def, el nombre y el parámetro pasado
#es función porque no está dentro de una clase
def home(request):
    cadena = '<center><h1><b>Hola Mundo</b></h1></center>'
    return HttpResponse(cadena)
'''

DEBUG = True

#########################
#       1. HOME
#########################

def home(request):
    # para que coja el debug tienes que poner global para que coja la de afuera, sino sale none porque no encuentra la variable
    global DEBUG
    print("Hola estoy en home " + str(DEBUG))
    nombreProyecto = 'PORTFOLIO'
    fechaCreacion = '23/09/2024'

    actual = request.user
    idusuario = 0
    idusuario = actual.id
    request.session['idusuario'] = idusuario
    numconectados = 0
    dato = ""
    # ip externa o publica
    lista = "0123456789."
    ip = ""
    try:
        dato = urllib.request.urlopen('https://www.wikipedia.org').headers['X-Client-IP']
        #dato = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        print("IP PUBLICA =" + str(dato))
    except:
        print("Error en la librería de la IP")
        dato = ""
    finally:
        print("USUARIO ACTUAL...[" + str(actual) + "]")
    for x in str(dato):
        if x in lista:
            ip += x
    if str(actual) == "AnonymousUser":
        request.session['tipousuario'] = 'anonimo'
        print('IP ANÓNIMO...' + str(ip))
    usuario = 'prueba'

    # estructura clave:valor se llama diccionario
    context = {'nombreProyecto':nombreProyecto,'fechaCreacion':fechaCreacion,'ip':ip}
    # el context es para pasar del back al front las variables (la información)
    return render(request, 'home.html', context=context)
    
#########################
#      2. SOBRE MI
#########################

def sobremi(request):
    print("Hola estoy en sobre mí")
    nombre = 'Irene'
    edad = 18
    telefono = '612345678'
    cargo = 'CEO'
    #select * from Categoria
    listaCategorias = Categoria.objects.all().order_by('-nombre_categoria')
    for r in listaCategorias:
        print(str(r.nombre_categoria))
    # estructura clave:valor se llama diccionario
    context = {'nombre':nombre,'edad':edad,'telefono':telefono,'cargo':cargo,'listaCategorias':listaCategorias}
    # el context es para pasar del back al front las variables (la información)
    return render(request, 'sobremi.html', context=context)
    
#########################
#     3. HABILIDADES
#########################

def habilidades(request):
    print('Hola estoy en habilidades')
    # select * from Habilidad order by habilidad desc| Habilidad: es la tabla, se coge el mismo nombre que en el modelo
    #habilidades: es un objeto de tipo queryset
    habilidades = Habilidad.objects.all().order_by('-habilidad')
    page = request.GET.get('page')
    paginator = Paginator(habilidades, 3)  # 2 registros por página
    if page == None:
        # coge la última por defecto
        print(" page recibe fuera de get o post NONE=" + str(page))
        # coge el nº de páginas por defecto (en nuestro caso 3)
        page = paginator.num_pages
        # variable inventada global (sirve para todo el proyecto), sin tipo
        request.session["pagina"] = page
    else:
        # coge la página en la que estés
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':  # si estoy entrando en la página
        pagina = request.session["pagina"]  # recupera la página en la que estábamos en la última sesión
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    # condición muy importante, para saber si existe la variable en la sesión
    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        habilidades = paginator.get_page(page)  # intenta coger la página que tenga
    except PageNotAnInteger:
        habilidades = paginator.page(1)  # si no tiene número que coja la 1
    except EmptyPage:
        habilidades = paginator.page(paginator.num_pages)
    context = {'habilidades':habilidades}
    return render(request, 'habilidades.html', context=context)

#########################
#   3.1. VER HABILIDAD
#########################

def ver_habilidad(request,id):
    habi_id=id
    habilidad = Habilidad.objects.get(id=habi_id)
    context = {'habilidad': habilidad}
    return render(request, 'ver_habilidad.html',context=context)

#########################
# 3.2. ELIMI HABILIDAD
#########################

def eliminarHabilidad(request,pk):
    print("ELIMINAR")
    habi_id=pk
    habilidad = Habilidad.objects.get(id=habi_id)
    if request.method == 'POST': #post: darle al botón | si pulsa el botón elimina la habilidad
        habilidad.delete()
        return redirect('habilidades'
                        '')
    return render(request, 'eliminar_habilidad.html', {'habilidad': habilidad})

#########################
# 3.3. CREAR HABILIDAD
#########################

def crear_habilidad(request):
    if request.method == 'POST':
        # Para coger lo que escribas en el cuadrito de texto
#   nombre variable        nombre cajita de texto
        habilidad = request.POST.get('habilidad')
        nivel = request.POST.get('nivel')
        comentario = request.POST.get('comentario')

        # Crear el objeto persona
        #persona = Personal(nombre=nombre, ap1=ap1, ap2=ap2, edad=edad)
        habilidad1 = Habilidad()
        habilidad1.habilidad = habilidad
        habilidad1.nivel = nivel
        habilidad1.comentario = comentario
        # El que se encarga de hacer el insertInto
        habilidad1.save()
        return redirect('habilidades')  # Redirige

    return render(request, 'crear_habilidad.html')

#########################
# 3.3. EDITAR HABILIDAD
#########################

def editar_habilidad (request, habi_id):
    habilidad1 = Habilidad.objects.get(id=habi_id)
    if request.method == 'POST':
        habilidad = request.POST.get('habilidad')
        nivel = request.POST.get('nivel')
        comentario = request.POST.get('comentario')

        #habilidad1 = Habilidad()
        habilidad1.habilidad = habilidad
        habilidad1.nivel = nivel
        habilidad1.comentario = comentario
        # El que se encarga de hacer el insertInto
        habilidad1.save()
        return redirect('habilidades')  # Redirige

    return render(request, 'editar_habilidad.html', {'habilidad':habilidad1})

#########################
#     4. CATEGORÍAS
#########################

def categorias(request):
    #obtener objeto queryset del módelo de categorías
    lista_categorias = Categoria.objects.all()  # select * from Categoria;
    page = request.GET.get('page')
    paginator = Paginator(lista_categorias, 5)  # 2 registros por página
    if page == None:
        # coge la última por defecto
        print(" page recibe fuera de get o post NONE=" + str(page))
        # coge el nº de páginas por defecto (en nuestro caso 3)
        page = paginator.num_pages
        # variable inventada global (sirve para todo el proyecto), sin tipo
        request.session["pagina"] = page
    else:
        #coge la página en la que estés
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET': # si estoy entrando en la página
        pagina = request.session["pagina"] # recupera la página en la que estábamos en la última sesión
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    # condición muy importante, para saber si existe la variable en la sesión
    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_categorias = paginator.get_page(page) # intenta coger la página que tenga
    except PageNotAnInteger:
        lista_categorias = paginator.page(1) # si no tiene número que coja la 1
    except EmptyPage:
        lista_categorias = paginator.page(paginator.num_pages)

    context = {'lista_categorias': lista_categorias}
    return render(request, 'categorias.html', context=context)

#########################
#       5. ESTUDIOS
#########################

def estudios(request):
    #obtener objeto queryset del módelo de categorías
    lista_estudios = Estudio.objects.all().order_by('-id')  # select * from Categoria;
    numregistros = Estudio.objects.all().count()
    page = request.GET.get('page')
    paginator = Paginator(lista_estudios, 2)  # 2 registros por página
    if page == None:
        # coge la última por defecto
        print(" page recibe fuera de get o post NONE=" + str(page))
        # coge el nº de páginas por defecto (en nuestro caso 3)
        page = paginator.num_pages
        # variable inventada global (sirve para todo el proyecto), sin tipo
        request.session["pagina"] = page
    else:
        #coge la página en la que estés
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET': # si estoy entrando en la página
        pagina = request.session["pagina"] # recupera la página en la que estábamos en la última sesión
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    # condición muy importante, para saber si existe la variable en la sesión
    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_estudios = paginator.get_page(page) # intenta coger la página que tenga
    except PageNotAnInteger:
        lista_estudios = paginator.page(1) # si no tiene número que coja la 1
    except EmptyPage:
        lista_estudios = paginator.page(paginator.num_pages)

    context = {'lista_estudios': lista_estudios, 'numregistros': numregistros}
    return render(request, 'estudios.html', context=context)

#########################
#     6. EXPERIENCIAS
#########################

def experiencias(request):
    #obtener objeto queryset del módelo de categorías
    lista_experiencias = Experiencia.objects.all().order_by('id')  # select * from Categoria;
    page = request.GET.get('page')
    paginator = Paginator(lista_experiencias, 2)  # 2 registros por página
    if page == None:
        # coge la última por defecto
        print(" page recibe fuera de get o post NONE=" + str(page))
        # coge el nº de páginas por defecto (en nuestro caso 3)
        page = paginator.num_pages
        # variable inventada global (sirve para todo el proyecto), sin tipo
        request.session["pagina"] = page
    else:
        #coge la página en la que estés
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET': # si estoy entrando en la página
        pagina = request.session["pagina"] # recupera la página en la que estábamos en la última sesión
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    # condición muy importante, para saber si existe la variable en la sesión
    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_experiencias = paginator.get_page(page) # intenta coger la página que tenga
    except PageNotAnInteger:
        lista_experiencias = paginator.page(1) # si no tiene número que coja la 1
    except EmptyPage:
        lista_experiencias = paginator.page(paginator.num_pages)

    context = {'lista_experiencias': lista_experiencias}
    return render(request, 'experiencias.html', context=context)

#########################
#   6.1. VER EXPERIENCIA
#########################

def ver_experiencia(request,id):
    expe_id=id
    experiencia = Experiencia.objects.get(id=expe_id)
    context = {'experiencia': experiencia}
    return render(request, 'ver_experiencia.html',context=context)

#########################
# 6.2. ELIMI EXPERIENCIA
#########################

def eliminarExperiencia(request,pk):
    print("ELIMINAR")
    expe_id=pk
    experiencia = Experiencia.objects.get(id=expe_id)
    if request.method == 'POST': #post: darle al botón | si pulsa el botón elimina la experiencia
        experiencia.delete()
        return redirect('experiencias')
    return render(request, 'eliminar_experiencia.html', {'experiencia': experiencia})

#########################
#       7. LOGIN
#########################

def login_view(request):
    print("Login_view")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) # Método de protección
        if user is not None:
            login(request, user)

            actual = request.user  # usuario actual
            idusuario = 0
            idusuario = actual.id
            request.session["idusuario"] = idusuario
            print("idusuario=" + str(idusuario))
            entrevistador = Entrevistador.objects.get(user=idusuario)
            idEntrevistador = entrevistador.id
            print("idEntrevistador=" + str(idEntrevistador))
            fotoperfil = settings.MEDIA_URL + str(entrevistador.avatar) if entrevistador.avatar else settings.MEDIA_URL + "niña.png" # niña.png: imagen por defecto por si no ponen avatar
            print("avatar=" + str(fotoperfil))
            context = {'fotoperfil': fotoperfil}
            return render(request, 'home.html', context=context)
            # return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

#########################
#      8. REGISTRO
#########################

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login')  # Redirige al login una vez registrado
    return render(request, 'register.html')

#########################
#    9. CERRAR SESIÓN
#########################

def cerrar(request):
    username = request.user.username
    password = request.user.password
    idusuario = request.user.id
    print("logout................" + username + "clave=" + str(password) + "id=" + str(idusuario))
    user = authenticate(request, username=username, password=password)
    # desconectamos al usuario
    logout(request)
    return redirect('/')

#########################
#   10. ENTREVISTADORES
#########################

def entrevistadores(request):
    print('Hola estoy en entrevistadores')
    entrevistadores = Entrevistador.objects.all().order_by('empresa')
    page = request.GET.get('page')
    paginator = Paginator(entrevistadores, 2)  # 2 registros por página
    if page == None:
        # coge la última por defecto
        print(" page recibe fuera de get o post NONE=" + str(page))
        # coge el nº de páginas por defecto (en nuestro caso 3)
        page = paginator.num_pages
        # variable inventada global (sirve para todo el proyecto), sin tipo
        request.session["pagina"] = page
    else:
        # coge la página en la que estés
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':  # si estoy entrando en la página
        pagina = request.session["pagina"]  # recupera la página en la que estábamos en la última sesión
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    # condición muy importante, para saber si existe la variable en la sesión
    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        entrevistadores = paginator.get_page(page)  # intenta coger la página que tenga
    except PageNotAnInteger:
        entrevistadores = paginator.page(1)  # si no tiene número que coja la 1
    except EmptyPage:
        entrevistadores = paginator.page(paginator.num_pages)
    context = {'entrevistadores':entrevistadores}
    print("Hola")
    return render(request, 'entrevistadores.html', context=context)

#########################
#   11. SUBIR IMÁGENES
#########################

def subir_imagenes(request):
    #idUsuario = request.session['idusuario'] // Cazar quien es el usuario activo
    if request.method == 'POST':
        imagenes = request.FILES.getlist('imagenes') # 'imagenes': nombre del array de file, creado en el html
        comentario = request.POST.get('comentario')  # Obtén el comentario del formulario

        for imagen in imagenes:
            if imagen.name.endswith(('.png','.jpg','.jpeg','.gif','.jfif')):
                img=Imagen(imagen=imagen, comentario=comentario) # Crea el objeto
                #img.imagen = imagen
                img.save()
        return redirect('subir_imagenes')

    imagenes = Imagen.objects.all()
    return render(request, 'subir_imagenes.html', {'imagenes':imagenes})

#########################
#  11.1 ELIMI IMAGEN
#########################

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    if request.method == 'POST':
        imagen.delete() # Borra
        return redirect('subir_imagenes')  # Redirige a la galería de imágenes
    return redirect('subir_imagenes')  # Redirige a la galería de imágenes

#########################
#  11.2 EDITAR IMAGEN
#########################

def editar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)

    if request.method == 'POST':
        # Solo actualiza la imagen si hay una nueva imagen cargada
        if request.FILES.get('nueva_imagen'):
            imagen.imagen = request.FILES['nueva_imagen']

        # Actualiza el comentario, aunque no se cargue una nueva imagen
        comentario = request.POST.get('comentario')
        if comentario is not None:
            imagen.comentario = comentario

        imagen.save()  # Guarda los cambios
        return redirect('subir_imagenes')  # Redirige a la galería de imágenes

    return redirect('subir_imagenes')


#########################
#   12. SUBIR VÍDEOS
#########################

def subir_videos(request):
    if request.method == 'POST' and request.FILES['videos']:
        videos = request.FILES.getlist('videos')
        comentario = request.POST.get('comentario')  # Obtén el comentario del formulario

        for video in videos:
            if video.name.endswith(('.mp3','.mp4','.mov','.avi','.mkv')):
                v=Video(video=video, comentario=comentario)
                #v.video = video
                v.save()
        return redirect('subir_videos')

    videos = Video.objects.all()
    return render(request, 'subir_videos.html', {'videos':videos})

#########################
#  12.1 ELIMI VIDEO
#########################

def eliminar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        video.delete() # Borra
        return redirect('subir_videos')  # Redirige a la galería de vídeos
    return redirect('subir_videos')  # Redirige a la galería de vídeos

#########################
#  12.2 EDITAR VIDEO
#########################

def editar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        # Solo actualiza el video si se ha subido un nuevo archivo
        if request.FILES.get('nuevo_video'):
            video.video = request.FILES['nuevo_video']

        # Actualiza el comentario sin importar si se subió un nuevo video
        comentario = request.POST.get('comentario')
        if comentario is not None:
            video.comentario = comentario

        video.save()  # Guarda los cambios
        return redirect('subir_videos')  # Redirige a la galería de videos

    return redirect('subir_videos')

#########################
#      13. CONTACTO
#########################

def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("mensaje")

        context = {'nombre': nombre, 'email': email, 'asunto': asunto, 'mensaje': mensaje}
        template = render_to_string('email_template.html', context=context)

        email = EmailMessage(asunto, template, settings.EMAIL_HOST_USER, ['ireeneejimenezz@gmail.com'])

        email.fail_silenty = False  # Que no marque error en gmail
        email.send()

        messages.success(request, 'Se ha enviado tu email')
        return redirect('home')
    return render(request, 'correo.html')

#########################
#   14. LISTAR ENTREVI.
#########################

def listar_entrevistadores(request):
    entrevistadores = Entrevistador.objects.all()
    return render(request, 'listar_entrevistadores.html', {'entrevistadores':entrevistadores})

#########################
#     15. GENERAR PDF
#########################

def generar_pdf(request, entre):
    entrevistador = Entrevistador.objects.get(id=entre) # select * from Entrevistador where id=xx

    # Crear una respuesta HTTP con contenido tipo PDF
    response = HttpResponse(content_type='application/pdf') # Para indicarle que es una página de formato PDF
    # f': para que pueda coger lo que hay dentro de las llaves que hay entre las comillas
    #                                 para mezclar variables con parte fija
    response['Content-Disposition'] = f'attachment; filename="entrevistador_{entrevistador.id}.pdf"' # Es el nombre que se le va a poner al PDF

    # Crear el objeto canvas de ReportLab
    p = canvas.Canvas(response, pagesize=letter) # El lienzo, lo que es el cuadrado del archivo PDF

    # Configuración del título
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(300, 770, "Reporte de Entrevistador") # Para centrar el título

    # Volver al tamaño de fuente normal
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)

    # Datos del entrevistador
    p.drawString(100, 720, f"ID: {entrevistador.id}")
    p.drawString(100, 700, f"Empresa: {entrevistador.empresa or 'N/A'}")
    p.drawString(100, 680, f"Fecha de Entrevista: {entrevistador.fecha_entrevista or 'N/A'}")
    p.drawString(100, 660, f"Conectado: {'Sí' if entrevistador.conectado else 'No'}")
    p.drawString(100, 640, f"Seleccionado: {'Sí' if entrevistador.seleccionado else 'No'}")
    p.drawString(100, 620, f"Usuario: {entrevistador.user.username if entrevistador.user else 'N/A'}")

    # Añadir avatar si existe
    if entrevistador.avatar:
        avatar_path = entrevistador.avatar.path
        p.drawImage(avatar_path, 100, 500, width=100, height=100)

    # Guardar el PDF
    p.showPage()
    p.save()

    return response

#########################
#   16. GENERAR CV
#########################

def generar_curriculum(request):
    personal = Personal.objects.get(id=1)

    if request.method == "POST":
        c = Curriculum()

        c.nombre = personal.nombre
        c.apellido1 = personal.apellido1
        c.apellido2 = personal.apellido2
        c.email = request.POST.get("email")
        c.telefono = request.POST.get("telefono")

        c.save()

        return redirect('ver_curriculum', id=personal.id)

    return render(request, 'generar_curriculum.html')

#########################
#   17. VER CV
#########################

def ver_curriculum(request, id):
    curriculum = get_object_or_404(Curriculum, id=id)
    estudios = DetalleCurriculumEstudio.objects.filter(curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(curriculum=curriculum)
    context = {'curriculum':curriculum,'estudios':estudios,'experiencias':experiencias}
    return render(request, 'ver_curriculum.html', context)

#########################
#   18. GENERAR PDF CV
#########################

def generar_pdfCV(request, id):
    curriculum = get_object_or_404(Curriculum, id=id)
    estudios = DetalleCurriculumEstudio.objects.filter(curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(curriculum=curriculum)

    # Crear la respuesta HttpResponse con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="curriculum_{curriculum.nombre}_{curriculum.apellido1}.pdf"'

    # Crear un objeto canvas de ReportLab para generar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Cargar imagen de avatar
    try:
        avatar_path = os.path.join(settings.MEDIA_ROOT, "media/niña.png")
        c.drawImage(avatar_path, width - 150, height - 150, width=100, height=100)
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
        pass  # Si no se encuentra la imagen, el PDF se generará sin ella

    # Título del curriculum en color
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#4BB8E8"))
    c.drawString(100, height - 100, f"Curriculum de {curriculum.nombre} {curriculum.apellido1}")

    # Información de contacto
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#30639F"))

    # Ajustar la posición vertical
    y_position = height - 130
    c.drawString(100, y_position, f"Nombre: {curriculum.nombre}")
    y_position -= 20  # Mover hacia abajo para la siguiente línea
    c.drawString(100, y_position, f"Primer apellido: {curriculum.apellido1}")
    y_position -= 20
    c.drawString(100, y_position, f"Segundo apellido: {curriculum.apellido2}")
    y_position -= 20
    c.drawString(100, y_position, f"Email: {curriculum.email}")
    y_position -= 20
    c.drawString(100, y_position, f"Teléfono: {curriculum.telefono}")

    # Sección de estudios
    y_position = height - 200
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#FFB343"))
    y_position -= 40
    c.drawString(100, y_position, "Estudios:")

    y_position -= 20
    c.setFont("Helvetica", 12)
    for estudio in estudios:
        c.setFillColor(colors.black)
        c.drawString(100, y_position, f"{estudio.estudio.titulacion} con nota media: {estudio.estudio.notaMedia} ({estudio.estudio.fechaInicio} - {estudio.estudio.fechaFin})")
        y_position -= 20

    # Sección de experiencia laboral
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#30639F"))
    c.drawString(100, y_position, "Experiencia laboral:")

    y_position -= 20
    c.setFont("Helvetica", 12)
    for experiencia in experiencias:
        c.setFillColor(colors.black)
        c.drawString(100, y_position, f"{experiencia.experiencia.empresa} como {experiencia.experiencia.categoria} ({experiencia.experiencia.fecha_inicio} - {experiencia.experiencia.fecha_fin})")
        y_position -= 20

    # Finalizar el PDF
    c.showPage()
    c.save()

    return response

#########################
#  19. LISTAR NOTICIAS
#########################

def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha_creacion')

    return render(request, 'lista_noticias.html', {'noticias': noticias})

#########################
#   20. CREAR NOTICIA
#########################

def crear_noticia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if titulo and contenido:
            noticia = Noticia.objects.create(titulo=titulo, contenido=contenido, imagen=imagen)
            return redirect('lista_noticias')
        else:
            return HttpResponse("Error: El título y elc ontenido son obligatorios")

    return render(request, 'crear_noticia.html')
#########################
#   21. LISTAR VALORA.
#########################

def listar_valoraciones(request):
    valoraciones = Valoracion.objects.all()
    return render(request, 'list.html', {'valoraciones': valoraciones})

#########################
#  21. ACTUALIZAR VALORA.
#########################

def actualizar_valoracion(request, pk):
    valoracion = get_object_or_404(Valoracion, pk=pk)
    if request.method == 'POST':
        votos_entrevista = int(request.POST.get('votos_entrevista', valoracion.votos_entrevista))
        votos_empresa= int(request.POST.get('votos_empresa', valoracion.votos_empresa))

        # Actualizar los votos y recalcular la media
        valoracion.votos_entrevista = votos_entrevista
        valoracion.votos_empresa = votos_empresa
        valoracion.media_aspectos = (votos_entrevista + votos_empresa) / 2
        valoracion.save()

        return redirect('listar_valoraciones')

    return render(request, 'update.html', {'valoracion': valoracion})

#########################
#   22. AÑADIR VALORA.
#########################

def añadir_valoracion(request):
    if request.method == 'POST':
        entrevista = request.POST.get('entrevista')
        empresa = request.POST.get('empresa')
        votos_entrevista = int(request.POST.get('votos_entrevista', 0))
        votos_empresa = int(request.POST.get('votos_empresa', 0))

        # Calcular la media de los aspectos
        media_aspectos = (votos_entrevista + votos_empresa) / 2

        # Crear y guardar la nueva valoración
        nueva_valoracion = Valoracion.objects.create(
            entrevista=entrevista,
            empresa=empresa,
            votos_entrevista=votos_entrevista,
            votos_empresa=votos_empresa,
            media_aspectos=media_aspectos
        )
        return redirect('listar_valoraciones')

    return render(request, 'add.html')

#########################
#   23. CHAT VIEW
#########################

@login_required
def chat_view(request, entrevistador_id):
    entrevistador = get_object_or_404(Entrevistador, id=entrevistador_id)
    mensajes = Mensaje.objects.filter(
        (models.Q(remitente=request.user) & models.Q(destinatario=entrevistador.user)) |
        (models.Q(remitente=entrevistador.user) & models.Q(destinatario=request.user))
    )

    # Agregar la propiedad 'clase' para usarla en el template
    for mensaje in mensajes:
        mensaje.clase = 'enviado' if mensaje.remitente == request.user else 'recibido'

    # Renderizar solo el chat para la respuesta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'mensajesHtml': render_to_string('chat_mensajes.html', {'mensajes': mensajes}),
        })

    return render(request, 'chat.html', {'entrevistador': entrevistador, 'mensajes': mensajes})

#########################
#   24. ENVIAR MENSAJE
#########################

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        destinatario_id = request.POST.get('destinatario_id')
        destinatario = get_object_or_404(User, id=destinatario_id)

        # Crear el mensaje enviado por el usuario
        mensaje = Mensaje.objects.create(
            remitente=request.user,
            destinatario=destinatario,
            contenido=contenido
        )

        # Respuestas automáticas basadas en palabras clave
        respuestas_automaticas = {
            "Hola": "Hola, ¿en qué puedo ayudarte?",
            "Adiós": "Hasta luego, ¡que tengas un buen día!",
            "Ayuda": "Claro, dime en qué necesitas ayuda."
        }

        respuesta = None
        for palabra, respuesta_automatica in respuestas_automaticas.items():
            if palabra.lower() in contenido.lower():
                respuesta = respuesta_automatica
                break

        # Si hay una respuesta automática, crearla como mensaje
        if respuesta:
            Mensaje.objects.create(
                remitente=destinatario,
                destinatario=request.user,
                contenido=respuesta
            )

        return JsonResponse({
            'status': 'success',
            'mensaje': mensaje.contenido,
            'respuesta': respuesta,
            'fecha_envio': mensaje.fecha_envio
        })

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

#########################
#  25. SELECC. ENTREV.
#########################

@login_required
def seleccionar_entrevistadores(request):
    entrevistadores = Entrevistador.objects.all()
    # Si el usuario está enviando un formulario, redirigir al chat con el entrevistador seleccionado
    if request.method == 'POST':
        entrevistador_id = request.POST.get('entrevistador_id')
        return redirect('chat_view', entrevistador_id=entrevistador_id)
    return render(request, 'seleccionar_entrevistador.html', {'entrevistadores': entrevistadores})

#########################
#    26. LISTAR TAREA
#########################

def listar_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'listar_tareas.html', {'tareas': tareas})

#########################
#    27. CREAR TAREA
#########################

def crear_tarea(request):
    if request.method == 'POST':
        tarea = request.POST.get('tarea')
        fecha = request.POST.get('fecha')
        estado_id = request.POST.get('estado')
        estado = get_object_or_404(Estado, id=estado_id)

        Tarea.objects.create(tarea=tarea, fecha=fecha, estado=estado)
        return redirect('listar_tareas')

    estados = Estado.objects.all()
    return render(request, 'crear_tarea.html', {'estados': estados})

#########################
#    28. EDITAR TAREA
#########################

def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    estados = Estado.objects.all()

    if request.method == 'POST':
        # Mantener los valores anteriores si no se cambian
        nueva_tarea = request.POST.get('tarea', tarea.tarea)
        nueva_fecha = request.POST.get('fecha', tarea.fecha)  # Mantener fecha si no se actualiza
        nuevo_estado_id = request.POST.get('estado', tarea.estado.id)

        # Actualizar la tarea
        tarea.tarea = nueva_tarea
        tarea.fecha = nueva_fecha
        tarea.estado_id = nuevo_estado_id
        tarea.save()

        return redirect('listar_tareas')

    return render(request, 'crear_tarea.html', {'tarea': tarea, 'estados': estados})

#########################
#   29. ELIMINAR TAREA
#########################

def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    return redirect('listar_tareas')

#########################
#  30. LISTAR PROYECTOS
#########################

def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'listar_proyectos.html', {'proyectos': proyectos})

#########################
#   31. CREAR PROYECTO
#########################

def crear_proyecto(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        lenguaje = request.POST.get('lenguaje')
        tecnologias = request.POST.get('tecnologias')
        observaciones = request.POST.get('observaciones')
        fecha_publicacion = request.POST.get('fecha_publicacion')

        # Convertir fecha_publicacion a un objeto datetime (si existe)
        #if fecha_publicacion:
         #   try:
          #      fecha_publicacion = datetime.strptime(fecha_publicacion, '%Y-%m-%d %H:%M:%S')
           # except ValueError:
            #    fecha_publicacion = None  # Manejar error en el formato de fecha

        Proyecto.objects.create(titulo=titulo, lenguaje=lenguaje, tecnologias=tecnologias, observaciones=observaciones, fecha_publicacion=fecha_publicacion)
        return redirect('listar_proyectos')

    return render(request, 'crear_proyecto.html')

#########################
#   32. EDITAR PROYECTO
#########################

def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    if request.method == 'POST':
        # Mantener los valores anteriores si no se cambian
        nuevo_titulo = request.POST.get('titulo', proyecto.titulo)
        nuevo_lenguaje = request.POST.get('lenguaje', proyecto.lenguaje)
        nueva_tecnologia = request.POST.get('tecnologias', proyecto.tecnologias)
        nueva_observacion = request.POST.get('observaciones', proyecto.observaciones)
        proyecto.fecha_publicacion = request.POST.get('fecha_publicacion')

        # Actualizar solo si hay cambios
        #if nuevo_titulo:
         #   proyecto.titulo = nuevo_titulo
        #if nuevo_lenguaje:
         #   proyecto.lenguaje = nuevo_lenguaje
        #if nueva_tecnologia:
         #   proyecto.tecnologias = nueva_tecnologia
        #if nueva_observacion:
         #   proyecto.observaciones = nueva_observacion
        #if nueva_fecha_publicacion:
         #   try:
          #      proyecto.fecha_publicacion = datetime.strptime(nueva_fecha_publicacion, '%Y-%m-%d %H:%M:%S')
           # except ValueError:
            #    pass  # Ignorar si la fecha tiene un formato incorrecto

        # Actualizar el proyecto
        proyecto.titulo = nuevo_titulo
        proyecto.lenguaje = nuevo_lenguaje
        proyecto.tecnologias = nueva_tecnologia
        proyecto.observaciones = nueva_observacion
        proyecto.save()

        return redirect('listar_proyectos')

    return render(request, 'editar_proyecto.html', {'proyecto': proyecto})

#########################
#  29. ELIMINAR PROYECTO
#########################

def eliminar_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    proyecto.delete()
    return redirect('listar_proyectos')