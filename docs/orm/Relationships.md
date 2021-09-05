在 `Django ORM` 中, 关系的定义有三种, 它们全部都使用 `数据库` 的 `Foreign Key` 来描述和定义.  
&nbsp;    
# [One-to-one](examples/relationship/onetoonefield/tests.py#L10)   

    # 仔细观察上面的建表语句, 发现:
    # 1. onetoonefield_restaurant 表, 并不自动生成 id 自增列.
    # 2. 使用 CONSTRAINT FOREIGN KEY 将 onetoonefield_restaurant.place_id 和  onetoonefield_place.id 进行绑定, 一一对应.

`一对一`对应在数据库中关键字是`Foreign Key`, 从数据库建表定义中看它和`多对一`没有区别,   
但是从`Django ORM`提供的功能来看, 它们的区别是, 被关联的表可以直接`select_related`查询到主表.

`一对一`关系的定义通常是由 `从表` 链向 `主表`, 即: `从表` 是对 `主表` 进行字段上的补充.  
`一对一`呈现在数据库建表语句上的表现是:
    <div style="padding-left:40px">1. 没有自增id列;</div> 
    <div style="padding-left:40px">2. ;</div> 

```python3
from django.db import models


# CREATE TABLE `onetoonefield_place` (                                                              # Django-建表语句
#   `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
#   `name` varchar(50) NOT NULL,
#   `address` varchar(80) NOT NULL
# );
#
#
# CREATE TABLE `onetoonefield_place` (                                                   # 数据库连接工具查看DDL-建表语句
#   `id` int(11) NOT NULL AUTO_INCREMENT,
#   `name` varchar(50) NOT NULL,
#   `address` varchar(80) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


# CREATE TABLE `onetoonefield_restaurant` (                                                         # Django-创建语句
#   `place_id` integer NOT NULL PRIMARY KEY,
#   `serves_hot_dogs` bool NOT NULL,
#   `serves_pizza` bool NOT NULL
# );
# ALTER TABLE `onetoonefield_restaurant`
# ADD CONSTRAINT `onetoonefield_restau_place_id_0b11dabf_fk_onetoonef` FOREIGN KEY (`place_id`)
# REFERENCES `onetoonefield_place` (`id`);
#
#
# CREATE TABLE `onetoonefield_restaurant` (                                             # 数据库连接工具查看DDL-建表语句
#   `place_id` int(11) NOT NULL,
#   `serves_hot_dogs` tinyint(1) NOT NULL,
#   `serves_pizza` tinyint(1) NOT NULL,
#   PRIMARY KEY (`place_id`),
#   CONSTRAINT `onetoonefield_restau_place_id_0b11dabf_fk_onetoonef` FOREIGN KEY (`place_id`) \
#   REFERENCES `onetoonefield_place` (`id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
class Restaurant(models.Model):

    place = models.OneToOneField(
        Place,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)
```




&nbsp;  
# [Many-to-one](examples/relationship/manytoonefield/tests.py#L11)  
  `多对一`对应在数据库中关键字是`Foreign Key`, [即主表指向到另外一张表的关联字段.](examples/relationship/manytoonefield/models.py#L17)   
  `一对多`指的是`Django ORM`提供支持, [使被关联的表可以反过来查询到主表.](examples/relationship/manytoonefield/tests.py#L63)  
  
&nbsp;  
# [Many-to-many](examples/relationship/manytomanyfield/tests.py#L11)  
  `多对多`对应在数据库中关键字是`附加表 + Foreign Key`,    
  [由`附加表`来管理`Foreign Key`, 即`附加表`指向主表和关联表](examples/relationship/manytomanyfield/models.py#L33).  
  