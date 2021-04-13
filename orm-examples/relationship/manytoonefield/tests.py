from datetime import date
from django.test import TestCase, TransactionTestCase
from .models import Reporter, Article


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_n_plus_1(self):
        # 准备数据
        r = Reporter.objects.create(first_name='John', last_name='Smith', email='john@example.com')
        Article.objects.create(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)

        # 查询数据
        # SELECT `manytoonefield_article`.`id`,
        #        `manytoonefield_article`.`headline`,
        #        `manytoonefield_article`.`pub_date`,
        #        `manytoonefield_article`.`reporter_id`
        # FROM `manytoonefield_article`
        # WHERE `manytoonefield_article`.`id` = 1
        # LIMIT 21
        article = Article.objects.get(pk=1)

        # SELECT `manytoonefield_reporter`.`id`,
        #        `manytoonefield_reporter`.`first_name`,
        #        `manytoonefield_reporter`.`last_name`,
        #        `manytoonefield_reporter`.`email`
        # FROM `manytoonefield_reporter`
        # WHERE `manytoonefield_reporter`.`id` = 1
        # LIMIT 21
        self.assertEqual(article.reporter, r)

    def test_b_the_case(self):
        # 准备数据
        r = Reporter.objects.create(first_name='John', last_name='Smith', email='john@example.com')
        Article.objects.create(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)

        # 查询数据
        # SELECT `manytoonefield_article`.`id`,
        #        `manytoonefield_article`.`headline`,
        #        `manytoonefield_article`.`pub_date`,
        #        `manytoonefield_article`.`reporter_id`,
        #        `manytoonefield_reporter`.`id`,
        #        `manytoonefield_reporter`.`first_name`,
        #        `manytoonefield_reporter`.`last_name`,
        #        `manytoonefield_reporter`.`email`
        # FROM `manytoonefield_article`
        # INNER JOIN `manytoonefield_reporter`
        #       ON (`manytoonefield_article`.`reporter_id` = `manytoonefield_reporter`.`id`)
        # WHERE `manytoonefield_article`.`id` = 1
        # LIMIT 21
        article = Article.objects.select_related('reporter').get(pk=1)
        self.assertEqual(article.reporter, r)

    def test_c_the_reverse_side(self):
        # 准备数据
        r = Reporter.objects.create(first_name='John', last_name='Smith', email='john@example.com')
        a = Article.objects.create(headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)

        # 查询数据
        # SELECT `manytoonefield_reporter`.`id`,
        #        `manytoonefield_reporter`.`first_name`,
        #        `manytoonefield_reporter`.`last_name`,
        #        `manytoonefield_reporter`.`email`
        # FROM `manytoonefield_reporter`
        # WHERE `manytoonefield_reporter`.`id` = 1
        # LIMIT 21
        reporter = Reporter.objects.get(pk=1)

        # 一对多和多对多的被指向对象, 只能通过 tablename_set.all() 的方式来方向查找关联数据.
        # 一对一的被指向对象, 可以通过 select_related() 的方式来查找关联, 也就是说, 一对一关系, 双边都是ForeignKey.
        #
        # article_set 被理解为是 manytoonefield_article 表.
        # 站在Reporter的角度来看, 这就是 OneToMany.
        # SELECT `manytoonefield_article`.`id`,
        #        `manytoonefield_article`.`headline`,
        #        `manytoonefield_article`.`pub_date`,
        #        `manytoonefield_article`.`reporter_id`
        # FROM `manytoonefield_article`
        # WHERE `manytoonefield_article`.`reporter_id` = 1
        # ORDER BY `manytoonefield_article`.`headline` ASC
        articles = reporter.article_set.all()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0], a)
