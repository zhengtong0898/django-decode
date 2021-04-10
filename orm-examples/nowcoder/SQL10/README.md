[题链接](https://www.nowcoder.com/practice/32c53d06443346f4a2f2ca733c19660c?tpId=82&&tqId=29762&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell
# 建表
drop table if exists  `dept_manager` ; 
drop table if exists  `employees` ; 
CREATE TABLE `dept_manager` (
  `dept_no` char(4) NOT NULL,
  `emp_no` int(11) NOT NULL,
  `from_date` date NOT NULL,
  `to_date` date NOT NULL,
  PRIMARY KEY (`emp_no`,`dept_no`)
);

CREATE TABLE `employees` (
  `emp_no` int(11) NOT NULL,
  `birth_date` date NOT NULL,
  `first_name` varchar(14) NOT NULL,
  `last_name` varchar(16) NOT NULL,
  `gender` char(1) NOT NULL,
  `hire_date` date NOT NULL,
  PRIMARY KEY (`emp_no`)
);


# 插入数据
INSERT INTO dept_manager VALUES('d001',10002,'1996-08-03','9999-01-01');
INSERT INTO dept_manager VALUES('d002',10003,'1990-08-05','9999-01-01');
INSERT INTO employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');
INSERT INTO employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');
INSERT INTO employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');


# 期望断言数据
10001
```

&nbsp;   
&nbsp;  
### 子查询(subquery)
- SQL语句
  ```shell
  select emp_no
  from employees where emp_no
  not in (select emp_no from dept_manager)
  ```
- explain  

  |id|select_type|table|type|possible_keys|key|key_len|ref|rows|Extra|
  |---|---|---|---|---|---|---|---|---|---| 
  |1|PRIMARY|employees|index|-|PRIMARY|4|-|3|Using where; Using index|
  |2|MATERIALIZED|dept_manager|index|PRIMARY|PRIMARY|20|-|2|Using index|

- explain 解释
   
  |字段|值|说明|  
  |---|---|---|
  |select_type|PRIMARY|表示该`select`是最外层语句|
  |select_type|MATERIALIZED|表示是一个子查询, 采用虚拟表先查询出所有结果, 然后再与外层表做比较(避免多次`n+1`查询).|  
  |type|index|表示是按照索引顺序全表扫描.|
  |possible_keys|PRIMARY|查询条件的字段存在多个索引, 需要面临索引字段的选择, 这里列出所有相关联的索引名称.<br><br>PRIMARY表示`emp_no`字段存在于主键索引中.|
  |key|PRIMARY|`MySQL`优化器根据索引优先级选择最佳的索引, 由于这里只有一个索引, 所以不需要做选择, 直接使用PRIMARY索引|
  |key_len|4|选中的索引, 如果是单个字段索引, 那么`key_len`就是该字段的类型长度. <br>int的话就是固定4, <br>char(10)是定长类型, 所以是10<br>char(20)和varchar(20)是20*4+2==82| 
  |ref|-|用索引字段来比较查询值|
  |rows|3|预计要扫描多少行| 
  |Extra|Using where|该查询有`where`查询条件|
  |Extra|Using index|该查询有命中索引|

&nbsp;  
&nbsp;  
### 左联查询(left outer join)
- SQL语句
  ```shell
  select employees.emp_no 
  from employees 
  left join dept_manager on (employees.emp_no = dept_manager.emp_no) 
  where dept_manager.dept_no is null;
  ```
- explain  

  |id|select_type|table|type|possible_keys|key|key_len|ref|rows|Extra|
  |---|---|---|---|---|---|---|---|---|---| 
  |1|SIMPLE|employees|index|-|PRIMARY|4|-|3|Using index|
  |1|SIMPLE|dept_manager|ref|PRIMARY|PRIMARY|4|employees.emp_no|3|Using where; Using index; Not exists|

- explain 解释
   
  |字段|值|说明|  
  |---|---|---|
  |select_type|SIMPLE|表示使用了简单SELECT,不使用UNION或子查询等|
  |type|index|表示是按照索引顺序全表扫描.|
  |type|ref|比较是基于索引查找来比较的, 比较快.|
  |possible_keys|PRIMARY|查询条件的字段存在多个索引, 需要面临索引字段的选择, 这里列出所有相关联的索引名称.<br><br>PRIMARY表示`emp_no`字段存在于主键索引中.|
  |key|PRIMARY|`MySQL`优化器根据索引优先级选择最佳的索引, 由于这里只有一个索引, 所以不需要做选择, 直接使用PRIMARY索引|
  |key_len|4|选中的索引, 如果是单个字段索引, 那么`key_len`就是该字段的类型长度. <br>int的话就是固定4, <br>char(10)是定长类型, 所以是10<br>char(20)和varchar(20)是20*4+2==82| 
  |ref|employees.emp_no|用索引字段来比较查询值|
  |rows|3|预计要扫描多少行| 
  |Extra|Using where|该查询有`where`查询条件|
  |Extra|Using index|该查询有命中索引|

&nbsp;  
&nbsp;   
> 参考:  
> https://dev.mysql.com/doc/refman/8.0/en/explain-output.html   
> https://segmentfault.com/a/1190000016591055    
