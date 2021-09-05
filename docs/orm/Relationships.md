在 `Django ORM` 中, 关系的定义有三种, 它们全部都使用 `数据库` 的 `Foreign Key` 来描述和定义.  
&nbsp;    
# [One-to-one](https://docs.djangoproject.com/en/3.2/topics/db/examples/one_to_one/) 

### 对象描述
`Place` 场所名称  
`Restaurant` 餐厅服务  

并不是所有的 `Place` 都是餐厅，但是被 `Restaurant` 关联上的 `Place` 一定都是餐厅.  
从上面的模型定义来看, `Restaurant` 仅标记是否提供 `热狗` 和 `披萨` 菜品.  

### 对象关系
从 `数据库` 的角度来看, `Place`是主表, `Restaurant`是补充表.  
从 `ORM` 的角度来看, `Restaurant` 使用 `models.OneToOneField` 来绑定与 `Place` 是一对一的关系.  

### 对象约束
`One-to-one` 是 `ORM` 的概念, 它必须传递一个 `主表对象` 作为参数来约束补充表的创建和更新的操作.  
传统模式的纯`SQL`开发模式并没有这种约束限制，定义了外键后，你就是可以插入多条数据并同时只想到一个主表.  


&nbsp;  
model.py
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

> 注意事项  
> 1. onetoonefield_restaurant 表, 并不自动生成 id 自增列.  
> 2. onetoonefield_restaurant.place_id 字段, 定义为 primary key, 即: 表示不会有相同的值.  
> 3. onetoonefield_restaurant.place_id 字段, 还被定义为 foreign key, 指向 onetoonefield_place.id.  
> 
>满足这三个约束的关系, 被称为 One-to-one Relationship.

&nbsp;  
views.py
```python3
from django.shortcuts import HttpResponse
from .models import Place, Restaurant


def index(request):
    
    # INSERT INTO `onetoonefield_place` (`name`, `address`)
    # VALUES ("全家便利店", "毕升路191号")
    # RETURNING `onetoonefield_place`.`id`
    family = Place(name="全家便利店", address="毕升路191号")
    family.save()


    # Question: 为什么一个 save 会触发 update 和 insert 这两个 sql ?
    #           当提交的 value 所对应的字段是一个 foreign key,
    #           Django 将会先执行 update 然后在根据返回值决定是否要执行 insert.
    #
    #           先执行 update,
    #           如果执行失败, 那么将会执行 insert.
    #           如果执行成功, 则不会去执行 insert.
    #
    # Question: 如何判定 update 是否成功?
    #           update 会返回 effect_rows, 表明成功更新了多少条数据.
    #           当 effect_rows 大于 0 时, 表明更新成功.
    #           当 effect_rows 等于 0 时, 表明没有更新成功.
    #
    #
    # UPDATE `onetoonefield_restaurant`
    # SET    `serves_hot_dogs` = 1,
    #        `serves_pizza` = 0
    # WHERE  `onetoonefield_restaurant`.`place_id` = 1;
    #
    # INSERT INTO `onetoonefield_restaurant` (`place_id`, `serves_hot_dogs`, `serves_pizza`)
    # VALUES (1, 1, 0);
    restaurant = Restaurant(place=family, serves_hot_dogs=True, serves_pizza=False)
    restaurant.save()
```

TODO: 从主表角度查询补充表  
TODO: 从补充表角度查询主表





&nbsp;  
# [Many-to-one](examples/relationship/manytoonefield/tests.py#L11)  
  `多对一`对应在数据库中关键字是`Foreign Key`, [即主表指向到另外一张表的关联字段.](examples/relationship/manytoonefield/models.py#L17)   
  `一对多`指的是`Django ORM`提供支持, [使被关联的表可以反过来查询到主表.](examples/relationship/manytoonefield/tests.py#L63)  
  
&nbsp;  
# [Many-to-many](examples/relationship/manytomanyfield/tests.py#L11)  
  `多对多`对应在数据库中关键字是`附加表 + Foreign Key`,    
  [由`附加表`来管理`Foreign Key`, 即`附加表`指向主表和关联表](examples/relationship/manytomanyfield/models.py#L33).  
  