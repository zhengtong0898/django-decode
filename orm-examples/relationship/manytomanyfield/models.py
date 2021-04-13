from django.db import models


# Create your models here.
# 多对多 -- 关联表, 没有 Foreign Key
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


# 多对多 -- 主表, 没有 Foreign Key
# CREATE TABLE `manytomanyfield_article` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `headline` varchar(100) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


# 多对多 -- 附加表
# CREATE TABLE `manytomanyfield_article_publications` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `article_id` int(11) NOT NULL,
#   `publication_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   -- 备注: 联合索引, 提高效率
#   UNIQUE KEY `manytomanyfield_article__article_id_publication_i_459a4946_uniq` (`article_id`,`publication_id`),
#   KEY `manytomanyfield_arti_publication_id_d42f24f8_fk_manytoman` (`publication_id`),
#   -- 备注: 外键, 指向主表
#   CONSTRAINT `manytomanyfield_arti_article_id_471a4ce9_fk_manytoman` FOREIGN KEY (`article_id`) REFERENCES `manytomanyfield_article` (`id`),
#   -- 备注: 外键, 指向关联表
#   CONSTRAINT `manytomanyfield_arti_publication_id_d42f24f8_fk_manytoman` FOREIGN KEY (`publication_id`) REFERENCES `manytomanyfield_publication` (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
