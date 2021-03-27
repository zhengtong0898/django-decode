### get
`db.models.query.QuerySet.get`   
该方法用于获取一条数据, 当查询到的结果是多条时会抛异常.    
> 对应的sql语句:   
> select ALL_FIELDS from TABLE limit 21;

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L16)     

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L399)

&nbsp;  
&nbsp;  
### create
`db.models.query.QuerySet.create`  
该方法用于插入一条数据.
> 对应的sql语句:   
> insert into TABLE (FIELDS) value (VALUES);

- [使用案例](../orm-examples/myqueryset/get_/tests.py#L63)  

- [源码分析](../src/Django-3.0.8/django/db/models/query.py#L451)
