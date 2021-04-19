from django.db import models


# CREATE TABLE `salaries` (
#   `emp_no` int(11) NOT NULL,
#   `salary` int(11) NOT NULL,
#   `from_date` date NOT NULL,
#   `to_date` date NOT NULL,
#   PRIMARY KEY (`emp_no`,`from_date`)          # Django 无法简历复合主键, 由于查询需要用到 emp_no,
# );                                            # 而 emp_no 有重复数据, 因此不能用它来做主键, 所以下面采用复合索引办法.
class salaries(models.Model):

    emp_no = models.IntegerField(verbose_name="员工编号", null=False)
    salary = models.IntegerField(verbose_name="薪资", null=False)
    from_date = models.DateField(verbose_name="from_date", null=False)
    to_date = models.DateField(verbose_name="to_date", null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['emp_no', 'from_date'], name="sql7_uc_emp_no_from_date"), ]
