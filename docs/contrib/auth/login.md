
### 登陆   


- get
  
  当请求是`Get`时, [ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L129) 通过 [LoginView.get_context_data](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L107) 获取`'registration/login.html'` 需要使用到的上下文变量.   
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
  > 重点备注(解耦):   
  > `auth.LoginView` 将登陆验证相关的逻辑代码全部抽离到`auth.__init__`中,    
  > 主要目的是为了让`auth.LoginView`这个`View`看起来更聚焦于继承的覆盖(多态),    
  > 同时也让业务逻辑代码和`View`的相对解耦.
