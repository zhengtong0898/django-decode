from django.db import models


# Create your models here.
# 参考: https://docs.djangoproject.com/en/3.2/topics/db/aggregation/
class Author(models.Model):
    """ 作者表 """
    name = models.CharField(max_length=100)
    age = models.IntegerField()


class Publisher(models.Model):
    """ 发行商表 """
    name = models.CharField(max_length=300)


class Book(models.Model):
    """ 图书表 """
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()


class Store(models.Model):
    """ 书店表 """
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)
