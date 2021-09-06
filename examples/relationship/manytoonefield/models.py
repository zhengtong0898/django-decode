from django.db import models


# CREATE TABLE `manytoonefield_reporter` (                                                             -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `first_name` varchar(30) NOT NULL,
#   `last_name` varchar(30) NOT NULL,
#   `email` varchar(254) NOT NULL
# );
#
#
# CREATE TABLE `manytoonefield_reporter` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,                                                   -- django自动补充该字段, 自增ID
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
# REFERENCES `manytoonefield_reporter` (`id`)                                                       -- Django 添加外键语句
#
#
# Question: 辅助索引与外键有什么区别?
#           https://stackoverflow.com/questions/1732467/what-is-the-difference-between-an-index-and-a-foreign-key
#           辅助索引的内部是一个b+树的数据结构, 对于随机查询起到加速的作用.
#           外键仅仅是对只想其他表的主键.
# CREATE TABLE `manytoonefield_article` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,                                                   -- django自动补充该字段, 自增ID
#   `headline` varchar(100) NOT NULL,
#   `pub_date` date NOT NULL,
#   `reporter_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),                                                                                  -- 主键(聚集索引)
#   KEY `manytoonefield_artic_reporter_id_01692140_fk_manytoone` (`reporter_id`),                             -- 辅助索引
#   CONSTRAINT `manytoonefield_artic_reporter_id_01692140_fk_manytoone` FOREIGN KEY (`reporter_id`) \
#   REFERENCES `manytoonefield_reporter` (`id`)                                                               -- 外键索引
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)                                    # Many-to-one
