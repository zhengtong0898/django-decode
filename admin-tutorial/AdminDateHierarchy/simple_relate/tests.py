from django.test import TestCase
from .models import ArticleModel, AuthorModel


# Create your tests here.
class TestSelectRelated(TestCase):

    def test_select_related(self):

        author_aa = AuthorModel(name='aaa')
        author_aa.save()

        article_aa = ArticleModel(title="aaa", content="aaa", author=author_aa)
        article_aa.save()

        get_article = ArticleModel.objects.select_related('author').get(id=1)
        self.assertTrue(True)
