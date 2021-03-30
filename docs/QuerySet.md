### count
`db.models.query.QuerySet.count`   
该方法采用两套统计策略:   
1. 当缓存值存在时, 返回缓存值总数;   
2. 当缓存值不存在时, 返回整表统计.

对应的sql语句
```shell
select COUNT(*) from TABLE;
```

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L107)     

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L386)


&nbsp;  
&nbsp;  
### get
`db.models.query.QuerySet.get`   
该方法用于获取一条数据, 当查询到的结果是多条时会抛异常.    


对应的sql语句
```shell
select ALL_FIELDS from TABLE limit 21;
```

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L19)     

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L399)

&nbsp;  
&nbsp;  
### create
`db.models.query.QuerySet.create`  
该方法用于插入一条数据.    

对应的sql语句:   
```shell
insert into TABLE (FIELDS) value (VALUES);
```

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L66)  

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L451)


&nbsp;  
&nbsp;  
### bulk_create
`db.models.query.QuerySet.bulk_create`  
该方法用于批量插入一组数据.

对应的sql语句:
```shell
insert into `TABLE` (FIELDS)     
values (VALUES),    
       (VALUES),   
       (VALUES);   
```

- [使用案例-1](../orm-examples/myqueryset/get_/tests.py#L147)  
- [使用案例-2](../orm-examples/myqueryset/bulk_create_/views.py#L7)  

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L469)


&nbsp;  
&nbsp;  
### bulk_update
`db.models.query.QuerySet.bulk_update`  
该方法用于批量更新一组数据.   

对应的sql语句
```shell
UPDATE `get__product` 
SET `name` =        CASE WHEN (`get__product`.`id` = 1007) THEN 'aaa-0-updated' 
                         WHEN (`get__product`.`id` = 1008) THEN 'aaa-1-updated' 
                         ELSE NULL END, 
    `description` = CASE WHEN (`get__product`.`id` = 1007) THEN 'aaa-0-updated' 
                         WHEN (`get__product`.`id` = 1008) THEN 'aaa-1-updated' 
                         ELSE NULL END 
WHERE `get__product`.`id` IN (1007, 1008)
```

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L181)

- 源码分析 TODO: 待补充


&nbsp;  
&nbsp;  
### get_or_create
`db.models.query.QuerySet.get_or_create`  
该方法用于获取一条数据, 如果数据不存在则使用`defaults` + `kwargs`参数的值来创建一条数据(后返回该数据).   
要使用这个方法, 就是已经做好了数据可能会不存在的预期, 因此就需要提供创建数据的默认值.   

对应的sql语句
```shell
# 查询
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
WHERE `get__product`.`name` = 'aaa-15'
LIMIT 21

# 插入
# mariadb >= 10.5.0 的版本支持插入返回: INSERT ... RETURNING; 
INSERT INTO `get__product` (`name`, 
                            `price`, 
                            `description`, 
                            `production_date`, 
                            `expiration_date`, 
                            `date_joined`) 
VALUES ('aaa-15', 
        '12.00', 
        'aaa-15', 
        '2001-10-10', 
        120, 
        '2021-03-28 12:20:28.121343') 
RETURNING `get__product`.`id`";
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L244)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L617)


&nbsp;  
&nbsp;  
### update_or_create
`db.models.query.QuerySet.update_or_create`  
该方法用于更新一条数据, 如果数据不存在则使用`defaults` + `kwargs`参数的值来创建一条数据(后返回该数据).   
要使用这个方法, 就是已经做好了数据可能会不存在的预期, 因此就需要提供创建数据的默认值.

对应的sql语句
```shell
# 数据存在(查询, 更新)
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
WHERE `get__product`.`name` = 'aaa-5'
LIMIT 21
FOR UPDATE

UPDATE `get__product`
SET `name` = 'aaa-5',
    `price` = '10.00',
    `description` = 'aaa-x5',
    `production_date` = '1999-10-20',
    `expiration_date` = 170,
    `date_joined` = '2021-03-28 14:11:18.417537'
WHERE `get__product`.`id` = 1033



# 数据不存在(查询, 插入)
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
WHERE `get__product`.`name` = 'aaa-15'
LIMIT 21
FOR UPDATE

INSERT INTO `get__product` (`name`,
                            `price`,
                            `description`,
                            `production_date`,
                            `expiration_date`,
                            `date_joined`)
VALUES ('aaa-15',
        '12.00',
        'aaa-15',
        '2001-10-10',
        120,
        '2021-03-28 14:15:17.710272')
```  
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L296)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L640)


&nbsp;  
&nbsp;  
### earliest
`db.models.query.QuerySet.earliest`  
按指定字段, 正向排序, 提取第一条数据(即: 最早的一条数据).   

对应的sql语句
```shell
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
ORDER BY `get__product`.`production_date` ASC               # 按给定字段正向排序
LIMIT 1                                                     # 只提取第一条数据
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L386)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L754)

&nbsp;  
&nbsp;  
### latest
`db.models.query.QuerySet.latest`  
按指定字段, 反向排序, 提取第一条数据(即: 最晚的一条数据).   

对应的sql语句
```shell
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
ORDER BY `get__product`.`production_date` DESC        # 按给定字段反向排序
LIMIT 1                                               # 只提取第一条数据
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L416)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L758)


&nbsp;  
&nbsp;  
### first   
`db.models.query.QuerySet.first`     
基于已排序的`QuerySet`容器中提取第一条数据(这种方式不查询数据库).  
`QuerySet`未排序时, 调用本方法, 将会再次查询数据库(附加上按 pk 字段正向排序, 以及只取一条数据).  
如果不提供`QuerySet`, 而是直接调用本方法, 将会按 pk 字段正向排序, 然后提取第一条数据.   

对应的sql语句
```shell
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
ORDER BY `get__product`.`id` ASC                      # 按 pk 字段正向排序
LIMIT 1                                               # 提取第一条数据
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L446)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L768)


&nbsp;  
&nbsp;  
### last
`db.models.query.QuerySet.last`   
与 [first](./QuerySet.md#first) 概念一致, 唯一的区别在于`last`排序是按 pk 字段反向排序.  

对应的sql语句
```shell
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
ORDER BY `get__product`.`id` DESC                 # 按 pk 字段反向排序
LIMIT 1                                           # 提取第一条数据
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L497)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L787)

&nbsp;  
> earlist 和 first 有什么区别?    
>
> earlist 要求提供排序字段, 当查询的数据集未空时, 报错.   
> 
> first 不要求提供排序字段, 当查询的数据集为空时, 不报错, 返回 None.   
> first 支持再任何已排序的 `QuerySet` 的基础上, 提取第一条数据.   
> first 补充支持, 如果没有提供queryset那么就按照pk来正向排序, 然后提取第一个元素. 

&nbsp;  
&nbsp;  
### in_bulk
`db.models.query.QuerySet.in_bulk(self, id_list=None, *, field_name='pk')`   
该方法用于批量获取一组数据.

参数说明:      
- `field_name`  
  默认值是'pk', 如果需要提供其他值, 那么该值必须是 `unique` 类型字段名.
- `id_list`  
  当参数值是`None`时, 整表查询.  
  当参数值时`[]`或`False`时, 返回空字典.
  当参数值时有效值时, 对 `field_name` 字段做 `in` 操作来匹配 `id_list`. 

对应的sql语句
```shell
# product.objects.in_bulk(id_list=[1,2,3], field_name='pk')
SELECT `get__product`.`id`,
       `get__product`.`name`,
       `get__product`.`price`,
       `get__product`.`description`,
       `get__product`.`production_date`,
       `get__product`.`expiration_date`,
       `get__product`.`date_joined`
FROM `get__product`
WHERE `get__product`.`id` IN (1, 2, 3)            # pk in (1, 2, 3)
```
- [使用案例](../orm-examples/myqueryset/get_/tests.py#L536)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L796)


&nbsp;  
&nbsp;  
### delete
`db.models.query.QuerySet.delete(self)`   
该方法用于删除一条或多条数据.   
该方法只能作用在`QuerySet`对象上, 即: 那些已经写好过滤条件的`QuerySet`对象.  

对应的sql语句:
```shell
$ 情况一:
# Django知道 brand 这张表被引用了(referenced),
# 所以在删除 brand 的数据之前, 需要:
# 1. 先查询当前数据
# 2. 拿查询出来的结果的id, 去尝试删除引用表与
#    外键值一致的那条些(可能是一条也可能是多条)数据.
# 3. 拿查询出来的结果的id, 去尝试删除brand的数据.

# 1. 查询
SELECT `delete__brand`.`id`,
       `delete__brand`.`name`,
       `delete__brand`.`description`
FROM `delete__brand`
WHERE `delete__brand`.`id` = 1

# 2. 删除子表指定数据
DELETE FROM `delete__product`
WHERE `delete__product`.`brand_id_id` IN (1)

# 3. 删除父表指定数据
DELETE FROM `delete__brand`
WHERE `delete__brand`.`id` IN (1)



# 情况二:
# Django知道product这张表没有被引用(referenced),
# 所以不需要先查询在删除, 而是直接删除.
DELETE FROM `delete__product`
WHERE `delete__product`.`id` = 2'
```

- [使用案例](../orm-examples/myqueryset/delete_/tests.py#L9)

- 源码分析 TODO: 待补充


&nbsp;  
&nbsp;  
### update
`db.models.query.QuerySet.update(self, **kwargs)`   
该方法根据当前的`QuerySet`对象中的`filter`条件, 根据参数`kwargs`来组装成sql, 然后提交给数据库去执行更新.    

对应的sql语句:
```shell
# filter(expiration_date=170) 不会提交数据库做查询, 而是将过滤条件写入到 QuerySet中,    
# update(description="bbbb") 先将更新参数写入到QuerySet中, 最后执行execute_sql,
# execute_sql 会将 QuerySet 中所有属性拼装成一个有效的sql, 提交给数据库去执行. 
# rows = product.objects.filter(expiration_date=170).update(description="bbbb")

UPDATE `get__product`
SET `description` = 'bbbb'
WHERE `get__product`.`expiration_date` = 170
```

- [使用案例](../orm-examples/myqueryset/delete_/tests.py#L77)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L886)


&nbsp;  
&nbsp;  
### exists
`db.models.query.QuerySet.exists(self)`  
该方法通过检查`QuerySet._result_cache`缓存集合, 当有值时返回`True`.   
当没有值时, `exists`会根据 `QuerySet` 中标记好的`filter`条件到数据库中去查询数据, 并返回相应的结果(`bool`类型).   

对应的sql语句
```shell
# pp = product.objects.filter(pk=99).exists()


SELECT (1) AS `a`
FROM `delete__product`
WHERE `delete__product`.`id` = 99
LIMIT 1
```
- [使用案例](../orm-examples/myqueryset/delete_/tests.py#L103)

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L927)

