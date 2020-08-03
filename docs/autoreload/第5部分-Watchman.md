# Watchman
`Watchman`这个环节`Django`提供了两种实现方式, 一种是使用第三方库[pywatchman](https://github.com/facebook/watchman), 另外一种是内置实现`StatReloader`.  由于`Django`默认采用内置实现, 所以这里仅分析内置实现.   
`Watchman`的主要工作职责在[这里](第1部分-核心原理.md)已经介绍过了, 即: 扫描文件, 比较文件的最后修改时间; 但是本文更关心的是扫描文件之外的其他能力.  

&nbsp;   
# 代码结构  
`BaseReloader`是一个抽象类, 提供了一组具有默认实现的抽象方法.    
`StatReloader`继承了`BaseReloader`之后, 原封不动的直接使用了`BaseReloader`的默认实现;      
`BaseReloader`声明了 `tick` 和 `check_availability` 两个接口, 要求必须由继承者来完成具体的实现, 这同时也意味着`BaseReloader`不能单独用来实例化.   

源码片段: django/utils/autoreload.py#249行
```python
class BaseReloader:
    def __init__(self):
        self.extra_files = set()
        self.directory_globs = defaultdict(set)
        self._stop_condition = threading.Event()

    def watch_dir(self, path, glob):                            """ 省略代码细节, 仅关注代码结构 """

    def watched_files(self, include_globs=True):                """ 省略代码细节, 仅关注代码结构 """

    def wait_for_apps_ready(self, app_reg, django_main_thread): """ 省略代码细节, 仅关注代码结构 """

    def run(self, django_main_thread):                          """ 省略代码细节, 仅关注代码结构 """

    def run_loop(self):                                         """ 省略代码细节, 仅关注代码结构 """

    def tick(self):
        raise NotImplementedError('subclasses must implement tick().')

    @classmethod
    def check_availability(cls):
        raise NotImplementedError('subclasses must implement check_availability().')

    def notify_file_changed(self, path):                        """ 省略代码细节, 仅关注代码结构 """

    @property
    def should_stop(self):
        return self._stop_condition.is_set()

    def stop(self):
        self._stop_condition.set()


class StatReloader(BaseReloader):
    
    def tick(self):                                             """ 省略代码细节, 仅关注代码结构 """
    
    def snapshot_files(self):                                   """ 省略代码细节, 仅关注代码结构 """
    
    @classmethod
    def check_availability(cls):                                
        return True                                                                                   
```  
|方法名|描述|
|---|:---|
|**def** watch_dir| 按[glob](https://docs.python.org/3/library/glob.html)模板, 添加目录到`self.directory_globs`中 |
|**def** watched_files| 扫描所有python模块的文件、`self.directory_globs`中符合`glob`模板的文件. |
|**def** wait_for_apps_ready| apps是一个模块级别的变量, 等待apps全部加载完成, 然后set()通知到当前函数的wait() |
|**def** run| 通知`autoreload_start`的所有订阅者, `BaseReloader`已经准备就绪, 订阅者可以将自己要watch的文件或目录, 添加到`BaseReloader`中来统一由`BaseReloader`进行代理扫描. |
|**def** run_loop| 开始循环扫描 |
|**def** tick| 公共接口, 不具备默认实现, 要求继承者必须自行实现: 该接口的作用是检查文件最后修改时间是否发生变更 |
|**def** check_availability| 公共接口, 不具备默认实现, 要求继承者必须自行实现: 该接口的作用是告知调用者当前对象是否可用 |
|**def** notify_file_changed| 通知`file_changed`的订阅者, 文件已经发生变动, 请自行处理后续动作, 缓存该清清, 文件该删删. 我要退出当前进程了. |
|**def** should_stop| 返回bool值, 检查`_stop_condition`这个Event, 是否要停止检查 |
|**def** stop| 将`_stop_condition`这个Event, 设定为True |

&nbsp;  
# Watchman 入口
在 [第四部分-两个线程](第4部分-两个线程.md) 的最后, 聊到了Watchman的入口, 往下延申就是`StatReloader.run`方法.   
```python
class BaseReloader:

    def wait_for_apps_ready(self, app_reg, django_main_thread):
        """
        django_main_thread.is_alive: This method returns True just before the run() method 
                                     starts until just after the run() method terminates.
                                     译: 在threading.run()方法运行结束之前, 返回的都是True.

        app_reg.ready_event.wait():  如果不提供timeout参数, 除非有其他线程.set(), 否则就会一直堵塞.
                                     如果提供timeout参数, 除非有其他线程.set(). 否则timeout时间一到就会返回False.
        """
        while django_main_thread.is_alive():
            if app_reg.ready_event.wait(timeout=0.1):
                return True
        else:
            logger.debug('Main Django thread has terminated before apps are ready.')
            return False

    def run(self, django_main_thread):
        """
        通知所有订阅了 autoreload_started 的消费者说, 我的app已经加载好了, 
        你们可以开始把需要监控文件最后修改时间变更的清单发给我, 由我来统一进行监控和比较.
        """
        logger.debug('Waiting for apps ready_event.')
        self.wait_for_apps_ready(apps, django_main_thread)
        logger.debug('Apps ready_event triggered. Sending autoreload_started signal.')
        autoreload_started.send(sender=self)
        self.run_loop()
```

&nbsp;  
# Signal 订阅
`django.utils.translation`模块中有一个监控所有`.mo`后缀文件的需求, 它在`Watchman`入口之前就已经订阅了 `autoreload_started`.  
```python
# django/utils/translation/__init__.py#60行
class Trans:
    def __getattr__(self, real_name):
        # 将watch_for_translation_changes函数当作autoreload_started订阅者, 即: 任何消息通知都会抵达这里.
        from django.utils.translation.reloader import watch_for_translation_changes, translation_file_changed
        autoreload_started.connect(watch_for_translation_changes, dispatch_uid='translation_file_changed')      # 这里
        file_changed.connect(translation_file_changed, dispatch_uid='translation_file_changed')

```

&nbsp;  
# Signal 通知
```python
class BaseReloader:

    def run(self, django_main_thread):
        ...
        autoreload_started.send(sender=self)                       # apps 加载完成后, 通知订阅了autoreload_started的消费者
        ...
```

&nbsp;  
# Signal 响应
```python
# django/utils/translation/reloader.py#13行
def watch_for_translation_changes(sender, **kwargs):
    from django.conf import settings

    if settings.USE_I18N:
        directories = [Path('locale')]                              # 1. 将locale目录包裹成Path对象, 写入到列表中
        directories.extend(
            Path(config.path) / 'locale'
            for config in apps.get_app_configs()
            if not _is_django_module(config.module)
        )
        directories.extend(Path(p) for p in settings.LOCALE_PATHS)  # 2. 将settings.LOCALE_PATHS都追加到列表中

        for path in directories:                                    # 3. 遍历列表
            sender.watch_dir(path, '**/*.mo')                       # 4. 调用StatReloader.watch_dir, 将这些路径和glob加入到, 待扫描目录中.
```

&nbsp;  
# Watchman 数据就位
由于`StatReloader.run`中直接使用了`autoreload_started.send`, 这在`OOP`的概念里面被称为`依赖`关系(即: `StatReloader`依赖`autoreload_started`).   
那么所有订阅了`autoreload_started`的消费者, 也就间接的与`StatReloader`对象发生了潜在的关联关系, 所有`Signal 响应`的行为, 最终都会作用回到`StatReloader`中.  
以`translation.reloader.watch_for_translation_changes`为例, 它回调了`StatReloader.watch_dir`方法, 将要监控的路径(`pathlib.Patch`)和模板(`**/*.mo`), 塞到`StatReloader.directory_globs`中.  
```python
class BaseReloader:

    """
    调用watch_dir方法, 将需要监控的Path(路径/模板), 
    追加到self.directory_globs的行为, 被称为 数据就位.
    """

    def __init__(self):
        self.directory_globs = defaultdict(set)

    def watch_dir(self, path, glob):
        path = Path(path)
        try:
            path = path.absolute()
        except FileNotFoundError:
            logger.debug(
                'Unable to watch directory %s as it cannot be resolved.',
                path,
                exc_info=True,
            )
            return
        logger.debug('Watching dir %s with glob %s.', path, glob)
        self.directory_globs[path].add(glob)
```

&nbsp;  
# Watchman 开始循环
```python
class BaseReloader:

    def run(self, django_main_thread):
        ...
        self.run_loop()                     # 1. 主线程进入循环

    def run_loop(self):
        ticker = self.tick()                # 2. self.tick()调用的是StatReloader的tick方法, 返回的是一个generator对象.
        while not self.should_stop:
            try:
                next(ticker)                # 3. next(ticker)表示, 执行 StatReloader.tick 方法内的 while 1 次.
            except StopIteration:
                break
        self.stop()                         
```

&nbsp;  
# Watchman tick接口
`tick接口`是用来迭代所有`self.directory_globs`中所有文件, 并且比较文件的两个最后修改时间是否发生变化.
```python

class StatReloader(BaseReloader):
    SLEEP_TIME = 1  # Check for changes once per second.

    def tick(self):
        mtimes = {}
        while True:
            for filepath, mtime in self.snapshot_files():       # 4. 遍历所有文件
                old_time = mtimes.get(filepath)                 # 5. 尝试从缓存中提取该文件的最后修改时间 
                mtimes[filepath] = mtime                        # 6. 写入该文件的最后修改时间
                if old_time is None:                            # 7. old_time is None 表示文件还没由缓存过, 不做比较.
                    logger.debug('File %s first seen with mtime %s', filepath, mtime)
                    continue
                elif mtime > old_time:                          # 8. old_time 和 当前最后修改时间比较, 
                    logger.debug('File %s previous mtime: %s, current mtime: %s', filepath, old_time, mtime)
                    self.notify_file_changed(filepath)          # 9. 检查到文件已发生变化, 通知变化.

            time.sleep(self.SLEEP_TIME)                         # 10. 停1秒钟, 然后再继续扫描和继续比较.
            yield

    def snapshot_files(self):
        seen_files = set()
        for file in self.watched_files():                       # 4.1 遍历所有文件
            if file in seen_files:                              # 4.2 去重
                continue
            try:
                mtime = file.stat().st_mtime                    # file 变量的类型是: pathlib.Path, 它提供了stat方法和glob方法
            except OSError:
                # This is thrown when the file does not exist.
                continue
            seen_files.add(file)
            yield file, mtime
```

&nbsp;  
# Watchman 遍历文件
`pathlib.Path.glob(pattern)`根据参数`pattern`来模糊匹配到指定目录下面符合规则的文件, 返回的是一个列表(`[Path('xx1'), Path('xx2'), ..]`).   
例如:  "/home/zhangsan"目录下有文件 "a.py", "b.py", "c.txt" , `Path('/home/zhangsan'').glob('*.py')` 就会把"a.py"和"b.py"找出来.  
```python
class BaseReloader:
    
    def __init__(self):
        self.directory_globs = defaultdict(set)

    def watched_files(self, include_globs=True):
        yield from iter_all_python_module_files()                       # 所有python内置模块的文件
        if include_globs:
            for directory, patterns in self.directory_globs.items():
                for pattern in patterns:
                    yield from directory.glob(pattern)                  # 订阅autoreload_started的消费者添加的文件
```

&nbsp;  
# Watchman 通知(已发生变化)
`StatReloader`的tick接口, 每停顿一秒钟都会重新扫描一次所有监控列表中的文件, 当文件发生变化时, 就会通知订阅了`file_changed`的消费者.   
也就是说`StatReloader`和`file_changed`也产生了关联关系.
```python
class BaseReloader:
    
    def notify_file_changed(self, path):
        results = file_changed.send(sender=self, file_path=path)                        #2. 通知那些订阅了`file_changed`的消费者
        logger.debug('%s notified as changed. Signal results: %s.', path, results)      
        if not any(res[1] for res in results):
            trigger_reload(path)

class StatReloader(BaseReloader):
    SLEEP_TIME = 1  # Check for changes once per second.

    def tick(self):
        mtimes = {}
        while True:
            for filepath, mtime in self.snapshot_files():       
                old_time = mtimes.get(filepath)                 
                mtimes[filepath] = mtime                        
                if old_time is None:                            
                    logger.debug('File %s first seen with mtime %s', filepath, mtime)
                    continue
                elif mtime > old_time:                          
                    logger.debug('File %s previous mtime: %s, current mtime: %s', filepath, old_time, mtime)
                    self.notify_file_changed(filepath)                                  # 1. 这里

            time.sleep(self.SLEEP_TIME)                         
            yield

    
```

&nbsp;  
# Signal 处理(已发生变化情况)
还是以`django.utils.translation`为例, 它也订阅了`file_changed`.
他就做了这么一件事情, 当接到文件发生变化的通知后, 清除缓存. 
```python
# django/utils/translation/reloader.py#19行
def translation_file_changed(sender, file_path, **kwargs):
    """Clear the internal translations cache if a .mo file is modified."""
    if file_path.suffix == '.mo':
        import gettext
        from django.utils.translation import trans_real
        gettext._translations = {}
        trans_real._translations = {}
        trans_real._default = None
        trans_real._active = Local()
        return True
```

&nbsp;
# Watchman 退出当前进程
通知了所有`file_changed`的消费者, 并且等这些消费者全部执行完各自的事务之后, `Watchman`接下来要做的事情就是结束自己的这个子进程,
让主进程重新启动另外一个子进程, 由另外一个Watchman再重新完成文件监控的任务.
```python
def trigger_reload(filename):
    logger.info('%s changed, reloading.', filename)
    print("trigger_reload: os.getpid(): ", os.getpid())
    sys.exit(3)                                                                         # 退出当前进程

class BaseReloader:
    
    def notify_file_changed(self, path):
        results = file_changed.send(sender=self, file_path=path)                       
        logger.debug('%s notified as changed. Signal results: %s.', path, results)      
        if not any(res[1] for res in results):                      
            trigger_reload(path)                                                        # 这里
```

&nbsp;
# 再次拉起子进程, 往复循环
具体的分析在 [第3部分-两个进程](第3部分-两个进程.md) .

&nbsp;  
# 题外话
本来想借这个机会去写一个`热更新`的程序, 让程序不是重启而是直接`reload`, 这样让代码更新更丝滑.    
在尝试过程中使用`importlib.import_module(name)` 和 `importlib.reload(module)`, 这两个函数不能直接覆盖现有模块的对象.  
必须使用`importlib.reload(module)的返回值`中的`class`来创建对象, 这种方式必然是要对class做hook的.   

网上找了两个库来参考: [reloadr](https://github.com/hoh/reloadr) 和 [hotreload](https://github.com/say4n/hotreload), 外加翻阅了`vue.js`的官方介绍它自己的`hotreload`.   
最终得出的结论就是, `hotreload`比较有局限性, 并不是什么都可以`hotreload`:  
 - 可以`hotreload`的情况
   1. `class`新增`method`
   2. `class`新增`attribute`
   3. `class`更新`method`内的代码
 - 不可以`hotreload`的情况
   1. `class`删除某个被重度使用的`method`
   2. `class`删除某个`attribute`
 
即便是`vue.js`也是局部`hotreload`, 涉及到`<script>`部分也是要`Destroy`掉原有对象, 重新实例化相同类型的对象; 并且在`Product`模式下不建议使用.   
