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

- 源码分析 TODO


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
