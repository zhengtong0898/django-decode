from django.db import models
from django.template.defaultfilters import truncatechars


# Create your models here.
class product(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=50, unique=True)
    price = models.DecimalField(verbose_name="商品价格", max_digits=5, decimal_places=2)
    description = models.TextField(verbose_name="商品描述")
    production_date = models.DateField(verbose_name="生产日期")
    expiration_date = models.IntegerField(verbose_name="有效期", help_text="按天")
    date_joined = models.DateTimeField(verbose_name="商品录入时间", auto_now=True)

    @property
    def short_description(self):
        return truncatechars(self.description, 100)
