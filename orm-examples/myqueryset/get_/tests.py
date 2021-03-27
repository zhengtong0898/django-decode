from .models import product
from django.test import TestCase


# Create your tests here.
class SimpleTest(TestCase):

    """
    注意事项:

    unittest.test_runner 在加载 TestCase 时,
    方法加载顺序按照方法名顺序来加载,
    所以这里采用了顺序来规避 pk=1 这种强依赖问题.
    """

    def test_a_get(self):
        # 准备数据
        product(name="aaa", price=10.00, description="aaa", production_date="1999-12-31", expiration_date=170).save()
        product(name="bbb", price=10.00, description="bbb", production_date="1999-12-31", expiration_date=170).save()

        # 断言-1
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`id` = 2
        # LIMIT 21
        ss = product.objects.get(pk=1)
        self.assertEqual(ss.name, "aaa")

        # 断言-2
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`id` = 2
        # LIMIT 21
        ss = product.objects.get(pk=2)
        self.assertEqual(ss.name, "bbb")

        # 断言-3:
        with self.assertRaises(Exception):
            # SELECT `get__product`.`id`,
            #        `get__product`.`name`,
            #        `get__product`.`price`,
            #        `get__product`.`description`,
            #        `get__product`.`production_date`,
            #        `get__product`.`expiration_date`,
            #        `get__product`.`date_joined`
            # FROM `get__product`
            # WHERE `get__product`.`expiration_date` = 170
            # LIMIT 21
            ss = product.objects.get(expiration_date=170)

    def test_b_create(self):
        """
        QuerySet.create
        插入一条数据.

        product(**kwargs).save()  等同于  product.objects.create(**kwargs)
        """

        # 准备数据
        # INSERT INTO `get__product` (`name`,
        #                             `price`,
        #                             `description`,
        #                             `production_date`,
        #                             `expiration_date`,
        #                             `date_joined`)
        # VALUES (ccc,
        #         10.00,
        #         ccc,
        #         1999-12-31,
        #         170,
        #         2021-03-27 01:35:41.116658)
        product.objects.create(name="ccc",
                               price=10.00,
                               description="ccc",
                               production_date="1999-12-31",
                               expiration_date=170)

        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` = ccc
        # LIMIT 21
        ss = product.objects.get(name="ccc")

        # 断言
        self.assertEqual(ss.name, "ccc")
