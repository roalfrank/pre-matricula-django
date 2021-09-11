# Generated by Django 3.1.3 on 2021-09-11 14:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='CategoriaOcupacional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre Categoría Ocupacional')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Curso')),
                ('duracion', models.IntegerField(verbose_name='Duración en Horas')),
                ('descripcion', models.TextField(verbose_name='Descripción del Curso')),
                ('corto', models.BooleanField(verbose_name='Tipo de Curso')),
                ('nextCurso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='preMatricula.curso')),
            ],
        ),
        migrations.CreateModel(
            name='CursoInteres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frecuencia', models.IntegerField(verbose_name='Frecuencia')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.curso', verbose_name='Curso de Interes')),
            ],
        ),
        migrations.CreateModel(
            name='CursoSiscae',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Curso Siscae')),
            ],
        ),
        migrations.CreateModel(
            name='Discapacidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre Discapacidad')),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Entidad')),
                ('telefono', models.CharField(blank=True, max_length=8, null=True, verbose_name='Telefono')),
                ('direccion', models.CharField(max_length=200, verbose_name='Dirección')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMatricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Estado Matricula')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('usuario_sisce', models.CharField(blank=True, max_length=30, null=True, verbose_name='Usuario del siscae')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user', verbose_name='usuario')),
                ('categoria_ocupacional', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.categoriaocupacional', verbose_name='Categoría Ocupacional')),
                ('creado_por', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creado_por', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('discapacidad', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.discapacidad', verbose_name='Discapacidad')),
            ],
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='JCP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_jcp', models.CharField(max_length=10, unique=True, verbose_name='Codigo JCP')),
                ('entidad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.entidad', verbose_name='Entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Modalidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de la Modalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Ocupacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Nombre Ocupación')),
            ],
        ),
        migrations.CreateModel(
            name='PreMatricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacidad', models.IntegerField(verbose_name='Capacidad Total a Matricular')),
                ('frecuencia', models.IntegerField(verbose_name='Frecuencia semanal')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha Fin')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.curso', verbose_name='Curso')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.estadomatricula', verbose_name='Estado de la PreMatricula')),
                ('modalidad', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.modalidad', verbose_name='Modalidad')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True, verbose_name='Provincia')),
            ],
        ),
        migrations.CreateModel(
            name='TipoGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Tipo de Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Maestro',
            fields=[
                ('instructor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='preMatricula.instructor', verbose_name='Instructor')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_region', models.CharField(max_length=10, unique=True, verbose_name='Código Región')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Región')),
                ('jcp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.jcp', verbose_name='Joven Club Provincial')),
            ],
        ),
        migrations.CreateModel(
            name='PreMatriculaEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activo', models.BooleanField(verbose_name='El Estudiante ha sido chequeado')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
                ('preMatricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.prematricula', verbose_name='Pre-Matricula')),
            ],
        ),
        migrations.AddField(
            model_name='prematricula',
            name='tipo_grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.tipogrupo', verbose_name='Tipo Grupo'),
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Municipio')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.provincia')),
            ],
        ),
        migrations.CreateModel(
            name='JCM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_jcm', models.CharField(max_length=10, unique=True, verbose_name='Código Joven Club Municipal')),
                ('entidad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.entidad', verbose_name='Entidad')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.region', verbose_name='Región')),
            ],
        ),
        migrations.CreateModel(
            name='JCB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_jcb', models.CharField(max_length=10, unique=True, verbose_name='Código Joven Club')),
                ('entidad', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.entidad', verbose_name='Entidad')),
                ('jcm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.jcm', verbose_name='Joven Club Municipal')),
            ],
        ),
        migrations.CreateModel(
            name='InstructorEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creado', models.DateTimeField(auto_now=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.gestor', verbose_name='Gestor')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('ci', models.IntegerField(unique=True, verbose_name='Carnet Identidad')),
                ('usuario_siscae', models.CharField(max_length=50, null=True, verbose_name='Usuario del siscae')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user', verbose_name='Usuario')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.cargo', verbose_name='Cargo')),
                ('jcb', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.jcb', verbose_name='Joven Club')),
            ],
        ),
        migrations.CreateModel(
            name='GestorEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creado', models.DateTimeField(auto_now=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
                ('gestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.gestor', verbose_name='Gestor')),
            ],
        ),
        migrations.AddField(
            model_name='gestor',
            name='jcm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.jcm', verbose_name='Joven Club Municipal'),
        ),
        migrations.CreateModel(
            name='EstudianteCursoSiscae',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cursoSiscae', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.cursosiscae', verbose_name='Curso Siscae')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='EstudianteCursoInteres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sugerencia', models.CharField(max_length=200, verbose_name='Sugerencia')),
                ('fecha_creado', models.DateField(verbose_name='fecha creado')),
                ('cursoInteres', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.cursointeres', verbose_name='Curso de Interes')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
            ],
        ),
        migrations.AddField(
            model_name='estudiante',
            name='ocupacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.ocupacion', verbose_name='Ocupación'),
        ),
        migrations.AddField(
            model_name='entidad',
            name='municipio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='preMatricula.municipio', verbose_name='Municipio'),
        ),
        migrations.AddField(
            model_name='cursointeres',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.municipio', verbose_name='Municipio'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto del comentario')),
                ('fecha_comentario', models.DateField(auto_now=True, verbose_name='Fecha Creado')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
                ('preMatricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.prematricula', verbose_name='Pre matricula')),
            ],
        ),
        migrations.CreateModel(
            name='PreMatriculaMaestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preMatricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.prematricula', verbose_name='Pre-Matricula')),
                ('maestro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.maestro', verbose_name='Maestro')),
            ],
        ),
    ]
