# 概述
`Migration`是`Django`为`ORM`扩展出来的一套`Model To Schema`的同步方案, `Model`是python中的`Class`而`Schema`是数据库中的`table`的统称.  

> 备注 
>  
> `Migration`这个主题非常庞大, 无法简单的线性穿越所有子级主题, 所以这里是按模块来进行拆解分析. 正确的阅读这个大主题的方式是: 根据 [使用场景](examples.md) 提供的案例来理解 `migration`， 想了解哪块就直接去看具体对象的分析即可。    
 
 &nbsp;  
# 命令
`Django`提供了一些`命令`用于完成`Migration`操作.   

|命令|描述|
|---|---|
|**makemigration**|生成`Migration`指令文件|
|**migrate**|执行迁移|
|**sqlmigrate**|TODO: 待补充|
|**showmigrations**|TODO:待补充|
|**squashmigrations**|将多个指令文件合并成一个指令文件|


&nbsp;  
# 流程
一个简单、常规的流程操作如下:   
1. [定义`model`](fragments/polls/models.py)
2. [生成指令文件](fragments/polls/migrations/0001_initial.py): `python manage.py makemigration polls`
3. 同步到数据库: `python manage.py migrate polls`


&nbsp;  
# 生成指令文件
`makemigration`(生成指令文件)的操作是一个复杂的过程, 它涉及到了如下表格的这些对象   

|对象|描述|
|---|---|
|[ArgumentParser](ArgumentParser.md)|参数解析|
|[Migration](Migration.md)|指令容器, 用于描述当前对象与其他对象的依赖关系和操作指令集合(`dependencies`/`operations`) |
|[MigrationLoader](MigrationLoader.md)|Model源码文件解析 / 版本历史版本一致性 / 检查冲突|
|[MigrationGraph](MigrationGraph.md)|Model源码文件解析 / 版本历史版本一致性 / 检查冲突|
|[MigrationRecorder](MigrationRecorder.md)|从数据库中获取某个app历史提交(`applied`)记录<br />`applied`指的是那些执行了`migrate`的操作, `Django`每执行完一个同步之后都会记录该文件名到数据库, 用于历史一致性做比较.|
|InteractiveMigrationQuestioner|以交互形式让用户选择处理方案|
|NonInteractiveMigrationQuestioner|预定义参数形式省略交互选择|
|MigrationWriter|读取`Model`源码文件, 写入到指令文件|


### makemigration(代码结构)
代码位置: django/core/management/commands/makemigrations.py#23行
```python
class Command(BaseCommand):
    help = "Creates new migration(s) for apps."

    def add_arguments(self, parser):                         """ 省略代码细节, 仅关注代码结构 """

    @no_translations
    def handle(self, *app_labels, **options):                """ 省略代码细节, 仅关注代码结构 """

    def write_migration_files(self, changes):                """ 省略代码细节, 仅关注代码结构 """

    def handle_merge(self, loader, conflicts):               """ 省略代码细节, 仅关注代码结构 """
```
从代码结构来看, 能一眼就能看明白的操作是三个: `add_arguments`(参数预定义)、`write_migration_files`(生成指令文件)、`handle_merge`(处理合并), 而不能直接看明白的`handle`则是生成指令文件的开端.
```python
class Command(BaseCommand):

    @no_translations
    def handle(self, *app_labels, **options):
        ################################################################################
        # 从ArgumentParser中提取所有需要用到的参数                                        
        ################################################################################
        self.verbosity = options['verbosity']
        self.interactive = options['interactive']
        self.dry_run = options['dry_run']
        self.merge = options['merge']
        self.empty = options['empty']
        self.migration_name = options['name']
        if self.migration_name and not self.migration_name.isidentifier():
            raise CommandError('The migration name must be a valid Python identifier.')
        self.include_header = options['include_header']
        check_changes = options['check_changes']

        #################################################################################
        # 从 apps.app_config 里面校验命令行提供 app_labels 是否有效.                     
        #                                                                              
        # app_labels: 是执行 python manage.py makemigration 这里的参数                  
        #             要为多个app生成指令文件, 则可以用空格来分隔app名称                  
        #             例如: python manage.py makemigration polls heartbeat watchman    
        #################################################################################
        app_labels = set(app_labels)
        has_bad_labels = False
        for app_label in app_labels:
            try:
                apps.get_app_config(app_label)
            except LookupError as err:
                self.stderr.write(str(err))
                has_bad_labels = True
        if has_bad_labels:
            sys.exit(2)

        #################################################################################
        # MigrationLoader对象的主要职责是加载已存在的指令文件, 
        # 并且提供验证已存在的指令 文件的一致性和有效性能力.                                                                                 
        #################################################################################
        loader = MigrationLoader(None, ignore_no_migrations=True)                     

        #################################################################################
        # 从数据库中拉取历史版本来检查当前指令文件的一致性.
        #################################################################################
        # Raise an error if any migrations are applied before their dependencies.
        consistency_check_labels = {config.label for config in apps.get_app_configs()}
        # Non-default databases are only checked if database routers used.
        aliases_to_check = connections if settings.DATABASE_ROUTERS else [DEFAULT_DB_ALIAS]
        for alias in sorted(aliases_to_check):
            connection = connections[alias]
            if (connection.settings_dict['ENGINE'] != 'django.db.backends.dummy' and any(
                    # At least one model must be migrated to the database.
                    router.allow_migrate(connection.alias, app_label, model_name=model._meta.object_name)
                    for app_label in consistency_check_labels
                    for model in apps.get_app_config(app_label).get_models()
            )):
                loader.check_consistent_history(connection)

        #################################################################################
        # 从已存在的指令文件结构中找到 leaf_node(末端叶子节点), 
        # 如果有多个 leaf_node 则表示存在冲突. 
        #################################################################################
        conflicts = loader.detect_conflicts()

        # If app_labels is specified, filter out conflicting migrations for unspecified apps
        if app_labels:
            conflicts = {
                app_label: conflict for app_label, conflict in conflicts.items()
                if app_label in app_labels
            }

        #################################################################################
        # 存在冲突, 但是没有提供--merge参数, 那么就把错误信息抛出来
        #################################################################################
        if conflicts and not self.merge:
            name_str = "; ".join(
                "%s in %s" % (", ".join(names), app)
                for app, names in conflicts.items()
            )
            raise CommandError(
                "Conflicting migrations detected; multiple leaf nodes in the "
                "migration graph: (%s).\nTo fix them run "
                "'python manage.py makemigrations --merge'" % name_str
            )

        #################################################################################
        # 提供了--merge参数, 但不存在冲突, 退出程序.
        #################################################################################
        if self.merge and not conflicts:
            self.stdout.write("No conflicts detected to merge.")
            return

        #################################################################################
        # 存在冲突, 也提供了--merge参数, 进入 self.handle_merge 函数去执行合并的代码, 并退出程序.
        #################################################################################
        if self.merge and conflicts:
            return self.handle_merge(loader, conflicts)
 
        #################################################################################
        # questioner: 默认情况下是 InteractiveMigrationQuestioner, 
        #             它是一个input("please enter some answer")的增强版, 
        #             主要是为了获取用户输入的值.
        #           
        #             bool              提问: input("Please answer yes or no: ");
        #             choice            提问: 多选项选择
        #             通用              提问: 调用者传递什么它就提什么问题, 用户输入什么它就返回什么值
        #             addtion字段为null 提问: 预定义模板
        #             alter字段为null   提问: 预定义模板
        #################################################################################
        if self.interactive:
            questioner = InteractiveMigrationQuestioner(specified_apps=app_labels, dry_run=self.dry_run)
        else:
            questioner = NonInteractiveMigrationQuestioner(specified_apps=app_labels, dry_run=self.dry_run)

        #################################################################################
        # TODO: 待补充
        #################################################################################
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            questioner,
        )

        #################################################################################
        # 生成空的指令文件, 用于自定义编辑和同步
        #################################################################################
        # If they want to make an empty migration, make one for each app
        if self.empty:
            if not app_labels:
                raise CommandError("You must supply at least one app label when using --empty.")
            # Make a fake changes() result we can pass to arrange_for_graph
            changes = {
                app: [Migration("custom", app)]
                for app in app_labels
            }
            changes = autodetector.arrange_for_graph(
                changes=changes,
                graph=loader.graph,
                migration_name=self.migration_name,
            )
            self.write_migration_files(changes)
            return

        #################################################################################
        # 比较当前models和历史指令文件是否有发生变化
        #################################################################################
        # Detect changes
        changes = autodetector.changes(
            graph=loader.graph,
            trim_to_apps=app_labels or None,
            convert_apps=app_labels or None,
            migration_name=self.migration_name,
        )

        #################################################################################
        # 如果当前models和历史指令文件发生了变化, 那么就把变化的那部分, 生成出一份最新编号的指令文件.
        #################################################################################
        if not changes:
            # No changes? Tell them.
            if self.verbosity >= 1:
                if app_labels:
                    if len(app_labels) == 1:
                        self.stdout.write("No changes detected in app '%s'" % app_labels.pop())
                    else:
                        self.stdout.write("No changes detected in apps '%s'" % ("', '".join(app_labels)))
                else:
                    self.stdout.write("No changes detected")
        else:
            self.write_migration_files(changes)
            if check_changes:
                sys.exit(1)

```