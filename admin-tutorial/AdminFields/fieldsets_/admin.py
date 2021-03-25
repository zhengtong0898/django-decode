from django.contrib import admin
from .models import ArticleModel


# Register your models here.
class ArticleModelAdmin(admin.ModelAdmin):

    fieldsets = (
        ("栏目一", {'fields': (("author", "title", "tags"), )}),
        ("栏目二", {'fields': ("content",)}),

        ("栏目三", {
            'fields': ("date_joined", "date_changed"),
            'classes': ('collapse', ),
            'description': '请注意: 这里应该这样, 这样, 这样, 对, 对, 就这样.'
        }),
    )


admin.site.register(ArticleModel, ArticleModelAdmin)
