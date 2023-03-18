# Generated by Django 3.2.12 on 2022-04-27 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rndapp', '0016_auto_20220426_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='terapist',
            name='user',
        ),
        migrations.AlterField(
            model_name='danisan',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('K', 'Kadın'), ('E', 'Erkek')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='terapist',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('K', 'Kadın'), ('E', 'Erkek')], default='B', max_length=1),
        ),
    ]