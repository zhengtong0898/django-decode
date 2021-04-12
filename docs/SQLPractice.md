### 牛客网
| 题号 | 题目 | 关键词 |
| :---: | :---: | ---: |
|SQL1|[查找最晚入职员工的所有信息](../orm-examples/nowcoder/SQL1/tests.py#L10)| 嵌套, extra, subquery |
|SQL2|[查找入职员工时间排名倒数第三的员工所有信息](../orm-examples/nowcoder/SQL2/tests.py#L10)| limit offset |
|SQL3|[查找各个部门当前领导当前薪水详情以及其对应部门编号dept_no](../orm-examples/nowcoder/SQL3/tests.py#L8)| left join |
|SQL4|[查找所有已经分配部门的员工的last_name和first_name](../orm-examples/nowcoder/SQL4/README.md)| left join |
|SQL5|[查找所有员工的last_name和first_name以及对应部门编号dept_no](../orm-examples/nowcoder/SQL5/README.md)| left join |
|SQL7|[查找薪水涨幅超过15次的员工号emp_no以及其对应的涨幅次数t](../orm-examples/nowcoder/SQL7/tests.py#L10)| `group by`, `having`, `count` |
|SQL8|[找出所有员工当前具体的薪水salary情况](../orm-examples/nowcoder/SQL8/README.md)| `group by`, `order by` |
|SQL10|[获取所有非manager的员工emp_no](../orm-examples/nowcoder/SQL10/README.md)| `left join` |
|SQL11|[获取所有员工当前的manager](../orm-examples/nowcoder/SQL11/README.md)| `left join`, `<>` |
|SQL12|[获取所有部门中当前员工薪水最高的相关信息](../orm-examples/nowcoder/SQL12/README.md)| `left join`, `inner join`, `生成临时表` |
|SQL15|[查找employees表所有emp_no为奇数](../orm-examples/nowcoder/SQL15/README.md)| `mod取余求奇偶` |
|SQL16|[统计出当前各个title类型对应的员工当前薪水对应的平均工资](../orm-examples/nowcoder/SQL16/README.md)| `avg`, `group by`, `inner join` |
|SQL17|[获取当前薪水第二多的员工的emp_no以及其对应的薪水salary](../orm-examples/nowcoder/SQL17/README.md)| `limit`, `offset` |
|SQL18|[查找当前薪水排名第二多的员工编号emp_no](../orm-examples/nowcoder/SQL18/README.md)| `subquery`, `subquery`, `subquery` |
|SQL19|[查找所有员工的last_name和first_name以及对应的dept_name](../orm-examples/nowcoder/SQL19/README.md)| `left join`, `left join`, `left join` |
|SQL21|[查找所有员工自入职以来的薪水涨幅情况](../orm-examples/nowcoder/SQL21/README.md)| - |
|SQL22|[统计各个部门的工资记录数](../orm-examples/nowcoder/SQL22/README.md)| - |
|SQL23|[对所有员工的当前薪水按照salary进行按照1-N的排名](../orm-examples/nowcoder/SQL23/README.md)| `subquery`, `dense_rank`, `distinct`, `count` |
|SQL24|[获取所有非manager员工当前的薪水情况](../orm-examples/nowcoder/README.md#SQL24)| `subquery`, `inner join`, `不能用left join` |
|SQL25|[获取员工其当前的薪水比其manager当前薪水还高的相关信息](../orm-examples/nowcoder/README.md#SQL25)|  |
|SQL26|[汇总各个部门当前员工的title类型的分配数目](../orm-examples/nowcoder/README.md#SQL26)| `group by 多字段联合分组` |
|SQL28|[查找描述信息中包括robot的电影对应的分类名称以及电影数目](../orm-examples/nowcoder/README.md#SQL28)| `having count` |
|SQL29|[使用join查询方式找出没有分类的电影id以及名称](../orm-examples/nowcoder/README.md#SQL29)| `强调 left join 的必要性` |
|SQL30|[使用子查询的方式找出属于Action分类的所有电影对应的title,description](../orm-examples/nowcoder/README.md#SQL30)| `subquery` |
|SQL32|[将employees表的所有员工的last_name和first_name拼接起来作为Name，中间以一个空格区分](../orm-examples/nowcoder/README.md#SQL32)| `concat字符串拼接` |
|SQL33|[创建一个actor表，包含如下列信息](../orm-examples/nowcoder/README.md#SQL33)| `create table` |
|SQL34|[批量插入数据](../orm-examples/nowcoder/README.md#SQL34)| `insert into` |
|SQL35|[批量插入数据,如果数据已经存在，请忽略，不使用replace操作](../orm-examples/nowcoder/README.md#SQL35)| `insert into select` |
|SQL36|[创建一个actor_name表，将actor表中的所有first_name以及last_name导入改表](../orm-examples/nowcoder/README.md#SQL36)|  |
|SQL37|[对first_name创建唯一索引uniq_idx_firstname，对last_name创建普通索引idx_lastname](../orm-examples/nowcoder/README.md#SQL37)| `alter table add unique index`  |
|SQL38|[针对actor表创建视图actor_name_view](../orm-examples/nowcoder/README.md#SQL38)| `create view` |
|SQL39|[针对上面的salaries表emp_no字段创建索引idx_emp_no，查询emp_no为10005,](../orm-examples/nowcoder/README.md#SQL39)| `force index` |
|SQL40|[在last_update后面新增加一列名字为create_date](../orm-examples/nowcoder/README.md#SQL40)| `alter table add column` |




&nbsp;  
&nbsp;   
### 力扣
| 属性 | 描述 |
|---| :---: |
|||