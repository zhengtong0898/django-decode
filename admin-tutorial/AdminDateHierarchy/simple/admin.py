from django.contrib import admin
from .models import ArticleModel


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_joined']
    date_hierarchy = 'date_joined'


admin.site.register(ArticleModel, ArticleModelAdmin)
