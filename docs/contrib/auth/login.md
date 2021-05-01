
### 登录   

- get
  
  当请求是`Get`时, [ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L129) 通过 [LoginView.get_context_data](../../../src/Django-3.0.8/django/contrib/auth/views.py#L107) 获取`'registration/login.html'` 需要使用到的上下文变量.   
  在然后就是将上下文变量分配给 [TemplateResponseMixin.render_to_response](../../../src/Django-3.0.8/django/views/generic/base.py#L140), 用于渲染模板文件(`html`)和返回数据给客户端.
  
  ```shell
  # LoginView继承树
  LoginView(SuccessURLAllowedHostsMixin, FormView)
      django.views.generic.edit.FormView
          django.views.generic.base.TemplateResponseMixin             # 模板响应的混入类对象, render_to_response 在这里.
  ```    

- post   

  当请求是`Post`时, [BaseForm](../../../src/Django-3.0.8/django/forms/forms.py#L57) 提供了 [is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L178) 方法, 用于验证表单内容是否有效.   
  当表单验证结果为True时, 表示有效, [LoginView.form_valid](../../../src/Django-3.0.8/django/contrib/auth/views.py#L101)负责跳转到后台. TODO: 待验证   
  当表单验证结果为False时, 表示验证失败, 跳转到错误页面.   
  
  TODO: full_clean 的流程和标准.   
  TODO: authentication 的原理.   
  TODO: auth_login 的原理.    



&nbsp;  
&nbsp;  
> 备注-1: 解耦   
> [auth.LoginView](../../../src/Django-3.0.8/django/contrib/auth/views.py#L103) 将登陆验证相关的逻辑代码全部抽离到 [auth.\_\_init__.login](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L86) 中,    
> 主要目的是为了让`auth.LoginView`这个`View`看起来更聚焦于继承的覆盖(多态),    
> 同时也让业务逻辑代码和`View`的相对解耦.   
>    
> &nbsp;      
> 备注-2: AuthenticationMiddleware   
> [django.settings.MIDDLEWARE](../../../examples/myqueryset/myqueryset/settings.py#L54) 中, 
> 声明了 [AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L16) 中间件对象.   
> [WSGIHandler](../../../src/Django-3.0.8/django/core/handlers/wsgi.py#L133) 被触发时, 就会立马 [初始化和执行](../../../src/Django-3.0.8/django/core/handlers/base.py#L75) `AuthenticationMiddleware`.    
> 
> `AuthenticationMiddleware` 的作用是, 读取`request`请求头中的`session`字段,    
> 然后到数据库中根据该`session`查找到对应的`user_id`, 然后再查找到`User`表中对应的整行数据,    
>
> `AuthenticationMiddleware` 采用 [SimpleLazyObject](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L24) 对象延迟触发.  
> 也就是说在 WSGIHandler 搜集数据阶段一直到进入业务视图(View)这中间的过程是严格禁止数据库交互的.  
> 
> `AuthenticationMiddleware` 它真正被触发是在 [权限验证环节](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L381), 在这里会迸发出两条`SQL`,   
> `SQL-1`: 根据请求头的`session`去查询到对应的`user_id`,    
> `SQL-2`: 根据`user_id`去查询到对应的整行用户数据,    
> 根据查询到的数据, 判断用户是否具备 [`is_active` 和 `is_staff`](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L189) 权限,  
> 当两个权限都具备时, 且请求方法是`GET`时, 跳转到后台.   
>