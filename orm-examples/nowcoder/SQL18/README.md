[题链接](https://www.nowcoder.com/practice/c1472daba75d4635b7f8540b837cc719?tpId=82&&tqId=29770&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

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