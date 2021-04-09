from django.db import models


# 1. Django不支持符合主键(Composite Primary Key).
# 2. Django不支持关闭主键(Disable Primary Key),
#   当表中的所有字段都没有定义 Primary Key 时,
#   Django会自动增加一个id字段, 并将primary key设定到id字段上.
#
#
# 一般情况下, InnoDB在建表时, 当没有定义Primary Key时,
# 如果有 Unique Key 时, InnoDB会将该Unique Key当作聚集索引.
# 如果也没有 Unique Key时, InnoDB会创建一个隐藏的PrimaryKey(聚集索引).
#
#
# 所以, 像这样的建表语句, Model无法百分之百还原.
# CREATE TABLE `salaries` (
#   `emp_no` int(11) NOT NULL,
#   `salary` int(11) NOT NULL,
#   `from_date` date NOT NULL,
#   `to_date` date NOT NULL,
#   PRIMARY KEY (`emp_no`,`from_date`)
# );
class salaries(models.Model):
    """
    CREATE TABLE `SQL3_dept_manager` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `dept_no` varchar(4) NOT NULL,
        `emp_no` integer NOT NULL,
        `to_date` date NOT NULL
    );
    ALTER TABLE `SQL3_salaries` ADD CONSTRAINT `uc_emp_no_from_date` UNIQUE (`emp_no`, `from_date`);
    """

    emp_no = models.IntegerField(verbose_name="员工编号", null=False)
    salary = models.IntegerField(verbose_name="薪资", null=False)
    from_date = models.DateField(verbose_name="from_date", null=False)
    to_date = models.DateField(verbose_name="to_date", null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['emp_no', 'from_date'], name="uc_emp_no_from_date"), ]


class dept_manager(models.Model):
    """
    CREATE TABLE `SQL3_salaries` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `emp_no` integer NOT NULL,
        `salary` integer NOT NULL,
        `from_date` date NOT NULL,
        `to_date` date NOT NULL
    );
    ALTER TABLE `SQL3_dept_manager` ADD CONSTRAINT `uc_emp_no_dept_no` UNIQUE (`emp_no`, `dept_no`);
    """

    dept_no = models.CharField(verbose_name="部门编号", max_length=4, null=False)
    emp_no = models.IntegerField(verbose_name="员工编号", null=False)
    to_date = models.DateField(verbose_name="to_date", null=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['emp_no', 'dept_no'], name="uc_emp_no_dept_no"), ]
