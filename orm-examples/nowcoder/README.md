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