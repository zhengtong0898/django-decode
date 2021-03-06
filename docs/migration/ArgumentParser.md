# 参数管理
参数管理上`Django`采用的是`ArgumentParser`, 主要目的是为了规范参数的类型、必填项控制, 为复杂性提供参数进行场景拆分和解耦.    

`makemigration`的命令行参数表格   

|参数|必填|描述|
|---|:---:|---|
| args | 是 | `app`的名称(一个或多个); `makemigration`会自动找到这些`app`并读取它们的`model`文件.|
| --dry-run | 否 | 演习(只跑检查, 不生成文件) |
| --merge | 否 | 必须有冲突的情况下使用`merge`参数才有效, 否则会报错; 使用`merge`表示冲突已经人工处理好了. | 
| --empty | 否 | 生成空的`migration`样板文件, 用于人工编辑处理冲突, 或其他复杂情况. | 
| --noinput | 否 | 通知`migration`, 有冲突也不要问我怎么处理. |
| --name | 否 | 指定`migration`生成的文件名, 默认时按照序列号来排列(例如: `0001_initial.py` | 
| --no-header | 否 | 生成文件中不包含头部的`# Generated by Django 3.0.8 on 2020-07-20 18:00` 字眼, 默认时包含. | 
| --check | 否 | 无用 |

除了`args`是必填之外, 我觉得有用的是`--dry-run`、`--merge`, 其他真的可有可无.

&nbsp;
# 参数的源码定义
源码片段: django/core/management/commands/makemigrations.py#23行
```python
class Command(BaseCommand):
    help = "Creates new migration(s) for apps."

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label', nargs='*',
            help='Specify the app label(s) to create migrations for.',
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help="Just show what migrations would be made; don't actually write them.",
        )
        parser.add_argument(
            '--merge', action='store_true',
            help="Enable fixing of migration conflicts.",
        )
        parser.add_argument(
            '--empty', action='store_true',
            help="Create an empty migration.",
        )
        parser.add_argument(
            '--noinput', '--no-input', action='store_false', dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '-n', '--name',
            help="Use this name for migration file(s).",
        )
        parser.add_argument(
            '--no-header', action='store_false', dest='include_header',
            help='Do not add header comments to new migration file(s).',
        )
        parser.add_argument(
            '--check', action='store_true', dest='check_changes',
            help='Exit with a non-zero status if model changes are missing migrations.',
        )
```

`parser.add_argument`的参数备注说明:
   
|参数|必填|描述|
|---|:---:|---|
|第一个参数|是| 参数简写 |
|第二个参数|否| 参数全写 |
|metavar|否| 在help帮助文档中显示的名字 |
|nargs='*'|否| 表示要求至少填写一个参数 |
|action|否| 大致的意思是对值进行加工, 让它附有特定含义, 具体例子[参考这里](https://docs.python.org/3/library/argparse.html#action) |
|dest|否| 参数名别名 |
|help|否| 当提供的参数值不符合要求时, 按`help`的值来报错 |