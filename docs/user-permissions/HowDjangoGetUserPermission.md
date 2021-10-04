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
    def _get_group_permissions(self, user_obj):
        # user_groups_field: <django.db.models.fields.related.ManyToManyField 'auth.User.groups'> 
        # get_user_model 是 Django 提供的可配置对象，默认值是: django.contrib.auth.models.User
        # 在 django/conf/global_settings.py 配置文件中, AUTH_USER_MODEL = 'auth.User'
        # 由于 django.contrib.auth.models.User 定义了 groups 多对多字段, 
        # 因此 get_user_model()._meta.get_field('groups') 的意思是, 获取 groups 这个多对多字段对象
        user_groups_field = get_user_model()._meta.get_field('groups')
        # user_groups_query: str 'group__user'
        user_groups_query = 'group__%s' % user_groups_field.related_query_name()
        # Permission.objects.filter(**{'group__user': <django.contrib.auth.models.User zyn>})
        return Permission.objects.filter(**{user_groups_query: user_obj})
```

&nbsp;  
问题-1:  
Permission 指向了哪些表(主动与哪些表产生了关系)?   
Permission 通过声明外键，主动指向 ContentType 表，即: 主动与 ContentType 表建立多对一的关系.  
```shell
class Permission(models.Model):                   # 表名
    name:         str
    content_type: ForeignKey                      # 指向 ContentType 表
    codename:     str 
```

&nbsp;  
问题-2:   
Permission 被哪些表指向了(被动与哪些表产生了关系)?  
Permission 被 Group 采用多对多语法指向，即: 被动与 Group 表建立多对多的关系.  
Permission 被 User 采用多对多语法指向, 即: 被动与 User 表建立多对多的关系.  
```shell
class Group(models.Model):                        # 表名
    name:        str
    permissions: ManyToManyField                  # 指向 Permission 表


# 将继承数打平统一展示
class User(AbstractUser):                         # 表名
    username:         str                         # AbstractUser.username
    first_name:       str                         # AbstractUser.first_name
    last_name:        str                         # AbstractUser.last_name
    email:            str                         # AbstractUser.email
    is_staff:         bool                        # AbstractUser.is_staff
    is_active:        bool                        # AbstractUser.is_active
    date_joined:      datetime                    # AbstractUser.date_joined
    
    password:         str                         # AbstractBaseUser.password
    last_login:       datetime                    # AbstractBaseUser.last_login
    
    is_superuser:     bool                        # PermissionsMixin.is_superuser
    groups:           ManyToManyField             # 指向 Group 表
    user_permissions: ManyToManyField             # 指向 User  表
```

&nbsp;  
问题-3:   
Permission 对象有哪些 "关联与被关联的" 方法/属性?  
**关联:** content_type  
**被关联:** user_set、group_set
```shell
def index(request):
    # ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', 
    #  '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', 
    #  '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', 
    #  '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', 
    #  '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_check_column_name_clashes', 
    #  '_check_constraints', '_check_field_name_clashes', '_check_fields', '_check_id_field', 
    #  '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names', 
    #  '_check_m2m_through_same_relationship', '_check_managers', '_check_model', 
    #  '_check_model_name_db_lookup_clashes', '_check_ordering', 
    #  '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key', 
    #  '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display', 
    #  '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', 
    #  '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', 
    #  '_save_table', '_set_pk_val', '_state', 'check', 'clean', 'clean_fields', 'codename', 'content_type', 
    #  'content_type_id', 'date_error_message', 'delete', 'from_db', 'full_clean', 'get_deferred_fields', 
    #  'group_set', 'id', 'name', 'natural_key', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 
    #  'save', 'save_base', 'serializable_value', 'unique_error_message', 'user_set', 'validate_unique']
    perm = Permission.objects.get(pk=1)
    return HttpResponse(b"hello world!")
```

&nbsp;  
问题-4:  
如何理解 `Permission.objects.filter(**{user_groups_query: user_obj})` 这行代码的含义?   
