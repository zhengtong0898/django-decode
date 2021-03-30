from django.test import TestCase, TransactionTestCase
from .models import product, brand


# Create your tests here.
class SimpleTest(TransactionTestCase):
    reset_sequences = True

    def test_a_delete_relate(self):

        b1 = brand(name="fenghuang", description="fhdc")
        b2 = brand(name="auldey", description="adsg")

        b1.save()
        b2.save()

        product(name="凤凰牌男款自行车",
                     price=100.00,
                     description="男款带横梁, 经典款",
                     production_date="1999-10-10",
                     expiration_date=170,
                     brand_id=b1).save()

        product(name="凤凰牌女款自行车",
                     price=199.00,
                     description="凤凰牌女款自行车",
                     production_date="1999-10-10",
                     expiration_date=170,
                     brand_id=b1).save()

        product(name="奥迪双钻四驱车-蜘蛛王",
                     price=19.00,
                     description="奥迪双钻四驱车-蜘蛛王",
                     production_date="1999-10-11",
                     expiration_date=170,
                     brand_id=b2).save()

        # Django知道 brand 这张表被引用了(referenced),
        # 所以在删除 brand 的数据之前, 需要:
        # 1. 先查询当前数据
        # 2. 拿查询出来的结果的id, 去尝试删除引用表与
        #    外键值一致的那条些(可能是一条也可能是多条)数据.
        # 3. 拿查询出来的结果的id, 去尝试删除brand的数据.
        #
        # 1. 查询
        # SELECT `delete__brand`.`id`,
        #        `delete__brand`.`name`,
        #        `delete__brand`.`description`
        # FROM `delete__brand`
        # WHERE `delete__brand`.`id` = 1
        #
        # 2. 删除子表指定数据
        # DELETE FROM `delete__product`
        # WHERE `delete__product`.`brand_id_id` IN (1)
        #
        # 3. 删除父表指定数据
        # DELETE FROM `delete__brand`
        # WHERE `delete__brand`.`id` IN (1)
        delete_success, delete_count = brand.objects.filter(pk=1).delete()
        # 断言-1: 确认product表中id=1的这条数据已经被删除了.
        self.assertEqual(delete_success, 3)
        self.assertEqual(len(delete_count), 2)
        self.assertEqual(delete_count["delete_.brand"], 1)
        self.assertEqual(delete_count["delete_.product"], 2)

        # Django知道product这张表没有被引用(referenced),
        # 所以不需要先查询在删除, 而是直接删除.
        #
        # DELETE FROM `delete__product`
        # WHERE `delete__product`.`id` = 2'
        delete_success, delete_count = product.objects.filter(pk=3).delete()
        # 断言-2
        self.assertEqual(delete_success, 1)
        self.assertEqual(len(delete_count), 1)
        self.assertEqual(delete_count["delete_.product"], 1)

    def test_b_update(self):
        b1 = brand(name="fenghuang", description="fhdc")
        b1.save()

        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170,
                         brand_id=b1)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # update 只负责更新 queryset 对象中的数据.
        # UPDATE `get__product`
        # SET `description` = 'bbbb'
        # WHERE `get__product`.`expiration_date` = 170
        rows = product.objects.filter(expiration_date=170).update(description="bbbb")
        # 断言: 批量更新了10条数据.
        self.assertEqual(rows, 10)

    def test_c_exists(self):
        b1 = brand(name="fenghuang", description="fhdc")
        b1.save()

        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170,
                         brand_id=b1)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # SELECT (1) AS `a`
        # FROM `delete__product`
        # WHERE `delete__product`.`id` = 99
        # LIMIT 1
        pp = product.objects.filter(pk=99).exists()
        self.assertEqual(pp, False)

        # SELECT (1) AS `a`
        # FROM `delete__product`
        # WHERE `delete__product`.`id` = 1
        # LIMIT 1
        pp = product.objects.filter(pk=1).exists()
        self.assertEqual(pp, True)
