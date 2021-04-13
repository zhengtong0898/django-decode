from django.test import TestCase, TransactionTestCase
from .models import Publication, Article


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_n_plus_1(self):
        # 准备数据
        p1 = Publication.objects.create(title='The Python Journal')
        p2 = Publication.objects.create(title='Science News')
        p3 = Publication.objects.create(title='Science Weekly')

        # 准备数据
        # INSERT INTO `manytomanyfield_article` (`headline`)
        # VALUES ('Django lets you build Web apps easily') RETURNING `manytomanyfield_article`.`id`
        a = Article.objects.create(headline='Django lets you build Web apps easily')

        # 准备数据: 一次性插入两条数据.
        # INSERT IGNORE INTO `manytomanyfield_article_publications` (`article_id`, `publication_id`)
        # VALUES (1, 1), (1, 2)
        a.publications.add(p1, p2)

        # 准备数据: 一次性插入一条数据
        # INSERT IGNORE INTO `manytomanyfield_article_publications` (`article_id`, `publication_id`)
        # VALUES (1, 3)
        a.publications.add(p3)

        # SELECT `manytomanyfield_article`.`id`,
        #        `manytomanyfield_article`.`headline`
        # FROM `manytomanyfield_article`
        # WHERE `manytomanyfield_article`.`id` = 1
        # LIMIT 21
        aa = Article.objects.get(pk=1)

        # SELECT `manytomanyfield_publication`.`id`,
        #        `manytomanyfield_publication`.`title`
        # FROM `manytomanyfield_publication`
        # INNER JOIN `manytomanyfield_article_publications`
        #       ON (`manytomanyfield_publication`.`id` = `manytomanyfield_article_publications`.`publication_id`)
        # WHERE `manytomanyfield_article_publications`.`article_id` = 1
        # ORDER BY `manytomanyfield_publication`.`title` ASC
        pp = aa.publications.all()                                     # n + 1
        self.assertEqual(len(pp), 3)

    def test_b_the_case(self):
        # 准备数据
        p1 = Publication.objects.create(title='The Python Journal')
        p2 = Publication.objects.create(title='Science News')
        p3 = Publication.objects.create(title='Science Weekly')

        # 准备数据
        # INSERT INTO `manytomanyfield_article` (`headline`)
        # VALUES ('Django lets you build Web apps easily') RETURNING `manytomanyfield_article`.`id`
        a = Article.objects.create(headline='Django lets you build Web apps easily')

        # 准备数据: 一次性插入两条数据.
        # INSERT IGNORE INTO `manytomanyfield_article_publications` (`article_id`, `publication_id`)
        # VALUES (1, 1), (1, 2)
        a.publications.add(p1, p2, p3)

        # 同时发起两条查询指令
        # SELECT `manytomanyfield_article`.`id`,
        #        `manytomanyfield_article`.`headline`
        # FROM `manytomanyfield_article`
        # WHERE `manytomanyfield_article`.`id` = 1
        # LIMIT 21
        #
        # 采用 INNER JOIN
        # SELECT (`manytomanyfield_article_publications`.`article_id`) AS `_prefetch_related_val_article_id`,
        #         `manytomanyfield_publication`.`id`, `manytomanyfield_publication`.`title`
        # FROM `manytomanyfield_publication`
        # INNER JOIN `manytomanyfield_article_publications`
        #      ON (`manytomanyfield_publication`.`id` = `manytomanyfield_article_publications`.`publication_id`)
        # WHERE `manytomanyfield_article_publications`.`article_id` IN (1)              # in 对应的是多对多!!!
        # ORDER BY `manytomanyfield_publication`.`title` ASC
        aa = Article.objects.prefetch_related('publications').get(pk=1)

    def test_c_the_reverse_side(self):
        # 准备数据
        p1 = Publication.objects.create(title='The Python Journal')
        p2 = Publication.objects.create(title='Science News')
        p3 = Publication.objects.create(title='Science Weekly')

        # 准备数据
        # INSERT INTO `manytomanyfield_article` (`headline`)
        # VALUES ('Django lets you build Web apps easily') RETURNING `manytomanyfield_article`.`id`
        a = Article.objects.create(headline='Django lets you build Web apps easily')

        # 准备数据: 一次性插入两条数据.
        # INSERT IGNORE INTO `manytomanyfield_article_publications` (`article_id`, `publication_id`)
        # VALUES (1, 1), (1, 2)
        a.publications.add(p1, p2, p3)

        # SELECT `manytomanyfield_publication`.`id`,
        #        `manytomanyfield_publication`.`title`
        # FROM `manytomanyfield_publication`
        # WHERE `manytomanyfield_publication`.`id` = 1
        # LIMIT 21
        pp = Publication.objects.get(pk=1)

        # 一对多和多对多的被指向对象, 只能通过 tablename_set.all() 的方式来方向查找关联数据.
        # 一对一的被指向对象, 可以通过 select_related() 的方式来查找关联, 也就是说, 一对一关系, 双边都是ForeignKey.
        #
        # SELECT `manytomanyfield_article`.`id`,
        #        `manytomanyfield_article`.`headline`
        # FROM `manytomanyfield_article`
        # INNER JOIN `manytomanyfield_article_publications`
        #       ON (`manytomanyfield_article`.`id` = `manytomanyfield_article_publications`.`article_id`)
        # WHERE `manytomanyfield_article_publications`.`publication_id` = 1     # 对于单个 publication 而言, 这里是一对多.
        # ORDER BY `manytomanyfield_article`.`headline` ASC
        aa = pp.article_set.all()
        self.assertEqual(len(aa), 1)
