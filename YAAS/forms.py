""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 8.10.2014"
__version__ = "Version: "

from django.contrib.auth.forms import UserCreationForm
from django import forms
from yaas.models import User

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=False,
                                 max_length=20, label='first_name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=False,
                                max_length=20, label='last_name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, label='email',
                             widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password1'].widget = forms.TextInput(attrs={'placeholder': 'Create password'})
        self.fields['password2'].widget = forms.TextInput(attrs={'placeholder': 'Confirm password'})
"""
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        person = User.objects.get_or_create(user=user )
        person[0].email = self.cleaned_data['email']
        if commit:
            person[0].save()
        return user
    """




