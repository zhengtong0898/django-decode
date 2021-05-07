
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

- `PasswordChangeForm` 表单数据保存
  ```python
  # django.contrib.auth.forms.PasswordChangeForm
  #     django.contrib.auth.forms.SetPasswordForm                     # save() 更新密码保存的代码在这里.
  
  
  class SetPasswordForm(forms.Form):
  
      def save(self, commit=True):
          # self.cleaned_data 是已经验证过的数据.
          password = self.cleaned_data["new_password1"]
          # 在这里根据文本密码生成一个加密的字符串
          # 存储在 self.user.password 中, 而原始文本密码存储在 self.user._password 中.
          self.user.set_password(password)
          # 是否自动提交.
          if commit:
              # 触发update保存, 可以看得出来, 不论是修改一个字段还是多个字段, 都是争取整行更新.
              # UPDATE `auth_user` SET `password` = '%s',
              #                       `last_login` = '%s,
              #                       `is_superuser` = %s,
              #                       `username` = '%s',
              #                       `first_name` = '',
              #                       `last_name` = '',
              #                       `email` = '%s',
              #                       `is_staff` = %s,
              #                       `is_active` = %s,
              #                       `date_joined` = '%s'
              # WHERE `auth_user`.`id` = 1
              self.user.save()
          return self.user
  ```

- session更新  
  ```python
  # 调用栈
  # django.contrib.auth.views.PasswordChangeView.form_valid
  #     django.contrib.auth.update_session_auth_hash
  #         django.contrib.sessions.backends.base.SessionBase.cycle_key       
  #             django.contrib.sessions.backends.base.SessionStore.create
  # 
  #                 # 这里负责将数据 {'_auth_user_id': '1', 
  #                 #                '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend', 
  #                 #                '_auth_user_hash': '7659a6147a58029837dedac9def9760840a4da8c'}
  #                 # encode 和 base64 转成一个串码, 保存到数据库中(django_session表的session_data字段)
  #                 django.contrib.sessions.backends.base.SessionStore.save
  ```


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