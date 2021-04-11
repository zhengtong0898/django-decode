[题链接](https://www.nowcoder.com/practice/fc7344ece7294b9e98401826b94c6ea5?tpId=82&&tqId=29773&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

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