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
```python
class MigrationGraph:

    def __init__(self):
        self.node_map = {}
        self.nodes = {}

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

# 添加一组Migration和校验一致性
### 数据准备
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