from datetime import date
from django.db import connections
from django.test import TestCase, TransactionTestCase
from .models import salaries, dept_manager


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def prepare_data(self):
        # 建表语句
        # CREATE TABLE `sql3_dept_manager` (
        # 	`id` INT ( 11 ) NOT NULL AUTO_INCREMENT,
        # 	`dept_no` VARCHAR ( 4 ) NOT NULL,
        # 	`emp_no` INT ( 11 ) NOT NULL,
        # 	`to_date` date NOT NULL,
        # 	PRIMARY KEY ( `id` ),
        #   UNIQUE KEY `uc_emp_no_dept_no` ( `emp_no`, `dept_no` )
        # ) ENGINE = INNODB DEFAULT CHARSET = utf8mb4;
        #
        # CREATE TABLE `sql3_salaries` (
        # 	`id` INT ( 11 ) NOT NULL AUTO_INCREMENT,
        # 	`emp_no` INT ( 11 ) NOT NULL,
        # 	`salary` INT ( 11 ) NOT NULL,
        # 	`from_date` date NOT NULL,
        # 	`to_date` date NOT NULL,
        # 	PRIMARY KEY ( `id` ),
        #   UNIQUE KEY `uc_emp_no_from_date` ( `emp_no`, `from_date` )
        # ) ENGINE = INNODB DEFAULT CHARSET = utf8mb4;

        # 一次只能插入一条数据,
        # 如果想要插入多条数据, 需要采用 executemany 配合 insert into sql1_employees values (xxx), (xxx), (xxx);
        cursor = connections['default'].cursor()
        cursor.execute("""INSERT INTO sql3_dept_manager (dept_no, emp_no, to_date) VALUES('d001',10002,'9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_dept_manager (dept_no, emp_no, to_date) VALUES('d002',10006,'9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_dept_manager (dept_no, emp_no, to_date) VALUES('d003',10005,'9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_dept_manager (dept_no, emp_no, to_date) VALUES('d004',10004,'9999-01-01');""")

        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10001,88958,'2002-06-22','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'2001-08-02','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43311,'2001-12-01','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10004,74057,'2001-11-27','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10005,94692,'2001-09-09','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'2001-08-02','9999-01-01');""")
        cursor.execute("""INSERT INTO sql3_salaries (emp_no, salary, from_date, to_date) VALUES(10007,88070,'2002-02-07','9999-01-01');""")

    def clear_data(self):
        cursor = connections['default'].cursor()
        cursor.execute('delete from sql3_salaries;')
        cursor.execute('delete from sql3_dept_manager;')

    def pre_assert(self, qs):
        # 断言:
        # 10002|72527|2001-08-02|9999-01-01|d001
        # 10004|74057|2001-11-27|9999-01-01|d004
        # 10005|94692|2001-09-09|9999-01-01|d003
        # 10006|43311|2001-08-02|9999-01-01|d002
        self.assertEqual(len(qs), 4)
        self.assertEqual(qs[0].emp_no, 10002)
        self.assertEqual(qs[0].salary, 72527)
        self.assertEqual(qs[0].from_date, date(year=2001, month=8, day=2))
        self.assertEqual(qs[0].to_date, date(year=9999, month=1, day=1))
        self.assertEqual(qs[0].dept_no, 'd001')

        self.assertEqual(qs[1].emp_no, 10004)
        self.assertEqual(qs[1].salary, 74057)
        self.assertEqual(qs[1].from_date, date(year=2001, month=11, day=27))
        self.assertEqual(qs[1].to_date, date(year=9999, month=1, day=1))
        self.assertEqual(qs[1].dept_no, 'd004')

        self.assertEqual(qs[2].emp_no, 10005)
        self.assertEqual(qs[2].salary, 94692)
        self.assertEqual(qs[2].from_date, date(year=2001, month=9, day=9))
        self.assertEqual(qs[2].to_date, date(year=9999, month=1, day=1))
        self.assertEqual(qs[2].dept_no, 'd003')

        self.assertEqual(qs[3].emp_no, 10006)
        self.assertEqual(qs[3].salary, 43311)
        self.assertEqual(qs[3].from_date, date(year=2001, month=8, day=2))
        self.assertEqual(qs[3].to_date, date(year=9999, month=1, day=1))
        self.assertEqual(qs[3].dept_no, 'd002')

    def test_sql_2_1(self):
        # 准备数据
        self.prepare_data()

        # TODO: 由于表没有外键关联, 暂时没有找到 LEFT OUTER JOIN 的写法.
        #       有一个思路是: 在 model 里面增加 ForeignKey 字段,
        #       但是不执行 makemigrations 和 migrate, 只使用他的对象定义.
        # 查找各个部门当前领导当前薪水详情以及其对应部门编号dept_no
        # select salaries.*, dept_manager.dept_no
        # from dept_manager
        # left join salaries on dept_manager.emp_no = salaries.emp_no
        qs = dept_manager.objects.raw("""select s.id as id, 
                                                s.emp_no as emp_no, 
                                                s.salary as salary, 
                                                s.from_date as from_date, 
                                                s.to_date as to_date, 
                                                d.dept_no as dept_no 
                                         from sql3_dept_manager as d 
                                         left join sql3_salaries as s on d.emp_no = s.emp_no""")

        # 断言
        self.pre_assert(qs)

        # 清空
        self.clear_data()
