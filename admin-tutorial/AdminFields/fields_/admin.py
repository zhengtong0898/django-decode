from django.contrib import admin
from .models import ArticleModel


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):

    fields = (("author", "title", "tags"),         # 这三个字段放在同一行
              "content",                            # 这个字段单独一行
              ("date_joined", "date_changed"))      # 这两个字段放在同一行


admin.site.register(ArticleModel, ArticleModelAdmin)
