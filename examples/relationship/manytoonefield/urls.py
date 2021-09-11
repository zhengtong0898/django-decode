from django.urls import path

from . import views


urlpatterns = [
    path('single_create', views.single_create, name='single_create'),
    path('multi_create', views.multi_create, name='multi_create'),
]