# Generated by Django 3.1.3 on 2021-04-29 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('preMatricula', '0002_cargo_instructor'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaOcupacional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Categoría Ocupacional')),
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
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.municipio', verbose_name='Municipio')),
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
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Discapacidad')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMatricula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de la Estado Matricula')),
            ],
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_sisce', models.CharField(blank=True, max_length=30, null=True, verbose_name='Usuario del siscae')),
                ('categoria_ocupacional', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.categoriaocupacional', verbose_name='Categoría Ocupacional')),
                ('discapacidad', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.discapacidad', verbose_name='Discapacidad')),
            ],
        ),
        migrations.CreateModel(
            name='Gestor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jcm', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='preMatricula.jcm', verbose_name='Joven Club Municipal')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Maestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.instructor', verbose_name='Instructor')),
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
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Ocupación')),
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
            name='TipoGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Tipo de Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='PreMatriculaMaestro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maestro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.maestro', verbose_name='Maestro')),
                ('preMatricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.prematricula', verbose_name='Pre-Matricula')),
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
            name='InstructorEstudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creado', models.DateTimeField(auto_now=True)),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.estudiante', verbose_name='Estudiante')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preMatricula.gestor', verbose_name='Gestor')),
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
            model_name='estudiante',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='usuario'),
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
    ]