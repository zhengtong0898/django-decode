from django.test import TestCase, TransactionTestCase
from .models import Book, Publisher, Author
from django.db.models import Avg


# Create your tests here.
class SimpleTest(TransactionTestCase):

    reset_sequences = True

    def test_a_avg(self):
        # 准备数据
        publisher = Publisher.objects.create(name="人民邮电出版社")
        author_1 = Author.objects.create(name="Robert Sedgewick", age=20)
        author_2 = Author.objects.create(name="Kevin Wayne", age=22)
        author_3 = Author.objects.create(name="谢路云 译", age=24)
        book = Book.objects.create(name="算法(第四版)", pages=636, price=99,
                                   rating=3.5, publisher=publisher, pubdate="2012-10-01")
        book.authors.add(author_1, author_2, author_3)

        publisher = Publisher.objects.create(name="机械工业出版社")
        author_1 = Author.objects.create(name="Sartaj Sahni", age=20)
        author_2 = Author.objects.create(name="王立柱", age=22)
        author_3 = Author.objects.create(name="刘志红", age=24)
        book = Book.objects.create(name="数据结构、算法与应用 C++语言描述",
                                   pages=543, price=79, rating=2.5,
                                   publisher=publisher, pubdate="2019-05-01")
        book.authors.add(author_1, author_2, author_3)

        # SELECT AVG(`aggregate__book`.`price`) AS `price__avg`
        # FROM `aggregate__book`
        qs = Book.objects.all().aggregate(Avg("price"))
        self.assertIsInstance(qs, dict)
        self.assertEqual(qs["price__avg"], 89)
