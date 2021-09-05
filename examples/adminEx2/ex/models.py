from django.db import models


# Create your models here.
class Publisher(models.Model):

    name = models.CharField('name', max_length=150, unique=True)


class Country(models.Model):

    name = models.CharField('name', max_length=150, unique=True)


class Book(models.Model):

    name = models.CharField('name', max_length=150, unique=True)
    publisher = models.ForeignKey(
        Publisher,
        models.CASCADE,
        verbose_name='publisher name',
    )
    country = models.ForeignKey(
        Country,
        models.CASCADE,
        verbose_name='publisher name',
    )

    class Meta:
        unique_together = [['name', 'country', 'publisher']]
