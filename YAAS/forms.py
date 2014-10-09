""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 8.10.2014"
__version__ = "Version: "

from django.forms import ModelForm
from yaas.models import User

class RegisterationForm(ModelForm):

    class Meta:
        model = User



