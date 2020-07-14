# 为什么要替代 mysqlclient ?
`Django` 默认使用的mysql库是 [mysqlclient](https://github.com/PyMySQL/mysqlclient-python), 它是基于 [MySQLdb1](https://github.com/farcepest/MySQLdb1) 库做的二次开发.  
由于 `MySQLdb1库` 依赖 `mysql.h` 这个头文件, 而 `mysql.h` 在windows环境下需要安装mysql相关软件, 因此整个事情变得一环扣一环, 甚至我在自己的电脑上安装了mysql-server后, 依然报 找不到mysql.h头文件问题, 经过大量查询资料和尝试都失败后, 找到了[一篇替换mysqlclient的文章](https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/). 

&nbsp;

# 怎么做?
1. [下载 OpenSSL-v1.1 完整版](https://slproweb.com/products/Win32OpenSSL.html)
2. 安装 OpenSSL-v1.1 ; 假设安装路径使: `C\OpenSSL-Win64-1.1`
3. 打开 `cmd` 窗口, 安装 `cryptography`
```
set LIB=C:\OpenSSL-Win64-1.1\lib;%LIB%
set INCLUDE=C:\OpenSSL-Win64-1.1\include;%INCLUDE%
pip.exe install cryptography, PyMySQL
```
4.&emsp;打开 `django 项目的 settings.py` 配置文件
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'USER': 'root',
        'PASSWORD': 'xxxxx',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

pymysql.version_info = (1, 4, 2, "final", 0)            # add here
pymysql.install_as_MySQLdb()                            # add here

```

&nbsp;

# 参考
[cryptography Issues](https://github.com/pyca/cryptography/issues/3028#issuecomment-552228389)    
[How to use PyMySQL with Django](https://adamj.eu/tech/2020/02/04/how-to-use-pymysql-with-django/)
