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
