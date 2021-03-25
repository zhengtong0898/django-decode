import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):

    # verbose_name: 列表头(column head)
    question_text = models.CharField(verbose_name='问题标题', max_length=200)
    pub_date = models.DateTimeField(verbose_name='发布时间')

    def was_published_recently(self):
        # problem
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        #
        # fix:
        now = timezone.now()
        # now - datetime.timedelta(days=1)      == yesterday
        # yesterday <= self.pub_date            == 一天内发布的
        # self.pub_date <=                      == 不能是未来的时间
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # 给 was_published_recently 方法添加一些属性.
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '近期发布?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)