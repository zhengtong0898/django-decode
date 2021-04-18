&nbsp;  
&nbsp;  
### SQL1
- 题目  
  查找最晚入职员工的所有信息

- [题链接](https://www.nowcoder.com/practice/218ae58dfdcd4af195fff264e062138f?tpId=82&&tqId=29753&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  # 第一种写法: order by 和 limit
  SELECT `SQL1_employees`.`emp_no`,
         `SQL1_employees`.`birth_date`,
         `SQL1_employees`.`first_name`,
         `SQL1_employees`.`last_name`,
         `SQL1_employees`.`gender`,
         `SQL1_employees`.`hire_date`
  FROM `SQL1_employees`
  ORDER BY `SQL1_employees`.`hire_date`
  DESC LIMIT 1
  
  # 第二种写法: subquery
  SELECT `SQL1_employees`.`emp_no`,
         `SQL1_employees`.`birth_date`,
         `SQL1_employees`.`first_name`,
         `SQL1_employees`.`last_name`,
         `SQL1_employees`.`gender`,
         `SQL1_employees`.`hire_date`
  FROM `SQL1_employees`
  WHERE `SQL1_employees`.`hire_date` = (SELECT MAX(U0.`hire_date`) AS `ss`
                                        FROM `SQL1_employees` U0)  
  ```


&nbsp;  
&nbsp;  
### SQL2
- 题目  
  查找入职员工时间排名倒数第三的员工所有信息

- [题链接](https://www.nowcoder.com/practice/ec1ca44c62c14ceb990c3c40def1ec6c?tpId=82&&tqId=29754&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  SELECT `SQL2_employees`.`emp_no`,
         `SQL2_employees`.`birth_date`,
         `SQL2_employees`.`first_name`,
         `SQL2_employees`.`last_name`,
         `SQL2_employees`.`gender`,
         `SQL2_employees`.`hire_date`
  FROM `SQL2_employees`
  ORDER BY `SQL2_employees`.`hire_date` DESC
  LIMIT 1 OFFSET 2
  ```


&nbsp;  
&nbsp;  
### SQL3
- 题目  
  查找各个部门当前领导当前薪水详情以及其对应部门编号dept_no

- [题链接](https://www.nowcoder.com/practice/c63c5b54d86e4c6d880e4834bfd70c3b?tpId=82&&tqId=29755&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select s.id as id, 
         s.emp_no as emp_no, 
         s.salary as salary, 
         s.from_date as from_date, 
         s.to_date as to_date, 
         d.dept_no as dept_no 
  from sql3_dept_manager as d 
  left join sql3_salaries as s on d.emp_no = s.emp_no
  ```


&nbsp;  
&nbsp;  
### SQL4
- 题目  
  查找所有已经分配部门的员工的last_name和first_name

- [题链接](https://www.nowcoder.com/practice/6d35b1cd593545ab985a68cd86f28671?tpId=82&&tqId=29756&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  # 以dept_emp为主表连接查询employees表.
  
  select employees.last_name as last_name, 
         employees.first_name as first_name, 
         dept_emp.dept_no as dept_no 
  from dept_emp left join employees on (dept_emp.emp_no=employees.emp_no)
  ```
  

&nbsp;  
&nbsp;  
### SQL5
- 题目  
  查找所有员工的last_name和first_name以及对应部门编号dept_no

- [题链接](https://www.nowcoder.com/practice/dbfafafb2ee2482aa390645abd4463bf?tpId=82&&tqId=29757&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)


- SQL
  ```shell
  # 以employees为主表连接查询dept_no表.
  select employees.last_name, 
         employees.first_name, 
         dept_emp.dept_no 
  from employees 
  left join dept_emp on employees.emp_no=dept_emp.emp_no;
  ```


&nbsp;  
&nbsp;  
### SQL7
- 题目  
  查找薪水涨幅超过15次的员工号emp_no以及其对应的涨幅次数t

- [题链接](https://www.nowcoder.com/practice/6d4a4cff1d58495182f536c548fee1ae?tpId=82&&tqId=29759&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select emp_no, count(to_date) as t
  from salaries
  group by emp_no
  having t > 15;
  ```


&nbsp;  
&nbsp;  
### SQL8
- 题目  
  找出所有员工当前具体的薪水salary情况

- [题链接](https://www.nowcoder.com/practice/ae51e6d057c94f6d891735a48d1c2397?tpId=82&&tqId=29760&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select salary 
  from salaries 
  group by salary 
  order by salary desc
  ```


&nbsp;  
&nbsp;  
### SQL10
- 题目  
  获取所有非manager的员工emp_no

- [题链接](https://www.nowcoder.com/practice/32c53d06443346f4a2f2ca733c19660c?tpId=82&&tqId=29762&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- 建表、数据、断言预期
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
  
- 子查询
  ```shell
  select emp_no
  from employees where emp_no
  not in (select emp_no from dept_manager)
  ```  
  
  explain  
   
  |id|select_type|table|type|possible_keys|key|key_len|ref|rows|Extra|
  |---|---|---|---|---|---|---|---|---|---| 
  |1|PRIMARY|employees|index|-|PRIMARY|4|-|3|Using where; Using index|
  |2|MATERIALIZED|dept_manager|index|PRIMARY|PRIMARY|20|-|2|Using index|
  
  explain 解释  
  
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


- 左联查询(left outer join)   

  ```shell
  select employees.emp_no 
  from employees 
  left join dept_manager on (employees.emp_no = dept_manager.emp_no) 
  where dept_manager.dept_no is null;
  ```
  
  explain
  
  |id|select_type|table|type|possible_keys|key|key_len|ref|rows|Extra|
  |---|---|---|---|---|---|---|---|---|---| 
  |1|SIMPLE|employees|index|-|PRIMARY|4|-|3|Using index|
  |1|SIMPLE|dept_manager|ref|PRIMARY|PRIMARY|4|employees.emp_no|3|Using where; Using index; Not exists|  
  
  explain 解释
  
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
  
  > 参考:  
  > https://dev.mysql.com/doc/refman/8.0/en/explain-output.html   
  > https://segmentfault.com/a/1190000016591055   


&nbsp;  
&nbsp;  
### SQL11
- 题目  
  获取所有员工当前的manager

- [题链接](https://www.nowcoder.com/practice/e50d92b8673a440ebdf3a517b5b37d62?tpId=82&&tqId=29763&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select e.emp_no as emp_no, 
         m.emp_no as manager 
  from dept_manager as m
  left join dept_emp as e 
  on m.dept_no=e.dept_no
  where m.emp_no <> e.emp_no;
  ```


&nbsp;  
&nbsp;  
### SQL12
- 题目  
  获取所有部门中当前员工薪水最高的相关信息

- [题链接](https://www.nowcoder.com/practice/4a052e3e1df5435880d4353eb18a91c6?tpId=82&&tqId=29764&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  -- 思路
  -- 1. 第一个子查询采用inner join创建一个临时表, 仅包含必须字段(dept_no, emp_no, salary).
  -- 2. 第二个子查询采用inner join创建一个临时表, 仅包含每个部门薪资最高的一条数据(dept_no, maxSalary)
  -- 3. 第一个临时表 left join 第二个临时表, 筛选条件: 部门相同且薪资相同的数据, 提取出来.
  --
  -- 最终得到每个部门薪资最高的员工表.
  select     innertable.* 
  from      (select de.dept_no as dept_no,
                    de.emp_no as emp_no,
                    ss.salary as salary
             from dept_emp as de
             inner join salaries as ss
             on de.emp_no = ss.emp_no) as innertable 
  
  left join (select de.dept_no as dept_no,
                    max(ss.salary) as maxSalary
             from dept_emp as de
             inner join salaries as ss
             on de.emp_no = ss.emp_no
             group by de.dept_no) as ms_table
  
  on         innertable.dept_no = ms_table.dept_no
  where      innertable.salary = ms_table.maxSalary
  order by   innertable.dept_no
  ```


&nbsp;  
&nbsp;  
### SQL15
- 题目  
  查找employees表所有emp_no为奇数

- [题链接](https://www.nowcoder.com/practice/a32669eb1d1740e785f105fa22741d5c?tpId=82&&tqId=29767&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select * 
  from employees 
  where last_name<>'Mary' and 
        mod(emp_no, 2)=1 
  order by hire_date desc;
  ```


&nbsp;  
&nbsp;  
### SQL16
- 题目  
  统计出当前各个title类型对应的员工当前薪水对应的平均工资

- [题链接](https://www.nowcoder.com/practice/c8652e9e5a354b879e2a244200f1eaae?tpId=82&&tqId=29768&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select t.title, AVG(s.salary) as avg_salary
  from titles as t 
  inner join salaries as s
  on t.emp_no = s.emp_no
  group by t.title
  order by avg_salary
  ```


&nbsp;  
&nbsp;  
### SQL17
- 题目  
  获取当前薪水第二多的员工的emp_no以及其对应的薪水salary

- [题链接](https://www.nowcoder.com/practice/8d2c290cc4e24403b98ca82ce45d04db?tpId=82&&tqId=29769&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select emp_no, salary 
  from salaries 
  order by salary desc 
  limit 1 offset 1
  ```


&nbsp;  
&nbsp;  
### SQL18
- 题目  
  查找当前薪水排名第二多的员工编号emp_no

- [题链接](https://www.nowcoder.com/practice/c1472daba75d4635b7f8540b837cc719?tpId=82&&tqId=29770&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select e.emp_no, s.salary, e.last_name, e.first_name 
  from employees as e 
  inner join (select * 
              from salaries 
              where salary=(select max(salary)
                            from salaries 
                            where salary<>(select max(salary) 
                                           from salaries))) as s
  on e.emp_no = s.emp_no;
  ```


&nbsp;  
&nbsp;  
### SQL19
- 题目  
  查找所有员工的last_name和first_name以及对应的dept_name

- [题链接](https://www.nowcoder.com/practice/5a7975fabe1146329cee4f670c27ad55?tpId=82&&tqId=29771&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select e.last_name, e.first_name, d.dept_name
  from employees as e
  left join dept_emp as de
  on e.emp_no = de.emp_no
  left join departments as d
  on de.dept_no = d.dept_no
  ```


&nbsp;  
&nbsp;  
### SQL21
- 题目  
  查找所有员工自入职以来的薪水涨幅情况

- [题链接](https://www.nowcoder.com/practice/fc7344ece7294b9e98401826b94c6ea5?tpId=82&&tqId=29773&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  # 第一种写法
  select * from (select e.emp_no, (max(s.salary) - min(s.salary)) as growth 
                 from employees as e
                 inner join salaries as s
                 on e.emp_no = s.emp_no
                 where e.hire_date = s.from_date or s.to_date='9999-01-01'            -- 入职时间 or 在职时间
                 group by e.emp_no) as r
  where r.emp_no in (select emp_no from salaries where to_date='9999-01-01')          -- in 在职时间
  order by r.growth;
  
  
  
  
  # 第二种写法
  select b.emp_no,(b.salary-a.salary) as growth
  from       (select e.emp_no,s.salary
              from employees e  
              join salaries s 
              on e.emp_no=s.emp_no
              and e.hire_date=s.from_date) a          -- 入职工资表
  inner join (select e.emp_no,s.salary
              from employees e  
              join salaries s 
              on e.emp_no=s.emp_no
              where s.to_date='9999-01-01') b         -- 现在工资表
  on a.emp_no=b.emp_no
  order by growth;
  ```


&nbsp;  
&nbsp;  
### SQL22
- 题目  
  统计各个部门的工资记录数

- [题链接](https://www.nowcoder.com/practice/6a62b6c0a7324350a6d9959fa7c21db3?tpId=82&&tqId=29774&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  select d.dept_no, d.dept_name, count(de.emp_no) 
  from dept_emp as de
  inner join departments as d on de.dept_no = d.dept_no
  inner join salaries as s on de.emp_no = s.emp_no 
  group by d.dept_no
  order by d.dept_no;
  ```



&nbsp;  
&nbsp;  
### SQL23
- 题目  
  对所有员工的当前薪水按照salary进行按照1-N的排名

- [题链接](https://www.nowcoder.com/practice/b9068bfe5df74276bd015b9729eec4bf?tpId=82&&tqId=29775&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  
  # 第一种写法
  select emp_no, 
         salary, 
         dense_rank() over (order by salary desc) as t_rank 
  from salaries;
  
  
  # 第二种写法
  # 1. 外层 s 由于使用了 order by s.salary desc, 所以每次迭代都会pop集合中最大的元素.
  # 2. 子查询 sub_s 做 >= 比较每次迭代最大的值, 即: 大于最大的数, 去重, 有几个数就是排名第几.
  #    第一次迭代: sub_s >= (s.salary 最大数), 去重 + count == 1
  #    第二次迭代: sub_s >= (s.salary 第二大数), 去重 + count == 2  
  select emp_no,
         salary,
         (select count(distinct salary) 
          from salaries sub_s
          where sub_s.salary>=s.salary) as rank 	
  from salaries s 
  order by s.salary desc;
  ```


&nbsp;  
&nbsp;  
### SQL24
- 题目   
  获取所有非manager员工当前的薪水情况
  
- [题链接](https://www.nowcoder.com/practice/8fe212a6c71b42de9c15c56ce354bebe?tpId=82&&tqId=29776&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL
  ```shell
  -- 这里使用 left join 则不满足预期结果, 使用 inner join 则满足.
  -- 因为 inner join 取交集, left join除了交集(intersection)还会把主表的数据(difference)保留下来.
  select de.dept_no, s.emp_no, s.salary 
  from (select * 
        from dept_emp
        where emp_no not in (select emp_no from dept_manager)) as de
  inner join salaries as s
  on de.emp_no = s.emp_no;
  ```  
  
&nbsp;  
&nbsp;  
### SQL25
- 题目  
  获取员工其当前的薪水比其manager当前薪水还高的相关信息   

- [题链接](https://www.nowcoder.com/practice/f858d74a030e48da8e0f69e21be63bef?tpId=82&&tqId=29777&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)  

- SQL  
  ```shell
  -- emps 员工薪资集合
  -- managers 管理者薪资集合
  -- on 相同部门 且 员工薪资 > 管理者薪资。
  
  select emps.emp_no, managers.emp_no, emps.salary, managers.salary 
  from (select de.emp_no as emp_no, de.dept_no as dept_no, s.salary as salary 
        from dept_emp as de
        inner join salaries as s
        on de.emp_no = s.emp_no
        where de.emp_no not in (select emp_no from dept_manager)) as emps
  inner join (select dm.emp_no as emp_no, dm.dept_no as dept_no, s.salary as salary
              from dept_manager as dm 
              inner join salaries as s 
              on dm.emp_no=s.emp_no) as managers
  on emps.dept_no = managers.dept_no and emps.salary > managers.salary;
  ```
  
&nbsp;  
&nbsp;  
### SQL26

- 题目   
  汇总各个部门当前员工的title类型的分配数目

- [题链接](https://www.nowcoder.com/practice/4bcb6a7d3e39423291d2f7bdbbff87f8?tpId=82&&tqId=29778&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  -- group by 多字段联合分组
  select de.dept_no, d.dept_name, t.title, count(*)
  from dept_emp as de 
  inner join departments as d on de.dept_no = d.dept_no
  inner join titles as t on de.emp_no = t.emp_no
  group by de.dept_no, t.title
  order by de.dept_no
  ```


&nbsp;  
&nbsp;  
### SQL28

- 题目   
  查找描述信息中包括robot的电影对应的分类名称以及电影数目

- [题链接](https://www.nowcoder.com/practice/3a303a39cc40489b99a7e1867e6507c5?tpId=82&&tqId=29780&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  -- 子查询: 将所有 count(film_id) >= 5 的分类id拿出来跟 sub_fc.category_id 做 in 比较.

  select sub_c.name,
         count(sub_c.name)
  from film as f
  inner join film_category as fc on f.film_id     = fc.film_id
  inner join category      as c  on c.category_id = fc.category_id
  where sub_f.description like '%robot%' and 
        sub_fc.category_id in (SELECT category_id FROM film_category GROUP BY category_id HAVING count(film_id)>=5)
  group by c.name;
  ```
  

&nbsp;  
&nbsp;  
### SQL29

- 题目   
  使用join查询方式找出没有分类的电影id以及名称

- [题链接](https://www.nowcoder.com/practice/a158fa6e79274ac497832697b4b83658?tpId=82&&tqId=29781&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  select f.film_id, f.title
  from film as f
  left join film_category as fc on f.film_id = fc.film_id
  where fc.category_id is null;
  ```  

&nbsp;  
&nbsp;  
### SQL30

- 题目   
  使用子查询的方式找出属于Action分类的所有电影对应的title,description

- [题链接](https://www.nowcoder.com/practice/2f2e556d335d469f96b91b212c4c203e?tpId=82&&tqId=29782&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  -- 纯子查询的方式
  select title, description 
  from film 
  where film_id in (select film_id 
                    from film_category 
                    where category_id in (select category_id 
                                          from category 
                                          where name='Action'))
  
  -- 常规方式
  select f.title, f.description 
  from film_category as fc
  inner join category as c on c.category_id = fc.category_id
  inner join film as f on f.film_id = fc.film_id
  where c.name = 'Action'
  ```  


&nbsp;  
&nbsp;  
### SQL32

- 题目   
  将employees表的所有员工的last_name和first_name拼接起来作为Name，中间以一个空格区分

- [题链接](https://www.nowcoder.com/practice/6744b90bbdde40209f8ecaac0b0516fe?tpId=82&&tqId=29800&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  select concat(last_name, ' ', first_name) 
  from employees
  ```  



&nbsp;  
&nbsp;  
### SQL33

- 题目   
  创建一个actor表，包含如下列信息

- [题链接](https://www.nowcoder.com/practice/ac233de508ef4849b0eeb4f38dcf09cf?tpId=82&&tqId=29801&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  -- 建表
  create table `actor` (
      actor_id smallint(5) not null primary key,
      first_name varchar(45) not null,
      last_name varchar(45) not null, 
      last_update date not null
  );
  ```  
  

&nbsp;  
&nbsp;  
### SQL34

- 题目   
  批量插入数据

- [题链接](https://www.nowcoder.com/practice/51c12cea6a97468da149c04b7ecf362e?tpId=82&&tqId=29802&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  insert into `actor` values (1, 'PENELOPE', 'GUINESS', '2006-02-15 12:34:33'), 
                             (2, 'NICK', 'WAHLBERG', '2006-02-15 12:34:33');
  ```    
  

&nbsp;  
&nbsp;  
### SQL35

- 题目   
  批量插入数据,如果数据已经存在，请忽略，不使用replace操作

- [题链接](https://www.nowcoder.com/practice/153c8a8e7805400ba8e384e03acc6b3e?tpId=82&&tqId=29803&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  -- (select '3', 'ED', 'CHASE', '2006-02-15 12:34:33') as tmp 作为临时表
  --
  -- select * from tmp where not exists; 如果不存在则使用tmp中的所有数据, 如果存在则不返回任何数据.  
  
  insert into actor 
      select * 
      from (select '3', 'ED', 'CHASE', '2006-02-15 12:34:33') as tmp
      where not exists (select * from actor where actor_id='3');
  ```    
  
&nbsp;  
&nbsp;  
### SQL36

- 题目   
  创建一个actor_name表，将actor表中的所有first_name以及last_name导入改表

- [题链接](https://www.nowcoder.com/practice/881385f388cf4fe98b2ed9f8897846df?tpId=82&&tqId=29804&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  create table `actor_name` (
      `first_name` varchar(45) not null,
      `last_name` varchar(45) not null
  );

  insert into `actor_name`
      select `first_name`, `last_name` 
      from `actor`;
  ```      

  
&nbsp;  
&nbsp;  
### SQL37

- 题目   
  对first_name创建唯一索引uniq_idx_firstname，对last_name创建普通索引idx_lastname

- [题链接](https://www.nowcoder.com/practice/e1824daa0c49404aa602cf0cb34bdd75?tpId=82&&tqId=29805&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  alter table `actor` add unique index `uniq_idx_firstname` (first_name);   -- 创建唯一索引
  alter table `actor` add index `idx_lastname` (last_name);                 -- 创建普通索引
  ```      

  
&nbsp;  
&nbsp;  
### SQL38

- 题目   
  针对actor表创建视图actor_name_view

- [题链接](https://www.nowcoder.com/practice/b9db784b5e3d488cbd30bd78fdb2a862?tpId=82&&tqId=29806&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  create view `actor_name_view` 
      (`first_name_v`, `last_name_v`)                       -- 视图字段名
  as 
      (select `first_name`, `last_name` from `actor`);
  ```      


  
&nbsp;  
&nbsp;  
### SQL39

- 题目   
  针对上面的salaries表emp_no字段创建索引idx_emp_no，查询emp_no为10005,

- [题链接](https://www.nowcoder.com/practice/f9fa9dc1a1fc4130b08e26c22c7a1e5f?tpId=82&&tqId=29807&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)   

- SQL   
  ```shell
  select * 
  from salaries 
  force index (`idx_emp_no`)            -- 指定使用`idx_emp_no`索引(不需要优化器自行选择).
  where emp_no=10005;
  ```      

&nbsp;  
&nbsp;  
### SQL40

- 题目   
  在last_update后面新增加一列名字为create_date
  
- [题链接](https://www.nowcoder.com/practice/119f04716d284cb7a19fba65dd876b03?tpId=82&&tqId=29808&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  alter table `actor` add column `create_date` datetime not null default '2020-10-01 00:00:00';
  ```


&nbsp;  
&nbsp;  
### SQL41

- 题目   
  构造一个触发器audit_log，在向employees表中插入一条数据的时候，触发插入相关的数据到audit中
  
- [题链接](https://www.nowcoder.com/practice/7e920bb2e1e74c4e83750f5c16033e2e?tpId=82&&tqId=29809&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  create trigger `audit_log` 
  after insert on `employees_test` for each row 
  begin
      insert into `audit` values (NEW.id, NEW.name);
  end
  ```



&nbsp;  
&nbsp;  
### SQL42

- 题目   
  删除emp_no重复的记录，只保留最小的id对应的记录。
  
- [题链接](https://www.nowcoder.com/practice/3d92551a6f6d4f1ebde272d20872cf05?tpId=82&&tqId=29810&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 注意事项
  -- 直接 select 出 min_id 然后 delete 会报错: You can’t specify target table ‘xxx’ for update in FROM clause.
  -- 这很可能是它内部用iterator的方式来处理数据, 要保证数据的完整性, 就需要再做一层子查询, 让它先把需要的数据提取出来, 然后在做删除.
  
  delete from `titles_test` 
  where id not in (select min_id 
                   from (select min(id) as min_id 
                         from `titles_test` 
                         group by emp_no) as a);
  ```


&nbsp;  
&nbsp;  
### SQL43

- 题目   
  将所有to_date为9999-01-01的全部更新为NULL,且
  
- [题链接](https://www.nowcoder.com/practice/859f28f43496404886a77600ea68ef59?tpId=82&&tqId=29811&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  update `titles_test` 
  set to_date=NULL, from_date='2001-01-01' 
  where to_date='9999-01-01';
  ```


&nbsp;  
&nbsp;  
### SQL44

- 题目   
  将id=5以及emp_no=10001的行数据替换成id=5以及emp_no=10005,其他数据保持不变，使用replace实现。
  
- [题链接](https://www.nowcoder.com/practice/2bec4d94f525458ca3d0ebf3bc8cd240?tpId=82&&tqId=29812&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  # 第一种写法
  replace into `titles_test` 
      select `id`, 1005, `title`, `from_date`, `to_date` 
      from `titles_test` 
      where `id`=5;
  
  
  # 第二种写法
  replace into `titles_test` values(5, 1005, 'ss', '9999-01-01', '9999-01-01');
  
  
  # 第三种写法
  replace into `titles_test` 
  set id=5, 
      emp_no=10005, 
      title='sss', 
      from_date='9999-01-01', 
      to_date='9999-01-01';
  ```



&nbsp;  
&nbsp;  
### SQL45

- 题目   
  将titles_test表名修改为titles_2017
  
- [题链接](https://www.nowcoder.com/practice/5277d7f92aa746ab8aa42886e5d570d4?tpId=82&&tqId=29813&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  rename table `titles_test` to `titles_2017`;
  ```


&nbsp;  
&nbsp;  
### SQL46

- 题目   
  在audit表上创建外键约束，其emp_no对应employees_test表的主键id
  
- [题链接](https://www.nowcoder.com/practice/aeaa116185f24f209ca4fa40e226de48?tpId=82&&tqId=29814&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  alter table `audit` 
  add foreign key `idx_audit_emp_no` (`emp_no`) 
  references `employees_test` (`id`);
  ```



&nbsp;  
&nbsp;  
### SQL48

- 题目   
  将所有获取奖金的员工当前的薪水增加10%
  
- [题链接](https://www.nowcoder.com/practice/d3b058dcc94147e09352eb76f93b3274?tpId=82&&tqId=29816&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  update `salaries` 
  set salary = salary * 1.1 
  where emp_no in (select emp_no from emp_bonus) and
        to_date='9999-01-01';
  ```



&nbsp;  
&nbsp;  
### SQL50

- 题目   
  将employees表中的所有员工的last_name和first_name通过(')连接起来。
  
- [题链接](https://www.nowcoder.com/practice/810bf4ee3ac64949b08983aa66ec7bee?tpId=82&&tqId=29818&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select concat(`last_name`, '\'', `first_name`) as name 
  from `employees`;
  ```


&nbsp;  
&nbsp;  
### SQL51

- 题目   
  查找字符串'10,A,B'
  
- [题链接](https://www.nowcoder.com/practice/e3870bd5d6744109a902db43c105bd50?tpId=82&&tqId=29819&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- length('10,A,B') 得出总长度: a
  -- length(replace('10,A,B', ',', '')) 得出减去','后的总长度: b
  -- a - b = ','的个数.
  select (length('10,A,B') - length(replace('10,A,B', ',', ''))) as cnt;
  ```



&nbsp;  
&nbsp;  
### SQL52

- 题目   
  获取Employees中的first_name，查询按照first_name最后两个字母，按照升序进行排列
  
- [题链接](https://www.nowcoder.com/practice/74d90728827e44e2864cce8b26882105?tpId=82&&tqId=29820&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  # 第一种写法
  select `first_name` 
  from `employees` 
  order by substr(`first_name`, -2)
  
  
  # 第二种写法
  select e.`first_name` 
  from (select `first_name`, substring(`first_name`, length(`first_name`)-1, 2) as fn 
        from employees order by fn) as e;
  ```



&nbsp;  
&nbsp;  
### SQL53

- 题目   
  按照dept_no进行汇总，属于同一个部门的emp_no按照逗号进行连接，结果给出dept_no以及连接出的结果employees
  
- [题链接](https://www.nowcoder.com/practice/6e86365af15e49d8abe2c3d4b5126e87?tpId=82&&tqId=29821&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select `dept_no`, group_concat(`emp_no` SEPARATOR ',') as employees 
  from `dept_emp` 
  group by `dept_no`;
  
  
  -- 参考资源: https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat
  -- 参考资源: https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php
  ```



&nbsp;  
&nbsp;  
### SQL54

- 题目   
  查找排除当前最大、最小salary之后的员工的平均工资avg_salary
  
- [题链接](https://www.nowcoder.com/practice/95078e5e1fba4438b85d9f11240bc591?tpId=82&&tqId=29822&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  # 第一种写法
  select (sum(`salary`) - max(`salary`) - min(`salary`)) / (count(`emp_no`) - 2) as average
  from `salaries` 
  where `to_date`='9999-01-01';
  
  # 第二种写法
  select
      avg(salary) as avg_salary
  from
      salaries
  where
      to_date = '9999-01-01'
      and salary != (select min(salary) from salaries where to_date = '9999-01-01')
      and salary != (select max(salary) from salaries where to_date = '9999-01-01')
  ```



&nbsp;  
&nbsp;  
### SQL55

- 题目   
  分页查询employees表，每5行一页，返回第2页的数据
  
- [题链接](https://www.nowcoder.com/practice/f24966e0cb8a49c192b5e65339bc8c03?tpId=82&&tqId=29823&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select * from employees limit 5 offset 5;
  ```


&nbsp;  
&nbsp;  
### SQL57

- 题目   
  使用含有关键字exists查找未分配具体部门的员工的所有信息。
  
- [题链接](https://www.nowcoder.com/practice/c39cbfbd111a4d92b221acec1c7c1484?tpId=82&&tqId=29825&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select e.* 
  from `employees` as e
  where not exists (select * from `dept_emp` as de where e.`emp_no` = de.`emp_no`);
  ```



&nbsp;  
&nbsp;  
### SQL59

- 题目   
  获取有奖金的员工相关信息。
  
- [题链接](https://www.nowcoder.com/practice/5cdbf1dcbe8d4c689020b6b2743820bf?tpId=82&&tqId=29827&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select e.`emp_no`,
         e.`first_name`,
         e.`last_name`,
         eb.`btype`,
         s.`salary`,
         (CASE 
              WHEN eb.`btype` = 1 THEN s.`salary` * 0.1
              WHEN eb.`btype` = 2 THEN s.`salary` * 0.2
              ELSE s.`salary` * 0.3
          END) as bonus 
  from `employees` as e
  inner join `emp_bonus` as eb on e.`emp_no` = eb.`emp_no` 
  inner join `salaries` as s on e.`emp_no` = s.`emp_no`
  where s.`to_date`='9999-01-01';
  ```



&nbsp;  
&nbsp;  
### SQL60

- 题目   
  统计salary的累计和running_total
  
- [题链接](https://www.nowcoder.com/practice/58824cd644ea47d7b2b670c506a159a6?tpId=82&&tqId=29828&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法
  -- sum: 一般情况下会将多行聚合成一行, 但是配合over一起使用, 它将采取窗口(非聚合)形式.
  -- over: 流式聚合, 即每次都是从0至当前行聚合计算.
  -- 参考: https://dev.mysql.com/doc/refman/8.0/en/window-functions-usage.html
  select emp_no, salary, sum(salary) over (order by emp_no) as running_total
  from salaries
  where to_date = '9999-01-01';
  
  
  -- 第二种写法
  set @running_total = 0;
  select `emp_no`, `salary`, (@running_total := @running_total + `salary`) as `running_total` 
  from `salaries` 
  where `to_date`='9999-01-01';
  ```


&nbsp;  
&nbsp;  
### SQL61

- 题目   
  对于employees表中，给出奇数行的first_name
  
- [题链接](https://www.nowcoder.com/practice/e3cf1171f6cc426bac85fd4ffa786594?tpId=82&&tqId=29829&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法
  -- 按照 employees.emp_no 来排序
  select a.`first_name`
  from (select `emp_no`, 
               `first_name`, 
                row_number() over(order by first_name) as row_num
        from `employees`) a
  where `row_num` % 2 = 1
  order by a.`emp_no`;
  
  
  -- 第二种写法
  -- 按照employees原有的顺序来显示
  select e.first_name from employees as e 
  left join (select emp_no, 
                    first_name, 
                    row_number() over(order by first_name asc) as row_num 
             from employees) as a
  on e.emp_no = a.emp_no
  where a.row_num % 2 = 1;
  ```



&nbsp;  
&nbsp;  
### SQL62

- 题目   
  出现三次以上相同积分的情况
  
- [题链接](https://www.nowcoder.com/practice/c69ac94335744480aa50646864b7f24d?tpId=82&&tqId=35079&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法
  select number from grade
  group by number
  having count(id) >= 3;
  
  
  -- 第二种写法
  select number 
  from (select number, 
               count(number) as counted 
        from grade group by number) as a 
  where a.counted >= 3;
  ```


&nbsp;  
&nbsp;  
### SQL63

- 题目   
  刷题通过的题目排名
  
- [题链接](https://www.nowcoder.com/practice/cd2e10a588dc4c1db0407d0bf63394f3?tpId=82&&tqId=35080&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- dense_rank () over (order by number desc) 表示: 先排序 number 字段, 然后为每个number统计数量, 得到一个count值.
  -- order by t_rank, id                       表示: 先排序 t_rank 字段, 然后再按照t_rank相同的组内再按 id 字段来排序.
  
  select id, 
         number, 
         dense_rank() over (order by number desc) as t_rank 
  from passing_number 
  order by t_rank, id;
  ```


&nbsp;  
&nbsp;  
### SQL64

- 题目   
  找到每个人的任务
  
- [题链接](https://www.nowcoder.com/practice/9dd9182d029a4f1d8c1324b63fc719c9?tpId=82&&tqId=35081&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select p.*, t.content
  from person as p 
  left join task t on p.id = t.person_id
  order by p.id;
  ```


&nbsp;  
&nbsp;  
### SQL65

- 题目   
  异常的邮件概率
  
- [题链接](https://www.nowcoder.com/practice/d6dd656483b545159d3aa89b4c26004e?tpId=82&&tqId=35083&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  # 第一种写法
  select e.date,round(sum(case e.type when "no_completed" then 1 else 0 end)/count(*),3) p
  from email e
  join user u1 on e.send_id = u1.id
  join user u2 on e.receive_id = u2.id
  where u1.is_blacklist = 0 and u2.is_blacklist = 0
  group by e.date
  order by date
  
  # 第二种写法
  select valid_e.`date`, 
         round(sum(IF(valid_e.`type` = 'no_completed', 1, 0)) / count(valid_e.id), 3) as p
  from (select sub_e.*
        from `email` as sub_e 
        inner join (select * from `user` where `is_blacklist`=1) as black_u
        on sub_e.`send_id`!=black_u.`id` and sub_e.`receive_id`!=black_u.`id`) as valid_e
  group by valid_e.`date`
  ```


&nbsp;  
&nbsp;  
### SQL66

- 题目   
  牛客每个人最近的登录日期(一)
  
- [题链接](https://www.nowcoder.com/practice/ca274ebe6eac40ab9c33ced3f2223bb2?tpId=82&&tqId=35084&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select `user_id`, max(`date`) 
  from `login` 
  group by `user_id` 
  order by `user_id`;
  ```


&nbsp;  
&nbsp;  
### SQL67

- 题目   
  牛客每个人最近的登录日期(二)
  
- [题链接](https://www.nowcoder.com/practice/7cc3c814329546e89e71bb45c805c9ad?tpId=82&&tqId=35085&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 子查询:   提取`login`最大日期和user_id
  -- 左联查询:  根据上面的子查询, 提取出有效的 client_id 
  -- 内联查询:  根据有效的 user_id 和 client_id, 提取出有效的 username, clientname, date.
  
  select u.`name`as u_n, c.`name` as c_n, l_2.`date` 
  from (select `user_id`, max(`date`) as `date` from `login` group by `user_id`) as l_1 
  left join `login` as l_2 on l_1.`user_id` = l_2.`user_id` and l_1.`date`=l_2.date
  inner join `user` as u on l_2.`user_id` = u.`id` 
  inner join `client` as c on l_2.`client_id` = c.`id`
  order by u.`name`;
  ```



&nbsp;  
&nbsp;  
### SQL68

- 题目   
  牛客每个人最近的登录日期(三)
  
- [题链接](https://www.nowcoder.com/practice/16d41af206cd4066a06a3a0aa585ad3d?tpId=82&&tqId=35086&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法(高效)
  -- 子查询:     提取user_id和最小的日期, 这样可以得出去重后所有用户(含: 有效和无效的用户)
  -- 左联查询:   根据 user_id 和 最小的日期+1天 查询出(仅含: 有效的用户)
  -- 计算存活率: 根据 有效用户 / 去重后的全量用户 = 存活率
  select 
          round(count(l2.user_id)*1.0/count(t.user_id),3) as p
  
  from 
         (select l1.user_id,min(l1.date) as d1 
          from login l1 
          group by l1.user_id) as t
  
  left join login l2 
  on t.user_id=l2.user_id and l2.date=date_add(d1, interval 1 day)
  
  
  -- 第二种写法(低效)
  -- 子查询:     提取user_id和最小的日期+1天, 得出(仅含: 有效用户)
  -- 内联查询:   根据user_id和最小的日期+1天, 得出(有效用户数量)
  -- 去重计数:   count(distinct user_id), 得出(去重后的所有用户)
  -- 计算存活率: 有效用户 / 去重后的所有用户 = 存活率
  select round(((select count(*)
                 from `login` as l 
                 inner join (select `user_id`, DATE_ADD(min(`date`), interval 1 day) as `date`
                             from `login` group by `user_id`) as sub_l
                 on l.`user_id` = sub_l.`user_id` and l.`date` = sub_l.`date`) / count(distinct user_id)), 3)
  from `login`;
  ```
  
  



&nbsp;  
&nbsp;  
### SQL69

- 题目   
  牛客每个人最近的登录日期(四)
  
- [题链接](https://www.nowcoder.com/practice/e524dc7450234395aa21c75303a42b0a?tpId=82&&tqId=35087&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法
  select
          -- 5. count将多行压缩成1行显示,
          --    当 u_c.user_id 的值存在时, 将多行压缩成1行.
          --    当 u_c.user_id 的值为空时, 计为0. 
          l_d.`date`, count(u_c.user_id) 
  from 
         -- 1. 获取去重后的日期的数据集合
         (select `date` 
          from `login` 
          group by `date`) as l_d
  
  -- 2. 左联要求即便不匹配数据, 主表l_d的数据也要列出来. 
  left join
   
         -- 3. 获取最小日期的数据, 即: 新用户数据的数据集合
         (select `user_id`, min(`date`) as date 
          from `login` 
          group by `user_id`) as u_c
  on 
          -- 4. 两个数据集的日期相同匹配, 
          --    当日期满足匹配的数据, 会纵向排列(成多行).
          --    当日期不满足匹配的数据, 会仅展示主表的数据, 联结表的数据为空.
          l_d.`date` = u_c.`date`
  
  group by l_d.`date`
  order by l_d.`date`;
  
  
  
  -- 第二种写法
  select
          -- 6. 补充处理空统计的情况. 
          login.date, ifnull(count,0) 
  from login 
  
  -- 3. 左联要求即便不匹配数据, 主表l_d的数据也要列出来. 
  left join
  
          -- 2. 统计新用户数据集合的数量: 日期, 数量
         (select t1.d,count(user_id) count 
          from 
  		          -- 1. 获取最小日期的数据, 即: 新用户数据的数据集合
  		         (select l.user_id,min(date) d 
				  from login l 
				  group by l.user_id) t1
          group by t1.d) t2
  
  -- 4. 有数据的项与主表联结,
  --    由于 t2 已经去重, 已经统计, 
  --    所以这里不会出现纵向排列的情况
  on login.date=t2.d
  
  -- 5. 获取去重后的日期的数据集合
  group by login.date;
  ```  



&nbsp;  
&nbsp;  
### SQL70

- 题目   
  牛客每个人最近的登录日期(五)
  
- [题链接](https://www.nowcoder.com/practice/ea0c56cd700344b590182aad03cc61b8?tpId=82&&tqId=35088&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 3. 筛选出有效的: 日期, 新用户次日留存率
  select 
          l_1.`date`, round((count(l_2.`user_id`) / count(l_1.`user_id`)), 3) as p 
  from 
          -- 1. 新用户, 日期
         (select `user_id`,min(`date`) as `date`
          from `login` 
          group by `user_id`) as l_1
  left join 
         `login` as l_2
  on 
          -- 2. 筛选出 l_2 中, 新用户的次日留存用户, 有效用户.
          l_1.`user_id`=l_2.`user_id` and 
          l_2.`date`=date_add(l_1.`date`, interval 1 day)
  group by l_1.`date`
  
  
  union
  
  
  select 
          date, 0.000 as p
  from 
         `login`
  where 
          -- 4. 筛选出哪些没有新用户的日期
          -- 子查询: 得出去重后的新用户,
          -- not in: 得出这一天没有新的用户.
         `date` not in (select min(`date`) 
                        from `login` 
                        group by `user_id`)
  order by `date`;

  ```  


&nbsp;  
&nbsp;  
### SQL71

- 题目   
  牛客每个人最近的登录日期(六)
  
- [题链接](https://www.nowcoder.com/practice/572a027e52804c058e1f8b0c5e8a65b4?tpId=82&&tqId=35089&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select u.`name`, 
         pn.`date`,
         -- 按名字分组(类似 group by), 然后再排序递增. 
         sum(pn.`number`) over (partition by u.`name` order by pn.`date`)
  from `user` as u 
  inner join `passing_number` as pn on u.`id` = pn.`user_id`
  order by pn.`date`, u.`name`;

  ```  


&nbsp;  
&nbsp;  
### SQL72

- 题目   
  考试分数(一)
  
- [题链接](https://www.nowcoder.com/practice/f41b94b4efce4b76b27dd36433abe398?tpId=82&&tqId=35492&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select `job`, 
          round(avg(`score`), 3) as avg_score 
  from `grade` 
  group by `job` 
  order by avg_score desc;
  ```  

&nbsp;  
&nbsp;  
### SQL73

- 题目   
  考试分数(二)
  
- [题链接](https://www.nowcoder.com/practice/f456dedf88a64f169aadd648491a27c1?tpId=82&&tqId=35493&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select g.`id`, g.`job`, g.`score` 
  from `grade` as g
  inner join 
          (select `job`, 
                   round(avg(`score`), 3) as avg_score 
           from `grade` 
           group by `job`) as avg_grade
  on g.`job` = avg_grade.`job` and g.`score` > avg_grade.`avg_score`;
  ```  

&nbsp;  
&nbsp;  
### SQL74

- 题目   
  考试分数(三)
  
- [题链接](https://www.nowcoder.com/practice/b83f8b0e7e934d95a56c24f047260d91?tpId=82&&tqId=35494&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select a.`user_id`, a.`language_name`, a.`score` from 
          (select g.`id` as user_id,
                  l.`id` as language_id,
                  l.`name` as language_name,
                  g.`score` as score,
  			          dense_rank() over (partition by l.`name` order by g.`score` desc) as d_rank
           from `grade` as g
           inner join `language` as l on g.`language_id` = l.`id`) as a
  where a.`d_rank` <= 2
  order by a.`language_name` asc, a.`score` desc, a.`user_id`;
  ```  

&nbsp;  
&nbsp;  
### SQL75

- 题目   
  考试分数(四)
  
- [题链接](https://www.nowcoder.com/practice/502fb6e2b1ad4e56aa2e0dd90c6edf3c?tpId=82&&tqId=35495&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select 
          `job`, 
  
          case (count(job) % 2)
              when 1 then                              -- 奇数
                  round((count(job) + 1) / 2, 0)
              else                                     -- 偶数
                  round(count(job) / 2, 0)
          end as `start`,
  			 
          case (count(job) % 2)
              when 1 then 
                  round((count(job) + 1) / 2, 0)
              else 
                  round((count(job) / 2) + 1, 0)
          end as `end`
  from `grade` 
  group by `job`
  order by `job`;
  ```  

&nbsp;  
&nbsp;  
### SQL76

- 题目   
  考试分数(五)
  
- [题链接](https://www.nowcoder.com/practice/b626ff9e2ad04789954c2132c74c0512?tpId=82&&tqId=35496&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  -- 第一种写法
  select 
          id,job,score,rank_ 
  from 
         (select *,
                 -- 得出分组排名数据
                 rank()over(partition by job order by score desc)as rank_,
                 -- 得出分组计数
                 count(*)over(partition by job) as total 
          from grade) as A
  where 
          -- 筛选符合中位数选项
          -- c++ 数据视角, 列出数据分布
          -- select round(abs(1-(3+1)/2)*1.0,2) == 1.00
          -- select round(abs(2-(3+1)/2)*1.0,2) == 0.00
          -- select round(abs(3-(3+1)/2)*1.0,2) == 1.00
          -- select round(abs(4-(3+1)/2)*1.0,2) == 2.00
          -- select round(abs(5-(3+1)/2)*1.0,2) == 3.00
          -- java 数据视角, 列出数据分布
          -- select round(abs(1-(2+1)/2)*1.0,2) == 0.50
          -- select round(abs(2-(2+1)/2)*1.0,2) == 0.50
          round(abs(rank_-(total+1)/2)*1.0,2)<1
  order by 
          id
  
  
  
  -- 第二种写法
  select   a.`id`, 
           a.`job`, 
           a.`score`, 
           a.`t_rank` 
  from 
          (select g_1.`id`, 
           g_1.`job`, 
           g_1.`score`, 
           g_1.`t_rank`, 
           g_2.`start`, 
           g_2.`end`, 
  
           -- 3. 得出索引位置
           row_number() over(partition by g_1.`job` order by g_1.`score`) as enum 
           from 
                      -- 2. 得出 所有字段 + t_rank(分组排名信息)
                      (select *, dense_rank() over(partition by `job` order by `score` desc) as t_rank 
                       from `grade`) as g_1
           inner join 
                      -- 1. 得出 job, start, end
                      (select 
                               `job`, 
          
                                case (count(job) % 2)
                                when 1 then                              -- 奇数
                                    round((count(job) + 1) / 2, 0)
                                else                                     -- 偶数
                                    round(count(job) / 2, 0)
                                end as `start`,
          			 
                                case (count(job) % 2)
                                when 1 then 
                                    round((count(job) + 1) / 2, 0)
                                else 
                                    round((count(job) / 2) + 1, 0)
                                end as `end`
                       from `grade` 
                       group by `job`
                       order by `job`) as g_2 
           on g_1.`job` = g_2.`job`) as a
  where 
           -- 4. 列出符合索引的数据
           a.`enum` in (a.`start`, a.`end`)
  order by 
           -- 5. 按照 `id` 排序
           a.`id`;
  ```  


&nbsp;  
&nbsp;  
### SQL77

- 题目   
  牛客的课程订单分析(一)
  
- [题链接](https://www.nowcoder.com/practice/d3aa5df807f046bea5003dbc04965d67?tpId=82&&tqId=37915&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select * 
  from  `order_info` 
  where `status`='completed' and 
         date>'2025-10-15' and 
         product_name in ('C++', 'Java', 'Python')
  ```  


&nbsp;  
&nbsp;  
### SQL78

- 题目   
  牛客的课程订单分析(二)
  
- [题链接](https://www.nowcoder.com/practice/4ca4137cb490420cad06d2147ae67456?tpId=82&&tqId=37916&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select `user_id`
  from  `order_info` 
  where `status`='completed' and 
         `date`>'2025-10-15' and 
         `product_name` in ('C++', 'Java', 'Python') 
  group by `user_id` 
  having count(`user_id`) >= 2
  order by `user_id`;
  ```  


&nbsp;  
&nbsp;  
### SQL79

- 题目   
  牛客的课程订单分析(三)
  
- [题链接](https://www.nowcoder.com/practice/4ae8cff2505f4d7cb68fb0ec7cf80c57?tpId=82&&tqId=37917&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select id,user_id,product_name,status,client_id,date 
  from
          (select *,count(id) over(partition by user_id) as counted     -- 将 `group by` 和 `having` 替换成 count over. 
           from order_info
           where status='completed' and date > '2025-10-15' and 
                 product_name in ('C++','Java','Python') ) oi          
  where oi.counted >= 2                                                 -- 将可判断条件(>= 2), 移交到外部来落地.
  order by id
  ```  


&nbsp;  
&nbsp;  
### SQL80

- 题目   
  牛客的课程订单分析(四)
  
- [题链接](https://www.nowcoder.com/practice/c93d2079282f4943a3771ca6fd081c23?tpId=82&&tqId=37918&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select `user_id`, 
          min(`date`), 
          count(`user_id`) 
  from   `order_info` 
  where  `status`='completed' and 
         `date`>'2025-10-15' and 
         `product_name` in ('C++', 'Java', 'Python') 
  group by `user_id` 
  having count(`user_id`) >= 2
  order by `user_id`;
  ```  


&nbsp;  
&nbsp;  
### SQL81

- 题目   
  牛客的课程订单分析(五)
  
- [题链接](https://www.nowcoder.com/practice/348afda488554ceb922efd2f3effc427?tpId=82&&tqId=37919&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

- SQL  
  ```shell
  select  oi.`user_id`, 
          min(oi.`date`) as first_buy_date,
          oi.`next_date` as second_buy_date, 
          count(oi.`user_id`) as cnt
  from   
         (select  *,
                  -- 增加一个字段: 获取当前字段行的跟随行, 1表示当前字段行的下一个行值.
                  lead(`date`, 1) over (partition by `user_id` order by `date` ASC)as next_date
          from   `order_info`
          where  `product_name` in ('C++','Python','Java') and 
                 `status` = 'completed'  and 
                 `date` > '2025-10-15') as oi
  group by oi.`user_id` 
  having count(oi.`user_id`)>=2
  order by oi.`user_id` ASC;

  ```  
