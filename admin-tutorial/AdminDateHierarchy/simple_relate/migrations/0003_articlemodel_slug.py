# Generated by Django 3.1.7 on 2021-03-22 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_relate', '0002_auto_20210323_0755'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlemodel',
            name='slug',
            field=models.SlugField(default='test', verbose_name='url_friendly_field'),
            preserve_default=False,
        ),
    ]
