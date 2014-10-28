""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 26.10.2014"
__version__ = "Version: "

from django.core.management.base import NoArgsCommand
from django.core import management

# TR2.3 Automated test for testing concurrency when bidding
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        management.call_command('test', 'yaas.tests.AuctionModelTest.test_concurrency')