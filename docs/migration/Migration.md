# Migration
`Migration`是一个 `模板` 类对象, 所谓的 `模板` 并不是 `c++` 的 `template` 的意思, 而是`app.migrations`目录下的`历史指令文件`都必须按照这个模板来定义指令.   
   
从代码层面来看就是定义 `app.migrations.submodule.Migration` 时必须继承 `django.db.migrations.migration.Migration`.   
   
`Migration`从功能层面上来看只有三个功能: `mutate_state`(将当前的`operations`转换成一个常规的`mode`对象), `apply`(将更新同步到数据库), `unapply`(从数据库中回滚操作).   


- operations    
定义在`opertations`中的成员对象, 必须是: `django.db.migrations.operations`目录下定义的操作对象, 全量操作对象清单[请参考这里](https://docs.djangoproject.com/en/3.0/ref/migration-operations/).

- dependencies   
定义在`operations`中的成员对象, 被视为是当前`Migration`依赖的对象, 从`有向图`角度来看这些`dependencies`就等于是`parents`, 必须先执行这些`dependencies`然后才能执行当前的`Migration`.

- run_before  
定义在`run_before`中的成员对象, 被视为是当前`Migration`被依赖的对象, 从`有向图`角度来看这些`run_before`就等于是`children`, 必须先执行当前`Migration`, 然后才能执行这些`run_before`.  
通常用于定义第三方`Migration`(指的是: 非当前app的`submodule.Migration`); 作用是声明当前`Migration`应该先运行, 然后再运行`run_before`列表中的第三方`Migration`.

- replaces  
定义在`replaces`中的成员对象, 被视为是被废弃的对象. `Django`会将这些对象中的内容合并(`squash`)到当前`Migration`中, 并生成一个新的文件.  
备注: 如果`replaces`的`Migration`已经被同步到数据库, 那么当前这个合并的`Migration`就不会被执行同步动作.

- initial   
声明当前`Migration`是第一个`Migration`, 从 `有向图` 角度来看, 它被视为是`顶点`.  
      
- atomic  
将`迁移操作`封装到一个事务中去执行, 只能在那些支持事务操作的数据库中执行.

```python
from django.db.transaction import atomic

from .exceptions import IrreversibleError


class Migration:
    """ The base class for all migrations. """

    operations = []

    dependencies = []

    run_before = []

    replaces = []

    initial = None

    atomic = True

    #####################################################################################
    # 参数类型注解:
    # name:         str               # 例如: 0001_initial(是app.migrations目录下的文件名)
    # app_label:    str               # 例如: polls 
    #####################################################################################
    def __init__(self, name, app_label):
        self.name = name
        self.app_label = app_label
        
        #################################################################################
        # 将当前Migration的类变量, 转变成对象变量.
        #################################################################################
        self.operations = list(self.__class__.operations)
        self.dependencies = list(self.__class__.dependencies)
        self.run_before = list(self.__class__.run_before)
        self.replaces = list(self.__class__.replaces)

    def __eq__(self, other):
        return (
            isinstance(other, Migration) and
            self.name == other.name and
            self.app_label == other.app_label
        )

    def __repr__(self):
        return "<Migration %s.%s>" % (self.app_label, self.name)

    def __str__(self):
        return "%s.%s" % (self.app_label, self.name)

    def __hash__(self):
        return hash("%s.%s" % (self.app_label, self.name))

    #################################################################################
    # 参数类型注解:
    # project_state:      ProjectState
    #
    # 函数职责:
    # 遍历 self.operations 里面的 ModelOperation, 对project_state的models进行操作,
    # 如果 self.operations 里面第一个ModelOperation是CreateModel, 那么就添加一个model到project_state中.
    # 如果 self.operations 里面第二个ModelOperation是DeleteModel, 那么就从project_state中移除指定的model.
    # 如果 self.operations 里面第三个ModelOperation是RenameModel, 那么就从project_state中移除指定的model, 然后在reload指定的model.
    # ...
    #################################################################################
    def mutate_state(self, project_state, preserve=True):
        """
        Take a ProjectState and return a new one with the migration's
        operations applied to it. Preserve the original object state by
        default and return a mutated state from a copy.
        """
        new_state = project_state
        if preserve:
            new_state = project_state.clone()

        for operation in self.operations:
            operation.state_forwards(self.app_label, new_state)
        return new_state

    def apply(self, project_state, schema_editor, collect_sql=False):
        """
        Take a project_state representing all migrations prior to this one
        and a schema_editor for a live database and apply the migration
        in a forwards order.

        Return the resulting project state for efficient reuse by following
        Migrations.
        """
        for operation in self.operations:
            # If this operation cannot be represented as SQL, place a comment
            # there instead
            if collect_sql:
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append(
                        "-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:"
                    )
                schema_editor.collected_sql.append("-- %s" % operation.describe())
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    continue
            # Save the state before the operation has run
            old_state = project_state.clone()
            operation.state_forwards(self.app_label, project_state)
            # Run the operation
            atomic_operation = operation.atomic or (self.atomic and operation.atomic is not False)
            if not schema_editor.atomic_migration and atomic_operation:
                # Force a transaction on a non-transactional-DDL backend or an
                # atomic operation inside a non-atomic migration.
                with atomic(schema_editor.connection.alias):
                    operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
            else:
                # Normal behaviour
                operation.database_forwards(self.app_label, schema_editor, old_state, project_state)
        return project_state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        """
        Take a project_state representing all migrations prior to this one
        and a schema_editor for a live database and apply the migration
        in a reverse order.

        The backwards migration process consists of two phases:

        1. The intermediate states from right before the first until right
           after the last operation inside this migration are preserved.
        2. The operations are applied in reverse order using the states
           recorded in step 1.
        """
        # Construct all the intermediate states we need for a reverse migration
        to_run = []
        new_state = project_state
        # Phase 1
        for operation in self.operations:
            # If it's irreversible, error out
            if not operation.reversible:
                raise IrreversibleError("Operation %s in %s is not reversible" % (operation, self))
            # Preserve new state from previous run to not tamper the same state
            # over all operations
            new_state = new_state.clone()
            old_state = new_state.clone()
            operation.state_forwards(self.app_label, new_state)
            to_run.insert(0, (operation, old_state, new_state))

        # Phase 2
        for operation, to_state, from_state in to_run:
            if collect_sql:
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append(
                        "-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:"
                    )
                schema_editor.collected_sql.append("-- %s" % operation.describe())
                schema_editor.collected_sql.append("--")
                if not operation.reduces_to_sql:
                    continue
            atomic_operation = operation.atomic or (self.atomic and operation.atomic is not False)
            if not schema_editor.atomic_migration and atomic_operation:
                # Force a transaction on a non-transactional-DDL backend or an
                # atomic operation inside a non-atomic migration.
                with atomic(schema_editor.connection.alias):
                    operation.database_backwards(self.app_label, schema_editor, from_state, to_state)
            else:
                # Normal behaviour
                operation.database_backwards(self.app_label, schema_editor, from_state, to_state)
        return project_state


class SwappableTuple(tuple):
    """
    Subclass of tuple so Django can tell this was originally a swappable
    dependency when it reads the migration file.
    """

    def __new__(cls, value, setting):
        self = tuple.__new__(cls, value)
        self.setting = setting
        return self


def swappable_dependency(value):
    """Turn a setting value into a dependency."""
    return SwappableTuple((value.split(".", 1)[0], "__first__"), value)

```