from datetime import date
from django.db import connections
from django.test import TestCase, TransactionTestCase
from .models import employees
from django.db.models import Max
from django.db.models.expressions import Subquery, OuterRef


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def prepare_data(self):
        # 建表语句
        # CREATE TABLE `sql1_employees` (
        #   `emp_no` int(11) NOT NULL,
        #   `birth_date` date NOT NULL,
        #   `first_name` varchar(14) NOT NULL,
        #   `last_name` varchar(16) NOT NULL,
        #   `gender` varchar(1) NOT NULL,
        #   `hire_date` date NOT NULL,
        #   PRIMARY KEY (`emp_no`)                          # 聚集索引
        # ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

        # 一次只能插入一条数据,
        # 如果想要插入多条数据, 需要采用 executemany 配合 insert into sql1_employees values (xxx), (xxx), (xxx);
        cursor = connections['default'].cursor()
        cursor.execute("""INSERT INTO sql2_employees VALUES(10001,'1953-09-02','Georgi','Facello','M','1986-06-26');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10002,'1964-06-02','Bezalel','Simmel','F','1985-11-21');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10003,'1959-12-03','Parto','Bamford','M','1986-08-28');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10004,'1954-05-01','Chirstian','Koblick','M','1986-12-01');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10005,'1955-01-21','Kyoichi','Maliniak','M','1989-09-12');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10006,'1953-04-20','Anneke','Preusig','F','1989-06-02');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10007,'1957-05-23','Tzvetan','Zielinski','F','1989-02-10');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10008,'1958-02-19','Saniya','Kalloufi','M','1994-09-15');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10009,'1952-04-19','Sumant','Peac','F','1985-02-18');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10010,'1963-06-01','Duangkaew','Piveteau','F','1989-08-24');""")
        cursor.execute("""INSERT INTO sql2_employees VALUES(10011,'1953-11-07','Mary','Sluis','F','1990-01-22');""")

    def clear_data(self):
        cursor = connections['default'].cursor()
        cursor.execute('delete from sql2_employees;')

    def pre_assert(self, qs):
        # 断言-期望: 10005|1955-01-21|Kyoichi|Maliniak|M|1989-09-12
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0].emp_no, 10005)
        self.assertEqual(qs[0].birth_date, date(year=1955, month=1, day=21))
        self.assertEqual(qs[0].first_name, "Kyoichi")
        self.assertEqual(qs[0].last_name, "Maliniak")
        self.assertEqual(qs[0].gender, "M")
        self.assertEqual(qs[0].hire_date, date(year=1989, month=9, day=12))

    def test_sql_2_1(self):
        # 准备数据
        self.prepare_data()

        # 查找入职员工时间排名倒数第三的员工所有信息
        # SELECT `SQL2_employees`.`emp_no`,
        #        `SQL2_employees`.`birth_date`,
        #        `SQL2_employees`.`first_name`,
        #        `SQL2_employees`.`last_name`,
        #        `SQL2_employees`.`gender`,
        #        `SQL2_employees`.`hire_date`
        # FROM `SQL2_employees`
        # ORDER BY `SQL2_employees`.`hire_date` DESC
        # LIMIT 1 OFFSET 2
        qs = employees.objects.order_by('-hire_date')[2:3]

        # 断言
        self.pre_assert(qs)

        # 清空
        self.clear_data()
