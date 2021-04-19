### WSGI数据流向
`Django`是一个`Web`框架, 不是一个`Web`服务器.  
`Django` 按照 `WSGI(Web Server Gateway Interface)` 接口标准运行.  
不借助外部程序来运行`Django`的情况下, `Django`采用标准库`simple_server.py`中的`WSGIServer`对象作为`Server`,  
用于监听`TCP`网络请求, 数据解析, 并按照`WSGI`标准将数据按照规范接口提交给上层框架.  
 
  1. `django.core.servers.basehttp.WSGIServer` 首先在启动服务时, 会进入到`serve_forever`无限循环, 等待客户端的网络请求.   
  2. `django.core.servers.basehttp.WSGIServer` 本身并没有 `server_forever` 方法, 但是它继承的对象(`socketserver.BaseServer`)有, 这里列出完整的继承树.  
     ```shell
     # 完整的继承树, 即: django的WSGIServer拥有下面这些对象的所有方法.
     django.core.servers.basehttp.WSGIServer
         wsgiref.simple_server.WSGIServer
             http.server.HTTPServer
                 socketserver.TCPServer
                     socketserver.BaseServer
     ```
  3. 当一个请求到达服务器之后, 会触发/激活`socketserver.BaseServer.server_forever`方法.
  4. 下一步是调用`socketserver.BaseServer._handle_request_noblock`方法.
  5. 下一步是进入到标准的`WSGI`流程, 即调用`self.process_request`方法.
  6. 将`socket`对象递交给`WSGIRequestHandler`来处理, 解析`method`, `url`, `args`, `kwargs`等等.
  7. 在`WSGIHandler._get_response`中, 解析`url`找到对应的`view`来执行视图函数, 即具体的业务函数.      
  
     > 备注:  
     > 当数据流进入到第5步时, `WSGI`数据流向已经结束了, 往后就是转交给上层框架进行处理.  
     > 这里之所以多出 6，7 这两步是为了起到一个承上启下的连续.  

&nbsp;  
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