from django.contrib import admin
from .models import Article


# Register your models here.
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')                     # queryset 是一个集合对象, update 可以批量对集合做更新操作.


make_published.short_description = "Mark selected stories as published"


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']                            # 排序
    actions = [make_published]                      # 批量操作(按make_published函数来操作: 批量更新发布状态.)


admin.site.register(Article, ArticleAdmin)