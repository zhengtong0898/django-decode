[题链接](https://www.nowcoder.com/practice/4a052e3e1df5435880d4353eb18a91c6?tpId=82&&tqId=29764&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

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