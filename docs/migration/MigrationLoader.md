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
|self.applied_migrations| 成员变量 | 已通过`migrate`同步到数据的指令文件对象, 这些都会被记录在数据库中, 用于历史一致性检查. |
|self.unmigrated_apps| 成员变量 | 尝试通过模块路劲加载`app`, 如果加载无效则存放在这个变量内. |
|self.migrated_apps| 成员变量 | 把所有`app.migrations`下的文件都视为历史指令文件(认为已同步到数据库了, 但是实际上可能还没有同步), <br />但是在`load_dist`阶段它存在的意义就是全部先加载进来, 后面处理依赖关系有其他环节负责. |
|self.graph| 成员变量 | `directed graph`(有向图)结构对象, 用于存储历史指令文件集. |
|self.ignore_no_migrations| 成员变量 | 忽略那些有问题的`migrations`, 出现问题时不需要报错, 直接跳过. |
|**def** migrations_module| 方法 | 从`apps.app_configs`中找到具体`app`, 返回字符串类型的值`app_name.migrations`(例如: `polls.migrations`) |
|**def** load_disk| 方法 | 根据`settings.INSTALL_APPS`配置, 从系统文件中加载 历史指令文件集, 含: <br />`Django`自带的admin, auth, session, message, contenttypes, staticfiles) |
|**def** build_graph| 方法 | 初始化 `self.graph`(图结构), 图结构可用来 构建对象依赖关系, 解决递归依赖关系检查, 一致性检查等能力等. |
|**def** get_migration| 方法 ||
|**def** get_migration_by_prefix| 方法 ||
|**def** check_key| 方法 | 检查 key 中, 是否含有特殊定义('__first__' 或 '__latest__') |
|**def** add_internal_dependencies| 方法 | 为那些与依赖对象是相同的app的对象绑定依赖关系 |
|**def** add_external_dependencies| 方法 | 为那些不是相同 app 内的依赖, 绑定关系. |
|**def** check_consistent_history| 方法 ||
|**def** detect_conflicts| 方法 |  |
|**def** project_state| 方法 ||

&nbsp;
# 初始化`有向图`结构: self.build_graph 
从`MigrationLoader.__init__`方法中可以看得出来, `self.build_graph`是用于初始化的方法(也是理解`MigrationLoader`的入口).   

这里列出可供参考的外部分析.
1. 添加节点: [self.graph.add_node(key, migration)](MigrationGraph.md#添加节点)
2. 添加依赖: [self.add_internal_dependencies(key, migration)](MigrationLoader.md#添加内部依赖)

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
        # self.replacements从磁盘的历史指令文件中搜罗出所有的含有replaces成员变量的Migration对象,
        # 而self.applied_migrations是从数据库中搜索出所有历史提交记录.
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
        # 当 (not any(applied_statuses)) == True 时, 它实际的值是这样的: (not any([False, False, False]))
        # 这意味着 这些migration.replaces 都还没有同步到数据库, 所以这些数据还不能存放到有效节点中, 所以要移除掉.
        #
        # all(applied_statuses) or (not any(applied_statuses)) 组合在一起做条件, 下面三种任意一个都会进入True条件块:
        # []                            数据库中没历史同步数据: 即: 无数据状态.
        # [True, True, True, ...]       数据库中有历史同步数据: 这些migtraion.replaces都已经同步到数据库了.
        # [False, False, False, ...]    数据库中有历史同步数据: 这些migration.replaces都还没有同步到数据库中.
        # 如果数据库的状态是一致的, 那么就可以执行替换迁移.
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
                #########################################################################
                # 如果数据库的状态不是一致的, 那么就取消替换.
                #
                # This replacing migration cannot be used because it is partially applied.
                # Remove it from the graph and remap dependencies to it (#25945).
                #########################################################################
                self.graph.remove_replacement_node(key, migration.replaces)

        #################################################################################
        # self.graph 是一个 `directed graph` 有向图结构对象.
        # 这里的 validate_consistency 的职责是, 找出那些没找到关联的对象,
        # 这些对象在做self.add_dependency的时候发现找不到任何关联, 
        # 然后把这些对象 `wrapper` 成一个 `DummyNode`, 表示是一个 `无向节点`,
        # validate_consistency的职责是, 确保当前 `有向图` 结构中不含有 `DummyNode`, 
        # 若含有 `DummyNode`, 就抛出 `NodeNotFoundError` 异常. 
        #
        # Ensure the graph is consistent.
        #################################################################################
        try:
            self.graph.validate_consistency()
        except NodeNotFoundError as exc:
            #############################################################################
            # TODO: 待处理
            #
            # Check if the missing node could have been replaced by any squash
            # migration but wasn't because the squash migration was partially
            # applied before. In that case raise a more understandable exception
            # (#23556).
            # Get reverse replacements.
            #############################################################################
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
    
        #################################################################################
        # 采用 Guido van Rossum 提供的 `Detecting Cycles in a Directed Graph` 算法,
        # 检查确保当前 `有向图` 结构中的所有节点, 不存在环形(相互依赖)的情况.
        #
        # 算法链接: https://neopythonic.blogspot.com/2009/01/detecting-cycles-in-directed-graph.html
        #################################################################################
        self.graph.ensure_not_cyclic()
```


&nbsp;  
# 从系统文件中加载历史指令文件集
那些已经执行过`makemigration`的`app`, 都会在`app.migrations`目录下生成一些历史指令文件(文件名大致是这样的: `0001_initial.py`), 
这些指令文件中存放着一个`Migration`的类对象, 关于更详细的`Migration`解读[请参考这里](Migration.md)
```python
#########################################################################################
# `Django` 将 `migrations` 作为 `app` 默认的子目录, 用于存放历史指令文件. 
#########################################################################################
MIGRATIONS_MODULE_NAME = 'migrations'


class MigrationLoader:

    @classmethod
    def migrations_module(cls, app_label):
        #################################################################################
        # `Django`还提供了 `settings.MIGRATION_MODULES` 配置, 让用户自己配置历史指令文件
        # 的目录在什么地方, 但是这个配置必须是能够被当作模块加载的模块格式.
        # 例如: polls.migrations
        # 
        # 返回值类型: (str, bool)
        # 返回值: ('polls.migrations', False) 或 ('polls.xxx', True)
        # 
        # 返回值的第二个成员是 `Bool` 对象, 
        # 当它是 `False` 时表示采用的时`Django`默认的模块路径.
        # 当它时`True`时则表示采用的是`settings.MIGRATION_MODULES`提供的模块路径
        #################################################################################
        if app_label in settings.MIGRATION_MODULES:
            return settings.MIGRATION_MODULES[app_label], True
        else:
            app_package_name = apps.get_app_config(app_label).name
            return '%s.%s' % (app_package_name, MIGRATIONS_MODULE_NAME), False

    def load_disk(self):
        #################################################################################
        # 每次执行load_dist都要变量重置, 数据重新加载.
        # 这意味着这个函数必须保证加载到的数据都是最新, 最全的.
        # 
        # 重新加载的要点体现在下面这几行代码中:
        # 1.   清空: `self.disk_migrations`, `self.unmigrated_apps`, `elf.migrated_apps`
        # 2. 再写入: `self.disk_migrations[app_config.label, migration_name]` = Migration
        #            `self.unmigrated_apps.add`
        #            `self.migrated_apps.add`
        # 3. reload: reload(module)    
        #################################################################################
        self.disk_migrations = {}
        self.unmigrated_apps = set()
        self.migrated_apps = set()

        #################################################################################
        # apps: 是`Django`在启动阶段预加载的一个对象, 它根据 `settings.INSTALL_APPS` 来:
        #       1. 读取每个 `app` 模块目录下的 `models.py` 文件并将该文件内的
        #          对象全部存到 apps.app_configs[app].models 中.
        #       2. 将 `app` 的路径存到 apps.app_configs[app].path 中.
        #       3. 将 `app` 的名称存到 apps.app_configs[app].label 中.
        #################################################################################
        for app_config in apps.get_app_configs():
            #############################################################################
            # 获取`app`的 历史指令文件目录 的模块路径
            # module_name: 'polls.migrations'
            # explicit: True
            # 变量含义的详细解释, 请看上面的 `migrations_module` 方法的解析
            #
            # 如果 模块路径 不存在, 则表示该 `app`的`migrate`行为将是无效的, 
            # 把它纳入到 `self.unmigrated_apps` 中, 让后续的代码可以通过判断来避开对它的操作.
            #############################################################################
            module_name, explicit = self.migrations_module(app_config.label)
            if module_name is None:
                self.unmigrated_apps.add(app_config.label)
                continue
    
            #############################################################################
            # was_loaded 变量定义再这里的目的是, 用于记录 `module_name` 是不是在加载之前就已经
            # 存在于 `sys.modules` 中了. 
            # 
            # 这个变量将用来判断: 
            # 如果之前就已经有了这个 `module_name`, 那么就应该重新加载: reload(module).
            # 如果之前没有这个`module_name`, 那么就表示它是最新的, 不需要重新加载.
            #############################################################################
            was_loaded = module_name in sys.modules
            try:
                module = import_module(module_name)
            except ImportError as e:
                #########################################################################
                # (explicit and self.ignore_no_migrations) == True
                # explicit == True 表示: 用户自定义 `settings.MIGRATION_MODULES`
                # self.ignore_no_migrations == True 表示: 出现错误不要报错.
                # 这里面其实是2个条件都必须满足才会忽略报错.
                # 
                # (not explicit and "No module named" in str(e) and MIGRATIONS_MODULE_NAME in str(e))
                # not explicit == (explicit == False) 表示: 采用`Django`默认的`app.migrations`目录模块路径
                # "No module named" in str(e) 表示: 错误信息里面含有 "No module named"
                # MIGRATIONS_MODULE_NAME in str(e) 表示: 错误信息里面含有 "app.migrations"
                # 这里面其实是3个条件都必须满足才会忽略报错.
                #
                # 满足任意一组条件, 都会忽略报错, 并且将 `问题app` 添加到 `self.unmigrated_apps` 中,
                # 后续代码在遍历所有 `app.migrations` 时, 都需要通过判断来避开`self.unmigrated_apps`
                # 中的`app`, 避免产生不可预期的错误.
                #
                # I hate doing this, but I don't want to squash other import errors.
                # Might be better to try a directory check directly.
                #########################################################################
                if ((explicit and self.ignore_no_migrations) or (
                        not explicit and "No module named" in str(e) and MIGRATIONS_MODULE_NAME in str(e))):
                    self.unmigrated_apps.add(app_config.label)
                    continue
                raise
            else:
                # Empty directories are namespaces.
                # getattr() needed on PY36 and older (replace w/attribute access).
                if getattr(module, '__file__', None) is None:
                    self.unmigrated_apps.add(app_config.label)
                    continue
                # Module is not a package (e.g. migrations.py).
                if not hasattr(module, '__path__'):
                    self.unmigrated_apps.add(app_config.label)
                    continue
                # Force a reload if it's already loaded (tests need this)
                if was_loaded:
                    reload(module)

            #############################################################################
            # 将无报错的`app`名字, 添加到 self.migrated_apps 中, 表示这个 `app` 是合规的 `app`.
            #############################################################################
            self.migrated_apps.add(app_config.label)
        
            #############################################################################
            # `migration_names` 是使用 `iter_modules` 模块下的子模块(通常是.py后缀的文件当作子模块) 
            # 子模块: `0001_initial.py` to `0001_initial`
            #
            # TODO: '_~'是什么?
            # 既然过滤代码能出现在这里, 即表示这种文件名有可能存在, 
            # 已知在 linux 下编辑一个文件, 会产生带有 .swp后缀的临时隐藏文件, 所以排除是编辑中的文件的情况.
            #############################################################################
            migration_names = {
                name for _, name, is_pkg in pkgutil.iter_modules(module.__path__)
                if not is_pkg and name[0] not in '_~'
            }

            #############################################################################
            # module_name: 'polls.migrations'
            # migration_name: '0001_initial'
            # migration_path: 'polls.migrations.0001_initial'
            # 这是在面向`import_module`编程, 拼接出`import_module`能合法加载的字符串模块路径.
            #
            # 尝试去加载子模块, 并且检查子模块中是否存在`Migration`这个对象.
            # 如果不存在就报错.
            # 如果存在就是将其实例化, 然后添加`self.dis_migrations`中暂存起来, 为后续代码的操作提供前提条件.  
            #############################################################################
            # Load migrations
            for migration_name in migration_names:
                migration_path = '%s.%s' % (module_name, migration_name)
                try:
                    migration_module = import_module(migration_path)
                except ImportError as e:
                    if 'bad magic number' in str(e):
                        raise ImportError(
                            "Couldn't import %r as it appears to be a stale "
                            ".pyc file." % migration_path
                        ) from e
                    else:
                        raise
                if not hasattr(migration_module, "Migration"):
                    raise BadMigrationError(
                        "Migration %s in app %s has no Migration class" % (migration_name, app_config.label)
                    )
                self.disk_migrations[app_config.label, migration_name] = migration_module.Migration(
                    migration_name,
                    app_config.label,
                )
```

&nbsp;   
# 添加内部依赖
这里列出可供参考的外部分析.
- 添加节点: [self.graph.add_dependency(migration, key, parent, skip_validation=True)](MigrationGraph.md#添加依赖)
```python

class MigrationLoader:

    #####################################################################################
    # 参数类型注解:
    # key：      typing.Dict(typing.Tuple(str, str)    # 例如: ('polls', '0002_menu')
    # migration: Migration
    #
    # migration.dependencies 必须有内容, 否则有效的添加依赖.
    #
    # key: 指的是当前操作对象的key
    # parent: 指的是当前操作对象依赖的对象的key
    # parent[0] == key[0] 这两个key的第一个元素, 必须一致, 否则就不是一个有效的依赖.
    # parent[1] != '__first__' 依赖的key的第二个元素, 不能是'__first__'.
    #####################################################################################
    def add_internal_dependencies(self, key, migration):
        for parent in migration.dependencies:
            # Ignore __first__ references to the same app.
            if parent[0] == key[0] and parent[1] != '__first__':
                self.graph.add_dependency(migration, key, parent, skip_validation=True)
```


&nbsp;   
# 添加外部依赖
```python

class MigrationLoader:
    #####################################################################################
    # 职责:
    # 用于处理 migration.dependencies 中的特殊定义('__first__' 和 '__latest__' 声明),
    # 当 dependencies 中含有'__first__'时, 返回 self.graph 中 `顶点` 的那个节点.
    # 当 dependencies 中含有'__latest__'时, 返回 self.graph 中 `终点` 的那个节点.
    #
    # 参数类型注解:
    # key:         typing.Tuple(str, str)      # 例如: ('polls', '0002_menu')
    # current_app: str                         # 例如: 'polls'
    #
    # (key[1] != "__first__" and key[1] != "__latest__"): 
    # key[1]中 不含有 '__first__', 也不含有 '__latest__': 表示key是有效的, 返回这个key.
    #
    # (key[1] != "__first__" and key[1] != "__latest__") or key in self.graph
    # key[1]中 含有 '__first__' 或 '__latest__', 并且 key 已经被缓存到self.graph中, 表示key是有效的.
    #
    # 当key不符合 `if (key[1] != "__first__" and key[1] != "__latest__") or key in self.graph:` 条件时, 开始执行它的职责工作.
    #####################################################################################
    def check_key(self, key, current_app):
        if (key[1] != "__first__" and key[1] != "__latest__") or key in self.graph:
            return key
        # Special-case __first__, which means "the first migration" for
        # migrated apps, and is ignored for unmigrated apps. It allows
        # makemigrations to declare dependencies on apps before they even have
        # migrations.
        if key[0] == current_app:
            # Ignore __first__ references to the same app (#22325)
            return
        if key[0] in self.unmigrated_apps:
            # This app isn't migrated, but something depends on it.
            # The models will get auto-added into the state, though
            # so we're fine.
            return
        if key[0] in self.migrated_apps:
            try:
                if key[1] == "__first__":
                    return self.graph.root_nodes(key[0])[0]
                else:  # "__latest__"
                    return self.graph.leaf_nodes(key[0])[0]
            except IndexError:
                if self.ignore_no_migrations:
                    return None
                else:
                    raise ValueError("Dependency on app with no migrations: %s" % key[0])
        raise ValueError("Dependency on unknown app: %s" % key[0])


    #####################################################################################
    # 职责:
    # 为那些不是相同 app 内的依赖, 绑定关系.
    # 例如: 在 django.contrib.admin.migrations.0001_initial.Migration.dependencies 中,
    #       声明了依赖对象是 ('contenttypes', '__first__').
    #####################################################################################
    def add_external_dependencies(self, key, migration):
        for parent in migration.dependencies:
            #############################################################################
            # 两个 key 都相同的话, 表示都是在同一个app内, 所以不需要再做关联了.
            # 
            # Skip internal dependencies
            #############################################################################
            if key[0] == parent[0]:
                continue

            #############################################################################
            # 代码能进入到这里, 说明 key 和 parent 的依赖关系不是在同一个 app 内.
            #
            # parent 是依赖对象的key.  
            # 
            # check_key:
            # 如果 parent 含有'__first__'的话, 返回 self.graph[app] 中 `顶点` 节点的key, 表示有效可以添加外部依赖.
            # 如果 parent 含有'__latest__'的话, 返回 self.graph[app] 中 `终点` 节点的key, 表示有效可以天机外部依赖.
            #############################################################################
            parent = self.check_key(parent, key[0])
            if parent is not None:
                self.graph.add_dependency(migration, key, parent, skip_validation=True)

        #################################################################################
        # migration.run_before: 用于强调migration的顺序.
        # 从顺序角度来看, migration.run_before 和 migration.dependencies 差别不大, 
        # 都是先执行这两个之后, 再执行 migration.operations 的内容.
        # 所以这里也为 run_before 添加外部依赖.
        #
        # TODO： run_before 缺少了 `if key[0] == parent[0]` 比较,
        #        由于 self.graph.add_dependency 中并没有做任何校验, 而是采取覆盖形式赋值,
        #        所以 run_before 既能处理内部依赖, 也能处理外部依赖.
        #        因此 这段代码 放在这里没有必要性!
        #################################################################################
        for child in migration.run_before:
            child = self.check_key(child, key[0])
            if child is not None:
                self.graph.add_dependency(migration, child, key, skip_validation=True)
```

&nbsp;  
# 检查冲突
```python
class MigrationLoader:
        
    #####################################################################################
    # 函数职责:
    # 检查所有 app 的末梢叶节点, 检查标准是: app 的末梢叶节点必须只有一个, 多余一个就会返回冲突的对象.
    #
    # self.graph.leaf_nodes():   返回值类型: set(node)
    # 不提供参数的情况下, 这个函数会返回所有 app 的末梢叶节点.
    #
    # seen_apps:                  变量类型: typing.Dict(typing.Tuple(str, str), set)
    # 用于隔离每个app的末梢叶节点.
    #
    # conflicting_apps:
    # 每个app应该只有一个末梢叶节点, 如果有发现多个则会存入到这里, 用于表示有冲突情况.
    #####################################################################################
    def detect_conflicts(self):
        """
        Look through the loaded graph and detect any conflicts - apps
        with more than one leaf migration. Return a dict of the app labels
        that conflict with the migration names that conflict.
        """
        seen_apps = {}
        conflicting_apps = set()
        for app_label, migration_name in self.graph.leaf_nodes():
            if app_label in seen_apps:
                conflicting_apps.add(app_label)
            seen_apps.setdefault(app_label, set()).add(migration_name)
        return {app_label: seen_apps[app_label] for app_label in conflicting_apps}
```
