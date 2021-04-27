
&nbsp;  
### django.contrib.auth  
`django.contrib.auth` 实际上是一个普通的`app`应用, 因为这个模块的程序文件分布结构与普通的`app`是一样的.   
接下来就从 `urls.py` 文件着手去分析它的工作原理, 该文件中定义了 `8` 个有效的路径.   
  
|路径|描述|视图|
|:---|:---:| :--- | 
|'login/'|登录界面 |[django.contrib.auth.views.LoginView.as_view()](#)|   
|'logout/'| - | [django.contrib.auth.views.LogoutView.as_view()](#)| 
|'password_change/'| - |[django.contrib.auth.views.PasswordChangeView.as_view()](#)|  
|'password_change/done/'| - |[django.contrib.auth.views.PasswordChangeDoneView.as_view()](#)|  
|'password_reset/'|  - |[django.contrib.auth.views.PasswordResetView.as_view()](#)| 
|'password_reset/done/'| - |[django.contrib.auth.views.PasswordResetDoneView.as_view(#)]()|  
|'reset/\<uidb64>/\<token>/'| - |[django.contrib.auth.views.PasswordResetConfirmView.as_view(#)]()|  
|'reset/done/'| - |[django.contrib.auth.views.PasswordResetCompleteView.as_view()](#)|  


&nbsp;  
&nbsp;  
### 数据流向
当前数据流向衔接 [WSGI数据流向](./wsgi.md) 中的`WSGIHandler._get_response`, 先解析`URL`找到对应的`View`, 然后再执行`View`相关的流程. 

- URL匹配流程(以 '/admin/login/' 为例)   
  一、尝试匹配 '^/' , 匹配命中, 移除命中部分, 剩余 'admin/login/' 继续进行匹配.     
  二、尝试匹配 '^admin/', 匹配命中, 移除命中部分, 剩余 'login/' 继续进行匹配.   
  三、尝试匹配 '', 匹配未命中, 继续进行匹配.   
  四、尝试匹配 'login/', 匹配命中, 提取对应的函数(MVC中的View, 也就是业务函数), 结束URL匹配流程.   

  > 补充-1:   
  > 上面这四个步骤的执行依据是什么?     
  > 根据用户创建的项目 [urls.py](../../examples/myqueryset/myqueryset/urls.py#L20) 中定义的 `path` 进行匹配和驱动.  
  > 
  > 补充-2:  
  > `django.contrib.auth`模块的路由的真相.  
  > 由于 `Django Admin` 的入口被定义在[这里](../../examples/myqueryset/myqueryset/urls.py#L20), 因此`AdminSite.urls`托管了整个路由入口,    
  > 并且 `AdminSite.get_urls` 方法中, 选择重写 `urlpatterns` 而不是根据注册的`app`去寻找它的`urls.py`, 因此 `django.contrib.auth` 的 `urls.py`    
  > 在 `Django Admin` 中是无效的.  
  > 
  > 补充-3:
  > 那 `django.contrib.auth` 的 `urls.py` 还有存在的必要吗?  
  > 站在 `Django Admin` 的角度来看, 没有存在的必要,  
  > 站在 `一个常规app` 的角度来看, 是有必要的,  
  > 因为保不准谁会有单独使用 `django.contrib.auth` 的需求, 那直接用起来就行了.  

