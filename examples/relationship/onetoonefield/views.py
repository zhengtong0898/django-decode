from django.shortcuts import HttpResponse
from .models import Place, Restaurant


def multi_create(request):

    # 从主表角度查询补充表
    # SELECT `onetoonefield_place`.`id`,
    #        `onetoonefield_place`.`name`,
    #        `onetoonefield_place`.`address`
    # FROM   `onetoonefield_place`
    # WHERE  `onetoonefield_place`.`id` = 1
    # LIMIT  21
    sha_xian = Place.objects.get(pk=1)
    # TODO: restaurant 是在什么情况下写入到 sha_xian 这个 Place 对象中的?
    # SELECT `onetoonefield_restaurant`.`place_id`,
    #        `onetoonefield_restaurant`.`serves_hot_dogs`,
    #        `onetoonefield_restaurant`.`serves_pizza`
    # FROM   `onetoonefield_restaurant`
    # WHERE  `onetoonefield_restaurant`.`place_id` = 1
    # LIMIT  21
    print(sha_xian.restaurant.serves_hot_dogs)

    # 从补充表角度查询主表
    # SELECT `onetoonefield_restaurant`.`place_id`,
    #        `onetoonefield_restaurant`.`serves_hot_dogs`,
    #        `onetoonefield_restaurant`.`serves_pizza`
    # FROM   `onetoonefield_restaurant`
    # WHERE  `onetoonefield_restaurant`.`place_id` = 1
    # LIMIT  21
    restaurant = Restaurant.objects.get(pk=1)
    # SELECT `onetoonefield_place`.`id`, `onetoonefield_place`.`name`, `onetoonefield_place`.`address`
    # FROM   `onetoonefield_place`
    # WHERE  `onetoonefield_place`.`id` = 1
    # LIMIT  21
    print(restaurant.place.name)

    return HttpResponse("hello world!")