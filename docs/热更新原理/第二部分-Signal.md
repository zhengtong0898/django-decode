# django.dispatch.Signal(信号调度对象)
**django.dispatch.Signal(后续简称DSignal)** 是 `多生产者/多消费者` 调度机制, 一讲到`生产/消费`的概念就肯定逃离不开`发布订阅模式`.  
通俗的讲`DSignal`是一个用来存储多个`消费者的`一个容器, 当`生产者`向`DSignal`发出一条消息时, `DSignal`就会通知所有`消费者`去处理这条消息.  
上述就是`DSignal`的核心原理, 除此之外它也提供了一些管理功能(稍后会详细讨论).  

&nbsp;  

# 代码结构(Structure)
源码片段: django/dispatch/dispatcher.py#19行 
```python
class Signal:

    def __init__(self, providing_args=None, use_caching=False):
        self.receivers = []
        self.lock = threading.Lock()
        self.use_caching = use_caching
        self.sender_receivers_cache = weakref.WeakKeyDictionary() if use_caching else {}
        self._dead_receivers = False

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None): """ 省略代码细节, 仅关注代码结构 """

    def disconnect(self, receiver=None, sender=None, dispatch_uid=None):    """ 省略代码细节, 仅关注代码结构 """

    def has_listeners(self, sender=None):                                   """ 省略代码细节, 仅关注代码结构 """

    def send(self, sender, **named):                                        """ 省略代码细节, 仅关注代码结构 """

    def send_robust(self, sender, **named):                                 """ 省略代码细节, 仅关注代码结构 """

    def _clear_dead_receivers(self):                                        """ 省略代码细节, 仅关注代码结构 """

    def _live_receivers(self, sender):                                      """ 省略代码细节, 仅关注代码结构 """

    def _remove_receiver(self, receiver=None):                              """ 省略代码细节, 仅关注代码结构 """
```

|方法名|描述|
|---|:---|
|**def** connect|将参数`receiver`添加到`self.receivers`中, 当作是一个`消费者`.|
|**def** disconnect|将`receiver`从`self.receivers`中移除掉.|
|**def** has_listeners|容器中有没有某个`消费者`.|
|**def** send|发送消息给`消费者`|
|**def** send_robust|发送消息给`消费者`, 含异常处理(即: 保证不报错)|
|**def** _clear_dead_receivers|清除那些`weakref`已经无效的`消费者`|
|**def** _live_receivers|找出那些仍然有效的`消费者`|
|**def** _remove_receiver|用于标识`self.receivers`消费者列表中存在无效`消费者`|

&nbsp;  
# 使用方法(Usage)
- 单消费者代码 
```python
from django.dispatch import Signal


class Person(object):

    def __init__(self, name):
        self.name = name

    def eat(self, something):
        print("%s is eating %s" % (self.name, something))


def consumer_1(**kwargs):
    sender = kwargs.pop("sender")                               # 由于python是弱类型语言, 这种写法其实非常危险...
    sender.eat(kwargs.pop("abc"))                               # 不确定性太多, 尤其是团队协作时...


def main():
    pubsub = Signal()                                           # 创建容器(调度器)对象
    pubsub.connect(consumer_1)                                  # 将消费者添加到容器对象中
    pubsub.send(Person("zhangsan"), abc="apple")                # 通知消费者, 有消息来了(并且将消费者需要用到的Person对象也传递过去)


if __name__ == '__main__':
    main()


# output:
# zhangsan is eating apple
```
  
- 多消费者代码
```python
from django.dispatch import Signal


class Person(object):

    def __init__(self, name):
        self.name = name

    def eat(self, something):
        print("%s is eating %s" % (self.name, something))


def consumer_1(**kwargs):
    sender = kwargs.pop("sender")
    sender.eat(kwargs.pop("abc"))


def main():
    zhangsan = Person("zhangsan")
    lisi = Person("lisi")

    pubsub = Signal()                                 # 创建容器(调度器)对象
    pubsub.connect(consumer_1, sender=zhangsan)       # 将消费者添加到容器对象中
    pubsub.connect(consumer_1, sender=lisi)           # 将消费者添加到容器对象中
    pubsub.send(zhangsan, abc="apple")                # 通知消费者, 有消息来了(并且将消费者需要用到的Person对象也传递过去)
    pubsub.send(lisi, abc="banana")                   # 通知消费者, 有消息来了(并且将消费者需要用到的Person对象也传递过去)


if __name__ == '__main__':
    main()

# output:
# zhangsan is eating apple
# lisi is eating banana
```

&nbsp;  

# 消费者保存原理
`DSignal`在将`消费者`添加到`self.receivers`之前, 都会为每个`消费者`生成一个`id`, 这通常被称为频道.     

生成`id`的源码片段: django/dispatch/dispatcher.py#49行 
```python
def _make_id(target):
    if hasattr(target, '__func__'):
        return (id(target.__self__), id(target.__func__))
    return id(target)


class Signal:

    def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
        lookup_key = (_make_id(receiver), _make_id(sender))                      # lookup_key == id 
        with self.lock:
            if not any(r_key == lookup_key for r_key, _ in self.receivers):
                self.receivers.append((lookup_key, receiver))
```

&nbsp;  

# 消息推送原理
当`self.receivers`中的`消费者`都按照特定频道存在时, 消息推送就必须按频道来推送.    

查找`id`的源码片段: django/dispatch/dispatcher.py#152行
```python
def _make_id(target):
    if hasattr(target, '__func__'):
        return (id(target.__self__), id(target.__func__))
    return id(target)


class Signal:

    def send(self, sender, **named):
        return [
            (receiver, receiver(signal=self, sender=sender, **named))
            for receiver in self._live_receivers(sender)
        ]

    def _live_receivers(self, sender):
        receivers = []
        with self.lock:
            senderkey = _make_id(sender)                                        # 频道id
            for (receiverkey, r_senderkey), receiver in self.receivers:         # r_senderkey == senderkey 比较频道id
                if r_senderkey == NONE_ID or r_senderkey == senderkey:
                    receivers.append(receiver)

        return receivers
```

&nbsp;

# 其他细节
- 每个涉及到`self.receivers`的操作, 都会加一个`with self.lock:`操作, 这是为了保证线程安全.
- 缓存(LazyEvaluated)提升查找速度, django的思想, 只要是涉及到查找列表的操作, 都应该利用缓存特性.
- weakRef是一个减少内存开销的手法(避免对象太庞大, 复制等问题).
