from django.db import models


# Create your models here.
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=30)


class Tag(models.Model):
    name = models.CharField(max_length=30)


class Article(models.Model):
    headline = models.CharField(max_length=100)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline
