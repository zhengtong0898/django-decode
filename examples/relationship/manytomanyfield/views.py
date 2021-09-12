from django.shortcuts import render, HttpResponse
# from .models import Publication, Article


def single_create(request):
    # 测试用例-1
    #
    return HttpResponse("many_to_many: single_create")


def multi_create(request):

    return HttpResponse("many_to_many: multi_create")
