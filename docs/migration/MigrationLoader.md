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
        self.disk_migrations = None                             # typing.Dict[typing.Tuple(str, str), Migration], 
        self.applied_migrations = None                          # typing.List[str]
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
|**def** load_disk| 方法 | 从系统文件中加载 历史指令文件集, 含: <br />`Django`自带的admin, auth, session, message, contenttypes, staticfiles) |
|**def** build_graph| 方法 ||
|**def** get_migration| 方法 ||
|**def** get_migration_by_prefix| 方法 ||
|**def** check_key| 方法 ||
|**def** add_internal_dependencies| 方法 ||
|**def** add_external_dependencies| 方法 ||
|**def** check_consistent_history| 方法 ||
|**def** detect_conflicts| 方法 |  |
|**def** project_state| 方法 ||

&nbsp;
# 初始化
从`MigrationLoader.__init__`方法中可以看得出来, `self.build_graph`是用于初始化的方法(也是理解`MigrationLoader`的入口).   
```python
class MigrationLoader:

    def build_graph(self):
        #################################################################################
        # 从系统文件中加载 历史指令文件集, 含:
        # Django自带的admin, auth, session, message, contenttypes, staticfiles)
        #################################################################################
        self.load_disk()

        #################################################################################
        # 从数据库中获取某个app历史提交(`applied`)记录
        # `applied`指的是那些执行了`migrate`的操作, `Django`每执行完一个
        # 同步之后都会记录该文件名到数据库, 用于历史一致性做比较.
        #
        # 当self.connection不是None时, 证明它是一个有效connection对象, 
        # 那么就将`applied`的历史提交的文件名写入到self.applied_migrations
        # 而self.applied_migrations数据集通常是用来做历史一致性比较
        #################################################################################
        if self.connection is None:
            self.applied_migrations = {}
        else:
            recorder = MigrationRecorder(self.connection)
            self.applied_migrations = recorder.applied_migrations()

        #################################################################################
        # 初始化MigrationGraph, 即: 初始化 图结构 对象
        # MigrationGraph的初始化过程中什么都没做, 
        # 只是初始化两个成员变量, 用于存储 图结构 的数据节点
        #
        # To start, populate the migration graph with nodes for ALL migrations
        # and their dependencies. Also make note of replacing migrations at this step.
        #################################################################################
        self.graph = MigrationGraph()
    
        #################################################################################
        # self.replacements用于存放那些历史指令文件中定义了replaces的Migration对象.
        # 用于和 self.applied_migrations 进行历史一致性比较.
        # 
        # 吐槽: self.replacements 变量应该在 __init__ 中定义, 并且应该声明它的类型注解
        #################################################################################
        self.replacements = {}                           # 类型注解: typing.Dict(typing.Tuple(str, str), Migration)
        
        #################################################################################
        # 将所有历史指令文件中的对象数据添加到self.graph
        #################################################################################
        for key, migration in self.disk_migrations.items():
            self.graph.add_node(key, migration)
            # Replacing migrations.
            if migration.replaces:
                self.replacements[key] = migration

        #################################################################################
        # 为每个self.graph中的节点, 建立关联关系
        #################################################################################
        for key, migration in self.disk_migrations.items():
            # Internal (same app) dependencies.
            self.add_internal_dependencies(key, migration)

        #################################################################################
        # TODO: 待处理
        # 
        # Add external dependencies now that the internal ones have been resolved.
        #################################################################################
        for key, migration in self.disk_migrations.items():
            self.add_external_dependencies(key, migration)

        #################################################################################
        # self.replacements从磁盘的历史指令文件中搜罗出所有的含有replaces成员便改良的Migration对象,
        # 而self.applied_migrations从数据库中搜索出所有历史提交记录.
        #
        # applied_statuses = [(target in self.applied_migrations) for target in migration.replaces]
        # 如果self.replacements的某个(遍历)Migration存在于self.applied_migrations中则表示它们已经同步过了.
        # 否则self.replacements中的这个Migration就被视为, 这个Migration对应的指令文件是没同步过的对象.
        #
        # self.applied_migrations.pop(key, None)
        # 从self.graph结构中删除掉: 用那些被拎出来(没有同步过)的对象, 
        # 这个操作意图是: 不能污染 self.graph对象, 它们都是干净的，经过比较是一致的, 有效的图结构数据节点.
        #
        # all(applied_statuses): all([]) 和 all([True, ...]) 都是 True, 这种状态的数据表示它是干净的，经过比较
        # 是一致的, 有效的图结构数据节点; 所以要把replaces里面的对象从self.graph的节点中移除掉, 确保不存在冗余的情况.
        #
        # Carry out replacements where possible.
        #################################################################################
        for key, migration in self.replacements.items():
            # Get applied status of each of this migration's replacement targets.
            applied_statuses = [(target in self.applied_migrations) for target in migration.replaces]
            # Ensure the replacing migration is only marked as applied if all of
            # its replacement targets are.
            if all(applied_statuses):
                self.applied_migrations[key] = migration
            else:
                self.applied_migrations.pop(key, None)
            # A replacing migration can be used if either all or none of its
            # replacement targets have been applied.
            if all(applied_statuses) or (not any(applied_statuses)):
                self.graph.remove_replaced_nodes(key, migration.replaces)
            else:
                # This replacing migration cannot be used because it is partially applied.
                # Remove it from the graph and remap dependencies to it (#25945).
                self.graph.remove_replacement_node(key, migration.replaces)
        # Ensure the graph is consistent.
        try:
            self.graph.validate_consistency()
        except NodeNotFoundError as exc:
            # Check if the missing node could have been replaced by any squash
            # migration but wasn't because the squash migration was partially
            # applied before. In that case raise a more understandable exception
            # (#23556).
            # Get reverse replacements.
            reverse_replacements = {}
            for key, migration in self.replacements.items():
                for replaced in migration.replaces:
                    reverse_replacements.setdefault(replaced, set()).add(key)
            # Try to reraise exception with more detail.
            if exc.node in reverse_replacements:
                candidates = reverse_replacements.get(exc.node, set())
                is_replaced = any(candidate in self.graph.nodes for candidate in candidates)
                if not is_replaced:
                    tries = ', '.join('%s.%s' % c for c in candidates)
                    raise NodeNotFoundError(
                        "Migration {0} depends on nonexistent node ('{1}', '{2}'). "
                        "Django tried to replace migration {1}.{2} with any of [{3}] "
                        "but wasn't able to because some of the replaced migrations "
                        "are already applied.".format(
                            exc.origin, exc.node[0], exc.node[1], tries
                        ),
                        exc.node
                    ) from exc
            raise exc
        self.graph.ensure_not_cyclic()
```