# Generated by Django 3.2.12 on 2022-03-29 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rndapp', '0011_auto_20220326_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danisan',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('E', 'Erkek'), ('K', 'Kadın')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='terapist',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('E', 'Erkek'), ('K', 'Kadın')], default='B', max_length=1),
        ),
    ]
