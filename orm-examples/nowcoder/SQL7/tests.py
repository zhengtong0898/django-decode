from datetime import date
from django.db import connections
from django.test import TestCase, TransactionTestCase
from .models import salaries
from django.db.models.aggregates import Count


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def prepare_data(self):
        # 建表语句
        # CREATE TABLE `sql7_salaries` (
        # 	`emp_no` INT ( 11 ) NOT NULL AUTO_INCREMENT,
        # 	`salary` INT ( 11 ) NOT NULL,
        # 	`from_date` date NOT NULL,
        # 	`to_date` date NOT NULL,
        #   PRIMARY KEY ( `emp_no` )
        # ) ENGINE = INNODB DEFAULT CHARSET = utf8mb4;

        # 一次只能插入一条数据,
        # 如果想要插入多条数据, 需要采用 executemany 配合 insert into sql1_employees values (xxx), (xxx), (xxx);
        cursor = connections['default'].cursor()

        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,60117,'1986-06-26','1987-06-26');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,62102,'1987-06-26','1988-06-25');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,66074,'1988-06-25','1989-06-25');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,66596,'1989-06-25','1990-06-25');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,66961,'1990-06-25','1991-06-25');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,71046,'1991-06-25','1992-06-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,74333,'1992-06-24','1993-06-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,75286,'1993-06-24','1994-06-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,75994,'1994-06-24','1995-06-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,76884,'1995-06-24','1996-06-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,80013,'1996-06-23','1997-06-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,81025,'1997-06-23','1998-06-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,81097,'1998-06-23','1999-06-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,84917,'1999-06-23','2000-06-22');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,85112,'2000-06-22','2001-06-22');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,85097,'2001-06-22','2002-06-22');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10001,88958,'2002-06-22','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'1996-08-03','1997-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'1997-08-03','1998-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'1998-08-03','1999-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'1999-08-03','2000-08-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'2000-08-02','2001-08-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'2001-08-02','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,40006,'1995-12-03','1996-12-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43616,'1996-12-02','1997-12-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43466,'1997-12-02','1998-12-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43636,'1998-12-02','1999-12-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43478,'1999-12-02','2000-12-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43699,'2000-12-01','2001-12-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,43311,'2001-12-01','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,40054,'1986-12-01','1987-12-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,42283,'1987-12-01','1988-11-30');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,42542,'1988-11-30','1989-11-30');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,46065,'1989-11-30','1990-11-30');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,48271,'1990-11-30','1991-11-30');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,50594,'1991-11-30','1992-11-29');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,52119,'1992-11-29','1993-11-29');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,54693,'1993-11-29','1994-11-29');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,58326,'1994-11-29','1995-11-29');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,60770,'1995-11-29','1996-11-28');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,62566,'1996-11-28','1997-11-28');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,64340,'1997-11-28','1998-11-28');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,67096,'1998-11-28','1999-11-28');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,69722,'1999-11-28','2000-11-27');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,70698,'2000-11-27','2001-11-27');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10004,74057,'2001-11-27','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,78228,'1989-09-12','1990-09-12');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,82621,'1990-09-12','1991-09-12');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,83735,'1991-09-12','1992-09-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,85572,'1992-09-11','1993-09-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,85076,'1993-09-11','1994-09-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,86050,'1994-09-11','1995-09-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,88448,'1995-09-11','1996-09-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,88063,'1996-09-10','1997-09-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,89724,'1997-09-10','1998-09-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,90392,'1998-09-10','1999-09-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,90531,'1999-09-10','2000-09-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,91453,'2000-09-09','2001-09-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10005,94692,'2001-09-09','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1990-08-05','1991-08-05');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1991-08-05','1992-08-04');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1992-08-04','1993-08-04');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1993-08-04','1994-08-04');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1994-08-04','1995-08-04');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1995-08-04','1996-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1996-08-03','1997-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1997-08-03','1998-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1998-08-03','1999-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1999-08-03','2000-08-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'2000-08-02','2001-08-02');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'2001-08-02','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,56724,'1989-02-10','1990-02-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,60740,'1990-02-10','1991-02-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,62745,'1991-02-10','1992-02-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,63475,'1992-02-10','1993-02-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,63208,'1993-02-09','1994-02-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,64563,'1994-02-09','1995-02-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,68833,'1995-02-09','1996-02-09');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,70220,'1996-02-09','1997-02-08');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,73362,'1997-02-08','1998-02-08');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,75582,'1998-02-08','1999-02-08');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,79513,'1999-02-08','2000-02-08');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,80083,'2000-02-08','2001-02-07');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,84456,'2001-02-07','2002-02-07');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10007,88070,'2002-02-07','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10008,46671,'1998-03-11','1999-03-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10008,48584,'1999-03-11','2000-03-10');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10008,52668,'2000-03-10','2000-07-31');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,60929,'1985-02-18','1986-02-18');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,64604,'1986-02-18','1987-02-18');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,64780,'1987-02-18','1988-02-18');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,66302,'1988-02-18','1989-02-17');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,69042,'1989-02-17','1990-02-17');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,70889,'1990-02-17','1991-02-17');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,71434,'1991-02-17','1992-02-17');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,74612,'1992-02-17','1993-02-16');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,76518,'1993-02-16','1994-02-16');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,78335,'1994-02-16','1995-02-16');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,80944,'1995-02-16','1996-02-16');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,82507,'1996-02-16','1997-02-15');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,85875,'1997-02-15','1998-02-15');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,89324,'1998-02-15','1999-02-15');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,90668,'1999-02-15','2000-02-15');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,93507,'2000-02-15','2001-02-14');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,94443,'2001-02-14','2002-02-14');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10009,95409,'2002-02-14','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'1996-11-24','1997-11-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'1997-11-24','1998-11-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'1998-11-24','1999-11-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'1999-11-24','2000-11-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'2000-11-23','2001-11-23');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'2001-11-23','9999-01-01');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10002,72527,'1985-11-21','1996-08-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10003,15828,'1986-08-28','1995-12-03');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1989-06-02','1990-08-05');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10006,43311,'1994-09-15','1998-03-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10010,94409,'1989-08-24','1996-11-24');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10008,25828,'1994-09-15','1998-03-11');""")
        cursor.execute("""INSERT INTO sql7_salaries (emp_no, salary, from_date, to_date) VALUES(10011,25828,'1990-01-22','9999-01-01');""")

    def clear_data(self):
        cursor = connections['default'].cursor()
        cursor.execute('delete from sql7_salaries;')

    def pre_assert(self, qs):
        # 断言:
        # 10001|17
        # 10004|16
        # 10009|18
        self.assertEqual(len(qs), 3)
        self.assertEqual(qs[0].get('emp_no'), 10001)
        self.assertEqual(qs[0].get('t'), 17)
        self.assertEqual(qs[1].get('emp_no'), 10004)
        self.assertEqual(qs[1].get('t'), 16)
        self.assertEqual(qs[2].get('emp_no'), 10009)
        self.assertEqual(qs[2].get('t'), 18)

    def test_sql_7_1(self):
        # 准备数据
        self.prepare_data()

        # select emp_no, count(to_date) as t
        # from salaries
        # group by emp_no
        # having t > 4;
        qs = (salaries.objects.values('emp_no')
                              .annotate(t=Count('emp_no'))
                              .filter(t__gt=15))
        # 断言
        self.pre_assert(qs)
        # 清空
        self.clear_data()
