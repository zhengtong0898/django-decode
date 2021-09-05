# 如何获取插入一条数据后的自增ID?

models.py
```python3
from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
```

&nbsp;  
views.py
```python3
from django.shortcuts import HttpResponse
from .models import Place, Restaurant


def index(request):

    family = Place(name="全家便利店", address="毕升路191号")     # step-1
    family.save()                                             # step-2
```

&nbsp;  
当 `step-1` 执行结束后, 返回 `family` 变量.  
`family` 变量是一个 `Place` 对象.   
`Place` 对象只负责存储实例化时存储的字段值.  

&nbsp;  
当执行 `step-2` 时, `Django ORM` 会生成并执行下面这个 `SQL`:
```shell
INSERT INTO `onetoonefield_place` (`name`, `address`)
VALUES      ("全家便利店", "毕升路191号")
RETURNING   `onetoonefield_place`.`id`
```
自增ID由数据库引擎内部算法来完成, 当数据写完之后数据库会返回这个自增好的ID.  


&nbsp;  
# 补充
我在 `Django` 中使用 `pymysql` 来完成 `SQL` 语句的提交.  
通过断点调试 `Django` 和 `pymysql` 发现:  
1. `pymysql` 通过 `socket.send` 发送 `SQL` 给 `mysql`.
2. `pymysql` 通过 `socket.makefile.read` 发送 `\x01` 这种字节来获取结果返回值.
