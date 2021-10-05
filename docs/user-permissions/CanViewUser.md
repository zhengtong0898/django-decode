# 问题
给一个用户添加 `CanViewUser` 权限时, 在`Django`里面发生了什么?  

&nbsp;  
&nbsp;  
# 准备
### 赋权之前
普通用户(zt): 登录后看到的页面
<p align="center">
    <img src="./imgs/img-zt-no-permissions.png" alt="drawing" width="800"/>
</p>

&nbsp;  
### 赋权
管理员用户(admin): 给 `zt` 用户添加 `CanViewUser` 权限
<p align="center">
    <img src="./imgs/img.png" alt="drawing" width="800"/>
</p>

&nbsp;  
### 赋权之后
普通用户(zt): 增加了 `CanViewUser` 权限后, 再次查看页面
<p align="center">
    <img src="./imgs/img-zt-has-can-view-user-permission.png" alt="drawing" width="800"/>
</p>

&nbsp;  
&nbsp;  
# 分析  

### 浏览器端的网络请求
当 `zt` 用户访问 `admin` 页面时.   
```shell
URI:     /admin/
METHOD:  GET
TYPE:    Document
```

&nbsp;     
### 服务端的响应处理流程
有关 `Django` 路由的介绍，请看 [wsgi](../contrib/wsgi.md) 和 [dataflow](../contrib/auth/dataflow.md)   


&nbsp;  
### 业务函数
当通过 `GET /admin/` 访问 `Django` 时, 触发的是下面[这段源码](../../src/Django-3.0.8/django/contrib/admin/sites.py#L504).   
该函数的逻辑是:  
1. 获取当前用户可访问的应用列表(app_list), 含具体的权限.
2. 获取系统通用的模板参数变量.
3. 将步骤 `1` 和 `2` 的值, 组合成一个接口数据: context.
4. 将 context 接口数据传递给 TemplateResponse 对象进行 html 文件渲染.  
   备注: 这里其实也能将 context 当作一个 json 作为 restful 接口值返回.
```python
# django.contrib.admin.sites.AdminSite.index


class AdminSite:
    @never_cache
    def index(self, request, extra_context=None):
        # 权限接口的数据结构: List[Dict]
        # app_list = [{'app_label': 'auth',
        #              'app_url': '/admin/auth/',
        #              'has_module_perms': True,
        #              'models': [{'add_url': None, 
        #                          'admin_url': '/admin/auth/user/', 
        #                          'name': 'Users', 
        #                          'object_name': 'User', 
        #                          'perms': {'add': False, 'change': False, 'delete': False, 'view': True}, 
        #                          'view_only': True}],
        #              'name': 'Authentication and Authorization'}]
        app_list = self.get_app_list(request)

        # 模板接口的数据结构: Dict
        # context = {'app_list': [{'app_label': 'auth',
        #                          'app_url': '/admin/auth/',
        #                          'has_module_perms': True,
        #                          'models': [{'add_url': None, 
        #                                      'admin_url': '/admin/auth/user/', 
        #                                      'name': 'Users', 
        #                                      'object_name': 'User', 
        #                                      'perms': {'add': False, 'change': False, 'delete': False, 'view': True}, 
        #                                      'view_only': True}],
        #                          'name': 'Authentication and Authorization'}],
        #            'available_apps': [{'app_label': 'auth',
        #                                'app_url': '/admin/auth/',
        #                                'has_module_perms': True,
        #                                'models': [{'add_url': None, 
        #                                            'admin_url': '/admin/auth/user/', 
        #                                            'name': 'Users', 
        #                                            'object_name': 'User', 
        #                                            'perms': {'add': False, 'change': False, 'delete': False, 'view': True}, 'view_only': True}],
        #                                'name': 'Authentication and Authorization'}],
        #            'has_permission': True,
        #            'is_nav_sidebar_enabled': True,
        #            'is_popup': False,
        #            'site_header': 'Django administration',
        #            'site_title': 'Django site admin',
        #            'site_url': '/',
        #            'title': 'Site administration'}
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.index_template or 'admin/index.html', context)
```

&nbsp;  
### 延申阅读
[`Django` 是如何获取到用户、组和菜单的权限的呢?](./HowDjangoGetUserPermission.md)
 