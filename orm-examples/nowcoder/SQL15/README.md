[题链接](https://www.nowcoder.com/practice/a32669eb1d1740e785f105fa22741d5c?tpId=82&&tqId=29767&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell

select * 
from employees 
where last_name<>'Mary' and 
      mod(emp_no, 2)=1 
order by hire_date desc;
```