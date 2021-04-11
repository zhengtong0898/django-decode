[题链接](https://www.nowcoder.com/practice/b9068bfe5df74276bd015b9729eec4bf?tpId=82&&tqId=29775&rp=1&ru=/ta/sql&qru=/ta/sql/question-ranking)

```shell

# 第一种写法
select emp_no, 
       salary, 
       dense_rank() over (order by salary desc) as t_rank 
from salaries;


# 第二种写法
# 1. 外层 s 由于使用了 order by s.salary desc, 所以每次迭代都会pop集合中最大的元素.
# 2. 子查询 sub_s 做 >= 比较每次迭代最大的值, 即: 大于最大的数, 去重, 有几个数就是排名第几.
#    第一次迭代: sub_s >= (s.salary 最大数), 去重 + count == 1
#    第二次迭代: sub_s >= (s.salary 第二大数), 去重 + count == 2  
select emp_no,
       salary,
       (select count(distinct salary) 
        from salaries sub_s
        where sub_s.salary>=s.salary) as rank 	
from salaries s 
order by s.salary desc;
```