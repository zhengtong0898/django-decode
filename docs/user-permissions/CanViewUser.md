当我给一个用户添加 `CanViewUser` 权限时, 在`Django`里面发生了什么?   
当前文档试图通过页面、数据库、源代码来描述整个过程的来龙去脉.

&nbsp;  
### 页面操作
zt 用户视角: 登录后看到的页面
<p align="center">
    <img src="./imgs/img-zt-no-permissions.png" alt="drawing" width="800"/>
</p>

admin 用户视角: 给 `zt` 用户添加 `CanViewUser` 权限
<p align="center">
    <img src="./imgs/img.png" alt="drawing" width="800"/>
</p>

zt 用户视角: 增加了 `CanViewUser` 权限后, 再次查看页面
<p align="center">
    <img src="./imgs/img-zt-has-can-view-user-permission.png" alt="drawing" width="800"/>
</p>


&nbsp;  
### 数据库结构
auth_user 表, 存储用户数据
<p align="center">
    <img src="./imgs/img-auth-user.png" alt="drawing" width="800"/>
</p>

auth_permission 表, 存储权限数据
<p align="center">
    <img src="./imgs/img-auth-permission.png" alt="drawing" width="800"/>
</p>

auth_user_user_permission 多对多表, 存储用户和权限的绑定关系数据.
<p align="center">
    <img src="./imgs/img-auth-user-user-permissions.png" alt="drawing" width="800"/>
</p>


&nbsp;  
### 源代码  
#### 浏览器端的网络请求
当 `zt` 用户访问 `admin` 页面时.   
```shell
URI:     /admin/
METHOD:  GET
TYPE:    Document
```
   
#### 服务端的响应处理流程
1. 有关 `Django` 路由的介绍，请看 [wsgi](../contrib/wsgi.md) 和 [dataflow](../contrib/auth/dataflow.md)   
   
2. `GET /admin/` 的入口函数是: [django.contrib.admin.sites.AdminSite.index](../../src/Django-3.0.8/django/contrib/admin/sites.py#L504)  
   
   源码  
   ```python
   class AdminSite:
       @never_cache
       def index(self, request, extra_context=None):
           """
           Display the main admin index page, which lists all of the installed
           apps that have been registered in this site.
           """
           app_list = self.get_app_list(request)

           context = {
               **self.each_context(request),
               'title': self.index_title,
               'app_list': app_list,
               **(extra_context or {}),
           }

           request.current_app = self.name

           return TemplateResponse(request, self.index_template or 'admin/index.html', context)
   ```
   该 `AdminSite.index` 入口函数, 主要的作用是: 获取 `app` 级别的 `context` 信息, 以及实例化一个 `TemplateResponse` 对象.
   ```python
   context = {
    'app_list': [{'app_label': 'auth',
                  'app_url': '/admin/auth/',
                  'has_module_perms': True,
                  'models': [{'add_url': None, 
                              'admin_url': '/admin/auth/user/', 
                              'name': 'Users', 
                              'object_name': 'User', 
                              'perms': {'add': False, 'change': False, 'delete': False, 'view': True}, 
                              'view_only': True}],
                  'name': 'Authentication and Authorization'}],
    'available_apps': [{'app_label': 'auth',
                        'app_url': '/admin/auth/',
                        'has_module_perms': True,
                        'models': [{'add_url': None, 
                                    'admin_url': '/admin/auth/user/', 
                                    'name': 'Users', 
                                    'object_name': 'User', 
                                    'perms': {'add': False, 'change': False, 'delete': False, 'view': True}, 'view_only': True}],
                        'name': 'Authentication and Authorization'}],
    'has_permission': True,
    'is_nav_sidebar_enabled': True,
    'is_popup': False,
    'site_header': 'Django administration',
    'site_title': 'Django site admin',
    'site_url': '/',
    'title': 'Site administration'}
 
   ```
   结论: 入口函数从 `context` 的内容来看, `models` 里面包含了页面应该显示什么哪个模块的数据.
   
3. 展示页面的渲染  
   TODO: 确认 `models` 里面的数据, 就是渲染的依据.
   
