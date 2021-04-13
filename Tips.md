&nbsp;  

### 快速的创建一个项目
```shell
# 创建项目 
django-admin startproject AdminActions

# 创建数据库
python AdminActions/manage.py migrate

# 创建管理员账号
# username: admin
# password: 123456
# email:    123@qq.com 
python AdminActions/manage.py createsuperuser

# 启动项目
python AdminActions/manage.py runserver
```


