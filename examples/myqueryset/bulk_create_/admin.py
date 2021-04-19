from django.contrib import admin
from .models import product


# Register your models here.
class ProductModel(admin.ModelAdmin):

    list_display = ('name', 'price', 'short_description', 'production_date', 'expiration_date')


admin.site.register(product, ProductModel)
