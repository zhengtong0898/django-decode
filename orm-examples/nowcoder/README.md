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
