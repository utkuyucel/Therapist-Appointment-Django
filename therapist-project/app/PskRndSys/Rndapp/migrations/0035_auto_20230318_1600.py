# Generated by Django 3.2.12 on 2023-03-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rndapp', '0034_auto_20220517_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danisan',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('E', 'Erkek'), ('K', 'Kadın')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='randevular',
            name='rndTime',
            field=models.DateTimeField(default='18/03/2023 16:00'),
        ),
        migrations.AlterField(
            model_name='terapist',
            name='gender',
            field=models.CharField(choices=[('B', 'Belirtilmedi'), ('E', 'Erkek'), ('K', 'Kadın')], default='B', max_length=1),
        ),
    ]
