# 准备阶段(Prepare)
通常在做比较的时候都会先获取对象之前的状态, 然后再去读取该对象的当前状态这样才有比较的意义;   
而`makemigration`默认情况下采取的是对文件的操作路径(备注: 也有对数据库操作的路径), 所以在`Prepare`阶段`Django`使用`MigrationLoader`对象来负责加载各个`installed_apps`的`app.models`模块文件, 为后续的比较做准备工作.  

&nbsp;  
# 代码结构(Structure)
`MigrationLoader`没有采用继承, 所有的行为都是内卷调用和通过`import`外部对象来使用, 从结构上来看比较单一.

备注:  
`MigrationLoader`假设`指令文件`(例如: `0001_initial.py`)都存放在`app.migrations`目录中, 即: 目录名`migrations`是固定死的.        
`MigrationLoader`假设`模型文件`(例如: `models.py`)都存放在`app`目录中, 即: 文件名`models.py`是固定死的.   
```python
MIGRATIONS_MODULE_NAME = 'migrations'


class MigrationLoader:

    def __init__(self, connection, load=True, ignore_no_migrations=False):
        self.connection = connection
        self.disk_migrations = None
        self.applied_migrations = None
        self.ignore_no_migrations = ignore_no_migrations
        if load:
            self.build_graph()

    @classmethod
    def migrations_module(cls, app_label):                      """ 省略代码细节, 仅关注代码结构 """

    def load_disk(self):                                        """ 省略代码细节, 仅关注代码结构 """
    
    def get_migration(self, app_label, name_prefix):            """ 省略代码细节, 仅关注代码结构 """
            
    def get_migration_by_prefix(self, app_label, name_prefix):  """ 省略代码细节, 仅关注代码结构 """

    def check_key(self, key, current_app):                      """ 省略代码细节, 仅关注代码结构 """

    def add_internal_dependencies(self, key, migration):        """ 省略代码细节, 仅关注代码结构 """

    def add_external_dependencies(self, key, migration):        """ 省略代码细节, 仅关注代码结构 """

    def build_graph(self):                                      """ 省略代码细节, 仅关注代码结构 """

    def check_consistent_history(self, connection):             """ 省略代码细节, 仅关注代码结构 """

    def detect_conflicts(self):                                 """ 省略代码细节, 仅关注代码结构 """

    def project_state(self, nodes=None, at_end=True):           """ 省略代码细节, 仅关注代码结构 """
```

|对象 | 类型|描述|
|---|:---:|---|
|self.connection| 成员变量 | 默认值: None(表示`Load from file`); 非None通常是一个数据库连接(表示`Load from database`)  |
|self.disk_migrations| 成员变量 | 加载`app`的所有历史已生成的`models`模块文件 |
|self.applied_migrations| 成员变量 | 待补充 |
|self.ignore_no_migrations| 成员变量 | 待补充 |
|**def** migrations_module| 方法 | 从`apps.app_configs`中找到具体`app`, 返回字符串类型的值`app_name.migrations`(例如: `polls.migrations`) |
|**def** load_disk| 方法 | 调用`self.migrations_module`返回的`polls.migrations`字符串, 利用`pkgutil.iter_modules`遍历所有文件, 加载该模块路径下的所有文件, 然后保存到`self.disk_migrations`中. |
|**def** build_graph| 方法 ||
|**def** get_migration| 方法 ||
|**def** get_migration_by_prefix| 方法 ||
|**def** check_key| 方法 ||
|**def** add_internal_dependencies| 方法 ||
|**def** add_external_dependencies| 方法 ||
|**def** check_consistent_history| 方法 ||
|**def** detect_conflicts| 方法 |  |
|**def** project_state| 方法 ||

