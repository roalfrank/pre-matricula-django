# Generated by Django 3.1.3 on 2021-09-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preMatricula', '0009_auto_20210921_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='prematricula',
            name='qr',
            field=models.ImageField(blank=True, default='qr_default.png', upload_to='qrcode'),
        ),
    ]