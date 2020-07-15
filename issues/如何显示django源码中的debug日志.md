# 问题
调试`autoreload`源码时, 想要让源码中的logger.debug打印出来.

&nbsp;   

# 怎么做?
1.&emsp;打开项目的 `settings.py` 文件.   
2.&emsp;在文件底部增加下面这段配置信息.
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.utils.autoreload': {                # 仅显示autoreload文件中的logger日志信息
            'handlers': {'console': {}},
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}
```

 |参数 | 说明| 
|---|---|
| **version**  |  是必填项, 且值必须是数字 1 <br /> 备注: 翻阅了logging源码, 只声明和强制要求, 并未使用这个值)|
| **disable_existing_loggers** | 待补充 |
| **handlers** | 使用'handlers' + 'console' 组合, 表示初始化 `logging.StreamHandler` <br />使用'handlers' + 'file' 组合, 表示初始化 `logging.handlers.RotatingFileHandler` |
| **loggers** | 为具体的`logger`设定日志等级, 默认是`INFO` |

&nbsp;  

# 参考
[Django configureing-logging](https://docs.djangoproject.com/en/3.0/topics/logging/#configuring-logging)   
[logging 官网 dictConfig](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details)  
[logging tutorial](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)