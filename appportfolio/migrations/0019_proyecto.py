# Generated by Django 4.1.5 on 2024-12-09 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appportfolio', '0018_alter_tarea_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Título proyecto')),
                ('lenguaje', models.CharField(blank=True, max_length=30, null=True, verbose_name='Lenguaje principal')),
                ('tecnologias', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tecnologías')),
                ('observaciones', models.CharField(blank=True, max_length=100, null=True, verbose_name='Observaciones')),
                ('fecha_publicacion', models.DateTimeField(blank=True, null=True, verbose_name='Fecha publicación')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
                'ordering': ['id'],
            },
        ),
    ]
