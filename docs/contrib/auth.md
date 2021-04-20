
&nbsp;  
### django.contrib.auth  
`django.contrib.auth` 实际上是一个普通的`app`应用, 因为这个模块的程序文件分布结构与普通的`app`是一样的.   
接下来就从 `urls.py` 文件着手去分析它的工作原理, 该文件中定义了 `8` 个有效的路径.   
  
|路径|视图|描述|
|:---|:---| :---: | 
|'login/'|[views.LoginView.as_view()](#)| 登录界面 |  
|'logout/'|[views.LogoutView.as_view()](#)| - |  
|'password_change/'|[views.PasswordChangeView.as_view()](#)| - |  
|'password_change/done/'|[views.PasswordChangeDoneView.as_view()](#)| - |  
|'password_reset/'|[views.PasswordResetView.as_view()](#)|   - |
|'password_reset/done/'|[views.PasswordResetDoneView.as_view(#)]()|  - | 
|'reset/\<uidb64>/\<token>/'|[views.PasswordResetConfirmView.as_view(#)]()|   - |
|'reset/done/'|[views.PasswordResetCompleteView.as_view()](#)|   - |