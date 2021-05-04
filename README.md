
&nbsp;  
### 源码分析
`Django-3.0.8`源码分析, 系统`win10 64位`, IDE`pycharm community 2019`, 语言`python3.8`    

|模块|源码|
|:---:|:---:|
|WSIG|[Django框架与WSGI接口的关系](docs/contrib/wsgi.md)|
|`django.contrib.auth`|[路由](docs/contrib/auth/router.md)、[数据流向](docs/contrib/auth/dataflow.md)、[表单工作流](docs/contrib/auth/form.md)、[登录功能](docs/contrib/auth/login.md)、[登出功能](docs/contrib/auth/logout.md)|
|autoreload|[核心原理](docs/autoreload/第1部分-核心原理.md) 、 [Signal](docs/autoreload/第2部分-Signal.md) 、 [两个进程](docs/autoreload/第3部分-两个进程.md)  、[两个线程](docs/autoreload/第4部分-两个线程.md)  、[Watchman](docs/autoreload/第5部分-Watchman.md)  、[响应式开发](docs/autoreload/第6部分-响应式开发.md)|
|migration|待补充|



&nbsp;  
&nbsp;   
### Debug困扰清单
- \_\_len\_\_ 和 \_\_str\_\_ 和 \_\_repr\_\_    
  很多时候在调试代码时, `Step Into` 明明没有执行任何代码, 
  但是`Console` 仍然是有在打印相关的内容.   
  
  例如: `django.db.models.query.QuerySet`对象, 
  当调试到 `QuerySet` 赋值给某变量后;   
  
  由于编辑器要把该变量显示到 Debugger 控制台上, 
  编辑器会触发它的   
  `__len__` 和 `__repr__` 和 `__str__` 方法来拿到具体的对象信息.     
  
  也正由于`QuerySet`内部实现了 `__len__`, 其内部引用了 `self._fetch_all`,   
  导致了它会对数据库执行查询操作, 因此会打印出一些查询相关的日志输出.   
  
  所以那些没有`step by step`进入到源码的执行, 就不会乱打印东西, 也不会重复执行sql.   
  
  所以当需要调试一个对象, 观察它的`SQL`语句的运行流程时, 千万不要`Debug`, 
  最好的做法是通过代码块的头尾部增加日志打印出常量字符串来观察.  
  

&nbsp;  
&nbsp;  
### 如何将orm操作的sql语句打印出来?
- 方案一: 编辑`Django`源码
  > 编辑 Lib/site-packages/django/db/models/sql/compiler.py 文件
  ```python
  # 在文件头部导入logging
  import logging
  logger = logging.getLogger('django.compiler')
  
  
  class SQLCompiler:
   
      def execute_sql(self, result_type=MULTI, chunked_fetch=False, 
                      chunk_size=GET_ITERATOR_CHUNK_SIZE):
          sql_info = sql % tuple(params)          # 在这里添加这行代码
          logger.info("sql: %s" % sql_info)       # 在这里添加这行代码
          cursor.execute(sql, params)             
  
  
  class SQLInsertCompiler(SQLCompiler):
      
      def execute_sql(self, returning_fields=None):
          sql_info = sql % tuple(params)          # 在这里添加这行代码
          logger.info("sql: %s" % sql_info)       # 在这里添加这行代码
          cursor.execute(sql, params)        
  ```
- 方案二: 编辑三方库(`pymysql`)源码
  > 编辑 Lib/site-packages/pymysql/connections.py 文件
  ```python
  class Connection:

      def _execute_command(self, command, sql):
          print("pymysql: command: %s; sql: %s;" % (command, sql))        # 在第一行加入这行代码
  ```

&nbsp;  
&nbsp;  
### ORM关系操作背后的SQL语句观察
在关系型数据库的哲学中绕不开的就是关系, 而关系主要体现在对`Foreign Key`的不同应用上.    
- [ManyToOneField](examples/relationship/manytoonefield/tests.py#L11)  
  `多对一`对应在数据库中关键字是`Foreign Key`, [即主表指向到另外一张表的关联字段.](examples/relationship/manytoonefield/models.py#L27)   
  `一对多`指的是`Django ORM`提供支持, [使被关联的表可以反过来查询到主表.](examples/relationship/manytoonefield/tests.py#L63)    

- [ManyToManyField](examples/relationship/manytomanyfield/tests.py#L11)  
  `多对多`对应在数据库中关键字是`附加表 + Foreign Key`,    
  [由`附加表`来管理`Foreign Key`, 即`附加表`指向主表和关联表](examples/relationship/manytomanyfield/models.py#L33).
  
- [OneToOneField](examples/relationship/onetoonefield/tests.py#L10)   
  `一对一`对应在数据库中关键字是`Foreign Key`, 从数据库建表定义中看它和`多对一`没有区别,   
  但是从`Django ORM`提供的功能来看, 它们的区别是, 被关联的表可以直接`select_related`查询到主表.   


&nbsp;  
&nbsp;  
### Django Admin 操作清单
- BaseModelAdmin

  | 属性 | 描述 | 位置 |
  |---|:---:| :---: |
  |autocompelete_fields = ()| [让外键下拉菜单支持搜索功能](./docs/BaseModelAdmin.md#autocompelete_fields) | 新增、编辑页面 |
  |raw_id_fields = ()| [将下拉菜单替换成文本输入框](./docs/BaseModelAdmin.md#raw_id_fields) | 新增、编辑页面 |
  |fields = None| [表单字段排版](./docs/BaseModelAdmin.md#fields) | 新增、编辑页面 |
  |exclude = None| [表单中排除字段](./docs/BaseModelAdmin.md#exclude) | 新增、编辑页面 |
  |fieldsets = None| [表单字段排版(支持分组)](./docs/BaseModelAdmin.md#fieldsets) | 新增、编辑页面 |
  |form = forms.ModelForm |   | - |
  |filter_vertical = ()| [多对多字段的表单纵向控件装饰](./docs/BaseModelAdmin.md#filter_vertical) | 新增、编辑页面 |
  |filter_horizontal = ()| [多对多字段的表单横向控件装饰](./docs/BaseModelAdmin.md#filter_horizontal) | 新增、编辑页面 |
  |radio_fields = {}|  [将下拉菜单替换成radio控件](./docs/BaseModelAdmin.md#radio_fields) | 新增、编辑页面 |
  |prepopulated_fields = {}| [自动填值功能(需配合slugField字段)](./docs/BaseModelAdmin.md#prepopulated_fields)  | 新增、编辑页面 |
  |formfield_overrides = {}| [表单字段控件替换](./docs/BaseModelAdmin.md#formfield_overrides) | 新增、编辑页面 |
  |readonly_fields = ()|  [只读字段](./docs/BaseModelAdmin.md#readonly_fields) |新增、编辑、`change`列表页面 |
  |ordering = None| [按给定的字段排序显示数据](./docs/BaseModelAdmin.md#ordering)  | `change`列表页面 |
  |sortable_by = None| [仅允许指定字段头拥有排序功能](./docs/BaseModelAdmin.md#sortable_by)  | `change`列表页面 |
  |view_on_site = True| [快捷跳转到于该数据象关的页面hook](./docs/BaseModelAdmin.md#view_on_site) | 编辑页面 |
  |show_full_result_count = True| [搜索右侧计数器的总合数字](./BaseModelAdmin.md#show_full_result_count) | `change`列表页面 |
  |checks_class = BaseModelAdminChecks |  | - |

- ModelAdmin   

  | 属性 | 描述 | 位置 |
  |---|:---:| :---: |
  |list_display = ('\_\_str\_\_',) | [控制字段显示](./docs/ModelAdmin.md#list_display) | `change`列表页面 | 
  |list_display_links = () | [将编辑数据的链接显示在指定字段](./docs/ModelAdmin.md#list_display_links) | `change`列表页面 |
  |list_filter = () | [按分类筛选](./docs/ModelAdmin.md#list_filter) | `change`列表页面 |
  |list_select_related = False | [是否查询关联表](./docs/ModelAdmin.md#list_select_related) | `change`列表页面 | 
  |list_per_page = 100 | [每页显示几行数据](./docs/ModelAdmin.md#list_per_page) | `change`列表页面 |
  |list_max_show_all = 200 | [`show_all`链接显示几行数据](./docs/ModelAdmin.md#list_per_page) | `change`列表页面 |
  |list_editable = () | [同时编辑多行数据](./docs/ModelAdmin.md#list_editable) | `change`列表页面 |
  |search_fields = () | [指定模糊查询字段](./docs/ModelAdmin.md#search_fields) | `change`列表页面 |
  |date_hierarchy = None | [时间分层器](./docs/ModelAdmin.md#date_hierarchy) | `change`列表页面 |
  |save_as = False | [用编辑的表单数据创建新数据](./docs/ModelAdmin.md#save_as)| 编辑页面 |
  |save_as_continue = True | [是否跳转回列表页面](./docs/ModelAdmin.md#save_as_continue)| 编辑页面 |
  |save_on_top = False | [表单上方显示按钮保存栏](./docs/ModelAdmin.md#save_on_top)| 编辑页面 |
  |paginator = Paginator | | - |
  |preserve_filters = True | [保留搜索内容](./docs/ModelAdmin.md#preserve_filters)| `change`列表页面 |
  |inlines = [] | [关联表数据展示](./docs/ModelAdmin.md#inlines) | 编辑页面 |
  | | | -|
  |add_form_template = None| | -|
  |change_form_template = None| | -|
  |change_list_template = None| | -|
  |delete_confirmation_template = None| | -|
  |delete_selected_confirmation_template = None| | -|
  |object_history_template = None| | -|
  |popup_response_template = None| | -|
  | | -|
  |actions = []| [批量更新字段](./docs/ModelAdmin.md#actions) | `change`列表页面 |
  |action_form = helpers.ActionForm| | - |
  |actions_on_top = True| [批量操作栏目位置](./docs/ModelAdmin.md#actions_on_top) | `change`列表页面 |
  |actions_on_bottom = False| [批量操作栏目位置](./docs/ModelAdmin.md#actions_on_top) | `change`列表页面 |
  |actions_selection_counter = True| [批量操作右侧已选中计数器](./docs/ModelAdmin.md#actions) | `change`列表页面 |
  |checks_class = ModelAdminChecks| | - |


&nbsp;  
&nbsp;  
### Django Model 操作清单 
- db.models.query.QuerySet  
  `Django ORM`中, 所有的查询都要通过`QuerySet`对象来完成, 
  包括常见的 `objects` 其实也是一个 `QuerySet` 对象.
  
  | 属性 | 描述 |
  |---| :---: |
  | self.model = model | 数据库模型对象 |
  | self._db = using | 默认值'default'(DATABASES的key) |
  | self._hints = hints or {} | |
  | self._query = query or sql.Query(self.model) | [`raw sql`语法生成器对象](./src/Django-3.0.8/django/db/models/sql/query.py#L146) |
  | self._result_cache = None | 查询结果缓存集合 |
  | self._sticky_filter = False | |
  | self._for_write = False | 是否标记为写状态 |
  | self._prefetch_related_lookups = () | 预查询多对多字段暂存列表 |
  | self._prefetch_done = False | 标记为缓存状态 |
  | self._known_related_objects = {}  # {rel_field: {pk: rel_obj}} | |
  | self._iterable_class = ModelIterable | |
  | self._fields = None | |
  | self._defer_next_filter = False | |
  | self._deferred_filter = None | |
  | | - |
  |def iterator(self, chunk_size=2000)| |
  |def aggregate(self, *args, **kwargs)| [聚合查询](./docs/QuerySet.md#aggregate) |
  |def count(self)| [统计总数](./docs/QuerySet.md#count) |
  |def get(self, *args, **kwargs)| [获取一条数据](./docs/QuerySet.md#get) |
  |def create(self, **kwargs)| [插入一条数据](./docs/QuerySet.md#create) |
  |def bulk_create(self, objs, batch_size=None, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ignore_conflicts=False)| [批量插入数据](./docs/QuerySet.md#bulk_create) |
  |def bulk_update(self, objs, fields, batch_size=None)| [批量更新数据](./docs/QuerySet.md#bulk_update) |
  |def get_or_create(self, defaults=None, **kwargs)| [获取不到数据则创建数据](./docs/QuerySet.md#get_or_create) |
  |def update_or_create(self, defaults=None, **kwargs)| [更新不到数据则创建数据](./docs/QuerySet.md#update_or_create) |
  |def earliest(self, *fields)| [按指定字段正向排序并提取最早(远)一条](./docs/QuerySet.md#earliest) |
  |def latest(self, *fields)| [按指定字段反向排序并提取最晚(近)一条](./docs/QuerySet.md#latest) |
  |def first(self)| [获取第一条数据](./docs/QuerySet.md#first) |
  |def last(self)| [获取最后一条数据](./docs/QuerySet.md#last) |
  |def in_bulk(self, id_list=None, *, field_name='pk')| [批量获取一组数据](./docs/QuerySet.md#in_bulk) |
  |def delete(self)| [删除一条或多条数据](./docs/QuerySet.md#delete) |
  |def update(self, **kwargs)| [更新一条或多条数据](./docs/QuerySet.md#update) |
  |def exists(self)| [数据是否存在](./docs/QuerySet.md#exists) |
  |def explain(self, *, format=None, **options)| [查询执行计划](./docs/QuerySet.md#explain) |
  |def raw(self, raw_query, params=None, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; translations=None, using=None) | [执行自定义SQL语句](./docs/QuerySet.md#raw) |
  |def values(self, *fields, **expressions) | [获取基于模型字段的字典-键值](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.values) |
  |def values_list(self, *fields, flat=False, named=False) |[获取基于模型字段的列表-仅值](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.values_list) |
  |def dates(self, field_name, kind, order='ASC') | [获取一组数据的时间(精确到天)](./docs/QuerySet.md#dates) |
  |def datetimes(self, field_name, kind, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; order='ASC', tzinfo=None, is_dst=None) | [获取一组数据的时间(精确到秒)](./docs/QuerySet.md#datetimes) |
  |def none(self) | [获取一个空的`QuerySet`](./docs/QuerySet.md#none) |
  |def filter(self, *args, **kwargs) | [使用实参提供过滤条件组合](./docs/QuerySet.md#filter) |
  |def exclude(self, *args, **kwargs) | [过滤条件组合的反向获取](./docs/QuerySet.md#exclude) |
  |def union(self, *other_qs, all=False) | [合并多组字段数量相同的数据集](./docs/QuerySet.md#union) |
  |def select_for_update(self, nowait=False, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; skip_locked=False, of=()) | [锁行或锁表来更新数据](./docs/QuerySet.md#select_for_update) |
  |def select_related(self, *fields) | [把指定外键字段一次性查询出来](./docs/QuerySet.md#select_related) |
  |def prefetch_related(self, *lookups) | [把指定多对多字段一次性查询出来](./docs/QuerySet.md#prefetch_related) |
  |def annotate(self, *args, **kwargs) | [通过注解定义字段的聚合处理](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate) |
  |def order_by(self, *field_names) | [按指定字段排序](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.annotate) |
  |def distinct(self, *field_names) | [按指定字段去重](./docs/QuerySet.md#distinct) |
  |def extra(self, select=None, where=None, params=None, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; tables=None, order_by=None, select_params=None) | [复杂查询条件扩展支持](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.extra) |
  |def reverse(self) |  |
  |def defer(self, *fields) | [排除字段](./docs/QuerySet.md#defer) |
  |def only(self, *fields) | [仅选字段](./docs/QuerySet.md#only) |
  |def using(self, alias) | [多库时, 指定某个数据库来查询](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#using) |


&nbsp;  
&nbsp;  
### 牛客网SQL练习
| 题号 | 题目 | 关键词 |
| :---: | :---: | ---: |
|SQL1|[查找最晚入职员工的所有信息](./examples/nowcoder/README.md#SQL1)| 嵌套, extra, subquery |
|SQL2|[查找入职员工时间排名倒数第三的员工所有信息](./examples/nowcoder/README.md#SQL2)| limit offset |
|SQL3|[查找各个部门当前领导当前薪水详情以及其对应部门编号dept_no](./examples/nowcoder/README.md#SQL3)| left join |
|SQL4|[查找所有已经分配部门的员工的last_name和first_name](./examples/nowcoder/README.md#SQL4)| left join |
|SQL5|[查找所有员工的last_name和first_name以及对应部门编号dept_no](./examples/nowcoder/README.md#SQL5)| left join |
|SQL7|[查找薪水涨幅超过15次的员工号emp_no以及其对应的涨幅次数t](./examples/nowcoder/README.md#SQL7)| `group by`, `having`, `count` |
|SQL8|[找出所有员工当前具体的薪水salary情况](./examples/nowcoder/README.md#SQL8)| `group by`, `order by` |
|SQL10|[获取所有非manager的员工emp_no](./examples/nowcoder/README.md#SQL10)| `left join` |
|SQL11|[获取所有员工当前的manager](./examples/nowcoder/README.md#SQL11)| `left join`, `<>` |
|SQL12|[获取所有部门中当前员工薪水最高的相关信息](./examples/nowcoder/README.md#SQL12)| `left join`, `inner join`, `生成临时表` |
|SQL15|[查找employees表所有emp_no为奇数](./examples/nowcoder/README.md#SQL15)| `mod取余求奇偶` |
|SQL16|[统计出当前各个title类型对应的员工当前薪水对应的平均工资](./examples/nowcoder/README.md#SQL16)| `avg`, `group by`, `inner join` |
|SQL17|[获取当前薪水第二多的员工的emp_no以及其对应的薪水salary](./examples/nowcoder/README.md#SQL17)| `limit`, `offset` |
|SQL18|[查找当前薪水排名第二多的员工编号emp_no](./examples/nowcoder/README.md#SQL18)| `subquery`, `subquery`, `subquery` |
|SQL19|[查找所有员工的last_name和first_name以及对应的dept_name](./examples/nowcoder/README.md#SQL19)| `left join`, `left join`, `left join` |
|SQL21|[查找所有员工自入职以来的薪水涨幅情况](./examples/nowcoder/README.md#SQL21)| - |
|SQL22|[统计各个部门的工资记录数](./examples/nowcoder/README.md#SQL22)| - |
|SQL23|[对所有员工的当前薪水按照salary进行按照1-N的排名](./examples/nowcoder/README.md#SQL23)| `subquery`, `dense_rank`, `distinct`, `count` |
|SQL24|[获取所有非manager员工当前的薪水情况](./examples/nowcoder/README.md#SQL24)| `subquery`, `inner join`, `不能用left join` |
|SQL25|[获取员工其当前的薪水比其manager当前薪水还高的相关信息](./examples/nowcoder/README.md#SQL25)|  |
|SQL26|[汇总各个部门当前员工的title类型的分配数目](./examples/nowcoder/README.md#SQL26)| `group by 多字段联合分组` |
|SQL28|[查找描述信息中包括robot的电影对应的分类名称以及电影数目](./examples/nowcoder/README.md#SQL28)| `having count` |
|SQL29|[使用join查询方式找出没有分类的电影id以及名称](./examples/nowcoder/README.md#SQL29)| `强调 left join 的必要性` |
|SQL30|[使用子查询的方式找出属于Action分类的所有电影对应的title,description](./examples/nowcoder/README.md#SQL30)| `subquery` |
|SQL32|[将employees表的所有员工的last_name和first_name拼接起来作为Name，中间以一个空格区分](./examples/nowcoder/README.md#SQL32)| `concat字符串拼接` |
|SQL33|[创建一个actor表，包含如下列信息](./examples/nowcoder/README.md#SQL33)| `create table` |
|SQL34|[批量插入数据](./examples/nowcoder/README.md#SQL34)| `insert into` |
|SQL35|[批量插入数据,如果数据已经存在，请忽略，不使用replace操作](./examples/nowcoder/README.md#SQL35)| `insert into select` |
|SQL36|[创建一个actor_name表，将actor表中的所有first_name以及last_name导入改表](./examples/nowcoder/README.md#SQL36)|  |
|SQL37|[对first_name创建唯一索引uniq_idx_firstname，对last_name创建普通索引idx_lastname](./examples/nowcoder/README.md#SQL37)| `alter table add unique index`  |
|SQL38|[针对actor表创建视图actor_name_view](./examples/nowcoder/README.md#SQL38)| `create view` |
|SQL39|[针对上面的salaries表emp_no字段创建索引idx_emp_no，查询emp_no为10005,](./examples/nowcoder/README.md#SQL39)| `force index` |
|SQL40|[在last_update后面新增加一列名字为create_date](./examples/nowcoder/README.md#SQL40)| `alter table add column` |
|SQL41|[构造一个触发器audit_log，在向employees表中插入一条数据的时候，触发插入相关的数据到audit中](./examples/nowcoder/README.md#SQL41)| `create trigger` |
|SQL42|[删除emp_no重复的记录，只保留最小的id对应的记录。](./examples/nowcoder/README.md#SQL42)| `delete from`, `回避iterator问题` |
|SQL43|[将所有to_date为9999-01-01的全部更新为NULL,且](./examples/nowcoder/README.md#SQL43)| `update` |
|SQL44|[将id=5以及emp_no=10001的行数据替换成id=5以及emp_no=10005,其他数据保持不变，使用replace实现。](./examples/nowcoder/README.md#SQL44)| `replace into` |
|SQL45|[将titles_test表名修改为titles_2017](./examples/nowcoder/README.md#SQL45)| `rename table` `表重命名` |
|SQL46|[在audit表上创建外键约束，其emp_no对应employees_test表的主键id](./examples/nowcoder/README.md#SQL46)| `alter table add foreign key` |
|SQL48|[将所有获取奖金的员工当前的薪水增加10%](./examples/nowcoder/README.md#SQL48)| `salary * percentage` |
|SQL50|[将employees表中的所有员工的last_name和first_name通过(')连接起来。](./examples/nowcoder/README.md#SQL50)|  |
|SQL51|[查找字符串'10,A,B'](./examples/nowcoder/README.md#SQL51)| `relace` `length` `计数` |
|SQL52|[获取Employees中的first_name，查询按照first_name最后两个字母，按照升序进行排列](./examples/nowcoder/README.md#SQL52)| `order by` `substr` |
|SQL53|[按照dept_no进行汇总，属于同一个部门的emp_no按照逗号进行连接，结果给出dept_no以及连接出的结果employees](./examples/nowcoder/README.md#SQL53)| `group by` `group_concat`|
|SQL54|[查找排除当前最大、最小salary之后的员工的平均工资avg_salary](./examples/nowcoder/README.md#SQL54)| `sum` `max` `min` `count` |
|SQL55|[分页查询employees表，每5行一页，返回第2页的数据](./examples/nowcoder/README.md#SQL55)| `limit` `offset` |
|SQL57|[使用含有关键字exists查找未分配具体部门的员工的所有信息。](./examples/nowcoder/README.md#SQL57)| `not exists` |
|SQL59|[获取有奖金的员工相关信息。](./examples/nowcoder/README.md#SQL59)| `CASE WHEN` |
|SQL60|[统计salary的累计和running_total](./examples/nowcoder/README.md#SQL60)| `set @variable` `sum over` |
|SQL61|[对于employees表中，给出奇数行的first_name](./examples/nowcoder/README.md#SQL61)| `row_number over` `rank % 2 求奇` |
|SQL62|[出现三次以上相同积分的情况](./examples/nowcoder/README.md#SQL62)| `group by` `having` |
|SQL63|[刷题通过的题目排名](./examples/nowcoder/README.md#SQL63)| `dense_rank` `order by col_1, col_2` |
|SQL64|[找到每个人的任务](./examples/nowcoder/README.md#SQL64)| `left join` |
|SQL65|[异常的邮件概率](./examples/nowcoder/README.md#SQL65)| `round` `sum` `if` `case when` `count`  |
|SQL66|[牛客每个人最近的登录日期(一)](./examples/nowcoder/README.md#SQL66)| `group by` `max`  |
|SQL67|[牛客每个人最近的登录日期(二)](./examples/nowcoder/README.md#SQL67)| `subquery` `left join` `inner join` |
|SQL68|[牛客每个人最近的登录日期(三)](./examples/nowcoder/README.md#SQL68)| `round` `date_add` `subquery` `left join` |
|SQL69|[牛客每个人最近的登录日期(四)](./examples/nowcoder/README.md#SQL69)| `subquery` `left join` `group by` |
|SQL70|[牛客每个人最近的登录日期(五)](./examples/nowcoder/README.md#SQL70)| `union` `subquery` `left join` `group by` |
|SQL71|[牛客每个人最近的登录日期(六)](./examples/nowcoder/README.md#SQL71)| `sum() over(partition by xx order by xx)` |
|SQL72|[考试分数(一)](./examples/nowcoder/README.md#SQL72)| `group by` `order by xx desc` `round` `avg` |
|SQL73|[考试分数(二)](./examples/nowcoder/README.md#SQL73)| `group by` `order by xx desc` `round` `avg` `inner join` |
|SQL74|[考试分数(三)](./examples/nowcoder/README.md#SQL74)| `subquery` `dense_rank over(partition by xx order by xx)` `inner join` |
|SQL75|[考试分数(四)](./examples/nowcoder/README.md#SQL75)| `case when` |
|SQL76|[考试分数(五)](./examples/nowcoder/README.md#SQL76)| `rank() over(partition by xx order by xx)` `dense_rank() over(partition by xx order by xx)` `row_number() over(partition by xx order by xx)` `subquery` `inner join` |
|SQL77|[牛客的课程订单分析(一)](./examples/nowcoder/README.md#SQL77)|  |
|SQL78|[牛客的课程订单分析(二)](./examples/nowcoder/README.md#SQL78)| `group by` `having` |
|SQL79|[牛客的课程订单分析(三)](./examples/nowcoder/README.md#SQL79)| `subquery` `count over` |
|SQL80|[牛客的课程订单分析(四)](./examples/nowcoder/README.md#SQL80)| `min` `count` `group by` `having` |
|SQL81|[牛客的课程订单分析(五)](./examples/nowcoder/README.md#SQL81)| `lead() over()` `subquery` `group by` `having` `order by` |
|SQL82|[牛客的课程订单分析(六)](./examples/nowcoder/README.md#SQL82)| `subquery` `count() over()` `left join` `order by` |
|SQL83|[牛客的课程订单分析(七)](./examples/nowcoder/README.md#SQL83)| `subquery` `count() over()` `left join` `order by` `group by` |
|SQL84|[实习广场投递简历分析(一)](./examples/nowcoder/README.md#SQL84)| `like` `sum` `group by` `order by` |
|SQL85|[实习广场投递简历分析(二)](./examples/nowcoder/README.md#SQL85)| `subquery` `date_format` `group by` `order by` |
|SQL86|[实习广场投递简历分析(三)](./examples/nowcoder/README.md#SQL86)| `subquery` `date_format` `date_add` `group by` `order by` |
|SQL87|[最差是第几名(一)](./examples/nowcoder/README.md#SQL87)| `sum() over()` |
|SQL88|[最差是第几名(二)](./examples/nowcoder/README.md#SQL88)| `subquery` `lag() over()` `case when` |
|SQL89|[获得积分最多的人(一)](./examples/nowcoder/README.md#SQL89)| `inner join` `group by` `order by` `sum` |
|SQL90|[获得积分最多的人(二)](./examples/nowcoder/README.md#SQL90)| `inner join` `group by` `order by` `sum` `dense_rank() over()` |
|SQL91|[获得积分最多的人(三)](./examples/nowcoder/README.md#SQL91)| `inner join` `group by` `order by` `sum` `dense_rank() over()` `with as` |

