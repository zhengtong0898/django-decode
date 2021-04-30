
&nbsp;  
### 数据流向
当前数据流向衔接 [WSGI数据流向](../wsgi.md) 中的 [WSGIHandler._get_response](../../../src/Django-3.0.8/django/core/handlers/base.py#L85), 先解析`URL`找到对应的`View`, 然后再执行`View`相关的流程. 

- URL匹配流程(以 '/admin/login/' 为例)   
  一、尝试匹配 '^/' , 匹配命中, 移除命中部分, 剩余 'admin/login/' 继续进行匹配.     
  二、尝试匹配 '^admin/', 匹配命中, 移除命中部分, 剩余 'login/' 继续进行匹配.   
  三、尝试匹配 '', 匹配未命中, 继续进行匹配.   
  四、尝试匹配 'login/', 匹配命中, 提取对应的函数(MVC中的View, 也就是业务函数), 结束URL匹配流程.   

  > 补充-1:   
  > 上面这四个步骤的执行依据是什么?     
  > 根据用户创建的项目 [urls.py](../../../examples/myqueryset/myqueryset/urls.py#L20) 中定义的 `path` 进行匹配和驱动.  
  > 
  > 补充-2:  
  > `django.contrib.auth`模块的路由的真相.  
  > 由于 `Django Admin` 的入口被定义在[这里](../../../examples/myqueryset/myqueryset/urls.py#L20), 因此`AdminSite.urls`托管了整个路由入口,    
  > 并且 [AdminSite.get_urls](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L240) 方法中, 选择重写 `urlpatterns` 而不是根据注册的`app`去   
  > 寻找它的`urls.py`, 因此 `django.contrib.auth` 的 `urls.py` 在 `Django Admin` 中是无效的.  
  > 
  > 补充-3:   
  > 那 `django.contrib.auth` 的 `urls.py` 还有存在的必要吗?  
  > 站在 `Django Admin` 的角度来看, 没有存在的必要,  
  > 站在 `一个常规app` 的角度来看, 是有必要的,  
  > 因为保不准谁会有单独使用 `django.contrib.auth` 的需求, 那直接用起来就行了.  

- 登陆流程被拦截   
  一、因为`Django Admin`在 [AdminSite.get_urls](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L240) 中重写了`urlpatterns`.  
  二、所以输入网址 `/admin/login/` 会进入到 [`AdminSite.login`](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L376) 方法中.   
  三、在`AdminSite.login`内, 首先[检查当前请求的cookie是否有效](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L380), 有效则直接跳转到后台页面, 登陆流程结束.   
  四、在`AdminSite.login`内, 检查cookie无效, [则收集`request`的上下文信息](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L392).  
  五、在`AdminSite.login`内, 收集完上下文信息后, 最终还是落地到 [django.contrib.auth.LoginView](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L416) 上.   

- as_view流程  
  `View`是`Django`强力推荐使用的一个功能模块, 使用经过高度封装的`View`可快速提升开发效率.  
  也正是因为`View`经过了高度封装, 它有一套属于自己的运作逻辑, 而 `as_view` 就是进入这个`View`流程的入口.    
  一、由于`auth.LoginView`继承了`View`对象, 因此它拥有了`as_view`这个入口方法.   
  二、在 [View.as_view](../../../src/Django-3.0.8/django/views/generic/base.py#L53) 方法中, 先做一个常规的检查, 不允许参数名中包含标准http的请求名字.  
  三、在 [View.as_view](../../../src/Django-3.0.8/django/views/generic/base.py#L63) 方法中, 紧接着是定义一个`view`临时函数, 并给`view`临时函数`patch`一些属性.   
  四、在 [View.as_view.view](../../../src/Django-3.0.8/django/views/generic/base.py#L65) 函数中, 会实例化`auth.LoginView`类, 并做一些冲突检查.   
  五、在 [View.as_view.view](../../../src/Django-3.0.8/django/views/generic/base.py#L65) 函数中, 执行`View.dispatch`标准接口, `dispatch`是`View`流程第一个节点.      
  六、在 [auth.LoginView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L54) 方法中, 通过多态利用 `View` 的公共接口, 补充满足自身业务的代码.  
  七、在 [auth.LoginView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L54) 方法中, 执行完附加代码后, 再回到 `View` 标准的流程中来.  
  八、在 [View.dispatch](../../../src/Django-3.0.8/django/views/generic/base.py#L96) 方法中, 根据 `request.method` 来提取对应的`LoginView`方法.   
  九、在 [View.dispatch](../../../src/Django-3.0.8/django/views/generic/base.py#L96) 方法中, 如果 `request.method` 是 `GET`, 则运行`LoginView.get`方法.  
  十、在 [View.dispatch](../../../src/Django-3.0.8/django/views/generic/base.py#L96) 方法中, 如果 `LoginView` 没有 `get` 方法, 那就从它的继承树中取找`get`方法.
  ```shell
  # auth.LoginView继承树
  LoginView(SuccessURLAllowedHostsMixin, FormView)
      django.views.generic.edit.FormView                                                    
          django.views.generic.edit.BaseFormView                                       
              django.views.generic.edit.BaseFormView
                  django.views.generic.edit.ProcessFormView             # get 和 post 方法在这里.
  ```
  