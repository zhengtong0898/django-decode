### 如何理解模型关系中的正向关联和反向关联?
**关键词:** [related_name](https://docs.djangoproject.com/zh-hans/3.2/ref/models/fields/#django.db.models.ForeignKey.related_name)

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
  反向关联查询是通过 特定属性(关联表名 + '_set') 去查询关联表的值.
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
**Tip-1**: 反向关联查询的特定属性(关联表名 + '_set')，[定义在这里](../../src/Django-3.0.8/django/db/models/fields/reverse_related.py#L172).
