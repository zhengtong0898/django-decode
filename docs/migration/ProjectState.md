```python
class ProjectState:
    """
    Represent the entire project's overall state. This is the item that is
    passed around - do it here rather than at the app level so that cross-app
    FKs/etc. resolve properly.
    """

    def __init__(self, models=None, real_apps=None):
        self.models = models or {}
        # Apps to include from main registry, usually unmigrated ones
        self.real_apps = real_apps or []
        self.is_delayed = False

    def add_model(self, model_state):                                   """ 省略代码细节, 仅关注代码结构 """

    def remove_model(self, app_label, model_name):                      """ 省略代码细节, 仅关注代码结构 """

    def _find_reload_model(self, app_label, model_name, delay=False):   """ 省略代码细节, 仅关注代码结构 """

    def reload_model(self, app_label, model_name, delay=False):         """ 省略代码细节, 仅关注代码结构 """

    def reload_models(self, models, delay=True):                        """ 省略代码细节, 仅关注代码结构 """

    def _reload(self, related_models):                                  """ 省略代码细节, 仅关注代码结构 """

    def clone(self):                                                    """ 省略代码细节, 仅关注代码结构 """

    def clear_delayed_apps_cache(self):                                 """ 省略代码细节, 仅关注代码结构 """

    @cached_property
    def apps(self):                                                     """ 省略代码细节, 仅关注代码结构 """

    @property
    def concrete_apps(self):                                            """ 省略代码细节, 仅关注代码结构 """

    @classmethod
    def from_apps(cls, apps):                                           """ 省略代码细节, 仅关注代码结构 """

    def __eq__(self, other):                                            """ 省略代码细节, 仅关注代码结构 """
        return self.models == other.models and set(self.real_apps) == set(other.real_apps)
```