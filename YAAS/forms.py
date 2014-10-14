""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 8.10.2014"
__version__ = "Version: "

from django.contrib.auth.forms import UserCreationForm
from django import forms
from yaas.models import User, Product, Auction, ProductCategory

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=False,
                                 max_length=20, label='first_name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=False,
                                max_length=20, label='last_name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, label='email',
                             widget=forms.TextInput(attrs={'placeholder': '* Email'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': '* Username'})
        self.fields['password1'].widget = forms.TextInput(attrs={'placeholder': '* Create password'})
        self.fields['password2'].widget = forms.TextInput(attrs={'placeholder': '* Confirm password'})
"""
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        person = User.objects.get_or_create(user=user )
        person[0].email = self.cleaned_data['email']
        if commit:
            person[0].save()
        return user
"""

#FIXME Category and more cleanups
class AuctionAddForm(forms.ModelForm):
    # CAT_LIST = ProductCategory.listProductCategory()
    name = forms.CharField(max_length=40, label='Product name',
                                widget=forms.TextInput(attrs={'placeholder': '* Product name'}))
    title = forms.CharField(max_length=40, label='Auction Title',
                                widget=forms.TextInput(attrs={'placeholder': '* Auction title'}))
    initial_price = forms.DecimalField(required=True, max_digits=10, decimal_places = 2, label='Initial price',
                                       widget=forms.TextInput(attrs={'placeholder': '* Initial price'}))
    end_time = forms.DateTimeField(required=True, label='End date',
                                       widget=forms.TextInput(attrs={'placeholder': '* End date and time'}))
    description = forms.CharField(max_length=400, label='Description',
                                  widget=forms.Textarea(attrs={'placeholder': '* Write product description.'}))
    #NOTE
   # product_category = forms.ModelChoiceField(queryset=ProductCategory.listProductCategory())


    class Meta:
        model = Product
        fields = ('name', 'title', 'initial_price', 'end_time', 'description', 'product_category')




