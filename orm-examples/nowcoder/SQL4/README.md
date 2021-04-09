[题链接](https://www.nowcoder.com/practice/6d35b1cd593545ab985a68cd86f28671?tpId=82&&tqId=29756&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell
# 以dept_emp为主表连接查询employees表.

select employees.last_name as last_name, 
       employees.first_name as first_name, 
       dept_emp.dept_no as dept_no 
from dept_emp left join employees on (dept_emp.emp_no=employees.emp_no)
```