from django.shortcuts import render
from django.http import HttpResponse
from .models import product


# Create your views here.
def index_view(request):
    # 批量插入1000条数据, 每一批插入10条数据.
    items = []
    for i in range(10000):
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
    ss = product.objects.bulk_create(objs=items, batch_size=1000)

    product.objects.all().delete()
    return HttpResponse(b"hello world!")
