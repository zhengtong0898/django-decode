# 问题
`Django` 是如何获取到用户、组和菜单的权限的呢?   
本文关注点是: 获取用户和用户组的权限的ORM是怎么写的，以及该ORM写法的工作原理梳理和理解。  

&nbsp;  
### 切入点
延续 [CanViewUser](./CanViewUser.md) 的 `get_app_list` 方法，继续深入探究权限的获取。  
通过调用栈, 以全局的视角去观察获取权限的顺序和路径。  
> 设计模式  
> 为什么获取用户这种简单的行为，需要这么长的调用栈?  
> 从文件名和对象名去分层考虑它们的目的和作用，例如: backends.ModelBackend 是不是专做缓存层?  
```shell
# 获取用户的权限(多对多)
django.contrib.admin.sites.AdminSite.index                                  # /admin 函数入口
django.contrib.admin.sites.AdminSite.get_app_list
django.contrib.admin.sites.AdminSite._build_app_dict
django.contrib.admin.options.BaseModelAdmin.has_module_permission
django.contrib.auth.models.PermissionsMixin.has_module_perms
django.contrib.auth.models._user_has_module_perms                          
django.contrib.auth.backends.ModelBackend.has_module_perms
django.contrib.auth.backends.ModelBackend.get_all_permissions
django.contrib.auth.backends.BaseBackend.get_all_permissions
django.contrib.auth.backends.ModelBackend.get_user_permissions              # 获取用户的所有权限
django.contrib.auth.backends.ModelBackend.get_group_permissions             # 获取用户组的所有权限
```

&nbsp;  
### 获取当前用户的所有权限
延续切入点的调用栈, 继续深入去观察获取用户的所有权限的调用栈
```shell
# 获取当前用户的所有权限的调用栈
django.contrib.auth.backends.ModelBackend.get_user_permissions
django.contrib.auth.backends.ModelBackend._get_user_permissions


# 观察实际的获取权限代码
class ModelBackend(BaseBackend):

    # user_obj: <django.contrib.auth.models.User zyn>
    # 由于 django.contrib.auth.models.User 定义了 user_permissions 多对一字段, 
    # 因此 user_obj.user_permissions.all() 的意思是, 获取 zyn 用户的所有权限数据.
    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()
```


&nbsp;  
### 获取当前用户所在组的所有权限
延续切入点的调用栈, 继续深入去观察获取用户的所有权限的调用栈
```shell
# 获取当前用户的所有权限的调用栈
django.contrib.auth.backends.ModelBackend.get_group_permissions
django.contrib.auth.backends.ModelBackend._get_group_permissions


# 观察实际的获取权限代码
class ModelBackend(BaseBackend):

    # user_obj: <django.contrib.auth.models.User zyn>
    # 
    def _get_group_permissions(self, user_obj):
        # user_groups_field: <django.db.models.fields.related.ManyToManyField 'auth.User.groups'> 
        # get_user_model 是 Django 提供的可配置对象，默认值是: django.contrib.auth.models.User
        # 在 django/conf/global_settings.py 配置文件中, AUTH_USER_MODEL = 'auth.User'
        # 由于 django.contrib.auth.models.User 定义了 groups 多对多字段, 
        # 因此 get_user_model()._meta.get_field('groups') 的意思是, 获取 groups 这个多对多字段对象
        user_groups_field = get_user_model()._meta.get_field('groups')
        # user_groups_query: str 'group__user'
        # TODO: 待补充这里的关系描述
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        # Permission.objects.filter(**{'group__user': <django.contrib.auth.models.User zyn>})
        # TODO: 待补充这里的查询逻辑
        return Permission.objects.filter(**{user_groups_query: user_obj})
```
