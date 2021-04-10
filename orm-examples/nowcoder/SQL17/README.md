[题链接](https://www.nowcoder.com/practice/8d2c290cc4e24403b98ca82ce45d04db?tpId=82&&tqId=29769&rp=1&ru=/activity/oj&qru=/ta/sql/question-ranking)

```shell

select emp_no, salary 
from salaries 
order by salary desc 
limit 1 offset 1
```