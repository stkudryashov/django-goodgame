# Generated by Django 3.1.7 on 2021-03-27 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20210326_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='casebody',
            name='image',
            field=models.ImageField(null=True, upload_to='images/cases/', verbose_name='изображение'),
        ),
    ]
