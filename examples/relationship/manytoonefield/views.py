from django.shortcuts import render, HttpResponse
from .models import Reporter, Article
from datetime import date


def single_create(request):
    # 测试用例-1: 创建一条维表数据和一条主表数据.
    # 1. 创建维表数据.
    # INSERT INTO `manytoonefield_reporter` (`first_name`, `last_name`, `email`)
    # VALUES ('John', 'Smith', 'john@example.com')
    # RETURNING `manytoonefield_reporter`.`id`;
    r = Reporter(first_name='John', last_name='Smith', email='john@example.com')
    r.save()
    # 2. 创建主表数据, 同时将维表数据作为参数
    # INSERT INTO `manytoonefield_article` (`headline`, `pub_date`, `reporter_id`)
    # VALUES ('This is a test', '2005-07-27', 1)
    # RETURNING `manytoonefield_article`.`id`;
    a = Article(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
    a.save()
    # 3. 正向查询.
    # SELECT `manytoonefield_article`.`id`,
    #        `manytoonefield_article`.`headline`,
    #        `manytoonefield_article`.`pub_date`,
    #        `manytoonefield_article`.`reporter_id`
    # FROM   `manytoonefield_article`
    # WHERE  `manytoonefield_article`.`id` = 1 LIMIT 21;
    af = Article.objects.get(pk=1)
    # N+1 查询
    # SELECT `manytoonefield_reporter`.`id`,
    #        `manytoonefield_reporter`.`first_name`,
    #        `manytoonefield_reporter`.`last_name`,
    #        `manytoonefield_reporter`.`email`
    # FROM   `manytoonefield_reporter`
    # WHERE  `manytoonefield_reporter`.`id` = 1 LIMIT 21;
    print("af.reporter.id: ", af.reporter.id)
    # 4. 反向查询.
    # SELECT `manytoonefield_reporter`.`id`,
    #        `manytoonefield_reporter`.`first_name`,
    #        `manytoonefield_reporter`.`last_name`,
    #        `manytoonefield_reporter`.`email`
    # FROM   `manytoonefield_reporter`
    # WHERE  `manytoonefield_reporter`.`id` = 1 LIMIT 21;
    r = Reporter.objects.get(pk=1)
    # SELECT `manytoonefield_article`.`id`,
    #        `manytoonefield_article`.`headline`,
    #        `manytoonefield_article`.`pub_date`,
    #        `manytoonefield_article`.`reporter_id`
    # FROM `manytoonefield_article`
    # WHERE `manytoonefield_article`.`reporter_id` = 1 LIMIT 21;                      # TODO: 为什么 all 对应的是limit 21?
    print(r.article_set.all())

    return HttpResponse("view_create")


def multi_create(request):
    # 测试用例-2: 创建一条维表数据和多条主表数据.
    # 1. 创建维表数据.
    r = Reporter.objects.create(first_name='John', last_name='Smith', email='john@example.com')
    # 2. 创建30条主表数据, 同时将维表数据作为参数
    for i in range(30):
        Article.objects.create(headline=f"This is a test-{i}", pub_date=date(2005, 7, 27), reporter=r)
    # 3. 正向查询
    af = Article.objects.get(pk=1)                                                 # Article 是 Many;   Reporter 是 One;
    print("af.reporter.id: ", af.reporter.id)                                      # 触发N+1;
    # 4. 反向查询
    # SELECT `manytoonefield_reporter`.`id`,
    #        `manytoonefield_reporter`.`first_name`,
    #        `manytoonefield_reporter`.`last_name`,
    #        `manytoonefield_reporter`.`email`
    # FROM   `manytoonefield_reporter`
    # WHERE  `manytoonefield_reporter`.`id` = 1 LIMIT 21;
    r = Reporter.objects.get(pk=1)
    # SELECT `manytoonefield_article`.`id`,
    #        `manytoonefield_article`.`headline`,
    #        `manytoonefield_article`.`pub_date`,
    #        `manytoonefield_article`.`reporter_id`
    # FROM   `manytoonefield_article`
    # WHERE  `manytoonefield_article`.`reporter_id` = 1 LIMIT 21
    articles = r.article_set.all()
    print("articles: ", articles)
    # SELECT `manytoonefield_article`.`id`,
    #        `manytoonefield_article`.`headline`,
    #        `manytoonefield_article`.`pub_date`,
    #        `manytoonefield_article`.`reporter_id`
    # FROM   `manytoonefield_article`
    # WHERE  `manytoonefield_article`.`reporter_id` = 1;
    for article in articles:
        print("article.id: ", article.id)

    return HttpResponse("view_query")
