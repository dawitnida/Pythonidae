""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 30.10.2014"
__version__ = "Version: "

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

'''
And again, All created users need Token to login to the API
Users will use Token Authentication and send it to the url:
and must satisfy & rest everything fully. RESTful-ness.
This was done from the python shell.
'''


class CreateUserToken:
    def create_token(self):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)