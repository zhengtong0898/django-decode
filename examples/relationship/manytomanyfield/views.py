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
    # 1. 创建主表数据
    # INSERT INTO `manytomanyfield_article` (`headline`)
    # VALUES ('NASA uses Python');
    aa1 = Article.objects.create(headline='NASA uses Python')
    # INSERT INTO `manytomanyfield_publication` (`title`)
    # VALUES ('The Python Journal');
    pp1 = Publication.objects.create(title='The Python Journal')
    # 3. 从维表对象的角度触发去执行关联操作, 也被称为反向操作.
    # INSERT IGNORE INTO `manytomanyfield_article_publications`
    # (`article_id`, `publication_id`) VALUES (8, 7)               # 这里跟上面的 a1.publications.add(p1)，生成的sql语句一致
    pp1.article_set.add(aa1)

    # 备注:
    # 当使用 aa1.publications.all() 时, 是以 aa1 的角度去拉取所有隶属于 aa1 的 publication.
    # 当使用 pp1.article_set.all() 是, 是以 pp1 的角度去拉取所有从属于 aa1 的 Article.
    return HttpResponse("many_to_many: single_create")


def multi_create(request):
    return HttpResponse("many_to_many: multi_create")
