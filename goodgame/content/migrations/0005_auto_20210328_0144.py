# Generated by Django 3.1.7 on 2021-03-28 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_casebody_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reward',
            name='profile',
        ),
        migrations.AddField(
            model_name='reward',
            name='user_id',
            field=models.TextField(null=True, verbose_name='владелец'),
        ),
    ]
