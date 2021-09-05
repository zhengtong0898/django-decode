from django.shortcuts import HttpResponse
from .models import Place, Restaurant


def multi_create(request):

    # TODO: 为什么 dir(sha_xian) 会拥有 restaurant 属性.
    #
    # INSERT INTO `onetoonefield_place` (`name`, `address`)
    # VALUES ("全家便利店", "毕升路191号")
    # RETURNING `onetoonefield_place`.`id`
    sha_xian = Place(name="全家便利店", address="毕升路191号")
    sha_xian.save()

    # Question: 为什么一个 save 会触发 update 和 insert 这两个 sql ?
    #           当提交的 value 所对应的字段是一个 foreign key,
    #           Django 将会先执行 update 然后在根据返回值决定是否要执行 insert.
    #
    #           先执行 update,
    #           如果执行失败, 那么将会执行 insert.
    #           如果执行成功, 则不会去执行 insert.
    #
    # Question: 如何判定 update 是否成功?
    #           update 会返回 effect_rows, 表明成功更新了多少条数据.
    #           当 effect_rows 大于 0 时, 表明更新成功.
    #           当 effect_rows 等于 0 时, 表明没有更新成功.
    #
    #
    # UPDATE `onetoonefield_restaurant`
    # SET    `serves_hot_dogs` = 1,
    #        `serves_pizza` = 0
    # WHERE  `onetoonefield_restaurant`.`place_id` = 1;
    #
    # INSERT INTO `onetoonefield_restaurant` (`place_id`, `serves_hot_dogs`, `serves_pizza`)
    # VALUES (1, 1, 0);
    restaurant = Restaurant(place=sha_xian, serves_hot_dogs=True, serves_pizza=False)
    restaurant.save()

    restaurant = Restaurant(place=sha_xian, serves_hot_dogs=True, serves_pizza=True)
    restaurant.save()

    # TODO: 为什么会触发一条 update 和 一条 insert ?
    #       pymysql.cursors._do_get_result
    #       result.insert_id  对应的是 lastrowid, 对应的是什么?
    #       result.rows 对应的是 什么?
    #       result.description 和什么组成字典?  参考 torndb ?
    #
    #
    # TODO: many-to-one 的 save 也是触发 update 和 insert 吗?
    # TODO: many-to-many 的 save 也是触发 update 和 insert 吗?

    # TODO: 手动在 mysql 交互命令行执行下面这条sql返回值是什么?
    #       UPDATE `onetoonefield_restaurant` SET `serves_hot_dogs` = 1, `serves_pizza` = 1 WHERE `onetoonefield_restaurant`.`place_id` = 7'
    #       在 pymysql 中返回值如下; pymysql 需要提取这段文本的内容.
    #       b'\x00\x01\x00\x02\x00\x00\x00(Rows matched: 1  Changed: 1  Warnings: 0'

    # TODO: insert 插入一条数据, 它是如何获取 insert id 的呢?
    #       insert 时指定 RETURNING 关键词.


    return HttpResponse("hello world!")