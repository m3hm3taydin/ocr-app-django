# Generated by Django 2.1.2 on 2019-02-11 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.ImageField(upload_to='images/%Y/%m/'),
        ),
    ]
