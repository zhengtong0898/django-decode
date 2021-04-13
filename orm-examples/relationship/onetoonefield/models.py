from django.db import models


# Create your models here.
# 生成对应的建表语句
# CREATE TABLE `onetoonefield_place` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(50) NOT NULL,
#   `address` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return "%s the place" % self.name


# 生成对应的建表语句
# 这里可以看出 OneToOneField, 其实就是一个外键.
# CREATE TABLE `onetoonefield_restaurant` (
#   `place_id` int(11) NOT NULL,
#   `serves_hot_dogs` tinyint(1) NOT NULL,
#   `serves_pizza` tinyint(1) NOT NULL,
#   PRIMARY KEY (`place_id`),
#   CONSTRAINT `onetoonefield_restau_place_id_0b11dabf_fk_onetoonef` FOREIGN KEY (`place_id`) REFERENCES `onetoonefield_place` (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Restaurant(models.Model):
    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return "%s the restaurant" % self.place.name


# 生成对应的建表语句
# CREATE TABLE `onetoonefield_waiter` (
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(50) NOT NULL,
#   `restaurant_id` int(11) NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `onetoonefield_waiter_restaurant_id_9a3d6f02_fk_onetoonef` (`restaurant_id`),
#   CONSTRAINT `onetoonefield_waiter_restaurant_id_9a3d6f02_fk_onetoonef` FOREIGN KEY (`restaurant_id`) REFERENCES `onetoonefield_restaurant` (`place_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Waiter(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s the waiter at %s" % (self.name, self.restaurant)
