from django.shortcuts import render, HttpResponse
from .models import Publication, Article


def single_create(request):
    # 测试用例-1(正向操作)
    # 1. 创建维表数据.
    # INSERT INTO `manytomanyfield_publication` (`title`)
    # VALUES ('The Python Journal');
    p1 = Publication.objects.create(title='The Python Journal')
    # 2. 创建主表数据.
    # INSERT INTO `manytomanyfield_article` (`headline`)
    # VALUES ('NASA uses Python');
    a1 = Article.objects.create(headline='NASA uses Python')
    # 3. 将维表数据和主表数据写入到附加表中.
    #    由于在 Article 中定义了 publications = models.ManyToManyField(Publication) 属性,
    #    因此可以通过 a1.publications 访问到附加表.
    # INSERT IGNORE INTO `manytomanyfield_article_publications`
    # (`article_id`, `publication_id`) VALUES (2, 1);
    a1.publications.add(p1)

    # 测试用例-2(反向操作)
    # 1.
    return HttpResponse("many_to_many: single_create")


def multi_create(request):

    return HttpResponse("many_to_many: multi_create")
