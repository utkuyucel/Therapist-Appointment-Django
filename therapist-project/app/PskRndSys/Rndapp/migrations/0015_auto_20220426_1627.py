# Generated by Django 3.2.12 on 2022-04-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rndapp', '0014_auto_20220426_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='randevular',
            name='pskId',
        ),
        migrations.AlterField(
            model_name='danisan',
            name='gender',
            field=models.CharField(choices=[('E', 'Erkek'), ('B', 'Belirtilmedi'), ('K', 'Kadın')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='terapist',
            name='gender',
            field=models.CharField(choices=[('E', 'Erkek'), ('B', 'Belirtilmedi'), ('K', 'Kadın')], default='B', max_length=1),
        ),
    ]