from django.db import models


# Create your models here.
class AuthorModel(models.Model):

    name = models.CharField(verbose_name="作者姓名", max_length=50)
    date_joined = models.DateTimeField(verbose_name="作者加入时间", auto_now=True)

    def __str__(self):
        return self.name


class ArticleModel(models.Model):

    title = models.CharField(verbose_name="文章标题", max_length=200)
    content = models.TextField(verbose_name="文章内容", max_length=5000)
    author = models.ForeignKey(verbose_name="作者", to=AuthorModel, on_delete=models.CASCADE)    # TODO: 不删除, 只隐藏.
    slug = models.SlugField(verbose_name="url_friendly_field", unique=False)

    date_joined = models.DateTimeField(verbose_name="文章创建时间", auto_now=True)
    date_last_change = models.DateTimeField(verbose_name="最后一次修改时间", auto_now=True)

    def __str__(self):
        return self.title
