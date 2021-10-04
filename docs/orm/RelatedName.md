### 如何理解模型关系中的正向关联和反向关联?
&nbsp;  
**正向关联:**   
在模型中声明了外键字段(产生了关联关系), 这种主动建立的关联关系, 被称为正向关联.  

**反向关联:**   
在模型中并没有声明任何关联字段, 并没有主动产生关联关系;   
但是在其他模型中声明了外键字段并指向了当前模型, 这种被动产生的关系，被称为反向关联.  

> **术语纠正**  
> 正向关联和反向关联不是一个名词术语，它们两是一个动词, 对应的分别是: 正向关联查询 和 反向关联查询.  


- 站在不同的角度去看两个模型
  ```shell
  
  # 被动: 没有声明任何关联关系, 但是它被 Permission.content_type 指向, 此时它们存在着关联关系.
  class ContentType(models.Model):                                                 
      app_label = models.CharField(max_length=100)
      model = models.CharField(_('python model class name'), max_length=100)
  

  # 主动: 声明外键字段，与 ContentType 建立关联关系.
  class Permission(models.Model):
      
      name = models.CharField(_('name'), max_length=255)
      content_type = models.ForeignKey(                                                                 
          ContentType,
          models.CASCADE,
          verbose_name=_('content type'),
      )
      codename = models.CharField(_('codename'), max_length=100)

  ```

- 通过关联字段: 正向查询关联表  
  正向关联查询是通过声明的字段名去查询关联表的值.
  ```shell
  # SELECT 
  #        `auth_permission`.`id`, 
  #        `auth_permission`.`name`, 
  #        `auth_permission`.`content_type_id`, 
  #        `auth_permission`.`codename` 
  # FROM 
  #        `auth_permission` 
  # WHERE 
  #        `auth_permission`.`id` = 1 
  # LIMIT   21
  perm_1 = Permission.objects.get(pk=1)           # 主表现查询到结果
  
  # SELECT 
  #         `django_content_type`.`id`, 
  #         `django_content_type`.`app_label`, 
  #         `django_content_type`.`model` 
  # FROM 
  #         `django_content_type` 
  # WHERE 
  #         `django_content_type`.`id` = 1 
  # LIMIT 21
  app_label = perm_1.content_type.app_label       # 然后在根据结果对象，再查询关联表的数据.
  ```
  
- 通过被关联字段: 反向查询关联表  
  反向关联查询是通过 [特定属性(关联表名 + '_set')](../../src/Django-3.0.8/django/db/models/fields/reverse_related.py#L167) 去查询关联表的值.
  ```shell
  # SELECT 
  #        `django_content_type`.`id`, 
  #        `django_content_type`.`app_label`, 
  #        `django_content_type`.`model` 
  # FROM 
  #        `django_content_type` 
  # WHERE 
  #        `django_content_type`.`id` = 1 
  # LIMIT 21
  content_type = ContentType.objects.get(pk=1)
  
  # SELECT     `auth_permission`.`id`, 
  #            `auth_permission`.`name`, 
  #            `auth_permission`.`content_type_id`, 
  #            `auth_permission`.`codename` 
  # FROM 
  #            `auth_permission` 
  # INNER JOIN 
  #            `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`) 
  # WHERE      
  #            `auth_permission`.`content_type_id` = 1 
  # ORDER BY 
  #            `django_content_type`.`app_label` ASC, 
  #            `django_content_type`.`model` ASC, 
  #            `auth_permission`.`codename` ASC
  permissions = content_type.permission_set.all()
  ```
    
&nbsp;  
### 参数验证
所有的关联关系对象都提供了一个可选的配置参数，即: [related_name](https://docs.djangoproject.com/zh-hans/3.2/ref/models/fields/#django.db.models.ForeignKey.related_name).  
该参数默认值是None, 它会为模型的实例对象附加一个 '关联表名_set' 的属性, 用于反向查找关联表的数据, 案例请参考上述 "通过被关联字段: 反向查询关联表".  
当为 `related_name` 提供参数值时, 他会为模型的实例对象附加一个 `related_name` 的属性, 用于反向查找关联表的数据, 例如:  
```shell


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


def index(request):
    simulate_content_type = SimulateContentType.objects.get(pk=1)

    # related_name='sp_set' 所以就不会有 simulatepermission_set 这个属性.
    # ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__',
    #  '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__',
    #  '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
    #  '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__',
    #  '_check_column_name_clashes', '_check_constraints', '_check_field_name_clashes', '_check_fields',
    #  '_check_id_field', '_check_index_together', '_check_indexes', '_check_local_fields', '_check_long_column_names',
    #  '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_model_name_db_lookup_clashes',
    #  '_check_ordering', '_check_property_name_related_field_accessor_clashes', '_check_single_primary_key',
    #  '_check_swappable', '_check_unique_together', '_do_insert', '_do_update', '_get_FIELD_display',
    #  '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks',
    #  '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val',
    #  '_state', 'app_label', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'from_db', 'full_clean',
    #  'get_deferred_fields', 'id', 'model', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save',
    #  'save_base', 'serializable_value', 'sp_set', 'unique_error_message', 'validate_unique']
    print(dir(simulate_content_type))

    # <QuerySet [<SimulatePermission: SimulatePermission object (1)>,
    #            <SimulatePermission: SimulatePermission object (2)>,
    #            <SimulatePermission: SimulatePermission object (3)>,
    #            <SimulatePermission: SimulatePermission object (4)>]>
    print(simulate_content_type.sp_set.all())
    return HttpResponse("hello world!")

```
