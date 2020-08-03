# 响应式开发
在`html`中所谓的响应式布局的核心原理是, css样式编译器针对一些关键字进行了`watch`行为, 比如说最常见的是`@media screen`;  
像`Bootstrp`这种框架之所以声称自己是响应式布局框架, 是因为它使用了`@media screen`对不同设备和组件的分辨率进行预设, 例如:  
当分辨率的宽度是`1400px`的时候, `表格组件是`横向排铺; 当分辨率的宽度是`1280`的时候, 是纵向排铺.   

在`vue.js`中也使用了响应式布局, 典型的案例是它的`template`模板, 还有`data`成员变量, 这些在`vue.js`中都是固定式, 都是提前安排好`watch`和组件的`render`绑定.  

&nbsp;  
# 发布订阅和响应式的区别?
[Responsive.py](Responsive.py) 采用的是标准的 `发布订阅` 模式来处理消息的流转, 从备注的结构来看很容易就能辨别出它与`autoreload`的结构很像; `connect`对应的是`subscribe`, `send`对应的是`CallAfter`/`CallLater`.    

严格意义上来说发布订阅模式就是响应式模式, 原因是[Responsive.py](Responsive.py)例子中的 `dispatch.Signal` 环节被封装在`pubsub`这个第三方库中, 而对外暴露的能看得到的操作对象是 `publish`, `subscribe`.

所以, 结论是没有区别.   

&nbsp;  
# 发布订阅的使用场景.
1. 适合所有响应式前端软件(手机app, 桌面软件, ipad app等).
2. 适合后端消息异步通知.
3. 适合 即时通讯 软件.
4. 适合 实时BI 软件.
