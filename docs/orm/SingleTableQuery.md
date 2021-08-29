# 单表查询
单表查询是 `Django ORM` 的默认表现.   

例如:
```python3
from django.contrib.auth.models import User

# SELECT 
#         `auth_user`.`id`, 
#         `auth_user`.`password`, 
#         `auth_user`.`last_login`, 
#         `auth_user`.`is_superuser`, 
#         `auth_user`.`username`, 
#         `auth_user`.`first_name`, 
#         `auth_user`.`last_name`, 
#         `auth_user`.`email`, 
#         `auth_user`.`is_staff`, 
#         `auth_user`.`is_active`, 
#         `auth_user`.`date_joined` 
# FROM 
#         `auth_user` LIMIT 21
users = User.objects.all()
list(users)                                    # 触发 sql
```