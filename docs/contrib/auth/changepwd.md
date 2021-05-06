
&nbsp;   
### get
GET '/admin/password_change/' 展示修改(自己的)密码的页面.   
[PasswordChangeView.template_name](../../../src/Django-3.0.8/django/contrib/auth/views.py#L345) 声明了模板路径.      
[PasswordChangeView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L351) 没做任何处理, 
直接调用父类的 [View.dispatch](../../../src/Django-3.0.8/django/views/generic/base.py#L96), 
最终进入到 [ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L131) 方法.  
[ProcessFormView.get](../../../src/Django-3.0.8/django/views/generic/edit.py#L131) 
通过 [PasswordContextMixin.get_context_data](../../../src/Django-3.0.8/django/contrib/auth/views.py#L208) 获取渲染参数, 
渲染 [PasswordChangeView.template_name](../../../src/Django-3.0.8/django/contrib/auth/views.py#L345) 页面.  


&nbsp;   
&nbsp;   
### post
POST '/admin/password_change' 更新数据库中(自己的)密码.   
[PasswordChangeView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L351) 
没做任何处理, 直接调用父类的 [View.dispatch](../../../src/Django-3.0.8/django/views/generic/base.py#L63), 
最终进入到 [ProcessFormView.post](../../../src/Django-3.0.8/django/views/generic/edit.py#L135) 方法.  
[ProcessFormView.post](../../../src/Django-3.0.8/django/views/generic/edit.py#L135) 
通过 [PasswordChangeForm.is_valid](../../../src/Django-3.0.8/django/forms/forms.py#L179) 验证请求参数是否符合`Model`定义的约束规范, [详细分析看这里](./login.md#POST).
[ProcessFormView.post](../../../src/Django-3.0.8/django/views/generic/edit.py#L135) 
通过 [PasswordChangeForm.form_valid](../../../src/Django-3.0.8/django/contrib/auth/views.py#L359) 来完成[表单数据保存](../../../src/Django-3.0.8/django/contrib/auth/views.py#L360), [session值更新动作](../../../src/Django-3.0.8/django/contrib/auth/views.py#L363).  

- `PasswordChangeForm` 表单对象的继承树
  ```shell
  django.contrib.auth.forms.PasswordChangeForm
      django.contrib.auth.forms.SetPasswordForm                       # form.save 在这里, 用于保存表单数据.               
          django.forms.forms.Form
              django.forms.forms.BaseForm                             # form.is_valid 在这里.
  ```  

- `PasswordChangeForm` 表单在哪里验证两次密码一致?  
  [在这里](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L361) 
  ``` shell 
  # 调用栈, CallStack
  PasswordChangeForm.is_valid
      django.forms.forms.BaseForm.is_valid
          django.forms.forms.BaseForm.errors
              django.forms.forms.BaseForm.full_clean
                  django.forms.forms.BaseForm._clean_fields                           # getattr(self, 'clean_%s' % name)()
                      django.contrib.auth.forms.SetPasswordForm.clean_new_password2   # 在这里验证两次密码的一致性.
  ```

TODO: 表单数据保存源码分析   
TODO: session更新源码分析


&nbsp;  
&nbsp;  
### csrf_protect


&nbsp;  
&nbsp;  
### sensitive_post_parameters


&nbsp;  
&nbsp;   
### AUTH_PASSWORD_VALIDATORS
- UserAttributeSimilarityValidator 相似的检查
- MinimumLengthValidator 最小长度检查
- CommonPasswordValidator 通用密码检查
- NumericPasswordValidator 纯数字密码检查