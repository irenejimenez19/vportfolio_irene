# Generated by Django 4.1.5 on 2024-11-20 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('appportfolio', '0013_noticia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('votos_entrevista', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Votos entrevista')),
                ('votos_empresa', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Votos empresa')),
                ('media_aspectos', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='Media aspectos')),
                ('entrevista', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción Entrevista')),
                ('empresa', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción Empresa')),
                ('num_valoraciones', models.IntegerField(blank=True, null=True, verbose_name='Num Valoraciones')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha')),
            ],
        ),
    ]