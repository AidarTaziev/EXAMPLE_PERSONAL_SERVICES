# Generated by Django 2.2.1 on 2020-10-30 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('render', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renderclass',
            name='styles',
            field=models.ManyToManyField(blank=True, null=True, to='render.RenderCSS', verbose_name='Стили класса'),
        ),
    ]
