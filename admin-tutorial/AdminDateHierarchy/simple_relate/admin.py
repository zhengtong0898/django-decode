from django.contrib import admin
from .models import ArticleModel, AuthorModel


# Register your models here.
class AuthorModelAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'author',
                    'date_joined',
                    'author__date_joined', 'custom_field']

    # 普通字段, 这里仅需填写字段名.
    # 如果字段是一个关联字段, 那么这里可以用双下滑线表示要显示关联表中的那个字段(必须是时间类型字段).
    date_hierarchy = 'author__date_joined'

    def author__date_joined(self, queryset):
        return queryset.author.date_joined

    author__date_joined.short_description = "作者加入时间(这是一个关联延申字段)"

    radio_fields = {'author': admin.HORIZONTAL}

    autocomplete_fields = ('author', )

    readonly_fields = ('custom_field', )

    def custom_field(self, model):
        """
        可以在这里显示额外的字段, 以html形式返回, 想提供什么链接都可以.
        readonly_fields 属性, 不适合对已有字段设定readonly,
        因为在新增的时候该字段也不能添加, 这不符合使用场景;
        readonly_fields 更适合额外增加多个自定义字段展示.
        """
        from django.utils.safestring import mark_safe
        return mark_safe("<span class='errors'>show something</span>")

    prepopulated_fields = {"slug": ("title", 'content')}

    from django.db import models
    from django.forms import TextInput

    # 一般情况下, TextField 通过多态重定义 self.formfield 方法,
    # 在该方法内声明 {'widget': forms.Textarea }, 进而可以在页面中显示 TextArea 表单控件.
    #
    # formfield_overrides 在这里将 forms.Textarea 改为 forms.CharField 控件对象.
    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }

    # 该属性作用在 change 编辑页面.
    # False 时, 表单底部显示 'Save and add another' 按钮
    # True 时, 表单底部显示 'save as new' 按钮
    #
    # 'save as new' 的作用是, 当模块表单字段过多, 新建一条数据时间成本较高时,
    # 可以采取编辑一条数据, 按需更改几个必要字段后, 点击 'save as new' 完成一条数据的创建.
    save_as = True

    # 开启这个属性, 会出现两行按钮保存栏, 他们分别出现在表单的头部和表单的底部.
    save_on_top = True

    save_as_continue = False

admin.site.register(ArticleModel, ArticleModelAdmin)
admin.site.register(AuthorModel, AuthorModelAdmin)