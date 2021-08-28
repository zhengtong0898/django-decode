&nbsp;  
### 如何将orm操作的sql语句打印出来?
- 方案一: 编辑`Django`源码
  > 编辑 Lib/site-packages/django/db/models/sql/compiler.py 文件
  ```python
  # 在文件头部导入logging
  import logging
  logger = logging.getLogger('django.compiler')
  
  
  class SQLCompiler:
   
      def execute_sql(self, result_type=MULTI, chunked_fetch=False, 
                      chunk_size=GET_ITERATOR_CHUNK_SIZE):
          sql_info = sql % tuple(params)          # 在这里添加这行代码
          logger.info("sql: %s" % sql_info)       # 在这里添加这行代码
          cursor.execute(sql, params)             
  
  
  class SQLInsertCompiler(SQLCompiler):
      
      def execute_sql(self, returning_fields=None):
          sql_info = sql % tuple(params)          # 在这里添加这行代码
          logger.info("sql: %s" % sql_info)       # 在这里添加这行代码
          cursor.execute(sql, params)        
  ```
- 方案二: 编辑三方库(`pymysql`)源码
  > 编辑 Lib/site-packages/pymysql/connections.py 文件
  ```python
  class Connection:

      def _execute_command(self, command, sql):
          print("pymysql: command: %s; sql: %s;" % (command, sql))        # 在第一行加入这行代码
  ```
