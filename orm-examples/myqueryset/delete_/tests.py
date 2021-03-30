from django.test import TestCase, TransactionTestCase


# Create your tests here.
class SimpleTest(TransactionTestCase):
    reset_sequences = True

    def test_a_delete_relate(self):
        from .models import product, brand

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
        brand.objects.filter(pk=1).delete()
        # 断言-1: 确认product表中id=1的这条数据已经被删除了.
        ss = product.objects.filter(pk=1)
        self.assertEqual(len(ss), 0)

        # Django知道product这张表没有被引用(referenced),
        # 所以不需要先查询在删除, 而是直接删除.
        #
        # DELETE FROM `delete__product`
        # WHERE `delete__product`.`id` = 2'
        product.objects.filter(pk=2).delete()
        # 断言-2
        ss = product.objects.filter(pk=2)
        self.assertEqual(len(ss), 0)
