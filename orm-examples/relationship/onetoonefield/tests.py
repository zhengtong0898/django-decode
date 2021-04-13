from django.test import TestCase, TransactionTestCase
from .models import Place, Restaurant, Waiter


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_n_plus_1(self):
        # 准备数据
        p1 = Place.objects.create(name='Demon Dogs', address='944 W. Fullerton')
        Restaurant.objects.create(place=p1, serves_hot_dogs=True, serves_pizza=False)

        # 查询数据
        # SELECT `onetoonefield_restaurant`.`place_id`,
        #        `onetoonefield_restaurant`.`serves_hot_dogs`,
        #        `onetoonefield_restaurant`.`serves_pizza`
        # FROM `onetoonefield_restaurant`
        # WHERE `onetoonefield_restaurant`.`place_id` = 1
        # LIMIT 21
        r = Restaurant.objects.get(pk=1)            # 提交sql
        self.assertEqual(r.place, p1)               # r.place触发再次提交sql, n+1

    def test_b_the_case(self):
        # 准备数据
        p1 = Place.objects.create(name='Demon Dogs', address='944 W. Fullerton')
        Restaurant.objects.create(place=p1, serves_hot_dogs=True, serves_pizza=False)

        # 查询数据
        # SELECT `onetoonefield_restaurant`.`place_id`,
        #        `onetoonefield_restaurant`.`serves_hot_dogs`,
        #        `onetoonefield_restaurant`.`serves_pizza`,
        #        `onetoonefield_place`.`id`,
        #        `onetoonefield_place`.`name`,
        #        `onetoonefield_place`.`address`
        # FROM `onetoonefield_restaurant`
        # INNER JOIN `onetoonefield_place` ON (`onetoonefield_restaurant`.`place_id` = `onetoonefield_place`.`id`)
        # WHERE `onetoonefield_restaurant`.`place_id` = 1
        # LIMIT 21
        r = Restaurant.objects.select_related('place').get(pk=1)        # 提交sql
        self.assertEqual(r.place, p1)                                   # 无sql提交.

    def test_c_the_reverse_side(self):
        # 准备数据
        p1 = Place.objects.create(name='Demon Dogs', address='944 W. Fullerton')
        r1 = Restaurant.objects.create(place=p1, serves_hot_dogs=True, serves_pizza=False)

        # 一对多和多对多的被指向对象, 只能通过 tablename_set.all() 的方式来方向查找关联数据.
        # 一对一的被指向对象, 可以通过 select_related() 的方式来查找关联, 也就是说, 一对一关系, 双边都是ForeignKey.
        #
        # 反向查找用 Left Join
        # SELECT `onetoonefield_place`.`id`,
        #        `onetoonefield_place`.`name`,
        #        `onetoonefield_place`.`address`,
        #        `onetoonefield_restaurant`.`place_id`,
        #        `onetoonefield_restaurant`.`serves_hot_dogs`,
        #        `onetoonefield_restaurant`.`serves_pizza`
        # FROM `onetoonefield_place`
        # LEFT OUTER JOIN `onetoonefield_restaurant`
        #      ON (`onetoonefield_place`.`id` = `onetoonefield_restaurant`.`place_id`)
        # WHERE `onetoonefield_place`.`id` = 1 LIMIT 21
        p = Place.objects.select_related('restaurant').get(pk=1)
        self.assertEqual(p.restaurant, r1)
