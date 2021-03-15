# Generated by Django 3.1.7 on 2021-03-15 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='время отправки')),
                ('value', models.FloatField(verbose_name='размер платежа')),
            ],
            options={
                'verbose_name': 'платеж',
                'verbose_name_plural': 'платежи',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='balance',
            field=models.FloatField(default=0, verbose_name='баланс'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='внешний ID'),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AddField(
            model_name='payment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.profile', verbose_name='профиль'),
        ),
    ]
