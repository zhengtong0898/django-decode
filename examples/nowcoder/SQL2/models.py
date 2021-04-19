from django.db import models


# 该模型在执行migrate时, 会转换成一条建表语句
# CREATE TABLE `sql1_employees` (
#   `emp_no` int(11) NOT NULL,
#   `birth_date` date NOT NULL,
#   `first_name` varchar(14) NOT NULL,
#   `last_name` varchar(16) NOT NULL,
#   `gender` varchar(1) NOT NULL,
#   `hire_date` date NOT NULL,
#   PRIMARY KEY (`emp_no`)                          # 聚集索引
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
class employees(models.Model):

    emp_no = models.IntegerField(verbose_name="员工", null=False, primary_key=True)
    birth_date = models.DateField(verbose_name="生日日期", null=False)
    first_name = models.CharField(verbose_name="姓氏", max_length=14, null=False)
    last_name = models.CharField(verbose_name="名字", max_length=16, null=False)
    gender = models.CharField(verbose_name="性别", max_length=1, null=False)
    hire_date = models.DateField(verbose_name="入职日期", null=False)
