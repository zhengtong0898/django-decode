# Generated by Django 3.1.7 on 2021-03-18 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsets_', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemodel',
            name='date_changed',
            field=models.DateTimeField(auto_now=True, verbose_name='最后一次'),
        ),
        migrations.AlterField(
            model_name='articlemodel',
            name='date_joined',
            field=models.DateTimeField(auto_now=True, verbose_name='发布时间'),
        ),
    ]