from django.contrib import admin
from .models import Article2
from django.contrib import messages
from django.utils.translation import ngettext


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    ordering = ['title']                         # 排序

    # actions = None                             # 关闭批量操作(页面中将不在显示批量操作下拉菜单)

    actions = ['make_published']                 # 批量操作(按make_published函数来操作: 批量更新发布状态.)

    # actions_selection_counter = False          # 默认是True, 表示显示已选中计数器; 设定为False则表示不显示计数器.

    # actions_on_top = False                     # actions_on_top 和 actions_on_bottom 需要两个同时配置, 如果两个都是True,
    # actions_on_bottom = True                   # 那么会再头部显示一行批量操作栏, 再底部也显示一行批量操作栏.

    def make_published(self, request, queryset):
        # queryset.update 返回的是一个数字,
        # 表示更新了几条数据.
        updated = queryset.update(status='p')       # queryset 是一个集合对象, update 可以批量对集合做更新操作.

        # 第一个参数: request: HttpRequest
        # 第二个参数: message: str
        # 第三个参数: level: int
        #
        # 其中 message = ngettext(str1, str2, number),
        # ngettext内部源码: 当 number 是 1 时, 返回 str1, 否则返回 str2.
        #
        # 第三个参数: 这里填写的是: messages.SUCCESS; 页面中将会显示绿色背景的提示条.
        #            除了 SUCCESS(绿色) , 有效的值还有  INFO(绿色) / WARNING(黄色) / ERROR(红色) .
        self.message_user(request, ngettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.ERROR)

    make_published.short_description = "Mark selected stories as published"

    # get_actions 是 admin.ModelAdmin 的公开接口,
    # 这里重新定义(覆盖)这个接口, 用于根据不同条件来返回不同的actions.
    def get_actions(self, request):

        # 执行父类的get_actions方法, 用于获取 actions.
        actions = super().get_actions(request)

        # 如果某个用户满足某个条件, 并且 actions 中含有 delete_selected, 那么就把它删除掉.
        # 所以, 想要根据什么条件返回什么actions, 在这里写具体的条件即可.
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']

        return actions


admin.site.register(Article2, ArticleAdmin)