from django.urls import path

from . import views

# 备注:
# django 从 2.0 版本开始就一直采用 path(非正则表达式), 在此之前采用的是 url(正则表达式).
# path是一种 DSL, 用于简化表达式, 但是其内部最终还是要转换回到标准的正则表达式.
app_name = 'polls'
urlpatterns = [
    path('', views.index_view, name='index_view'),
]