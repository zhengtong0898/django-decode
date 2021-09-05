from django.db import models


# CREATE TABLE `onetoonefield_place` (                                                                 -- Django 建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `name` varchar(50) NOT NULL,
#   `address` varchar(80) NOT NULL
# );
#
#
# CREATE TABLE `onetoonefield_place` (                                                     -- 数据库连接工具查看DDL 建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(50) NOT NULL,
#   `address` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


# CREATE TABLE `onetoonefield_restaurant` (                                                            -- Django 建表语句
#   `place_id` integer NOT NULL PRIMARY KEY,
#   `serves_hot_dogs` bool NOT NULL,
#   `serves_pizza` bool NOT NULL
# );
#
# ALTER TABLE `onetoonefield_restaurant`
# ADD CONSTRAINT `onetoonefield_restau_place_id_0b11dabf_fk_onetoonef` FOREIGN KEY (`place_id`)
# REFERENCES `onetoonefield_place` (`id`);                                                          -- Django 添加外键语句
#
#
# CREATE TABLE `onetoonefield_restaurant` (                                                -- 数据库连接工具查看DDL 建表语句
#   `place_id` int(11) NOT NULL,
#   `serves_hot_dogs` tinyint(1) NOT NULL,
#   `serves_pizza` tinyint(1) NOT NULL,
#   PRIMARY KEY (`place_id`),                                                                            -- 外键声明为主键
#   CONSTRAINT `onetoonefield_restau_place_id_0b11dabf_fk_onetoonef` FOREIGN KEY (`place_id`) \
#   REFERENCES `onetoonefield_place` (`id`)                              -- place_id即是主键也是外键，这就是所谓的 one-to-one
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Restaurant(models.Model):

    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
