# Generated by Django 3.1.3 on 2021-04-28 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('preMatricula', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ci', models.IntegerField(unique=True, verbose_name='Carnet Identidad')),
                ('usuario_sisce', models.CharField(max_length=50, null=True, verbose_name='Usuario del siscae')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.cargo', verbose_name='Cargo')),
                ('jcb', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.jcb', verbose_name='Joven Club')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]