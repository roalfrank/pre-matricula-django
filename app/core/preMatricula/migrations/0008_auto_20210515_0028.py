# Generated by Django 3.1.3 on 2021-05-15 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preMatricula', '0007_auto_20210502_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instructor',
            old_name='usuario_sisce',
            new_name='usuario_siscae',
        ),
    ]