""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 8.10.2014"
__version__ = "Version: "

from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django import forms

from yaas.models import User, Product, AuctionBidder


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=False,
                                 max_length=20, label='first_name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}
                                 )
    )
    last_name = forms.CharField(required=False,
                                max_length=20, label='last_name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}
                                )
    )
    email = forms.EmailField(required=True, label='email',
                             widget=forms.EmailInput(attrs={'placeholder': '* Email'})
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': '* Username'}
        )
        self.fields['password1'] = forms.CharField(required=True,
                                                   widget=forms.PasswordInput(
                                                       attrs={'placeholder': '* Create password'})
        )
        self.fields['password2'] = forms.CharField(required=True,
                                                   widget=forms.PasswordInput(
                                                       attrs={'placeholder': '* Confirm password'})
        )


class AuctionAddForm(forms.ModelForm):
    # CAT_LIST = ProductCategory.listProductCategory()
    name = forms.CharField(max_length=40, label='Product name',
                           widget=forms.TextInput(attrs={'placeholder': '* Product name'}
                           )
    )
    title = forms.CharField(max_length=40, label='Auction Title',
                            widget=forms.TextInput(
                                attrs={'placeholder': '* Auction title'}
                            )
    )
    initial_price = forms.DecimalField(required=True, max_digits=10, decimal_places=2, label='Initial price',
                                       widget=forms.TextInput(
                                           attrs={'placeholder': '* Initial price'}
                                       )
    )
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    end_time = forms.DateTimeField(required=True, label='End date',
                                   help_text="Minimum of 72 hours duration from now and Must be exactly this format '%s'" % now,
                                   widget=forms.TextInput(
                                       attrs={'placeholder': "* End date and time"}
                                   )
    )
    description = forms.CharField(max_length=400, label='Description',
                                  widget=forms.Textarea(
                                      attrs={'placeholder': '* Write product description'}
                                  )
    )

    class Meta:
        model = Product
        fields = ('name', 'title', 'initial_price', 'end_time', 'product_category', 'description')
        readonly_fields = ('name', 'title', 'initial_price', 'end_time', 'product_category', 'description')


class ProductUpdateForm(forms.Form):
    description = forms.CharField(max_length=400, label='Description',
                                  widget=forms.Textarea(
                                      attrs={'placeholder': '* Write item description update.',
                                             'cols': '200', 'rows': '10'}
                                  )
    )

    class Meta:
        model = Product
        fields = ('description',)


class EmailUpdateForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': '* Type Email.'}
    ))
    confirm_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': '* Retype your Email.'}
    ))


class AuctionBidderForm(forms.ModelForm):
    class Meta:
        model = AuctionBidder
        fields = ('bid_amount',)
