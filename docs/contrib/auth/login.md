 
&nbsp;  
### AuthenticationMiddleware   
[django.settings.MIDDLEWARE](../../../examples/myqueryset/myqueryset/settings.py#L54) 中, 
声明了 [AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L16) 中间件对象.   
[WSGIHandler](../../../src/Django-3.0.8/django/core/handlers/wsgi.py#L133) 被触发时, 就会立马 [初始化和执行](../../../src/Django-3.0.8/django/core/handlers/base.py#L75) `AuthenticationMiddleware`.    

`AuthenticationMiddleware` 的作用是, 读取`request`请求头中的`session`字段,    
然后到数据库中根据该`session`查找到对应的`user_id`, 然后再查找到`User`表中对应的整行数据,    

`AuthenticationMiddleware` 采用 [SimpleLazyObject](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L24) 对象延迟触发.  
也就是说在 WSGIHandler 搜集数据阶段一直到进入业务视图(View)这中间的过程是严格禁止数据库交互的.  

`AuthenticationMiddleware` 它真正被触发是在 [权限验证环节](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L381), 在这里会迸发出两条`SQL`,   
`SQL-1`: 根据请求头的`session`去查询到对应的`user_id`,    
`SQL-2`: 根据`user_id`去查询到对应的整行用户数据,    
根据查询到的数据, 判断用户是否具备 [`is_active` 和 `is_staff`](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L189) 权限,  
当两个权限都具备时, 且请求方法是`GET`时, 跳转到后台.   


&nbsp;  
&nbsp;  
### GET
  
  当请求是`Get`时, 且请求头中不含`session`字段, 或`session`字段无效时, 进入[ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L131)方法.
  
  [ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L129) 通过 [LoginView.get_context_data](../../../src/Django-3.0.8/django/contrib/auth/views.py#L107) 获取`'registration/login.html'` 需要使用到的上下文变量.   
  在然后就是将上下文变量分配给 [TemplateResponseMixin.render_to_response](../../../src/Django-3.0.8/django/views/generic/base.py#L140), 用于渲染模板文件(`html`)和返回数据给客户端.
  
  ```shell
  # LoginView继承树
  LoginView(SuccessURLAllowedHostsMixin, FormView)
      django.views.generic.edit.FormView
          django.views.generic.base.TemplateResponseMixin             # 模板响应的混入类对象, render_to_response 在这里.
  ```    


&nbsp;  
&nbsp;  
### POST   

当请求是`Post`时, 进入[ProcessFormView.post](../../../src/Django-3.0.8/django/views/generic/edit.py#L135)方法.   
在 `post` 方法中, `form.is_valid` 采用的不是继承树的方法, 而是`form_class = AuthenticationForm`的方法.

```shell
# AuthenticationForm继承树
AuthenticationForm(forms.Form)           # clean 这里提供具象化的验证行为.
    django.forms.forms.Form
        django.forms.forms.BaseForm      # is_valid / errors / full_clean / _clean_fields / _clean_form / _post_clean.
                                         # 这里提供一套特定的运行机制和通用的验证行为.
```    

- BaseForm.is_valid  
  [BaseForm](../../../src/Django-3.0.8/django/forms/forms.py#L57) 提供了 [is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L178) 方法, 用于验证表单内容是否有效. 
  
  [BaseForm.is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L178) 根据情况返回不同的值(布尔值).  
  [BaseForm.is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L178) 返回`True`,  当 `self.bound=True` 和 `self.errors=False` 时.    
  [BaseForm.is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L178) 返回`False`, 当 `self.bound=False` 或 `self.errors=True` 时.    

- BaseForm.errors  
  [BaseForm.errors 是一个property函数](../../../src/Django-3.0.8/django/forms/forms.py#L172), 这是`Django`特意设计的一个表单检查入口.    
  [BaseForm.errors](../../../src/Django-3.0.8/django/forms/forms.py#L172) 通过调用 `BaseForm.full_clean` 来完成所有验证工作.     
  在`BaseForm.full_clean`中, [BaseForm._clean_fields](../../../src/Django-3.0.8/django/forms/forms.py#L386) 是基于字段的验证(没有SQL网络请求): 字段必填, 字段名匹配, 执行自定义validator.   
  在`BaseForm.full_clean`中, [BaseForm._clean_form](.../../../src/Django-3.0.8/django/forms/forms.py#L423) 回调上层 [AuthenticationForm.clean](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L214) 方法, 使其可以聚焦到具象化的场景验证环节.   
  在`BaseForm.full_clean`中, [BaseForm._post_clean]((../../../src/Django-3.0.8/django/forms/forms.py#L432)) 是一个预留的hook, 可做一些验证后的事务.  
  
  > 重点备注  
  > 由 `BaseForm._clean_form` 回调上层 `AuthenticationForm.clean` 延申出来的具象化场景验证.
  >  
  > [AuthenticationForm.clean](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L214) 是一个helper方法, 它内部调用了外部的 [django.contrib.auth.authenticate](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L66) 来完成具象化的场景验证.   
  > [django.contrib.auth.authenticate](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L66) 检查用户是否存在于数据库中, 并检查密码是否与数据库中的密码一致.   
  > 
  > 如果将 `django.contrib.auth.authenticate` 的代码合并到 `AuthenticationForm.clean` 中, 这叫做耦合.    
  > 将 `django.contrib.auth.authenticate` 独立出来, 在`AuthenticationForm.clean`调用, 这叫做依赖.  
  >   
  > 更宏观一点的视角:    
  > 将 `Form` 和 `authenticate` 拆分开, 使`Form`聚焦表单, 使 `authenticate` 聚焦业务,   
  > `AuthenticationForm` 这个 `helperForm` 负责整合外部资源.  

- LoginView.form_valid  
  [LoginView.form_valid](../../../src/Django-3.0.8/django/contrib/auth/views.py#L101) 被执行, 表示已经满足表单和数据库这两个层面的验证.  
  [LoginView.form_valid](../../../src/Django-3.0.8/django/contrib/auth/views.py#L101) 聚焦三个动作, 创建和保存session, 记录登录日志, 跳转到后台.   

  > 重点备注  
  > [LoginView.form_valid](../../../src/Django-3.0.8/django/contrib/auth/views.py#L101) 这个 `helperView` 通过调用外部的 [django.contrib.auth.login](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L93) 完成 创建和保存session, 记录登录日志 动作.  
  > 
  > 将 `View` 和 `login` 拆分开, 使 `View` 聚焦参数的调度和流程的把控, 使`login`聚焦业务,    
  > `LoginView` 这个 `helperView` 除了利用参数实例化对象, 调度各个对象的方法进入不同的流程, 还需要整合外部资源对象来满足具象化的场景处理.   

