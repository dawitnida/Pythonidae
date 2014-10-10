from django.test import TestCase
from datetime import datetime

# Create your tests here.

from yaas.models import Product, ProductCategory, Auction, AuctionStatus

class AuctionStatusTest(TestCase):
    def setUp(self):
        AuctionStatus.objects.create(id = 1, name = 'Active')
        AuctionStatus.objects.create(id = 2, name = 'Due')
        AuctionStatus.objects.create(id = 3, name = 'Banned')

    def test_auction_has_state(self):
        active = AuctionStatus.objects.get(id = 1)
        due = AuctionStatus.objects.get(id = 2)
        banned = AuctionStatus.objects.get(id = 3)

        self.assertEqual(active.name, 'Active' )
        self.assertEqual(due.name, 'Due')
        self.assertEqual(banned.name, 'Banned')


class ProductTest(TestCase):
    def setUp(self):
        cat1 = ProductCategory.objects.create(id=1, name='Automobiles')
        cat2 = ProductCategory.objects.create(id=2, name='Electronics')
        cat3 = ProductCategory.objects.create(id=3, name='Machinary')

        Product.objects.create(id = 1,
                               name = 'Jaguar',
                               initial_price = 3200,
                               description = 'Amazing car',
                               timestamp = datetime.now(),
                               product_category = cat1,
                               )
        Product.objects.create(id = 2,
                               name = 'Asus',
                               initial_price = 400,
                               description = 'Beautiful Lap',
                               timestamp = datetime.now(),
                               product_category = cat2,
                               )
        Product.objects.create(id = 3,
                               name = 'Drill',
                               initial_price = 100,
                               description = 'machine in good condition',
                               timestamp = datetime.now(),
                               product_category = cat3,
                               )

    def test_prodct_has_category(self):
        jaguar = Product.objects.get(id = 1)
        asus = Product.objects.get(id = 2)
        drill = Product.objects.get(id = 3)

        self.assertEqual(jaguar.product_category, 'Automobiles' )
        self.assertEqual(asus.product_category, 'Electronics')
        self.assertEqual(drill.product_category, 'Machinary')
