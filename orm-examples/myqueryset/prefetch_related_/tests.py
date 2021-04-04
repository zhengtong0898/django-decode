from django.test import TestCase, TransactionTestCase
from .models import Pizza, Topping, Restaurant


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_normal_all(self):
        # 准备数据
        ham = Topping.objects.create(name="ham")
        pineapple = Topping.objects.create(name="pineapple")
        prawns = Topping.objects.create(name="prawns")
        smoked_salmon = Topping.objects.create(name="smoked salmon")

        hawaiian = Pizza.objects.create(name="Hawaiian")
        # hawaiian.toppings 类型是: ManyRelatedManager,
        # 源码位置: django/db/models/fields/relate_descriptors.py#L815
        # 对外公开的接口:
        # get_queryset(self),
        # get_prefetch_queryset(self, instances, queryset=None)
        # add(self, *objs, through_defaults=None)
        # remove(self, *objs):
        # clear(self)
        # set(self, objs, *, clear=False, through_defaults=None)
        # create(self, *, through_defaults=None, **kwargs)
        # get_or_create(self, *, through_defaults=None, **kwargs)
        # update_or_create(self, *, through_defaults=None, **kwargs)
        #
        # all(self)      该方法定义在父类 django/db/models/manager.BaseManager 对象中, 返回一个QuerySet.
        hawaiian.toppings.add(*[ham, pineapple])

        seafood = Pizza.objects.create(name="Seafood")
        seafood.toppings.add(*[prawns, smoked_salmon])

        # 关注点: 数据库查询方式?
        # 第一步: 查询所有数据(得到一个数据集合).
        # SELECT `prefetch_related__pizza`.`id`,
        #        `prefetch_related__pizza`.`name`
        # FROM `prefetch_related__pizza` LIMIT 21
        ss = Pizza.objects.all()
        self.assertEqual(len(ss), 2)

        # SELECT `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM `prefetch_related__topping`
        #      INNER JOIN `prefetch_related__pizza_toppings` ON
        #      (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE `prefetch_related__pizza_toppings`.`pizza_id` = 1
        self.assertEqual(len(ss[0].toppings.all()), 2)

        # SELECT `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM   `prefetch_related__topping`
        #        INNER JOIN `prefetch_related__pizza_toppings` ON
        #        (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE (`prefetch_related__pizza_toppings`.`pizza_id` = 1 AND
        #        `prefetch_related__topping`.`name` = 'pineapple')
        toppings = ss[0].toppings.filter(name="pineapple")
        self.assertEqual(len(toppings), 1)

        # SELECT `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM `prefetch_related__topping`
        #      INNER JOIN `prefetch_related__pizza_toppings` ON
        #      (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE `prefetch_related__pizza_toppings`.`pizza_id` = 2
        self.assertEqual(len(ss[1].toppings.all()), 2)

    def test_b_prefetch_related(self):

        """
        关注点: prefetch_related 的 SQL 运行流程.
        """

        # 准备数据
        # 准备 Topping 数据
        ham = Topping.objects.create(name="ham")
        pineapple = Topping.objects.create(name="pineapple")
        prawns = Topping.objects.create(name="prawns")
        smoked_salmon = Topping.objects.create(name="smoked salmon")
        # 准备 Pizza 数据 和 对应的多对多字段数据的填充.
        hawaiian = Pizza.objects.create(name="Hawaiian")
        hawaiian.toppings.add(*[ham, pineapple])
        seafood = Pizza.objects.create(name="Seafood")
        seafood.toppings.add(*[prawns, smoked_salmon])

        # 由于 prefetch_related() 没有提供任何参数,
        # 因此 prefetch_related() 并没有对 _prefetch_related_lookups 进行设置,
        # 因此 Pizza.objects.prefetch_related().all() 其实等同于 Pizza.objects.all()
        # SELECT `prefetch_related__pizza`.`id`,
        #        `prefetch_related__pizza`.`name`
        # FROM `prefetch_related__pizza`
        ss = Pizza.objects.prefetch_related().all()
        self.assertEqual(len(ss), 2)

        # prefetch_related 一次性产生两条sql:
        # 第一条: 查询 Pizza 表的所有数据
        # SELECT `prefetch_related__pizza`.`id`,
        #        `prefetch_related__pizza`.`name`
        # FROM `prefetch_related__pizza`
        #
        # 第二条: 将 pizza 表的所有数据的 id 放在 IN (id, id, id, ...) 中做 INNER JOIN 查询匹配.
        # SELECT (`prefetch_related__pizza_toppings`.`pizza_id`) AS `_prefetch_related_val_pizza_id`,
        #        `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM   `prefetch_related__topping`
        #        INNER JOIN `prefetch_related__pizza_toppings` ON
        #        (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE `prefetch_related__pizza_toppings`.`pizza_id` IN (1, 2)
        ss = Pizza.objects.prefetch_related('toppings').all()
        self.assertEqual(len(ss), 2)
        # 重点: 这里使用toppings.all()将不会再去查询数据库, 而是去命中缓存.
        self.assertEqual(len(ss[0].toppings.all()), 2)
        self.assertEqual(len(ss[1].toppings.all()), 2)

        # 重点: 这里使用toppings.filter()将会重新克隆一个QuerySet出来, 重构where条件, 所以这里会查询数据库.
        # SELECT `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM   `prefetch_related__topping`
        #        INNER JOIN `prefetch_related__pizza_toppings` ON
        #        (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE (`prefetch_related__pizza_toppings`.`pizza_id` = 1 AND
        #        `prefetch_related__topping`.`name` = 'ham')
        self.assertEqual(len(ss[0].toppings.filter(name="ham")), 1)

    def test_c_prefetch_related2(self):
        # 准备数据
        # 准备 Topping 数据
        ham = Topping.objects.create(name="ham")
        pineapple = Topping.objects.create(name="pineapple")
        prawns = Topping.objects.create(name="prawns")
        smoked_salmon = Topping.objects.create(name="smoked salmon")
        # 准备 Pizza 数据 和 对应的多对多字段数据的填充.
        hawaiian = Pizza.objects.create(name="Hawaiian")
        hawaiian.toppings.add(*[ham, pineapple])
        seafood = Pizza.objects.create(name="Seafood")
        seafood.toppings.add(*[prawns, smoked_salmon])
        # 准备 Restaurant 数据
        restaurant = Restaurant.objects.create(best_pizza=hawaiian)
        restaurant.pizzas.add(hawaiian)

        # 第一步: 查询 restaurant 表的所有数据
        # SELECT `prefetch_related__restaurant`.`id`,
        #        `prefetch_related__restaurant`.`best_pizza_id`
        # FROM `prefetch_related__restaurant`
        #
        # 第二步: 处理多对多
        # pizza 表 INNER JOIN restaurant_pizzas 关联表, 合并成临时表, 然后再匹配 关联表.`restaurant_id`.
        # SELECT (`prefetch_related__restaurant_pizzas`.`restaurant_id`) AS `_prefetch_related_val_restaurant_id`,
        #        `prefetch_related__pizza`.`id`,
        #        `prefetch_related__pizza`.`name`
        # FROM   `prefetch_related__pizza`
        #        INNER JOIN `prefetch_related__restaurant_pizzas` ON
        #        (`prefetch_related__pizza`.`id` = `prefetch_related__restaurant_pizzas`.`pizza_id`)
        # WHERE `prefetch_related__restaurant_pizzas`.`restaurant_id` IN (1)
        #
        # 第三步: 处理子级表的多对多
        # topping 表 INNER JOIN pizza_toppings 关联表, 合并成临时表, 然后再匹配 关联表的.`pizza_id`.
        # SELECT (`prefetch_related__pizza_toppings`.`pizza_id`) AS `_prefetch_related_val_pizza_id`,
        #        `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM   `prefetch_related__topping`
        #        INNER JOIN `prefetch_related__pizza_toppings` ON
        #        (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE `prefetch_related__pizza_toppings`.`pizza_id` IN (1)
        rr = Restaurant.objects.prefetch_related('pizzas__toppings')
        self.assertEqual(len(rr), 1)
        # 使用 all 接口, 不会再去查数据库, 而是直接使用缓存.
        self.assertEqual(len(rr[0].pizzas.all()), 1)

    def test_d_prefetch_related_and_select_related(self):
        # 准备数据
        # 准备 Topping 数据
        ham = Topping.objects.create(name="ham")
        pineapple = Topping.objects.create(name="pineapple")
        prawns = Topping.objects.create(name="prawns")
        smoked_salmon = Topping.objects.create(name="smoked salmon")
        # 准备 Pizza 数据 和 对应的多对多字段数据的填充.
        hawaiian = Pizza.objects.create(name="Hawaiian")
        hawaiian.toppings.add(*[ham, pineapple])
        seafood = Pizza.objects.create(name="Seafood")
        seafood.toppings.add(*[prawns, smoked_salmon])
        # 准备 Restaurant 数据
        restaurant = Restaurant.objects.create(best_pizza=hawaiian)
        restaurant.pizzas.add(hawaiian)

        # 第一步:
        # 这条SQL的服务对象: select_related('best_pizza'), 该对象是一个外键指向的是Pizza表.
        # 一句话总结这条SQL: 把所有存在于 restaurant 中的 pizza 数据都提取出来(INNER JOIN 是产生临时表, 把两张表的数据都合在一起).
        # SELECT `prefetch_related__restaurant`.`id`,
        #        `prefetch_related__restaurant`.`best_pizza_id`,
        #        `prefetch_related__pizza`.`id`,
        #        `prefetch_related__pizza`.`name`
        # FROM   `prefetch_related__restaurant`
        #        INNER JOIN `prefetch_related__pizza` ON
        #        (`prefetch_related__restaurant`.`best_pizza_id` = `prefetch_related__pizza`.`id`)
        #
        # 第二步
        # IN (1) 表示第一步返回的数据中只有一条数据, 所以这里只取这一条数据的id作为范围匹配.
        #        如果第一步返回的数据中是多条数据, 那么这里就是用 (id_1, id_2, id_3, ...) 范围来匹配
        #
        # 这条SQL的服务对象: prefetch_related('best_pizza__toppings'), 即: Pizza.toppings 对象(它是一个多对多的对象).
        # 一句话总结这条SQL: INNER JOIN 把 topping(配料表) 和 pizza_toppings(关联表) 合在一起,
        #                  然后筛选出隶属于 in (pizza_id_1, pizza_id_2, pizza_id_3, ...) 中的数据.
        #
        # SELECT (`prefetch_related__pizza_toppings`.`pizza_id`) AS `_prefetch_related_val_pizza_id`,
        #        `prefetch_related__topping`.`id`,
        #        `prefetch_related__topping`.`name`
        # FROM   `prefetch_related__topping`
        #        INNER JOIN `prefetch_related__pizza_toppings` ON
        #        (`prefetch_related__topping`.`id` = `prefetch_related__pizza_toppings`.`topping_id`)
        # WHERE `prefetch_related__pizza_toppings`.`pizza_id` IN (1)
        rr = Restaurant.objects.select_related('best_pizza').prefetch_related('best_pizza__toppings')
        self.assertEqual(len(rr), 1)
        # 使用 all 接口, 不会再去查数据库, 而是直接使用缓存.
        self.assertEqual(len(rr[0].best_pizza.toppings.all()), 2)
