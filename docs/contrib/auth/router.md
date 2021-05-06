
&nbsp;  
### 路由
`django.contrib.auth` 实际上是一个普通的`app`应用, 因为这个模块的程序文件分布结构与普通的`app`是一样的.   
接下来就从 [urls.py](../../../src/Django-3.0.8/django/contrib/auth/urls.py#L9) 文件着手去分析它的工作原理, 该文件中定义了 `8` 个有效的路径.   
  
|路径|功能|视图|
|:---|:---:| :--- | 
|'login/'| [登陆](./login.md) |[django.contrib.auth.views.LoginView.as_view()](../../../src/Django-3.0.8/django/contrib/auth/views.py#L40)|   
|'logout/'| [登出](./logout.md) | [django.contrib.auth.views.LogoutView.as_view()](../../../src/Django-3.0.8/django/contrib/auth/views.py#L119)| 
|'password_change/'| 修改密码 |[django.contrib.auth.views.PasswordChangeView.as_view()](#)|  
|'password_change/done/'| 密码修改成功 |[django.contrib.auth.views.PasswordChangeDoneView.as_view()](#)|  
|'password_reset/'|  - |[django.contrib.auth.views.PasswordResetView.as_view()](#)| 
|'password_reset/done/'| - |[django.contrib.auth.views.PasswordResetDoneView.as_view(#)]()|  
|'reset/\<uidb64>/\<token>/'| - |[django.contrib.auth.views.PasswordResetConfirmView.as_view(#)]()|  
|'reset/done/'| - |[django.contrib.auth.views.PasswordResetCompleteView.as_view()](#)|  


&nbsp;   
### 通用路由

通用路由定义在 [这里](../../../src/Django-3.0.8/django/contrib/admin/options.py#L602),    
使用了 [admin.register](../../../src/Django-3.0.8/django/) 或 [admin.site.register](../../../examples/myqueryset/simplerelate/admin.py#L25) 语法来  
注册到`Django Admin`后台的模块(`Model`)对象, 都会具备统一的通用路由.  


|路径|功能|视图|
|:---|:---:| :--- | 
|''| 列表清单| [django.contrib.admin.options.ModelAdmin.changelist_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1667) |   
|'add/'| 新增 | [django.contrib.admin.options.ModelAdmin.add_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1637) | 
|'autocomplete/'| TODO | [django.contrib.admin.options.ModelAdmin.autocomplete_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1634) |  
|'\<path:object_id\>/history/'| 历史操作记录 | [django.contrib.admin.options.ModelAdmin.history_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1891) |  
|'\<path:object_id\>/delete/'|  删除 | [django.contrib.admin.options.ModelAdmin.delete_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1829) | 
|'\<path:object_id\>/change/'| 修改 | [django.contrib.admin.options.ModelAdmin.change_view](../../../src/Django-3.0.8/django/contrib/admin/options.py#L1640) |  
|'\<path:object_id\>/'| 重定向指修改页面 | [django.views.generic.base.RedirectView](../../../src/Django-3.0.8/django/views/generic/base.py#L162) |  
