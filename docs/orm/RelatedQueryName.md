###  什么是`ORM`的反向过滤器?  
反向过滤器指的是, 利用 `Python` 的反射机制语法, 以字符串形式将小写的模型名称传递给 `filter` 过滤器进行查询.  
`Django` 会根据模型定义的关联关系, 自动的帮你组装好 join 的查询语句, 完成关联查询的动作.  

models.py
```python3
from django.db import models
from django.utils.translation import gettext_lazy as _


class SimulateContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(_('python model class name'), max_length=100)


class SimulatePermission(models.Model):
    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        SimulateContentType,
        models.CASCADE,
        verbose_name=_('content type'),
        related_name="sp_set"
    )
    codename = models.CharField(_('codename'), max_length=100)
```

views.py
```python3
from django.shortcuts import render, HttpResponse
from .models import SimulateContentType, SimulatePermission


def index_view(request):
    """
    四种查询方式, 同一时间仅能选择其中一种

    当前函数不能直接运行，需要对模型进行相应操作, 并注释掉其中三种查询方式, 才能运行.
    """

    # 查询方式-1
    # 1). 取消模型中的定义 ForeignKey.related_name = "sp_set"
    # 2). 取消模型中的定义 ForeignKey.related_query_name = "sp"
    simulate_data_1 = SimulateContentType.objects.filter(**{"simulatepermission__id": "1"})
    # SELECT
    #            `reverse_filter_query_simulatecontenttype`.`id`, '
    #            `reverse_filter_query_simulatecontenttype`.`app_label`,
    #            `reverse_filter_query_simulatecontenttype`.`model`
    # FROM
    #            `reverse_filter_query_simulatecontenttype`
    # INNER JOIN
    #            `reverse_filter_query_simulatepermission` ON (`reverse_filter_query_simulatecontenttype`.`id` = `reverse_filter_query_simulatepermission`.`content_type_id`)
    # WHERE
    #            `reverse_filter_query_simulatepermission`.`id` = 1 LIMIT 21
    print("simulate_data_1: ", simulate_data_1)

    # 查询方式-2
    # 1). 在模型中定义 ForeignKey.related_name = "sp_set"
    simulate_data_1 = SimulateContentType.objects.filter(**{"sp_set__id": "1"})
    # SELECT
    #            `reverse_filter_query_simulatecontenttype`.`id`,
    #            `reverse_filter_query_simulatecontenttype`.`app_label`,
    #            `reverse_filter_query_simulatecontenttype`.`model`
    # FROM
    #            `reverse_filter_query_simulatecontenttype`
    # INNER JOIN
    #            `reverse_filter_query_simulatepermission` ON (`reverse_filter_query_simulatecontenttype`.`id` = `reverse_filter_query_simulatepermission`.`content_type_id`)
    # WHERE
    #            `reverse_filter_query_simulatepermission`.`id` = 1
    print("simulate_data_1: ", simulate_data_1)

    # 查询方式-3
    # 1). 在模型中定义 ForeignKey.related_name = "sp_set"
    # 2). 在模型中定义 ForeignKey.related_query_name = "sp"
    simulate_data_1 = SimulateContentType.objects.filter(**{"sp__id": "1"})
    # SELECT
    #            `reverse_filter_query_simulatecontenttype`.`id`,
    #            `reverse_filter_query_simulatecontenttype`.`app_label`,
    #            `reverse_filter_query_simulatecontenttype`.`model`
    # FROM
    #            `reverse_filter_query_simulatecontenttype`
    # INNER JOIN
    #            `reverse_filter_query_simulatepermission` ON (`reverse_filter_query_simulatecontenttype`.`id` = `reverse_filter_query_simulatepermission`.`content_type_id`)
    # WHERE
    #            `reverse_filter_query_simulatepermission`.`id` = 1
    print("simulate_data_1: ", simulate_data_1)

    # 查询方式-4
    # 1). 在模型中定义 ForeignKey.related_name = "sp_set"
    # 2). 在模型中定义 ForeignKey.related_query_name = "sp"
    # 3). 先查好 SimulatePermission 对象数据.
    # 4). 然后再根据 SimulatePermission 对象 反向过滤查询.
    simulate_permission_1 = SimulatePermission.objects.get(pk=1)
    simulate_data_1 = SimulateContentType.objects.filter(**{"sp": simulate_permission_1})
    # SELECT
    #            `reverse_filter_query_simulatecontenttype`.`id`,
    #            `reverse_filter_query_simulatecontenttype`.`app_label`,
    #            `reverse_filter_query_simulatecontenttype`.`model`
    # FROM
    #            `reverse_filter_query_simulatecontenttype`
    # INNER JOIN
    #            `reverse_filter_query_simulatepermission` ON (`reverse_filter_query_simulatecontenttype`.`id` = `reverse_filter_query_simulatepermission`.`content_type_id`)
    # WHERE
    #            `reverse_filter_query_simulatepermission`.`id` = 1;
    print("simulate_data_1: ", simulate_data_1)

    return HttpResponse("hello world!")
```

### 参考  
1. [ForeignKey.related_query_name](https://docs.djangoproject.com/zh-hans/3.2/ref/models/fields/#django.db.models.ForeignKey.related_query_name)
2. [Options.default_related_name](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/#django.db.models.Options.default_related_name)
3. [Lookups that span relationships](https://docs.djangoproject.com/en/3.2/topics/db/queries/#lookups-that-span-relationships)
