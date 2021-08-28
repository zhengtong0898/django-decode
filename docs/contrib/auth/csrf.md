### MiddlewareMixin
`MiddlewareMixin` 是一个中间件`基类`.  
`MiddlewareMixin` 期望派生类应自行实现 `process_request` 和 `process_response` 方法, 可选(非必须).  
`MiddlewareMixin` 期望派生类实例化时, 提供 `get_response` 参数, 类型为 `Function`, 可选(非必须).  
`MiddlewareMixin` 被触发 `__call__` 时, 要求提供 `request` 参数.   
`MiddlewareMixin` 有两种方式执行 `request`, 一种是 `process_request`, 另外一种是 `get_response`.   
`MiddlewareMixin` 执行 `request` 的策略是, 先交给 `process_request` 处理, 返回值为None时, 交给 `get_response` 二次处理.  


### CsrfViewMiddleware
`CsrfViewMiddleware` 


https://blog.csdn.net/weixin_39922749/article/details/111207965
