from .models import product
from django.test import TestCase


# Create your tests here.
class SimpleTest(TestCase):

    """
    注意事项:

    1. unittest.test_runner 在加载 TestCase 时,
      方法加载顺序按照方法名顺序来加载,
      所以这里采用了顺序来规避 pk=1 这种强依赖问题.

    2. django在执行TestCase之前, 会将 set_autocommit(False),
       然后再执行TestCase, 当TestCase执行完之后, 再恢复为 set_autocommit(True).
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
        QuerySet.create: 插入一条数据.

        product.objects.create(**kwargs)  等同于  product(**kwargs).save()
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

    def test_c_count(self):
        """
        QuerySet.count: 统计总数

        方法 count 采取两套统计策略:
        1. 当 QuerySet 有缓存值(QuerySet._result_cache)时,
           表示之前就使用过这个QuerySet查询过数据库了,
           这里将不再查询数据库, 而是使用python内置len函数来统计缓存值.

        2. 当 QuerySet 没有缓存值时, 使用 select count(*) 去查询统计总数.
        """
        # 准备数据
        product(name="aaa", price=10.00, description="aaa", production_date="1999-10-20", expiration_date=170).save()
        product(name="bbb", price=10.00, description="bbb", production_date="1999-11-20", expiration_date=170).save()
        product(name="ccc", price=10.00, description="ccc", production_date="1999-12-20", expiration_date=170).save()

        # 统计全部
        # SELECT COUNT(*) AS `__count` FROM `get__product`
        ss = product.objects.count()

        # 断言-1
        self.assertEqual(ss, 3)

        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` = 'aaa'
        ss = product.objects.filter(name="aaa")

        # 使用 python 内置 len 函数统计数据总数.
        cc = ss.count()

        # 断言-2
        self.assertEqual(cc, 1)

    def test_d_bulk_create(self):
        # 批量插入1000条数据, 每一批插入10条数据.
        items = []
        for i in range(1000):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-20",
                         expiration_date=170)
            items.append(pp)

        # 每次插入10条数据, 一直遍历完1000条数据.
        # INSERT INTO `get__product` (`name`,
        #                             `price`,
        #                             `description`,
        #                             `production_date`,
        #                             `expiration_date`,
        #                             `date_joined`)
        # VALUES ('aaa-0', '10.00', 'aaa-0', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-1', '10.00', 'aaa-1', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-2', '10.00', 'aaa-2', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-3', '10.00', 'aaa-3', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-4', '10.00', 'aaa-4', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-5', '10.00', 'aaa-5', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-6', '10.00', 'aaa-6', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-7', '10.00', 'aaa-7', '1999-10-20', 170, '2021-03-27 16:44:11.254361'),
        #        ('aaa-8', '10.00', 'aaa-8', '1999-10-20', 170, '2021-03-27 16:44:11.255359'),
        #        ('aaa-9', '10.00', 'aaa-9', '1999-10-20', 170, '2021-03-27 16:44:11.255359')
        product.objects.bulk_create(objs=items, batch_size=10)

        # 从数据库中进行整表统计.
        ss = product.objects.count()
        self.assertEqual(ss, 1000)

    def test_e_bulk_update(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-20",
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        solution = 1
        # 准备更新-方案1: 从已有数据中修改, 提交修改.
        # 由于 mysql 和 mariadb < 10.5 的版本在批量插入时并不返回对象的 lastrow_id,
        # items集合中的数据的 pk 字段为 None, 这会导致 bulk_update 抛出异常.
        # 所以这个方案只支持 mariadb >= 10.5 的版本.
        #
        # 采用 create 而不是 bulk_create , 这样创建的数据就会包含 pk 字段, bulk_update 就不会抛异常.
        if solution == 1:
            items[0].name = items[0].name + "-updated"
            items[0].description = items[0].description + "-updated"

            items[1].name = items[1].name + "-updated"
            items[1].description = items[1].description + "-updated"
            to_update = [items[0], items[1]]

        # 准备更新-方案2: 从数据库中查询数据, 修改数据, 提交修改.
        # 支持所有版本.
        elif solution == 2:
            ss = product.objects.all()
            ss[0].name = ss[0].name + "-updated"
            ss[0].description = ss[0].description + "-updated"

            ss[1].name = ss[1].name + "-updated"
            ss[1].description = ss[1].description + "-updated"
            to_update = [ss[0], ss[1]]

        product.objects.bulk_update(to_update, ['name', 'description'])

        p1 = product.objects.get(pk=to_update[0].pk)
        p2 = product.objects.get(pk=to_update[1].pk)

        self.assertTrue(p1.name.endswith("-updated"))
        self.assertTrue(p1.description.endswith("-updated"))

        self.assertTrue(p2.name.endswith("-updated"))
        self.assertTrue(p2.description.endswith("-updated"))
