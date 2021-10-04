from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from .models import Book


# Create your views here.
def index_view(request):
    # perms = Permission.objects.filter(name="Can view group")
    # list(perms)

    # SELECT     `auth_permission`.`id`,
    #            `auth_permission`.`name`,
    #            `auth_permission`.`content_type_id`,
    #            `auth_permission`.`codename`
    # FROM       `auth_permission`
    # INNER JOIN `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
    # ORDER BY   `django_content_type`.`app_label` ASC,
    #            `django_content_type`.`model` ASC,
    #            `auth_permission`.`codename` ASC
    #
    # SELECT     `auth_permission`.`id`,
    #            `auth_permission`.`name`,
    #            `auth_permission`.`content_type_id`,
    #            `auth_permission`.`codename`
    # FROM       `auth_permission`
    # INNER JOIN `auth_group_permissions` ON (`auth_permission`.`id` = `auth_group_permissions`.`permission_id`)
    # INNER JOIN `auth_group` ON (`auth_group_permissions`.`group_id` = `auth_group`.`id`)
    # INNER JOIN `auth_user_groups` ON (`auth_group`.`id` = `auth_user_groups`.`group_id`)
    # INNER JOIN `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
    # WHERE      `auth_user_groups`.`user_id` = 1
    # ORDER BY   `django_content_type`.`app_label` ASC,
    #            `django_content_type`.`model` ASC,
    #            `auth_permission`.`codename` ASC';
    # perms = Permission.objects.filter(group__user=request.user)
    # list(perms)
    #
    # 线索，这里采用的是 一对多反向的方式来查找数据
    perms = Permission.objects.filter(group__user=1)
    list(perms)

    #
    # pub = Publisher.objects.filter(name="shanghai tushuguan")
    # if not pub:
    #     pk = Publisher(name="shanghai tushuguan").save()
    #     pub = Publisher.objects.get(pk=pk)
    # else:
    #     pub = pub[0]
    #
    # ss = pub.book_set.all()
    # print(ss)

    # 由于 Permission 定义了 content_type 外键字段,
    # 所以 Permission.objects.all() 会 inner join `django_content_type` 表.
    #
    # 其中 django_content_type 表, 存储的是 app 和 python model name 的对应表,
    # 即: 继承了 models.Model 对象的 Model 对象.
    #
    # SELECT `auth_permission`.`id`,
    #        `auth_permission`.`name`,
    #        `auth_permission`.`content_type_id`,
    #        `auth_permission`.`codename`
    # FROM `auth_permission`
    # INNER JOIN `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
    # ORDER BY `django_content_type`.`app_label` ASC,
    #          `django_content_type`.`model` ASC,
    #          `auth_permission`.`codename` ASC';
    # perms = Permission.objects.all()
    # list(perms)

    # users = User.objects.all()
    # list(users)

    # TODO: 为什么 Book.objects.all() 没有查询 ForeignKey 的字段,
    #       而 Permission.objects.all() 却会查询 ForeignKey 的字段.
    # books = Book.objects.all()
    # list(books)

    return HttpResponse(b"hello world!")


def index_view_2(request):
    content_type = ContentType.objects.get(pk=1)
    permissions = content_type.permission_set.all()
    return HttpResponse(b"hello world!")