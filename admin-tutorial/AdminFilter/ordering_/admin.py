from django.contrib import admin
from .models import ArticleModel
from django.urls import reverse


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):

    list_display = ('title', 'tags', 'author', 'date_joined', 'view_on_site')
    ordering = ('title', 'date_joined')                             # 按字段排序, 对应sql是: order by .
    sortable_by = ('tags', )

    search_fields = ('title', )
    show_full_result_count = True

    preserve_filters = True

    list_editable = ('tags', 'date_joined')

    def view_on_site(self, obj):
        """
        django 认为除了在 admin 站内显示数据之外,
        可能还会有前端网站页面, 这里可以快速的跳到前端网站查看对应的数据.
        """
        return "https://www.baidu.com"


admin.site.register(ArticleModel, ArticleModelAdmin)
