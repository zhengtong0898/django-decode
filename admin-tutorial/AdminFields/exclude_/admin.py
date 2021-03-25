from django.contrib import admin
from .models import ArticleModel


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):

    # 备注:
    # author 字段有两个隐藏参数: null=False 和 blank=False;
    # null = False          数据库不允许该字段为空值(None, '')
    # null = True           数据库允许字段为空值
    #
    # blank = False         Django Form Validate 要求表单必填.
    # blank = True          Django Form Validate 非必填.
    #
    # 由于这里把 author 排除掉了, 表单中没有这个字段, 所以 author 字段就绕过了 Form Validate 环节;
    # 因此这里就很容易产生 null=False + blank=False 不像预期那样生效(即: 字段没填写数据, 也能添加数据).
    exclude = ("author", )


admin.site.register(ArticleModel, ArticleModelAdmin)
