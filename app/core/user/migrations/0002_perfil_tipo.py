# Generated by Django 3.1.3 on 2021-09-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='tipo',
            field=models.CharField(choices=[('ES', 'Estudiante'), ('PR', 'Profesor'), ('GE', 'Gestor'), ('IN', 'Instructor')], default='ES', max_length=2),
        ),
    ]
