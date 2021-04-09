[题链接](https://www.nowcoder.com/practice/dbfafafb2ee2482aa390645abd4463bf?tpId=82&&tqId=29757&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)


```shell
# 以employees为主表连接查询dept_no表.
select employees.last_name, 
       employees.first_name, 
       dept_emp.dept_no 
from employees 
left join dept_emp on employees.emp_no=dept_emp.emp_no;
```