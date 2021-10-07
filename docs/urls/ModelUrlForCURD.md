# 问题  
`DjangoAdmin` 是如何为模型动态生成新增、修改、删除的URL的呢?

在 `django.contrib.auth.urls.urlpatterns` 中并没有定义 `/admin/auth/user/2/change/` 这种 `uri`,
但是 `DjangoAdmin` 却提供了这种具体的访问地址, 本文的关注点是这个路由定义的位置和路由寻找的过程.  

&nbsp;  
# 路由定义  
**线索追踪:** 由于 `/admin/auth/user/2/change/` 是一个动态路由, 它是按模块拆分和ID拆分成多个层级的路由,
所以采用精确查找无法找到路由定义在哪里, 经过多番尝试最终采用 `/change` 关键词, 
在 `django.contrib.admin.options.ModelAdmin.get_urls` 中找到了线索.    

**源码**
```python3
class ModelAdmin(BaseModelAdmin):
    
    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path('', wrap(self.changelist_view), name='%s_%s_changelist' % info),
            path('add/', wrap(self.add_view), name='%s_%s_add' % info),
            path('autocomplete/', wrap(self.autocomplete_view), name='%s_%s_autocomplete' % info),
            path('<path:object_id>/history/', wrap(self.history_view), name='%s_%s_history' % info),
            path('<path:object_id>/delete/', wrap(self.delete_view), name='%s_%s_delete' % info),
            path('<path:object_id>/change/', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            path('<path:object_id>/', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]
```

**问题-1: 这段代码是什么时候被触发运行的呢?**   
经调试发现, 这个路由是在 `Django` 启动时被触发, 在具体访问时并不触发.  
TODO: 需要列出调用栈.

**问题-2: 如何理解 `<path:object_id>` 是什么意思?**  

**问题-3: wrap具体都在做些什么事情?**  

&nbsp;  
# 路由查找过程

