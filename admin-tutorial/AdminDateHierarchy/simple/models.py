from django.db import models


# Create your models here.
class ArticleModel(models.Model):

    title = models.CharField(verbose_name="文章标题", max_length=200)
    content = models.TextField(verbose_name="文章内容", max_length=5000)
    author = models.CharField(verbose_name="作者", max_length=50)

    date_joined = models.DateTimeField(verbose_name="创建时间", auto_now=True)
    date_last_change = models.DateTimeField(verbose_name="最后一次修改时间", auto_now=True)
