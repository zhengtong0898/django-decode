# Generated by Django 3.1.7 on 2021-04-09 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SQL1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='emp_no',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='员工'),
        ),
    ]
