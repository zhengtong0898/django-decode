 
&nbsp;  
### AuthenticationMiddleware   
通常情况下能触发`/admin/lgout/`路由, 表示客户端是已登陆状态, 这意味着客户端请求头中必须包含有效 `cookies` 段, 同时 `cookies` 段中必须包含有效的 `session` 值.   
[AuthenticationMiddleware](../../../src/Django-3.0.8/django/contrib/auth/middleware.py#L16) 在这里的作用是, 根据 `cookies` 中的 `session` 值查询`django_session`表, 得到对应的`user_id`, 再然后是查找到`User`表中对应于`user_id`的整行数据.   

