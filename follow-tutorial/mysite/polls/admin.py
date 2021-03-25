from django.contrib import admin
from .models import Question, Choice


# Register your models here.
class ChoiceInline(admin.StackedInline):                # admin.StackedInline 栈排列
    model = Choice
    extra = 1                                           # 展示几条数据空数据(不含已由数据)
    verbose_name_plural = "投票关联表"                   # 栏目名称


class ChoiceTabularInline(admin.TabularInline):         # admin.TabularInline 表格排列
    model = Choice
    extra = 1
    verbose_name_plural = "投票关联表"


class QuestionAdmin(admin.ModelAdmin):
    # 控制字段顺序
    # fields = ['pub_date', 'question_text']

    # 将字段按栏目分组
    fieldsets = [
        ['必填字段',                                     # 栏目名称
         {'fields': ['question_text']}],                # 字段顺序

        ['非必填字段',                                   # 栏目名称
         {'fields': ['pub_date'],                       # 字段顺序
          'classes': ['collapse']}]                     # 收起或展开: 可用于隐藏非必填字段, 简化表单信息.
    ]

    # 显示关联表信息
    inlines = [ChoiceTabularInline]

    # 列表每行显示哪些字段
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # 按类型筛选, bool(会有两个筛选条件), 时间(会有today/past 7 days/this month/this year筛选条件)
    list_filter = ['pub_date']

    # 模糊查询: 根据给定的字段进行模糊查询.
    # 如果只给定 question_text 字段, 那么就只搜索question_text.
    # 如果给定 question_text 和 pub_date, 那么任意一个字段匹配命中都会显示该行数据.
    search_fields = ['question_text', 'pub_date']


admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
