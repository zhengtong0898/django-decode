# 概述
由于个人水平不足，无法量化触发 `InnerJoin` 的所有场景, 所以当前文档主要的目的是记录在学习和使用过程中触发 `InnerJoin` 的声明.  

# 排序声明
`Django ORM` 的 `Meta` 元数据选项中, 支持 `ordering` 选项,  
`Model.Meta.ordering` 选项用于更改 `Model` 的默认表现.  

当 `Model.Meta.ordering` 列表中, 包含了 `外键表` 的字段时,   
`Django ORM` 的查询将会从 `单表查询` 变更为 `InnerJoin` 查询.  

模板分析:  
```python3
class Permission(models.Model):
    
    name = models.CharField(_('name'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('content type'),
    )
    codename = models.CharField(_('codename'), max_length=100)

    objects = PermissionManager()

    class Meta:
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        unique_together = [['content_type', 'codename']]
        
        # Permission.content_type 是外键字段, 即: Permission 和 ContentType 是 多对一关系.  
        # content_type__app_label 和 content_type__model 会触发 InnerJoin 查询.  
        ordering = ['content_type__app_label', 'content_type__model', 'codename']    # 关键点在这里

    def __str__(self):
        return '%s | %s' % (self.content_type, self.name)

    def natural_key(self):
        print("==== natural_key ====")
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']
```

查询案例:   
```python3
from django.contrib.auth.models import Permission


# SELECT 
#            `auth_permission`.`id`,
#            `auth_permission`.`name`,
#            `auth_permission`.`content_type_id`,
#            `auth_permission`.`codename`
# FROM 
#            `auth_permission`
# INNER JOIN 
#            `django_content_type` ON (`auth_permission`.`content_type_id` = `django_content_type`.`id`)
# ORDER BY 
#            `django_content_type`.`app_label` ASC,
#            `django_content_type`.`model` ASC,
#            `auth_permission`.`codename` ASC';
perms = Permission.objects.all()
list(perms)                                    # 触发 sql
```