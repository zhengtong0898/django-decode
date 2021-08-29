在 `Django ORM` 中, 正面的关系定义有三种  
&nbsp;
> 在 `Django ORM` 中, 使用 `Foreign Key` 来描述关系的定义.

&nbsp;  
- [ManyToOneField](examples/relationship/manytoonefield/tests.py#L11)  
  `多对一`对应在数据库中关键字是`Foreign Key`, [即主表指向到另外一张表的关联字段.](examples/relationship/manytoonefield/models.py#L17)   
  `一对多`指的是`Django ORM`提供支持, [使被关联的表可以反过来查询到主表.](examples/relationship/manytoonefield/tests.py#L63)  
  
&nbsp;  
- [ManyToManyField](examples/relationship/manytomanyfield/tests.py#L11)  
  `多对多`对应在数据库中关键字是`附加表 + Foreign Key`,    
  [由`附加表`来管理`Foreign Key`, 即`附加表`指向主表和关联表](examples/relationship/manytomanyfield/models.py#L33).  
  
&nbsp;    
- [OneToOneField](examples/relationship/onetoonefield/tests.py#L10)   
  `一对一`对应在数据库中关键字是`Foreign Key`, 从数据库建表定义中看它和`多对一`没有区别,   
  但是从`Django ORM`提供的功能来看, 它们的区别是, 被关联的表可以直接`select_related`查询到主表.   

