from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.core.urlresolvers import reverse

from yaas.models import *


'''
TR2 Automated Functional Tests
UC3 Create a new auction
'''


def create_status(name):
    return AuctionStatus.objects.create(name=name)


def create_category(name):
    return ProductCategory.objects.create(name=name)


def get_category(id):
    return ProductCategory.objects.get(id=id)


def create_product(name, us, in_price, desc, timestamp, productcat):
    return Product.objects.create(name=name, seller=us, initial_price=in_price,
                                  description=desc, timestamp=timestamp, product_category=productcat)


class AuthenticateUserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('catman', 'catman@test.com', 'cat')

    def test_authentication(self):
        self.assertEqual(self.user.username, 'catman')
        self.client.login(username='catman', password='cat')
        self.assertTrue(self.user.is_authenticated())


# Simple Test case for Auction Status entry
class AuctionStatusModelTest(TestCase):
    def test_unicode_representation(self):
        aucstatus = AuctionStatus(name="Active")
        self.assertEqual(unicode(aucstatus), aucstatus.name)


class AuctionCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.new_category = create_category('Food')
        self.new_status = create_status('status')
        self.user = User.objects.create_user('catman', 'catman@test.com', 'cat')

    def test_auction_creation(self):
        self.client.login(username='catman', password='cat')
        self.assertIn('_auth_user_id', self.client.session)
        # Test Product and Auction model are empty
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(Auction.objects.count(), 0)
        self.auctiondata = {
            'name': 'car 200J',
            'title': "Jaguar",
            'initial_price': 45,
            'end_time': "2016-11-11 19:49:54",
            'product_category': 1,
            'description': 'amazingly cool'
        }
        url = reverse('yaas.views.add_product')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.auctiondata.update({'save': True})
        self.assertTemplateUsed(response, 'addproduct.html')

        # If <save> is submitted, user will be get the following content
        save_response = self.client.post(url, self.auctiondata)
        self.assertContains(save_response, "Product saved. Confirm to activate the auction.", status_code=200)

        # Data will be saved in the session so it is asserted!
        session = self.client.session.get("_new_product")
        self.assertEqual(session['title'], 'Jaguar')

        # If it's <yes_save> redirect to 'index.html'
        save_url = reverse('yaas.views.save_auction')
        yes_save_response = self.client.post(save_url, {'yes_save': True})
        self.failUnlessEqual(save_response.status_code, 200)
        self.assertRedirects(yes_save_response, '/index/')

        # Assert if <no_save> is chosed from the option & redirect to 'myauction'
        no_save_response = self.client.post(save_url, {'no_save': True})
        self.failUnlessEqual(response.status_code, 200)
        self.assertRedirects(no_save_response, '/myauction/')

        # Assert Product and Auction are created
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Auction.objects.count(), 1)


'''
TR2 Automated Functional Tests
UC6 Bid
'''


class BidTest(TestCase):
    fixtures = ['users.json', 'aucstatus.json', 'prodcat.json', 'products.json', 'auctions.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('robert', 'catman@test.com', 'ro')
        self.auc = Auction.objects.get(id=1)

    def test_bid_amount(self):
        self.client.login(username='robert', password='ro')
        self.assertIn('_auth_user_id', self.client.session)
        url = reverse('yaas.views.auction_detail', args=[self.auc.id, ])
        response = self.client.get(url, args=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.auc.current_price, 121)
        bid_url = reverse('yaas.views.bid_on_auction', args=[self.auc.id, ])
        data = {'bid_amount': 121.01, 'placebid': True}
        bid_response = self.client.post(bid_url, data)
        self.assertRedirects(bid_response, '/aucdetail/1/')

    def test_bidder(self):
        self.client.login(username='joey', password='jo')
        self.assertIn('_auth_user_id', self.client.session)
        url = reverse('yaas.views.auction_detail', args=[self.auc.id, ])
        response = self.client.get(url, args=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.auc.product.seller.username, 'joey')
        bid_url = reverse('yaas.views.bid_on_auction', args=[self.auc.id, ])
        data = {'bid_amount': 121.02, 'placebid': True}
        bid_response = self.client.post(bid_url, data)
        self.assertRedirects(bid_response, '/myauction/')

    def test_bid_auction(self):
        self.client.login(username='robert', password='ro')
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(AuctionBidder.objects.count(), 0)
        url = reverse('yaas.views.auction_detail', args=[self.auc.id, ])
        response = self.client.get(url, args=1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ratoonn")

        bid_url = reverse('yaas.views.bid_on_auction', args=[self.auc.id, ])
        data = {'bid_amount': 121.02, 'placebid': True}
        bid_response = self.client.post(bid_url, data)
        self.failUnlessEqual(bid_response.status_code, 302)

        resp = self.client.get('/aucdetail/1/')
        self.assertContains(resp, "Thank you for Bidding!", status_code=200)
        self.assertEqual(AuctionBidder.objects.count(), 1)
        self.assertEqual(Bidder.objects.count(), 1)


from concurrency.utils import ConcurrencyTestMixin
from concurrency.views import RecordModifiedError

'''
TR2 Automated Functional Tests
UC10 Support Multiple Concurrent Session
This assert that simultaneous task on the same auction will raise exception
So YAAS application should handle this exception <django-concurrency>
solves this problem by creating IntegerField  for each model
Version Field that returns a 'unique' version number for the record.
The version number is produced using
time.time() * 1000000, to get the benefits of microsecond if the system clock provides them.
'''


class AuctionConcurrencyTest(ConcurrencyTestMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        self.user_buyer = get_user_model().objects.create(username='jango')
        self.user_seller = get_user_model().objects.create(username='omano')
        self.category = ProductCategory.objects.create(name="Books")
        self.status = AuctionStatus.objects.create(name="Active")
        self.product = create_product('imacer', self.user_seller,
                                      90, 'Amazing mobile', self.now, self.category)

        self.auction = Auction.objects.create(title="macab", current_price=100,
                                              updated_time=self.now, end_time="2014-11-11 04:49:54",
                                              product=self.product, status=self.status)

    def test_auction_concurrency(self):
        concurrency_model = Auction
        self.auc_a = Auction.objects.get(pk=1)
        self.auc_b = Auction.objects.get(pk=1)
        self.assertEqual(self.auc_a, self.auc_b)

        self.auc_a.current_price = 12
        self.auc_b.current_price = 12

        self.auc_a.save()
        with self.assertRaisesMessage(RecordModifiedError, "Record has been modified"):
            self.auc_b.save()
        version_1 = self.auc_a.version
        self.auc_a.save()
        version_2 = self.auc_a.save()
        self.assertNotEqual(version_1, version_2)


class BidConcurrencyTest(ConcurrencyTestMixin, TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        self.user_buyer = get_user_model().objects.create(username='jango')
        self.user_seller = get_user_model().objects.create(username='omano')
        self.category = ProductCategory.objects.create(name="Books")
        self.status = AuctionStatus.objects.create(name="Active")
        self.product = create_product('imacer', self.user_seller,
                                      90, 'Amazing mobile', self.now, self.category)
        self.auction = Auction.objects.create(title="macab", current_price=100,
                                              updated_time=self.now, end_time="2014-11-11 04:49:54",
                                              product=self.product, status=self.status)

    # Assert concurrency is met: by just creating basic versioned model
    def test_bid_concurrency(self):
        concurrency_model = AuctionBidder
        self.auct = Auction.objects.get(pk=1)
        self.auct.product.description = "I am on editing"
        self.auct.current_price = 120
        raised = False
        try:
            self.auct.save()
            self.bidder = Bidder.objects.create(contender=self.user_buyer)
            aucbid = AuctionBidder.objects.create(auc=self.auct, bid_time="2014-11-11 22:49:54",
                                                  bid_amount=121, unique_bidder=self.bidder)
            self.assertEqual(self.auct, aucbid.auc)
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')


'''
More Automated Functional Tests
'''


class HomepageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        self.user = get_user_model().objects.create(username='django')
        self.category = ProductCategory.objects.create(name="Automobiles")
        self.status = AuctionStatus.objects.create(name="Active")
        self.product = create_product('Nokia Lumia 404', self.user,
                                      90, 'Amazing mobile', self.now, self.category)

        self.auction = Auction.objects.create(title="Archi-CAD Software", current_price=95.5,
                                              updated_time=self.now, end_time="2014-11-11 22:49:54",
                                              product=self.product, status=self.status)

    def test_index_page(self):
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_single_auction(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'django')
        self.assertContains(response, 90)
        self.assertContains(response, 'Automobiles')





