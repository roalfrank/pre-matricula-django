# Generated by Django 3.1.3 on 2021-04-28 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sitio_Web',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, unique=True, verbose_name='Nombre del sitio')),
                ('color_activo_menu', models.CharField(default='#007bff', max_length=20, verbose_name='Color activo menu')),
                ('color_no_activo_menu', models.CharField(default='#11101070', max_length=20, verbose_name='Color menu no activo')),
                ('color_sider', models.CharField(default='#0087c3', max_length=20, verbose_name='Color sider')),
                ('color_footer', models.CharField(default='#e8e8ea', max_length=20, verbose_name='Color footer')),
                ('color_header', models.CharField(default='#26bdef', max_length=20, verbose_name='Color header')),
                ('color_text_body', models.CharField(default='rgb(9, 79, 102)', max_length=20, verbose_name='Color Texto Body')),
                ('color_contenido', models.CharField(default='#fffff', max_length=20, verbose_name='Color contenido')),
                ('color_fondo_inicio', models.CharField(default='#26bdef', max_length=20, verbose_name='Color Fondo Inicio')),
                ('icono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Icono del sitio Barra Lateral')),
            ],
        ),
        migrations.CreateModel(
            name='TipoModulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, verbose_name='Nombre Modulo')),
                ('icono', models.CharField(max_length=20, unique=True, verbose_name='Icono')),
                ('estado', models.BooleanField()),
                ('padre_tipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='padre', to='sitio.tipomodulo', verbose_name='Padre')),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, verbose_name='Nombre del men??')),
                ('icono', models.CharField(max_length=20, verbose_name='Icono del Men??')),
                ('url_path', models.CharField(default='sitio:listar', max_length=50, verbose_name='Url')),
                ('estado', models.BooleanField()),
                ('grupos', models.ManyToManyField(to='auth.Group', verbose_name='Grupos')),
                ('tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modulos', to='sitio.tipomodulo', verbose_name='Tipo de M??dulo')),
            ],
        ),
    ]
