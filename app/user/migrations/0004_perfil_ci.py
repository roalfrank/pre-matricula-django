# Generated by Django 3.1.3 on 2021-04-28 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210428_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='ci',
            field=models.IntegerField(default=84093018929, unique=True, verbose_name='Carnet Identidad'),
        ),
    ]