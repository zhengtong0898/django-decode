&nbsp;  

### 快速的创建一个项目
```shell
# 定义项目名称变量
project_name="adminEx2"

# 定义数据库主机ip
db_ip="192.168.101.78"
db_name="adminEx2"
db_show="show create database ${db_name};"
db_create="create database if not exists ${db_name} character set utf8mb4;"
db_drop="drop database if exists ${db_name};"
db_sql="${db_drop} ${db_create} ${db_show}"


# 前置准备工作: 创建数据库名称
mysql -u root -h "${db_ip}" -P 3306 -e "${db_sql}" -p;

# 切换到 Django 项目的虚拟环境
source venv/bin/activate

# 创建项目 
django-admin startproject ${project_name}

# 创建数据库
python ${project_name}/manage.py migrate

# 创建管理员账号
# username: admin
# password: 123456
# email:    123@qq.com 
python ${project_name}/manage.py createsuperuser

# 启动项目
python ${project_name}/manage.py runserver
```

&nbsp;  
&nbsp;  
### 快速的创建一个应用
官方操作, 参考这里: https://docs.djangoproject.com/en/3.2/intro/tutorial01/#write-your-first-view
```shell
# 定义项目名称变量
project_name="adminEx2"

# 定义应用名称变量
app_name="ex"

# 进入项目文件夹
cd ${project_name}/

# 创建一个应用
python manage.py startapp ${app_name}

# 将应用添加到项目中
1. 将 "ex.apps.ExConfig" 写入到 "adminEx2.settings.INSTALLED_APPS" 列表中.
2. 将 path('ex/', include('ex.urls')) 写入到 "adminEx2.urls.urlpatterns" 路由列表中.
3. 创建 ex/urls.py 文件.
```

ex/urls.py 文件内容样板
```python
from django.urls import path

from . import views

# 备注:
# django 从 2.0 版本开始就一直采用 path(非正则表达式), 在此之前采用的是 url(正则表达式).
# path是一种 DSL, 用于简化表达式, 但是其内部最终还是要转换回到标准的正则表达式.
app_name = 'ex'
urlpatterns = [
    path('', views.index_view, name='index_view'),
]
```