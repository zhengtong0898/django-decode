from django.test import TestCase
import time


# Create your tests here.
class SimpleTest(TestCase):

    def test_get(self):
        from .models import product

        p = product(name="aaa", price=10.00, description="aaa", production_date="1999-12-31", expiration_date=170)
        p.save()

        # time.sleep(1000)
        ss = product.objects.get(pk=1)
        print("ss: ", ss)
        self.assertTrue(True)
