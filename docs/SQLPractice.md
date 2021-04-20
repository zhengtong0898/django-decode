### 牛客网
| 题号 | 题目 | 关键词 |
| :---: | :---: | ---: |
|SQL1|[查找最晚入职员工的所有信息](../examples/nowcoder/README.md#SQL1)| 嵌套, extra, subquery |
|SQL2|[查找入职员工时间排名倒数第三的员工所有信息](../examples/nowcoder/README.md#SQL2)| limit offset |
|SQL3|[查找各个部门当前领导当前薪水详情以及其对应部门编号dept_no](../examples/nowcoder/README.md#SQL3)| left join |
|SQL4|[查找所有已经分配部门的员工的last_name和first_name](../examples/nowcoder/README.md#SQL4)| left join |
|SQL5|[查找所有员工的last_name和first_name以及对应部门编号dept_no](../examples/nowcoder/README.md#SQL5)| left join |
|SQL7|[查找薪水涨幅超过15次的员工号emp_no以及其对应的涨幅次数t](../examples/nowcoder/README.md#SQL7)| `group by`, `having`, `count` |
|SQL8|[找出所有员工当前具体的薪水salary情况](../examples/nowcoder/README.md#SQL8)| `group by`, `order by` |
|SQL10|[获取所有非manager的员工emp_no](../examples/nowcoder/README.md#SQL10)| `left join` |
|SQL11|[获取所有员工当前的manager](../examples/nowcoder/README.md#SQL11)| `left join`, `<>` |
|SQL12|[获取所有部门中当前员工薪水最高的相关信息](../examples/nowcoder/README.md#SQL12)| `left join`, `inner join`, `生成临时表` |
|SQL15|[查找employees表所有emp_no为奇数](../examples/nowcoder/README.md#SQL15)| `mod取余求奇偶` |
|SQL16|[统计出当前各个title类型对应的员工当前薪水对应的平均工资](../examples/nowcoder/README.md#SQL16)| `avg`, `group by`, `inner join` |
|SQL17|[获取当前薪水第二多的员工的emp_no以及其对应的薪水salary](../examples/nowcoder/README.md#SQL17)| `limit`, `offset` |
|SQL18|[查找当前薪水排名第二多的员工编号emp_no](../examples/nowcoder/README.md#SQL18)| `subquery`, `subquery`, `subquery` |
|SQL19|[查找所有员工的last_name和first_name以及对应的dept_name](../examples/nowcoder/README.md#SQL19)| `left join`, `left join`, `left join` |
|SQL21|[查找所有员工自入职以来的薪水涨幅情况](../examples/nowcoder/README.md#SQL21)| - |
|SQL22|[统计各个部门的工资记录数](../examples/nowcoder/README.md#SQL22)| - |
|SQL23|[对所有员工的当前薪水按照salary进行按照1-N的排名](../examples/nowcoder/README.md#SQL23)| `subquery`, `dense_rank`, `distinct`, `count` |
|SQL24|[获取所有非manager员工当前的薪水情况](../examples/nowcoder/README.md#SQL24)| `subquery`, `inner join`, `不能用left join` |
|SQL25|[获取员工其当前的薪水比其manager当前薪水还高的相关信息](../examples/nowcoder/README.md#SQL25)|  |
|SQL26|[汇总各个部门当前员工的title类型的分配数目](../examples/nowcoder/README.md#SQL26)| `group by 多字段联合分组` |
|SQL28|[查找描述信息中包括robot的电影对应的分类名称以及电影数目](../examples/nowcoder/README.md#SQL28)| `having count` |
|SQL29|[使用join查询方式找出没有分类的电影id以及名称](../examples/nowcoder/README.md#SQL29)| `强调 left join 的必要性` |
|SQL30|[使用子查询的方式找出属于Action分类的所有电影对应的title,description](../examples/nowcoder/README.md#SQL30)| `subquery` |
|SQL32|[将employees表的所有员工的last_name和first_name拼接起来作为Name，中间以一个空格区分](../examples/nowcoder/README.md#SQL32)| `concat字符串拼接` |
|SQL33|[创建一个actor表，包含如下列信息](../examples/nowcoder/README.md#SQL33)| `create table` |
|SQL34|[批量插入数据](../examples/nowcoder/README.md#SQL34)| `insert into` |
|SQL35|[批量插入数据,如果数据已经存在，请忽略，不使用replace操作](../examples/nowcoder/README.md#SQL35)| `insert into select` |
|SQL36|[创建一个actor_name表，将actor表中的所有first_name以及last_name导入改表](../examples/nowcoder/README.md#SQL36)|  |
|SQL37|[对first_name创建唯一索引uniq_idx_firstname，对last_name创建普通索引idx_lastname](../examples/nowcoder/README.md#SQL37)| `alter table add unique index`  |
|SQL38|[针对actor表创建视图actor_name_view](../examples/nowcoder/README.md#SQL38)| `create view` |
|SQL39|[针对上面的salaries表emp_no字段创建索引idx_emp_no，查询emp_no为10005,](../examples/nowcoder/README.md#SQL39)| `force index` |
|SQL40|[在last_update后面新增加一列名字为create_date](../examples/nowcoder/README.md#SQL40)| `alter table add column` |
|SQL41|[构造一个触发器audit_log，在向employees表中插入一条数据的时候，触发插入相关的数据到audit中](../examples/nowcoder/README.md#SQL41)| `create trigger` |
|SQL42|[删除emp_no重复的记录，只保留最小的id对应的记录。](../examples/nowcoder/README.md#SQL42)| `delete from`, `回避iterator问题` |
|SQL43|[将所有to_date为9999-01-01的全部更新为NULL,且](../examples/nowcoder/README.md#SQL43)| `update` |
|SQL44|[将id=5以及emp_no=10001的行数据替换成id=5以及emp_no=10005,其他数据保持不变，使用replace实现。](../examples/nowcoder/README.md#SQL44)| `replace into` |
|SQL45|[将titles_test表名修改为titles_2017](../examples/nowcoder/README.md#SQL45)| `rename table` `表重命名` |
|SQL46|[在audit表上创建外键约束，其emp_no对应employees_test表的主键id](../examples/nowcoder/README.md#SQL46)| `alter table add foreign key` |
|SQL48|[将所有获取奖金的员工当前的薪水增加10%](../examples/nowcoder/README.md#SQL48)| `salary * percentage` |
|SQL50|[将employees表中的所有员工的last_name和first_name通过(')连接起来。](../examples/nowcoder/README.md#SQL50)|  |
|SQL51|[查找字符串'10,A,B'](../examples/nowcoder/README.md#SQL51)| `relace` `length` `计数` |
|SQL52|[获取Employees中的first_name，查询按照first_name最后两个字母，按照升序进行排列](../examples/nowcoder/README.md#SQL52)| `order by` `substr` |
|SQL53|[按照dept_no进行汇总，属于同一个部门的emp_no按照逗号进行连接，结果给出dept_no以及连接出的结果employees](../examples/nowcoder/README.md#SQL53)| `group by` `group_concat`|
|SQL54|[查找排除当前最大、最小salary之后的员工的平均工资avg_salary](../examples/nowcoder/README.md#SQL54)| `sum` `max` `min` `count` |
|SQL55|[分页查询employees表，每5行一页，返回第2页的数据](../examples/nowcoder/README.md#SQL55)| `limit` `offset` |
|SQL57|[使用含有关键字exists查找未分配具体部门的员工的所有信息。](../examples/nowcoder/README.md#SQL57)| `not exists` |
|SQL59|[获取有奖金的员工相关信息。](../examples/nowcoder/README.md#SQL59)| `CASE WHEN` |
|SQL60|[统计salary的累计和running_total](../examples/nowcoder/README.md#SQL60)| `set @variable` `sum over` |
|SQL61|[对于employees表中，给出奇数行的first_name](../examples/nowcoder/README.md#SQL61)| `row_number over` `rank % 2 求奇` |
|SQL62|[出现三次以上相同积分的情况](../examples/nowcoder/README.md#SQL62)| `group by` `having` |
|SQL63|[刷题通过的题目排名](../examples/nowcoder/README.md#SQL63)| `dense_rank` `order by col_1, col_2` |
|SQL64|[找到每个人的任务](../examples/nowcoder/README.md#SQL64)| `left join` |
|SQL65|[异常的邮件概率](../examples/nowcoder/README.md#SQL65)| `round` `sum` `if` `case when` `count`  |
|SQL66|[牛客每个人最近的登录日期(一)](../examples/nowcoder/README.md#SQL66)| `group by` `max`  |
|SQL67|[牛客每个人最近的登录日期(二)](../examples/nowcoder/README.md#SQL67)| `subquery` `left join` `inner join` |
|SQL68|[牛客每个人最近的登录日期(三)](../examples/nowcoder/README.md#SQL68)| `round` `date_add` `subquery` `left join` |
|SQL69|[牛客每个人最近的登录日期(四)](../examples/nowcoder/README.md#SQL69)| `subquery` `left join` `group by` |
|SQL70|[牛客每个人最近的登录日期(五)](../examples/nowcoder/README.md#SQL70)| `union` `subquery` `left join` `group by` |
|SQL71|[牛客每个人最近的登录日期(六)](../examples/nowcoder/README.md#SQL71)| `sum() over(partition by xx order by xx)` |
|SQL72|[考试分数(一)](../examples/nowcoder/README.md#SQL72)| `group by` `order by xx desc` `round` `avg` |
|SQL73|[考试分数(二)](../examples/nowcoder/README.md#SQL73)| `group by` `order by xx desc` `round` `avg` `inner join` |
|SQL74|[考试分数(三)](../examples/nowcoder/README.md#SQL74)| `subquery` `dense_rank over(partition by xx order by xx)` `inner join` |
|SQL75|[考试分数(四)](../examples/nowcoder/README.md#SQL75)| `case when` |
|SQL76|[考试分数(五)](../examples/nowcoder/README.md#SQL76)| `rank() over(partition by xx order by xx)` `dense_rank() over(partition by xx order by xx)` `row_number() over(partition by xx order by xx)` `subquery` `inner join` |
|SQL77|[牛客的课程订单分析(一)](../examples/nowcoder/README.md#SQL77)|  |
|SQL78|[牛客的课程订单分析(二)](../examples/nowcoder/README.md#SQL78)| `group by` `having` |
|SQL79|[牛客的课程订单分析(三)](../examples/nowcoder/README.md#SQL79)| `subquery` `count over` |
|SQL80|[牛客的课程订单分析(四)](../examples/nowcoder/README.md#SQL80)| `min` `count` `group by` `having` |
|SQL81|[牛客的课程订单分析(五)](../examples/nowcoder/README.md#SQL81)| `lead() over()` `subquery` `group by` `having` `order by` |
|SQL82|[牛客的课程订单分析(六)](../examples/nowcoder/README.md#SQL82)| `subquery` `count() over()` `left join` `order by` |
|SQL83|[牛客的课程订单分析(七)](../examples/nowcoder/README.md#SQL83)| `subquery` `count() over()` `left join` `order by` `group by` |
|SQL84|[实习广场投递简历分析(一)](../examples/nowcoder/README.md#SQL84)| `like` `sum` `group by` `order by` |
|SQL85|[实习广场投递简历分析(二)](../examples/nowcoder/README.md#SQL85)| `subquery` `date_format` `group by` `order by` |
|SQL86|[实习广场投递简历分析(三)](../examples/nowcoder/README.md#SQL86)| `subquery` `date_format` `date_add` `group by` `order by` |
|SQL87|[最差是第几名(一)](../examples/nowcoder/README.md#SQL87)| `sum() over()` |
|SQL88|[最差是第几名(二)](../examples/nowcoder/README.md#SQL88)| `subquery` `lag() over()` `case when` |
|SQL89|[获得积分最多的人(一)](../examples/nowcoder/README.md#SQL89)| `inner join` `group by` `order by` `sum` |
|SQL90|[获得积分最多的人(二)](../examples/nowcoder/README.md#SQL90)| `inner join` `group by` `order by` `sum` `dense_rank() over()` |
|SQL91|[获得积分最多的人(三)](../examples/nowcoder/README.md#SQL91)| `inner join` `group by` `order by` `sum` `dense_rank() over()` `with as` |





&nbsp;  
&nbsp;   
### 力扣
| 属性 | 描述 |
|---| :---: |
|||