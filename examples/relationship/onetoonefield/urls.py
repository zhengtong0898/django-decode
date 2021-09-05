from django.urls import path

from . import views


urlpatterns = [
    path('', views.multi_create, name='index_view'),
]