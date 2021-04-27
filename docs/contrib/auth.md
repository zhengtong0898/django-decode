
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
- URL匹配流程(以 '/admin/login/' 为例)   
  一、尝试匹配 '^/' , 匹配命中, 移除命中部分, 剩余 'admin/login/' 继续进行匹配.     
  二、尝试匹配 '^admin/', 匹配命中, 移除命中部分, 剩余 'login/' 继续进行匹配.   
  三、尝试匹配 '', 匹配未命中, 继续进行匹配.   
  四、尝试匹配 'login/', 匹配命中, 提取对应的函数(MVC中的View, 也就是业务函数), 结束URL匹配流程.   

