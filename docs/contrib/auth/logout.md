 
&nbsp;  
### AuthenticationMiddleware   
通常情况下能触发`/admin/lgout/`路由, 表示客户端是已登陆状态, 这意味着客户端请求头中必须包含有效 `cookies.session` 字段.   
[AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L16) 在这里的作用是, 
[根据 `cookies` 中的 `session` 值查询`django_session`表](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L239), 得到对应的`user_id`,  
[再然后是查找到`User`表中对应于`user_id`的整行数据](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L261).   


&nbsp;  
&nbsp;  
### 登出
[AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L24) 做session验证完成之后, 会将查询到得`user`整行数据, 赋值给`request.user`.   
随后代码会进入标准流程:    
[AdminSite.logout](../../../src/Django-3.0.8/django/contrib/admin/sites.py#L354)   
[LogoutView.as_view](../../../src/Django-3.0.8/django/views/generic/base.py#L49)   
[LogoutView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L129)  
[auth.auth_logout](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L168)  
由于 `Logout` 的业务相对比较简单(不涉及表单处理), 因此业务函数 [auth_logout](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L168) 就被放在 [LogoutView.dispatch](../../../src/Django-3.0.8/django/contrib/auth/views.py#L130) 中进行处理.   

&nbsp;   
> 重要事项:  
> 1. 后续所有需要使用到`user`得代码, 为了减少数据库查询, 可直接访问`request.user`(内存/缓存形式).  
> 2. `auth_logout` 被放在 `LogoutView.dispatch` 中,    
>    是因为不论http请求的方法是 `get` 还是 `post` , 都要运行同一套代码,   
>    所以就没有必要让它进入 `super().dispatch` 到 [ProcessFormView](../../../src/Django-3.0.8/django/views/generic/edit.py#L129) 中. 


&nbsp;  
&nbsp;  
### Model

'/admin/logout/' 这个 `API` 总共涉及使用了哪些 `Model` ?

|Model|描述|调用者|
|---|---|---|
|AnonymousUser| MockUserModel | [AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L273) |
|User(AbstractUser)| UserModel | [AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L261) / [auth_logout](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L168) |
|SessionStore(SessionBase)| SessionModel | [AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L239) / [auth_logout](../../../src/Django-3.0.8/django/contrib/auth/__init__.py#L201) |



&nbsp;   
&nbsp;   
### 现象:
发现django每次请求数据查询或写入之前, 都会先提交一条SQL指令   
`SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED`   
READ COMMITTED 隔离模式指的是一个事务提交之后, 其他事务才能看到改变.      

