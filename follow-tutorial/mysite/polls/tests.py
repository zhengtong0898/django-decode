import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


# django会找到所有继承了 django.test.TestCase 的对象,
# 并执行那些 test_ 开头的方法的测试用例.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        # time 是下个月的时间, 所以 future_question 是下个月的问题.
        # 断言期望: future_question.was_published_recently() == False
        # 当 future_question.was_published_recently() == False 时, 测试成功.
        # 当 future_question.was_published_recently() == True 时, 测试失败, 抛出异常.
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        # 边界值测试
        # 测试场景: 当 pub_date 是 1天零1秒前 时, 它不属于最近发布.
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        # 边界值测试
        # 测试场景: 当 pub_date 是 1天内时(即便时: 23:59:59秒之前), 它都属于最近发布.
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
