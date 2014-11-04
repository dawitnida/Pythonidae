""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 26.10.2014"
__version__ = "Version: "

from django.core.management.base import NoArgsCommand
from django.core import management


# TR2.2 Automated test for UC6 Bid
class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        management.call_command('test', 'yaas.tests.BidTest')

