# Many-to-many

### 对象描述
`Publication` 出版社  
`Article` 文章  

### 对象关系
从 `数据库` 的角度来看, `Publication`是独立表, `Article`也是独立表, `附加表`是双向外键表.  
从 `业务` 的角度来看, `Publication`是维度表, `Article`是主表(事实表), `附加表`是透明的.   
从 `ORM` 的角度来看, `Article` 使用 `models.ManyToManyField` 来绑定于 `Publication` 是多对多的关系.  

> 多对多(正向)  
> `Article` 为主线去执行 写/更新 操作, 都被时为 `正向多对多` 操作.  
>
> 多对多(反向)  
> `Publication` 为主线去执行 写/更新 操作, 都被时为 `反向多对多` 操作.


### 对象约束
`ORM` 通过利用 `附加表` 的 `多字段唯一索引约束` 和 `外键` 组成 `Many-to-many` 的概念.  

> 注意事项  
> 1. `manytomanyfield_publication` 是独立表.  
> 2. `manytomanyfield_article` 也是独立表.  
> 3. `manytomanyfield_article_publications` 是 `Django ORM` 的多对多概念.  
>    1). 创建 `附加表`, 包含 `publication_id` 和 `article_id` 两个字段.    
>    2). 给这两个字段创建一个唯一联合约束.  
>    3). 给这两个字段建立外键, 分别指向 `article` 和 `publication` 表的主键.  


models.py
```python3
from django.db import models


# CREATE TABLE `manytomanyfield_publication` (                                                       -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `title` varchar(30) NOT NULL
# );
#
# CREATE TABLE `manytomanyfield_publication` (                                          -- 数据库连接工具查看DDL 建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `title` varchar(30) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Publication(models.Model):
    title = models.CharField(max_length=30)


# CREATE TABLE `manytomanyfield_article` (                                                           -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `headline` varchar(100) NOT NULL
# );
#
# CREATE TABLE `manytomanyfield_article` (                                              -- 数据库连接工具查看DDL 建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `headline` varchar(100) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)


# CREATE TABLE `manytomanyfield_article_publications` (                                       -- Django 自动生成的附加表
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `article_id` integer NOT NULL,
#   `publication_id` integer NOT NULL
# );
#
# ALTER TABLE    `manytomanyfield_article_publications`                             -- Django 对两个字段进行唯一的组合约束
# ADD CONSTRAINT `manytomanyfield_article__article_id_publication_i_459a4946_uniq`  -- 目的是, 左表不能重复关联右表,
# UNIQUE         (`article_id`, `publication_id`);                                  -- 另一方面是为了起到索引加速的作用.
#
# ALTER TABLE    `manytomanyfield_article_publications`                                       -- Django 自动生成外键关联
# ADD CONSTRAINT `manytomanyfield_arti_article_id_471a4ce9_fk_manytoman`
# FOREIGN KEY    (`article_id`)
# REFERENCES     `manytomanyfield_article` (`id`);
#
# ALTER TABLE    `manytomanyfield_article_publications`                                       -- Django 自动生成外键关联
# ADD CONSTRAINT `manytomanyfield_arti_publication_id_d42f24f8_fk_manytoman`
# FOREIGN KEY    (`publication_id`)
# REFERENCES     `manytomanyfield_publication` (`id`);
#
#
# CREATE TABLE `manytomanyfield_article_publications` (                                 -- 数据库连接工具查看DDL 建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `article_id` int(11) NOT NULL,
#   `publication_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),
#
#   UNIQUE KEY `manytomanyfield_article__article_id_publication_i_459a4946_uniq` (`article_id`,`publication_id`),
#   KEY `manytomanyfield_arti_publication_id_d42f24f8_fk_manytoman` (`publication_id`),
#
#   CONSTRAINT `manytomanyfield_arti_article_id_471a4ce9_fk_manytoman` \
#   FOREIGN KEY (`article_id`) REFERENCES `manytomanyfield_article` (`id`),
#
#   CONSTRAINT `manytomanyfield_arti_publication_id_d42f24f8_fk_manytoman` \
#   FOREIGN KEY (`publication_id`) REFERENCES `manytomanyfield_publication` (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```

views.py
```python3
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

```