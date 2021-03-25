from django.db import models


# Create your models here.
class ArticleModel(models.Model):

    # 默认字段长度是多少?        CharFields字段要求 max_length 参数必填.
    # 默认是必填还是非必填?      blank=False(表单验证不允许为空) 和 null=False(数据库不允许为空).
    title = models.CharField(verbose_name="文章标题", max_length=100)
    content = models.TextField(verbose_name="文章内容")
    tags = models.CharField(verbose_name="文章标签, 用空格分隔", max_length=100)
    author = models.CharField(verbose_name="文章作者", max_length=50, null=False, blank=False)
    date_joined = models.DateTimeField(verbose_name="发布时间")
    date_changed = models.DateTimeField(verbose_name="最后一次")
