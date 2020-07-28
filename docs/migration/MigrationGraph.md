# 概述
`MigrationGraph`是一个有向图(`directed graph`), 每个`migration`对象都是一个`Node`节点, 每个`dependence`(依赖)都是一个`directed edge`(有向边);   

三种类型的节点:     
1. 标识有`initial`的`migration`被称为`root`节点, `root`节点只有`child`单(下)向边.  
2. 终节点只有`parent`单(上)向边.   
3. 中间节点, 既有`parent`也有`child`双向边.    

`MigrationGraph`通过利用`图的深度优先搜索`来找到从某个节点开始到结束的范围节点.


&nbsp;  
# Node(节点)
`Node`节点的`self.children`成员变量对应的是单(下)向边(被依赖的对象), `self.parents`成员变量对应的是单(上)向边(依赖的对象).  
`Node`是单一的结构, 没有继承对象, 有效方法是: `add_child`和`add_parent`.
```python
@total_ordering
class Node:
    """
    A single node in the migration graph. Contains direct links to adjacent nodes in either direction.
    """
    def __init__(self, key):
        self.key = key
        self.children = set()
        self.parents = set()

    def __eq__(self, other):
        return self.key == other

    def __lt__(self, other):
        return self.key < other

    def __hash__(self):
        return hash(self.key)

    def __getitem__(self, item):
        return self.key[item]

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return '<%s: (%r, %r)>' % (self.__class__.__name__, self.key[0], self.key[1])

    def add_child(self, child):
        self.children.add(child)

    def add_parent(self, parent):
        self.parents.add(parent)

```

&nbsp;  
# DummyNode
`DummyNode`对象表示该`Node`对应的`migration`对象没有定义`dependencies`属性, 或者定义关联不上其他`migration`, 导致 `directed graph` 无法有效的构建.
这通常意味着`migrations`目录下的`migration`文件生成出现了`错乱/错误`或人工编辑出现了关联失效情况.   
因此`DummyNode`多了一个`self.error_message`用于保存错误信息, 当需要报错的时候调用`raise_error`方法就能准确报错.  
```python
class DummyNode(Node):

    def __init__(self, key, origin, error_message):
        super().__init__(key)
        self.origin = origin
        self.error_message = error_message

    def raise_error(self):
        raise NodeNotFoundError(self.error_message, self.key, origin=self.origin)
```

&nbsp;  
# MigrationGraph
由于`MigrationGraph`这个类涉及到`图`结构, 加上这个类提供了很多方法, 所以整体感觉这个类很复杂, 给人一种吃不透的感觉, 所以这里要提供大量的场景去触发每个方法(掰开), 透过最终每个方法去了解它内部结构的运作机制(揉碎).   
```python
class MigrationGraph:

    def __init__(self):
        self.node_map = {}          # typing.Dict(typing.Tuple(str, str), Node)
        self.nodes = {}             # typing.Dict(typing.Tuple(str, str), Migration)

    def add_node(self, key, migration):                                        """ 省略代码细节, 仅关注代码结构 """

    def add_dummy_node(self, key, origin, error_message):                      """ 省略代码细节, 仅关注代码结构 """

    def add_dependency(self, migration, child, parent, skip_validation=False): """ 省略代码细节, 仅关注代码结构 """

    def remove_replaced_nodes(self, replacement, replaced):                    """ 省略代码细节, 仅关注代码结构 """

    def remove_replacement_node(self, replacement, replaced):                  """ 省略代码细节, 仅关注代码结构 """

    def validate_consistency(self):                                            """ 省略代码细节, 仅关注代码结构 """

    def forwards_plan(self, target):                                           """ 省略代码细节, 仅关注代码结构 """

    def backwards_plan(self, target):                                          """ 省略代码细节, 仅关注代码结构 """

    def iterative_dfs(self, start, forwards=True):                             """ 省略代码细节, 仅关注代码结构 """

    def root_nodes(self, app=None):                                            """ 省略代码细节, 仅关注代码结构 """

    def leaf_nodes(self, app=None):                                            """ 省略代码细节, 仅关注代码结构 """

    def ensure_not_cyclic(self):                                               """ 省略代码细节, 仅关注代码结构 """

    def _nodes_and_edges(self):                                                """ 省略代码细节, 仅关注代码结构 """

    def _generate_plan(self, nodes, at_end):                                   """ 省略代码细节, 仅关注代码结构 """

    def make_state(self, nodes=None, at_end=True, real_apps=None):             """ 省略代码细节, 仅关注代码结构 """

    def __str__(self):
        return 'Graph: %s nodes, %s edges' % self._nodes_and_edges()

    def __repr__(self):
        nodes, edges = self._nodes_and_edges()
        return '<%s: nodes=%s, edges=%s>' % (self.__class__.__name__, nodes, edges)

    def __contains__(self, node):
        return node in self.nodes

```

&nbsp;  
# 添加节点
```python
class MigrationGraph:
    
    def __init__(self):
        self.node_map = {}          # typing.Dict(typing.Tuple(str, str), Node)
        self.nodes = {}             # typing.Dict(typing.Tuple(str, str), Migration)

    #####################################################################################
    # 参数类型注解:
    # key: typing.Tuple(str, str)  # key值举例: ('polls', '0001_initial') 
    # migration: Migration         # 对象位置举例: polls.migrations.0001_initial.Migration
    #####################################################################################
    def add_node(self, key, migration):
        #####################################################################################
        # 如果 key 存在于 self.node_map 中, 就报错.
        # 这句话的目的很明确, 就是让你在 `添加节点` 之前, 先自己判断和保证: 要添加的节点不存在.
        #####################################################################################
        assert key not in self.node_map
    
        #####################################################################################
        # 创建一个Node对象, Node内部有两个链式结构, 分别是: self.parents 和 self.children
        # 用于存储 依赖(parent) 和 被依赖(children) 的对象, 这些依赖关系的建立在后续的
        # `add_dependency`会讲到. 
        #####################################################################################
        node = Node(key)
    
        #####################################################################################
        # self.node_map 用于存放 key 和 Node 的映射, 节点的依赖关系都在这里操作.
        # self.nodes 用于存放 key 和 Migration 的映射, 获取节点的对象基础信息都在这里操作.
        #####################################################################################
        self.node_map[key] = node
        self.nodes[key] = migration
```
### 添加一个节点
下面的代码有一个假设的前提条件, `polls`这个`app`必须要存在, `polls/migrations`这个目录必须要存在, `polls/migrations/0001_initial.py`这个文件必须要存在. 这几个文件如何生成[请参考这里](https://docs.djangoproject.com/en/3.0/intro/tutorial02/#creating-models).
```python
import importlib
from django.db.migrations.graph import MigrationGraph

                                       
app_label = "polls"                                                 
module_name = "0001_initial"
module_path = app_label + ".migrations." + module_name
migration_module = importlib.import_module(module_path)         # 等同于: import polls.migrations.0001_initial
migration = migration_module.Migration(module_name, app_label)  # 等同于: polls.migrations.0001_initial.Migration()

key = (app_label, module_name)
digraph = MigrationGraph()   
digraph.add_node(key=key, migration=migration)                  # 添加一个migration到digraph 
```

&nbsp;
# 添加依赖
历史指令样例文件: [0001_initial.py](fragments/polls/migrations/0001_initial.py)   
历史指令样例文件: [0002_menu.py](fragments/polls/migrations/0002_menu.py)   
历史指令样例文件: [0003_group.py](fragments/polls/migrations/0003_group.py)
```python
class MigrationGraph:

    def __init__(self):
        self.node_map = {}          # typing.Dict(typing.Tuple(str, str), Node)
        self.nodes = {}             # typing.Dict(typing.Tuple(str, str), Migration)

    #####################################################################################
    # 参数类型注解:
    # key：          typing.Dict(typing.Tuple(str, str)
    # origin:        Migration
    # error_message: str
    #
    # `DummyNode` 的解释看上面.
    #
    # 将 `DummyNode` 加入到 `self.node_map` 中的目的是用于标识 `该node` 是脏节点(假节点).
    # 这意味着后续代码需要自行通过isinstance来筛选出干净的节点或者脏的节点. 
    #
    # 置空 self.nodes[key] = None 是为了确保结构的干净. 
    #####################################################################################
    def add_dummy_node(self, key, origin, error_message):
        node = DummyNode(key, origin, error_message)
        self.node_map[key] = node
        self.nodes[key] = None

    #################################################################################
    # 如果 self.graph 中存在 DummyNode , 那么就抛出异常(报错).
    #################################################################################
    def validate_consistency(self):
        """Ensure there are no dummy nodes remaining in the graph."""
        [n.raise_error() for n in self.node_map.values() if isinstance(n, DummyNode)]

    #####################################################################################
    # 参数类型注解:
    # migration:         Migration
    # child:             typing.Dict(typing.Tuple(str, str)  # 被依赖的Node的key
    # parent:            typing.Dict(typing.Tuple(str, str)  # 依赖的Node的key
    # skip_validation:   bool       # True: 函数内完成验证, False: 函数外由开发自行触发验证.
    #####################################################################################
    def add_dependency(self, migration, child, parent, skip_validation=False):
        #################################################################################
        # polls.migrations.0001_initial.Migration 作为顶点节点, 不能在这里设定关联关系.
        # 顶点节点指的是, 它的 dependencies = [] 是空的值, 这样会导致错将 0001_initial 
        # 纳入到 DummyNode 范畴.   
        # 
        # 因为 这里的代码 要求建立关系的节点必须要定义 dependencies, 
        # 而定义 dependencies 的目的有两个:
        # 1. 用于标识版本号
        # 2. 用于标注必须先有依赖对象的那些表, 才能有我当前的操作, 否则会出现错误.
        # 
        # child:  以 self.node_map 的 key 的形式 描述 当前(参数)migration 对象 
        # parent: 以 self.node_map 的 key 的形式 描述 当前(参数)migration 对象的 dependencies 成员.
        #
        # if child not in self.nodes: 
        # 如果当前的migration的key不存在与 self.nodes中, 则表示这个 key 是由问题的, 将其纳入到 DummyNode 范畴.
        #
        # if parent not in self.nodes:
        # 如果当前的migrations.dependencies成员的key不存在与self.nodes中, 则表示这个 key 是由问题的, 将其纳入到 DummyNode 范畴.
        #################################################################################
        if child not in self.nodes:
            error_message = (
                "Migration %s dependencies reference nonexistent"
                " child node %r" % (migration, child)
            )
            self.add_dummy_node(child, migration, error_message)
        if parent not in self.nodes:
            error_message = (
                "Migration %s dependencies reference nonexistent"
                " parent node %r" % (migration, parent)
            )
            self.add_dummy_node(parent, migration, error_message)
        
        #################################################################################
        # self.node_map[child] 是当前 migration(参数) 的那个 Node 节点对象, 为当前 Node节点 添加依赖: self.node_map[parent]
        #
        # self.node_map[parent] 是依赖对象的Node节点对象, 为这个 Node 节点对象 添加被依赖对象: self.node_map[child]
        #################################################################################
        self.node_map[child].add_parent(self.node_map[parent])
        self.node_map[parent].add_child(self.node_map[child])

        #################################################################################
        # 验证一致性
        #################################################################################
        if not skip_validation:
            self.validate_consistency()
```


&nbsp;  
# RootNode(顶点)
```python
class MigrationGraph:

    def __init__(self):
        self.node_map = {}          # typing.Dict(typing.Tuple(str, str), Node)
        self.nodes = {}             # typing.Dict(typing.Tuple(str, str), Migration)

    #################################################################################
    # 参数类型注解:
    # app: str                  # 例如: 'admin' 或 'auth' 或 'polls' 等
    #
    # 参数作用:
    # 由于 self.nodes 是 key, value 结构, 而 key 本身的结构是:  typing.Tuple(str, str),
    # 因此 一个 self.nodes 对象, 可以存放多个 app 的数据而不会发生覆盖或冲突的情况.
    # 如果参数 app 是None, 那么函数将会返回所有 app 的 RootNode.
    # 如果参数 app 是一个具体的 app名称(例如: polls), 那么函数就会返回 polls 的 RootNode.
    #################################################################################
    def root_nodes(self, app=None):
        roots = set()
        
        #############################################################################
        # 类型注解:
        # node:                           typing.Tuple(str, str)
        # self.nodes[node]:               Migration
        # self.node_map[node]             Node
        # self.node_map[node].parents     typing.List(typing.Tuple(str, str), ...)
        # 备注: 这里就不应该取名为 node, 而是 node_key 更适合.
        # 
        # 顶点的那个node的parents肯定是空的, 而python得 all([]) 返回得是 True, 所以当 node 是一个顶点时: 
        # all(key[0] != node[0] for key in self.node_map[node].parents) == all([]) == True
        # 
        # key:                           Node
        # node:                          Node
        # key[0] == node[0] == node.key[0] == 'admin' 或 'auth' 或 'polls'
        # 既然 顶点的parents是空就能满足场景条件, 这里的条件为什么还要写 key[0] != node[0] ?
        # 我的理解是顶点有两种情况: 
        # 一种就是常规顶点, 即: parents为空
        # 一种是外部依赖, 即: 顶点也有parents, 但是这个parents 是其他app.
        #############################################################################
        for node in self.nodes:
            if all(key[0] != node[0] for key in self.node_map[node].parents) and (not app or app == node[0]):
                roots.add(node)
        return sorted(roots)
```


&nbsp;  
# LeafNode(末梢叶节点)
```python
class MigrationGraph:

    def __init__(self):
        self.node_map = {}          # typing.Dict(typing.Tuple(str, str), Node)
        self.nodes = {}             # typing.Dict(typing.Tuple(str, str), Migration)

    #############################################################################
    # 末梢叶节点的children肯定是空的, python得 all([]) 返回得是 True, 所以当 node 是一个末梢叶节点时:
    #  all(key[0] != node[0] for key in self.node_map[node].children) == all([]) == True
    # 
    # 除了这里描述有差别, 其余的都与上面个的RootNode(顶点)一致.
    #############################################################################
    def leaf_nodes(self, app=None):
        leaves = set()
        for node in self.nodes:
            if all(key[0] != node[0] for key in self.node_map[node].children) and (not app or app == node[0]):
                leaves.add(node)
        return sorted(leaves)
```

