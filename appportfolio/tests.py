# tests.py

import os # Usado para interactuar con el sistema de archivos, como la eliminación de archivos.
from django.test import TestCase  # Clase de Django que facilita la creación de pruebas unitarias.

# Permite sobrescribir configuraciones en un entorno de prueba, como MEDIA_ROOT para evitar usar el sistema de archivos real.
from django.test import override_settings

from appportfolio.models import *  # Importa modelos desde la aplicación.

# Facilita la creación de archivos simulados que se pueden cargar en el modelo.
from django.core.files.uploadedfile import SimpleUploadedFile

from os.path import basename #Extrae el nombre base del archivo (sin la ruta)).
import tempfile  # Utilizado para crear directorios temporales donde almacenar los archivos durante las pruebas.
from uuid import uuid4  # Genera un identificador único para evitar colisiones en los nombres de los archivos.

# Decorador que cambia la ruta solo para pruebas
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class NoticiaModelsTest(TestCase):
    # Método especial de Django para eliminar archivos después de las pruebas
    def tearDown(self):
        for noticia in Noticia.objects.all():
            if noticia.imagen and os.path.exists(noticia.imagen.path):
                os.remove(noticia.imagen.path)
        super().tearDown()

    def test_creacion_noticia_sin_imagen(self):
        """
        Prueba que una noticia se puede crear sin proporcionar una imagen.
        """
        noticia = Noticia.objects.create(
            titulo="Noticia sin imagen",
            contenido="Contenido de prueba sin imagen"
        )

        self.assertEqual(noticia.titulo, "Noticia sin imagen")
        self.assertEqual(noticia.contenido, "Contenido de prueba sin imagen")
        self.assertFalse(noticia.imagen)  # Verificar que no se asignó imagen

    def test_creacion_noticia_con_imagen(self):
        """
        Prueba que una noticia se puede crear con una imagen cargada.
        """
        unique_filename = f"test_image_{uuid4().hex}.jpg"
        imagen = SimpleUploadedFile(
            name=unique_filename,
            content=b"contenido de la imagen", # pasarlo a binario
            content_type="image/jpeg"
        )

        noticia = Noticia.objects.create(
            titulo="Noticia con imagen",
            contenido="Contenido de prueba con imagen",
            imagen=imagen
        )

        self.assertEqual(noticia.titulo, "Noticia con imagen")
        self.assertEqual(noticia.contenido, "Contenido de prueba con imagen")
        self.assertIsNotNone(noticia.imagen)  # La imagen no debería estar vacía
        # Comparar con el nombre dinámico generado
        self.assertEqual(os.path.basename(noticia.imagen.name), unique_filename)

