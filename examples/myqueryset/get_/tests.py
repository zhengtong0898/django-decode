from .models import product
from django.test import TestCase, TransactionTestCase


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True
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

        solution = 2
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
            ss = list(product.objects.all())
            ss[0].name = ss[0].name + "-updated"
            ss[0].description = ss[0].description + "-updated"

            ss[1].name = ss[1].name + "-updated"
            ss[1].description = ss[1].description + "-updated"
            to_update = [ss[0], ss[1]]

        # 提交更新
        # UPDATE `get__product`
        # SET `name` =        CASE WHEN (`get__product`.`id` = 1007) THEN 'aaa-0-updated'
        #                          WHEN (`get__product`.`id` = 1008) THEN 'aaa-1-updated'
        #                          ELSE NULL END,
        #     `description` = CASE WHEN (`get__product`.`id` = 1007) THEN 'aaa-0-updated'
        #                          WHEN (`get__product`.`id` = 1008) THEN 'aaa-1-updated'
        #                          ELSE NULL END
        # WHERE `get__product`.`id` IN (1007, 1008)
        product.objects.bulk_update(to_update, ['name', 'description'])

        # 从数据库中获取数据
        p1 = product.objects.get(pk=to_update[0].pk)
        p2 = product.objects.get(pk=to_update[1].pk)

        # 断言-1
        self.assertTrue(p1.name.endswith("-updated"))
        self.assertTrue(p1.description.endswith("-updated"))

        # 断言-2
        self.assertTrue(p2.name.endswith("-updated"))
        self.assertTrue(p2.description.endswith("-updated"))

    def test_f_get_or_create(self):
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

        # 用name='aaa-5'去查, 如果缓存或数据库中没有这个数据,
        # 则使用defaults字典去创建一条新数据.
        # 返回值: object, created;
        #
        # 该方法内部执行了两次sql: 第1次是查询是否存在, 第2次是插入一条数据.
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` = 'aaa-15'
        # LIMIT 21
        #
        # INSERT INTO `get__product` (`name`,
        #                             `price`,
        #                             `description`,
        #                             `production_date`,
        #                             `expiration_date`,
        #                             `date_joined`)
        # VALUES ('aaa-15',
        #         '12.00',
        #         'aaa-15',
        #         '2001-10-10',
        #         120,
        #         '2021-03-28 12:20:28.121343')
        # RETURNING `get__product`.`id`";
        #
        #
        # 备注: 补充一个情况, 由于get_or_create占用了 defaults 参数,
        #      因此当model里面刚好定义了defaults字段, 那么这里就会发生冲突,
        #      为了解决字段名和参数名一致冲突问题, 可以使用defaults__exact来告诉django, 这个字段冲突了.
        obj, is_created = product.objects.get_or_create(name='aaa-15', defaults={'price': 12.00,
                                                                                 'description': 'aaa-15',
                                                                                 'production_date': '2001-10-10',
                                                                                 'expiration_date': 120})
        self.assertEqual(is_created, True)
        self.assertEqual(obj.name, 'aaa-15')
        self.assertEqual(obj.price, 12.00)
        self.assertEqual(obj.description, 'aaa-15')

    def test_g_update_or_create(self):
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

        # 用name='aaa-5'去查,
        # 如果缓存或数据库中没有这个数据, 则使用defaults字典去创建一条新数据.
        # 如果缓存或数据库中存在这个数据, 则按defaults中的键值来更新数据.
        # 返回值: object, created;
        #
        #
        # 数据存在(查询, 更新)
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` = 'aaa-5'
        # LIMIT 21
        # FOR UPDATE
        #
        # UPDATE `get__product`
        # SET `name` = 'aaa-5',
        #     `price` = '10.00',
        #     `description` = 'aaa-x5',
        #     `production_date` = '1999-10-20',
        #     `expiration_date` = 170,
        #     `date_joined` = '2021-03-28 14:11:18.417537'
        # WHERE `get__product`.`id` = 1033
        obj, is_created = product.objects.update_or_create(name='aaa-5', defaults={'description': 'aaa-x5'})

        # 断言-1
        self.assertEqual(is_created, False)
        self.assertEqual(obj.name, 'aaa-5')
        self.assertEqual(obj.description, 'aaa-x5')

        # 用name='aaa-15'去查,
        # 如果缓存或数据库中没有这个数据, 则使用defaults字典去创建一条新数据.
        # 如果缓存或数据库中存在这个数据, 则按defaults中的键值来更新数据.
        # 返回值: object, created;
        #
        #
        # 数据不存在(查询, 插入)
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` = 'aaa-15'
        # LIMIT 21
        # FOR UPDATE
        #
        # INSERT INTO `get__product` (`name`,
        #                             `price`,
        #                             `description`,
        #                             `production_date`,
        #                             `expiration_date`,
        #                             `date_joined`)
        # VALUES ('aaa-15',
        #         '12.00',
        #         'aaa-15',
        #         '2001-10-10',
        #         120,
        #         '2021-03-28 14:15:17.710272')
        obj, is_created = product.objects.update_or_create(name='aaa-15', defaults={'price': 12.00,
                                                                                    'description': 'aaa-15',
                                                                                    'production_date': '2001-10-10',
                                                                                    'expiration_date': 120})

        # 断言-2
        self.assertEqual(is_created, True)
        self.assertEqual(obj.name, 'aaa-15')
        self.assertEqual(obj.price, 12.00)
        self.assertEqual(obj.description, 'aaa-15')

    def test_h_earliest(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 排序通常比较有效的是按照时间, 按照价格, 按照数字.
        # # 按指定字段, 正向排序, 提取第一条数据(即: 最早的一条数据).
        #
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # ORDER BY `get__product`.`production_date` ASC         # 按给定字段正向排序
        # LIMIT 1                                               # 只提取第一条数据
        ss = product.objects.earliest('production_date')
        self.assertEqual(ss.name, "aaa-0")

    def test_i_latest(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 排序通常比较有效的是按照时间, 按照价格, 按照数字.
        # # 按指定字段, 反向排序, 提取第一条数据(即: 最晚的一条数据).
        #
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # ORDER BY `get__product`.`production_date` DESC        # 按给定字段反向排序
        # LIMIT 1                                               # 只提取第一条数据
        ss = product.objects.latest('production_date')
        self.assertEqual(ss.name, "aaa-9")

    def test_j_first(self):

        # 按 pk 字段正向排序, 然后提取第一条数据,
        # 当数据不存在时, 返回一个None, 不报错.
        p = product.objects.first()

        # 断言-1
        self.assertIsNone(p)

        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 按 pk 字段正向排序, 然后提取第一条数据:
        # 当数据存在时, 返回第一条数据, 类型是: product
        #
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # ORDER BY `get__product`.`id` ASC                      # 按 pk 字段正向排序
        # LIMIT 1                                               # 提取第一条数据
        p = product.objects.first()

        # 断言-2
        self.assertIsInstance(p, product)
        self.assertTrue(p.name, "aaa-0")

        # 按自定义字段排序查询得出 queryset 结果集, 返回第一条数据.
        qs = product.objects.filter(production_date__range=('1999-10-13', '1999-10-15')).order_by('production_date')
        self.assertEqual(len(qs), 3)

        # 断言-3
        # 如果前面排序过了, 那么这里将不会再查询数据库排序;
        # 如果前面没有排序过, 那么这里就会重新查询数据库, 按 pk 字段正向排序.
        ps = qs.first()
        self.assertEqual(ps.name, 'aaa-3')

    def test_k_last(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 按 pk 字段反向排序, 然后提取第一条数据.
        #
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # ORDER BY `get__product`.`id` DESC                 # 按 pk 字段反向排序
        # LIMIT 1                                           # 提取第一条数据
        ps = product.objects.last()
        self.assertEqual(ps.name, "aaa-9")

        # 按自定义字段排序查询得出 queryset 结果集,
        # 返回第一条数据.
        qs = product.objects.filter(production_date__range=('1999-10-13', '1999-10-15'))
        self.assertEqual(len(qs), 3)

        # 断言-2
        ps = qs.last()
        self.assertEqual(ps.name, 'aaa-5')

    def test_l_in_bulk(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 批量按值查找
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`id` IN (1, 2, 3)            # pk in (1, 2, 3)
        ss = product.objects.in_bulk(id_list=[1,2,3])
        # 断言-1
        self.assertEqual(ss[1].name, "aaa-0")
        self.assertEqual(ss[2].name, "aaa-1")
        self.assertEqual(ss[3].name, "aaa-2")

        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`description`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        # WHERE `get__product`.`name` IN ('aaa-3', 'aaa-5', 'aaa-7')
        ss = product.objects.in_bulk(id_list=["aaa-3", "aaa-5", "aaa-7"], field_name="name")
        # 断言-2
        self.assertEqual(ss["aaa-3"].name, "aaa-3")
        self.assertEqual(ss["aaa-5"].name, "aaa-5")
        self.assertEqual(ss["aaa-7"].name, "aaa-7")

    def test_m_distinct(self):
        # 准备10条数据
        items = []
        for i in range(5):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa",
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        for i in range(5):
            pp = product(name="bbb-%s" % i,
                         price=10.00,
                         description="bbb",
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # 去重
        # SELECT DISTINCT `get__product`.`description`
        # FROM `get__product`
        qs = product.objects.values('description').distinct()
        self.assertEqual(len(qs), 2)
        self.assertIsInstance(qs[0], dict)
        self.assertEqual(qs[0]["description"], "aaa")
        self.assertEqual(qs[1]["description"], "bbb")

    def test_n_defer(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # defer用于排除字段
        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`,
        #        `get__product`.`production_date`,
        #        `get__product`.`expiration_date`,
        #        `get__product`.`date_joined`
        # FROM `get__product`
        qs = product.objects.defer('description')

        # 备注:
        # 当通过qs[0].description时, 会即时的触发数据库查询, 提取该字段的值.(慎重! 慎重! 慎重!)
        self.assertEqual(len(qs), 10)

    def test_o_only(self):
        # 准备10条数据
        items = []
        for i in range(10):
            pp = product(name="aaa-%s" % i,
                         price=10.00,
                         description="aaa-%s" % i,
                         production_date="1999-10-1%s" % i,
                         expiration_date=170)
            items.append(pp)

        # 批量插入10条数据
        product.objects.bulk_create(objs=items)

        # SELECT `get__product`.`id`,
        #        `get__product`.`name`,
        #        `get__product`.`price`
        # FROM `get__product`
        qs = product.objects.only('name', 'price')
        self.assertEqual(len(qs), 10)

        # 无sql查询
        self.assertEqual(qs[0].name, "aaa-0")

        # 触发sql查询
        # SELECT `get__product`.`id`,
        #        `get__product`.`description`
        # FROM `get__product`
        # WHERE `get__product`.`id` = 1
        # LIMIT 21
        self.assertEqual(qs[0].description, "aaa-0")
