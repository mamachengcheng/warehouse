from decimal import Decimal
from django.test import TestCase
from .models import Delivery
from account.models import Level
# Create your tests here.
class DeliveryFeeTest(TestCase):
    def setUp(self):
        Level.objects.create(name='a')
        Level.objects.create(name='b')
        Delivery.objects.create(name = 'test',
                                level_id=1,
                                eight = 13.45,        # 1.001-2.000
                                eighteen = 21.45,     #11.001-12.000
                                twenty_six = 31.34,   #19.001-20.000
                                twenty_seven = 33.34, #20.001-21.000
                                thirty_six = 32.3,    #29.001-30.000
                                thirty_seven = 1,     #30.001
                                )

    def test_get_price(self):
        d = Delivery.objects.get(name='test')
        self.assertEqual(d.get_price(1.456), Decimal('13.45'))
        self.assertEqual(d.get_price(11.456), Decimal('21.45'))
        self.assertEqual(d.get_price(20), Decimal('31.34'))
        self.assertEqual(d.get_price(20.00001), Decimal('33.34'))
        self.assertEqual(d.get_price(0), 0)
        self.assertEqual(d.get_price(-23.4), 0)
        self.assertEqual(d.get_price(35.3), Decimal('38.3'))

