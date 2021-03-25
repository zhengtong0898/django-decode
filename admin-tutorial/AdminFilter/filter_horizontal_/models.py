from django.db import models


# Create your models here.
class Publication(models.Model):
    title = models.CharField(verbose_name="出版社", max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(verbose_name="文章标题", max_length=100)
    content = models.TextField(verbose_name="文章内容", default='')
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline
