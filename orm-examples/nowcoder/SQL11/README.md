[题链接](https://www.nowcoder.com/practice/e50d92b8673a440ebdf3a517b5b37d62?tpId=82&&tqId=29763&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell

select e.emp_no as emp_no, 
       m.emp_no as manager 
from dept_manager as m
left join dept_emp as e 
on m.dept_no=e.dept_no
where m.emp_no <> e.emp_no;
```
