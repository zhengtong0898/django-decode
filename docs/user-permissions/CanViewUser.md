当我给一个用户添加 `CanViewUser` 权限时, 在`Django`里面发生了什么?   
当前文档试图通过页面、数据库、源代码来描述整个过程的来龙去脉.

&nbsp;  
### 页面操作
给 `zt` 用户添加 `CanViewUser` 权限
<p align="center">
    <img src="./imgs/img.png" alt="drawing" width="800"/>
</p>


&nbsp;  
### 数据库结构
auth_user 表, 存储用户数据
<p align="center">
    <img src="./imgs/img-auth-user.png" alt="drawing" width="800"/>
</p>

auth_permission 表, 存储权限数据
<p align="center">
    <img src="./imgs/img-auth-permission.png" alt="drawing" width="800"/>
</p>

auth_user_user_permission 多对多表, 存储用户和权限的绑定关系数据.
<p align="center">
    <img src="./imgs/img-auth-user-user-permissions.png" alt="drawing" width="800"/>
</p>


&nbsp;  
### 源代码  
TODO
