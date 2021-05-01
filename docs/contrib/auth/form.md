&nbsp;  
### 表单

在`GET`时, 浏览器需要一个登陆页面, 页面中需要包含一个登陆表单.   
在`POST`时, 服务端需要验证表单提交信息.   
在`Django`中, 表单负责与`数据库(Model)`交互, 并生成满足业务场景的字段表单.
  
登陆页面用哪个表单, 定义在`auth.LoginView.form_class`中, 值是`django.contrib.auth.forms.AuthenticationForm`.  
登陆页面用哪个模板, 定义在`auth.LoginView.template_name`中, 值是`registration/login.html`.  
  
在`as_view`流程中, 不论是进入到`get`还是`post`方法, 都需要使用到表单对象,  
获取表单对象使用的是`LoginView.get_form`, 然而 `LoginView` 并没有定义`get_form`方法,    
此时就需要从 `LoginView` 对象的继承树中去寻找这样一个方法.  
```shell
# auth.LoginView继承树
LoginView(SuccessURLAllowedHostsMixin, FormView)
    django.views.generic.edit.FormView                                                    
        django.views.generic.edit.BaseFormView                                       
            django.views.generic.edit.BaseFormView
                django.views.generic.edit.FormMixin                   # get_form 方法在这里.
  
```  
     
表单对象(`django.contrib.auth.forms.AuthenticationForm`)在实例化的过程中,   
会根据自身 [类变量](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L180) 中类型是 [form.Field](../../../src/Django-3.0.8/django/forms/forms.py#L31) 的字段到 [UserModel._meta](../../../src/Django-3.0.8/django/contrib/auth/forms.py#L207) 中提取对应的字段约束信息.   
备注: 这个表单实例化的过程没有任何`sql`网络请求.
