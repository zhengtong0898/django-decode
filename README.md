### 如何将orm操作的sql语句打印出来?
- 方案一: 编辑`Django`源码
  > 编辑 Lib/site-packages/django/db/models/sql/compiler.py 文件
  ```python
  # 在文件头部导入logging
  import logging
  logger = logging.getLogger('django.compiler')
  
  
  class SQLCompiler:
   
      def execute_sql(self, result_type=MULTI, chunked_fetch=False, chunk_size=GET_ITERATOR_CHUNK_SIZE):
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
### 源码分析
`Django-3.0.8`源码分析, 系统`win10 64位`, IDE`pycharm community 2019`, 语言`python3.8`    

|模块|源码|
|:---:|:---:|
|autoreload|[核心原理](docs/autoreload/第1部分-核心原理.md) 、 [Signal](docs/autoreload/第2部分-Signal.md) 、 [两个进程](docs/autoreload/第3部分-两个进程.md)  、[两个线程](docs/autoreload/第4部分-两个线程.md)  、[Watchman](docs/autoreload/第5部分-Watchman.md)  、[响应式开发](docs/autoreload/第6部分-响应式开发.md)|
|migration|待补充|


&nbsp;  

### 快速的创建一个项目
```shell
# 创建项目 
django-admin startproject AdminActions

# 创建数据库
python AdminActions/manage.py migrate

# 创建管理员账号
# username: admin
# password: 123456
# email:    123@qq.com 
python AdminActions/manage.py createsuperuser

# 启动项目
python AdminActions/manage.py runserver
```


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
  | self.model = model |  |
  | self._db = using | |
  | self._hints = hints or {} | |
  | self._query = query or sql.Query(self.model) | [`raw sql`语法生成器对象](./src/Django-3.0.8/django/db/models/sql/query.py#L146) |
  | self._result_cache = None | |
  | self._sticky_filter = False | |
  | self._for_write = False | |
  | self._prefetch_related_lookups = () | |
  | self._prefetch_done = False | |
  | self._known_related_objects = {}  # {rel_field: {pk: rel_obj}} | |
  | self._iterable_class = ModelIterable | |
  | self._fields = None | |
  | self._defer_next_filter = False | |
  | self._deferred_filter = None | |
  | | - |
  | @property<br> def query(self)  | |
  |def iterator(self, chunk_size=2000)| |
  |def aggregate(self, *args, **kwargs)| |
  |def count(self)| [统计总数](./docs/QuerySet.md#count) |
  |def get(self, *args, **kwargs)| [获取一条数据](./docs/QuerySet.md#get) |
  |def create(self, **kwargs)| [插入一条数据](./docs/QuerySet.md#create) |
  |def bulk_create(self, objs, batch_size=None, ignore_conflicts=False)| |
  |def bulk_update(self, objs, fields, batch_size=None)| |
  |def get_or_create(self, defaults=None, **kwargs)| |
  |def update_or_create(self, defaults=None, **kwargs)| |
  |def earliest(self, *fields)| |
  |def latest(self, *fields)| |
  |def first(self)| |
  |def last(self)| |
  |def in_bulk(self, id_list=None, *, field_name='pk')| |
  |def delete(self)| |
  |def update(self, **kwargs)| |
  |def exists(self)| |
  |def explain(self, *, format=None, **options)| |
  |def raw(self, raw_query, params=None, translations=None, using=None) | |
  |def values(self, *fields, **expressions) | |
  |def values_list(self, *fields, flat=False, named=False) | |
  |def dates(self, field_name, kind, order='ASC') | |
  |def datetimes(self, field_name, kind, order='ASC', tzinfo=None, is_dst=None) | |
  |def none(self) | |
  |def filter(self, *args, **kwargs) | |
  |def exclude(self, *args, **kwargs) | |
  |def complex_filter(self, filter_obj) | |
  |def union(self, *other_qs, all=False) | |
  |def intersection(self, *other_qs) | |
  |def difference(self, *other_qs) | |
  |def select_for_update(self, nowait=False, skip_locked=False, of=()) | |
  |def select_related(self, *fields) | |
  |def prefetch_related(self, *lookups) | |
  |def annotate(self, *args, **kwargs) | |
  |def order_by(self, *field_names) | |
  |def distinct(self, *field_names) | |
  |def extra(self, select=None, where=None, params=None, <br> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; tables=None, order_by=None, select_params=None) | |
  |def reverse(self) | |
  |def defer(self, *fields) | |
  |def only(self, *fields) | |
  |def using(self, alias) | |
  |@property <br> def ordered(self) | |
  |@property <br> def db(self) | |


&nbsp;  
&nbsp;   
### Debug困扰清单
- \_\_str\_\_ 和 \_\_repr\_\_    
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
  
 