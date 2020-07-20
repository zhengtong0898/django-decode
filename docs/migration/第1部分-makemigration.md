# 概述
`Migration`是`Django`为`ORM`扩展出来的一套`Model To Schema`的同步方案, `Model`是python中的`Class`而`Schema`是数据库中的`table`的统称.   
日常编码过程中`ORM`会涉及到`新增Model`、`删除Model`、`新增Field`、`删除Field`, `Migration`致力于将这些操作转换到数据库的表和字段中.  
 
 &nbsp;  
# 命令行参数
|命令|描述|
|---|---|
|makemigration|生成`Migration`指令文件|
|migrate|执行迁移|
|sqlmigrate|TODO: 待补充|
|showmigrations|TODO:待补充|

&nbsp;  
# 生成指令文件
定义好`Model`之后同步到数据库, 第一步要做的就是`python manage.py makemigration` 让它生成一个指令文件(`app/migrations/0001_initial.py`), 生成指令文件的操作是一个复杂的过程, 本文负责解码这个环节的代码, 它涉及到了:   

|对象|描述|
|---|---|
|ArgumentParser|参数解析|
|MigrationLoader|Model源码文件解析 / 版本历史版本一致性 / 检查冲突|
|InteractiveMigrationQuestioner|以交互形式让用户选择处理方案|
|NonInteractiveMigrationQuestioner|预定义参数形式省略交互选择|
|MigrationWriter|读取`Model`源码文件, 写入到指令文件|

