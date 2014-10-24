from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test.client import Client



# Create your tests here.
from .forms import AuctionAddForm
from .models import Product, ProductCategory, Auction, AuctionStatus


def create_status(name):
    return AuctionStatus.objects.create(name=name)


def user_instance(us, email, passwd):
    return User.objects.create(username=us, email=email, password=passwd)


def create_category(name):
    return ProductCategory.objects.create(name=name)


def insert_product(name, us, in_price, desc, timestamp, productcat):
    return Product.objects.create(name=name, seller=us, initial_price=in_price,
                                  description=desc, timestamp=timestamp, product_category=productcat)


class AuctionStatusTest(TestCase):
    def setUp(self):
        self.active = AuctionStatus.objects.create(name='Active')
        self.banned = create_status('Banned')
        self.due = create_status('Due')

    def test_auction_has_state(self):
        active = AuctionStatus.objects.get(id=1)
        banned = AuctionStatus.objects.get(id=2)
        due = AuctionStatus.objects.get(id=3)

        self.assertEqual(self.active.name, 'Activee')
        self.assertEqual(self.banned.name, 'Banned')
        self.assertEqual(self.due.name, 'Due')


class ProductModelTest(TestCase):
    fixtures = ['products.json']

    def setUp(self):
        self.user = get_user_model().objects.create(username='Jackson')
        self.category = ProductCategory.objects.create(name="Automobiles")
        self.product = insert_product('Jaguar', self.user, 200.75,
                                      'machines cool', datetime.now(), self.category)

    def test_product_creation(self):
        jaguar = Product.objects.get(id=1)

        self.assertEqual(self.product.seller, self.user)
        self.assertEqual(self.product.initial_price, 200.75)
        self.assertEqual(self.product.product_category, self.category)


class AuctionModelTest(TestCase):
    # fixtures = ['products.json','auctions.json']
    def setUp(self):
        self.category = ProductCategory.objects.create(name="Automobiles")
        self.status = AuctionStatus.objects.create(name="Active")
        self.user = get_user_model().objects.create(username='Neol')
        self.product = insert_product('Nokia Lumia 404', self.user,
                                      99200, 'Amazing mobile', datetime.now(), self.category)

        self.auc = Auction.objects.create(title="Archi-CAD Software", current_price=3.5,
                                          updated_time=datetime.now(),
                                          end_time="2014-10-11 22:49:54",
                                          product=self.product, status=self.status)

    def test_auction_creation(self):
        auc = Auction.objects.get(id=1)

        self.assertEqual(self.auc.title, "Archi-CAD Software")
        self.assertEqual(self.auc.product.seller.username, "Neol")
        self.assertEqual(self.auc.product.name, "Nokia Lumia 404")
        self.assertEqual(self.auc.end_time, "2014-10-11 22:49:54")


# TODO More test


# Simple Test case for Auction Status entry
class AuctionStatusModelTest(TestCase):
    def test_unicode_representation(self):
        aucstatus = AuctionStatus(name="Active")
        self.assertEqual(unicode(aucstatus), aucstatus.name)


# Test testcase
class YaasTest(TestCase):
    def test_indexpage(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        # self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_redirected(self):
        response = self.client.get('/aucdetail/')
        self.assertRedirects(response, '/listauc/')


"""
    def test_post(self):
        response = self.client.post('/somth/', {'name' : '', 'title': 'title'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thank you!!')

  #  def test_email(self):
"""


class HomepageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(username='django')
        self.category = ProductCategory.objects.create(name="Automobiles")
        self.status = AuctionStatus.objects.create(name="Active")
        self.product = insert_product('Nokia Lumia 404', self.user,
                                      99200, 'Amazing mobile', datetime.now(), self.category)

    def test_one_auction(self):
        Auction.objects.create(title="Archi-CAD Software", current_price=3.5,
                               updated_time=datetime.now(), end_time="2014-10-11 22:49:54",
                               product=self.product, status=self.status)

        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'django')
        self.assertContains(response, 99200)
        self.assertContains(response, 'Automobiles')


class AddAuctionFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='django')
        self.category = ProductCategory.objects.create(name="Automobiles")
        self.status = AuctionStatus.objects.create(name="Active")
        self.product = insert_product('Nokia Lumia 404', self.user,
                                      99200, 'Amazing mobile', datetime.now(), self.category)

        self.auction = Auction.objects.create(title="Archi-CAD Software", current_price=35.5,
                                              updated_time=datetime.now(), end_time="2014-10-11 22:49:54",
                                              product=self.product, status=self.status)

    def test_valid_data(self):
        form = AuctionAddForm({
                                  'title': "Archi-CAD Software",
                                  'current_price': 35.5,
                                  'updated_time': datetime.now(),
                                  'end_time': "2014-10-11 22:49:54",
                                  'product': self.product,
                                  'status': self.status
                              }, auction=self.auction)

        self.assertTrue(form.is_valid())
        auction = form.save()
        self.assertEqual(auction.title, "Archi-CAD Software")
        self.assertEqual(auction.product.seller, "Neol")
        self.assertEqual(auction.product.name, "Nokia Lumia 404")
        self.assertEqual(auction.end_time, "2014-10-11 22:49:54")


