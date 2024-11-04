# Generated by Django 5.1.1 on 2024-09-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appportfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=25, null=True, verbose_name='Nombre')),
                ('apellido1', models.CharField(blank=True, max_length=25, null=True, verbose_name='Primer apellido')),
                ('apellido2', models.CharField(blank=True, max_length=25, null=True, verbose_name='Segundo apellido')),
                ('edad', models.IntegerField(blank=True, null=True, verbose_name='Edad')),
            ],
            options={
                'verbose_name': 'Personal',
                'verbose_name_plural': 'Personales',
                'ordering': ['nombre'],
            },
        ),
        migrations.AlterField(
            model_name='habilidad',
            name='nivel',
            field=models.IntegerField(blank=True, null=True, verbose_name='Nivel'),
        ),
    ]
