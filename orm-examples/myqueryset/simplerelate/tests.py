from django.test import TestCase, TransactionTestCase
from .models import Article, Tag, Publication, Author


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_select_relate(self):
        # 准备数据
        publication_1 = Publication.objects.create(title="Python Official")
        publication_2 = Publication.objects.create(title="人民邮电出版社")

        author_1 = Author.objects.create(name="Robert Sedgewick")
        author_2 = Author.objects.create(name="Kevin Wayne")

        tag_1 = Tag.objects.create(name="计算机")
        tag_2 = Tag.objects.create(name="美食")
        tag_3 = Tag.objects.create(name="金融")

        # ManyToMany 不可以直接被创建, 为什么?
        # 因为 Article.publications 是一张独立表, 它即指向 Publication 表, 也指向 Article 表.
        # 前面的代码已经创建(插入)了 Publication 数据到数据库中, 因此可以获得一个有效的 Publication.id,
        # 然而 Article 在这里还没有插入数据到数据库, 因此不可以使用这种方式来完成插入动作.
        # Article.objects.create(headline="你好, 世界!", author=author_1, tag=tag_1, publications=(publication_1, ))
        # Article.objects.create(headline="爱吃蔬菜沙拉的胖子", author=author_2, tag=tag_2, publications=(publication_2, ))
        article_1 = Article.objects.create(headline="你好, 世界!", author=author_1, tag=tag_1)
        article_2 = Article.objects.create(headline="爱吃蔬菜沙拉的胖子", author=author_2, tag=tag_2)
        article_1.publications.add(publication_1)
        article_2.publications.add(publication_2)
        print("===article===")

        # 自动关联所有外键的数据, 后续调用 s.author, s.tag 时就不会再查数据库了.
        # SELECT `simplerelate_article`.`id`,
        #        `simplerelate_article`.`headline`,
        #        `simplerelate_article`.`author_id`,
        #        `simplerelate_article`.`tag_id`,
        #        `simplerelate_author`.`id`,
        #        `simplerelate_author`.`name`,
        #        `simplerelate_tag`.`id`,
        #        `simplerelate_tag`.`name`
        # FROM `simplerelate_article` INNER JOIN `simplerelate_author` ON (`simplerelate_article`.`author_id` = `simplerelate_author`.`id`)
        #                             INNER JOIN `simplerelate_tag` ON (`simplerelate_article`.`tag_id` = `simplerelate_tag`.`id`)
        # WHERE `simplerelate_article`.`id` = 1 LIMIT 21
        article_1 = Article.objects.select_related().get(pk=1)

        # 但是 select_related 不负责提取 manytomany 的数据, 还是需要自行操作.
        # TODO: DjangoAdmin有没有针对ManyToMany的相关操作, 还是需要自行查询才可以做相应展示?
        from django.db.models.manager import BaseManager
        # publications 这个ManyToMany字段, 是一个 BaseManager 类型, 也间接的是一个`QuerySet`.
        qs_manager: BaseManager = article_1.publications
        # SELECT `simplerelate_publication`.`id`,
        #        `simplerelate_publication`.`title`
        # FROM `simplerelate_publication` INNER JOIN `simplerelate_article_publications` ON (`simplerelate_publication`.`id` = `simplerelate_article_publications`.`publication_id`)
        # WHERE `simplerelate_article_publications`.`article_id` = 1
        # ORDER BY `simplerelate_publication`.`title` ASC
        qs_publications = qs_manager.all()

        # 断言-1
        self.assertEqual(article_1.headline, "你好, 世界!")
        self.assertEqual(article_1.author.name, "Robert Sedgewick")
        self.assertEqual(article_1.tag.name, "计算机")
        self.assertEqual(len(qs_publications), 1)
        self.assertEqual(qs_publications[0].title, "Python Official")


