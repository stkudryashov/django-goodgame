# Generated by Django 3.1.7 on 2021-03-28 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_auto_20210328_1852'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseGrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.TextField(blank=True, null=True, verbose_name='в каком клубе')),
                ('cost', models.IntegerField(blank=True, null=True, verbose_name='цена кейса')),
                ('text', models.TextField(blank=True, null=True, verbose_name='текст на кнопке')),
                ('rewards', models.TextField(blank=True, null=True, verbose_name='призы через запятую')),
            ],
            options={
                'verbose_name': 'цена кейса',
                'verbose_name_plural': 'цены кейсов',
            },
        ),
        migrations.DeleteModel(
            name='CasesCost',
        ),
        migrations.AlterModelOptions(
            name='casebody',
            options={'verbose_name': 'акция с кейсами', 'verbose_name_plural': 'акции с кейсами'},
        ),
    ]
