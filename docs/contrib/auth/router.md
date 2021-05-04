
&nbsp;  
### 路由
`django.contrib.auth` 实际上是一个普通的`app`应用, 因为这个模块的程序文件分布结构与普通的`app`是一样的.   
接下来就从 [urls.py](../../../src/Django-3.0.8/django/contrib/auth/urls.py#L9) 文件着手去分析它的工作原理, 该文件中定义了 `8` 个有效的路径.   
  
|路径|描述|视图|
|:---|:---:| :--- | 
|'login/'| [登陆功能](./login.md) |[django.contrib.auth.views.LoginView.as_view()](../../../src/Django-3.0.8/django/contrib/auth/views.py#L40)|   
|'logout/'| [登出功能](./logout.md) | [django.contrib.auth.views.LogoutView.as_view()](../../../src/Django-3.0.8/django/contrib/auth/views.py#L119)| 
|'password_change/'| - |[django.contrib.auth.views.PasswordChangeView.as_view()](#)|  
|'password_change/done/'| - |[django.contrib.auth.views.PasswordChangeDoneView.as_view()](#)|  
|'password_reset/'|  - |[django.contrib.auth.views.PasswordResetView.as_view()](#)| 
|'password_reset/done/'| - |[django.contrib.auth.views.PasswordResetDoneView.as_view(#)]()|  
|'reset/\<uidb64>/\<token>/'| - |[django.contrib.auth.views.PasswordResetConfirmView.as_view(#)]()|  
|'reset/done/'| - |[django.contrib.auth.views.PasswordResetCompleteView.as_view()](#)|  