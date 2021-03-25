from django.db import models


# Create your models here.
class ArticleModel(models.Model):

    title = models.CharField(verbose_name="文章标题", max_length=200)
    content = models.TextField(verbose_name="文章内容")
    author = models.CharField(verbose_name="作者", max_length=200)
    tags = models.CharField(verbose_name="文章标签", max_length=200)
    date_joined = models.DateTimeField(verbose_name="文章创建时间")
