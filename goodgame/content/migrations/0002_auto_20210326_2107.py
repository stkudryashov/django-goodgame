# Generated by Django 3.1.7 on 2021-03-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casebody',
            name='about_text',
            field=models.TextField(default='', verbose_name='о кейсах'),
        ),
        migrations.AlterField(
            model_name='casebody',
            name='club',
            field=models.TextField(default='', verbose_name='в каком клубе'),
        ),
        migrations.AlterField(
            model_name='casebody',
            name='how_open',
            field=models.TextField(default='', verbose_name='как открыть коробку'),
        ),
    ]
