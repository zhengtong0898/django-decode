from django.test import TestCase
import time


# Create your tests here.
class SimpleTest(TestCase):

    def test_get(self):
        from .models import product

        p = product(name="aaa", price=10.00, description="aaa", production_date="1999-12-31", expiration_date=170)
        p.save()

        p = product(name="bbb", price=10.00, description="bbb", production_date="1999-12-31", expiration_date=170)
        p.save()

        with self.assertRaises(Exception):
            ss = product.objects.get(expiration_date=170)
