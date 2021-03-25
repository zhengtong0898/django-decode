from django.contrib import admin
from .models import Article, Publication


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):
    # filter_horizontal = ('publications', )
    filter_vertical = ('publications', )

    list_display = ('headline', 'content')
    list_display_links = ('content', )

    list_per_page = 3
    list_max_show_all = 200

    raw_id_fields = ('publications', )


class PublicationModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleModelAdmin)
admin.site.register(Publication, PublicationModelAdmin)