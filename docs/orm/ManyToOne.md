# Many-to-one

### 对象描述
`Reporter` 作者信息表   
`Article` 文章表  

### 对象关系
从 `数据库` 的角度来看, `Reporter`是独立表, `Article`是外键表.  
从 `业务` 的角度来看, `Reporter`是维度表, `Article`是主表(事实表).  
从 `ORM` 的角度来看, `Article` 使用 `models.ForeignKey` 来绑定与 `Reporter` 是多对一的关系.

> 多对一(正向)  
> `Article` 由于定义了 foreign key, 因此具备指向能力.  
> `Article` 在创建多条数据时, 可以指向到同一条 `Reporter`.`id`, 这就是 `多对一` 的概念.  
> `Article` 为主线去执行 写/更新 操作, 都被视为 `多对一`.
> 
> 一对多(反向)  
> 一个 `Reporter` 就有可能被多个 `Article` 指向.  
> `Reporter` 为主线去执行 `写/更新` 操作, 都被视为 `一对多`.


### 对象约束
`Many-to-one` 是 `ORM` 和 `纯SQL编程` 都有且相同的概念.  
从数据模型的约束上来看, 主表通过 `Foreign Key` 指向`维度表`, 完成对一个对象的多维度描述.    
这里的约束指的是, 主表的`Foreign Key` 字段的值必须是 `维度表` 的 `主键`.  

> 注意事项  
> 1. manytoonefield_article 表(主表), 自动生成一个自增ID, 同时也是主键ID.    
> 2. manytoonefield_article.reporter 字段(外键), 指向 `维度表` 的 `主键`.    
> 3. manytoonefield_article.reporter 字段(索引), 该字段不与`维度表`的`主键`保持同步, 而是自己维护自己的`二叉平衡树`.  

models.py
```python3
from django.db import models


# CREATE TABLE `manytoonefield_reporter` (                                                             -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `first_name` varchar(30) NOT NULL,
#   `last_name` varchar(30) NOT NULL,
#   `email` varchar(254) NOT NULL
# );
#
#
# CREATE TABLE `manytoonefield_reporter` (                                                 -- 数据库连接工具查看DDL-建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,                                                   
#   `first_name` varchar(30) NOT NULL,
#   `last_name` varchar(30) NOT NULL,
#   `email` varchar(254) NOT NULL,
#   PRIMARY KEY (`id`)                                                                                   -- 主键(聚集索引)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


# CREATE TABLE `manytoonefield_article` (                                                              -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `headline` varchar(100) NOT NULL,
#   `pub_date` date NOT NULL,
#   `reporter_id` integer NOT NULL
# );
#
# ALTER TABLE `manytoonefield_article`
# ADD CONSTRAINT `manytoonefield_artic_reporter_id_01692140_fk_manytoone` FOREIGN KEY (`reporter_id`)
# REFERENCES `manytoonefield_reporter` (`id`)                                                       
#
#
# Question: 辅助索引与外键有什么区别?
#           https://stackoverflow.com/questions/1732467/what-is-the-difference-between-an-index-and-a-foreign-key
#           辅助索引的内部是一个b+树的数据结构, 对于随机查询起到加速的作用.
#           外键仅仅是对只想其他表的主键.
# CREATE TABLE `manytoonefield_article` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,                                                  -- 数据库连接工具查看DDL-建表语句
#   `headline` varchar(100) NOT NULL,
#   `pub_date` date NOT NULL,
#   `reporter_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),                                                                                  -- 主键(聚集索引)
#   KEY `manytoonefield_artic_reporter_id_01692140_fk_manytoone` (`reporter_id`),                             -- 辅助索引
#   CONSTRAINT `manytoonefield_artic_reporter_id_01692140_fk_manytoone` FOREIGN KEY (`reporter_id`) \
#   REFERENCES `manytoonefield_reporter` (`id`)                                                                  -- 外键
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)                                      # Many-to-one
```

views.py
```python3
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

```