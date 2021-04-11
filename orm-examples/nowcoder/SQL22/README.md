[题链接](https://www.nowcoder.com/practice/6a62b6c0a7324350a6d9959fa7c21db3?tpId=82&&tqId=29774&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

```shell

select d.dept_no, d.dept_name, count(de.emp_no) 
from dept_emp as de
inner join departments as d on de.dept_no = d.dept_no
inner join salaries as s on de.emp_no = s.emp_no 
group by d.dept_no
order by d.dept_no;
```