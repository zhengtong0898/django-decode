from django.db import models


# CREATE TABLE `manytoonefield_reporter` (
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `first_name` varchar(30) NOT NULL,
#   `last_name` varchar(30) NOT NULL,
#   `email` varchar(254) NOT NULL
# );
#
#
#
class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()


# CREATE TABLE `manytoonefield_article` (
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
# CREATE TABLE `manytoonefield_article` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,                                                         -- django自动补充该字段
#   `headline` varchar(100) NOT NULL,
#   `pub_date` date NOT NULL,
#   `reporter_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),                                                                                -- 主键(聚集索引)
#   KEY `manytoonefield_artic_reporter_id_01692140_fk_manytoone` (`reporter_id`),                           -- 普通索引
#   CONSTRAINT `manytoonefield_artic_reporter_id_01692140_fk_manytoone` FOREIGN KEY (`reporter_id`) \
#   REFERENCES `manytoonefield_reporter` (`id`)                                                             -- 外键索引
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)                                    # Many-to-one
