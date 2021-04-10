[题链接](https://www.nowcoder.com/practice/c8652e9e5a354b879e2a244200f1eaae?tpId=82&&tqId=29768&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell

select t.title, AVG(s.salary) as avg_salary
from titles as t 
inner join salaries as s
on t.emp_no = s.emp_no
group by t.title
order by avg_salary
```