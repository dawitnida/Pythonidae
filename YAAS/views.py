from datetime import datetime, timedelta

from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.db.models import Max
from django.utils.translation import ugettext as _

from yaas.forms import *
from yaas.models import Auction, Product, AuctionBidder, Bidder, ProductCategory
from yaas.api.authentications import CreateUserToken


# Class based view
class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        try:
            context['auctions'] = Auction.fetchActiveAuctions()
            return context
        except Auction.DoesNotExist:
            raise Http404


home = HomeView.as_view()

import string
import random


def fix_auction():
    auc = Auction.objects.all()
    pro = Product.objects.all()
    WORD = []

    def randomer(size=1, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for x in range(size))

    for a in auc:
        a.title = random.choice(WORD) + randomer()
        # a.product.name = a.title
        a.save()
    print 'Done!'


# login users
def user_login(request):
    # Get the request context
    # fix_auction()
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('login'):
        uname = request.POST.get('username', '')
        pword = request.POST.get('password', '')

        user = authenticate(username=uname, password=pword)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.is_staff:
                messages.success(request, _('Happy Auctionarying Staff! %s') % request.user.username)
            else:
                messages.success(request, _('Happy Auctionarying! %s') % request.user.username)
            return HttpResponseRedirect('/index/')
        else:
            messages.info(request, _("Invalid username or  password."))
            return HttpResponseRedirect('/login/')

    context = {}
    context.update(csrf(request))
    return render_to_response('account/login.html',
                              context,
                              context_instance)


# New registration to yaas web application, username and email should be unique
def register(request):
    # Get the request context
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('signup'):
        reg_form = RegistrationForm(request.POST or None)
        if reg_form.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            new_user = reg_form.save(commit=False)

            if exists(email):
                new_user = reg_form.save()
                new_user = authenticate(username=new_user.username, password=password1)
                if new_user is not None and new_user.is_active:
                    login(request, new_user)
                    messages.success(request, "Registration Successful, Enjoy Yaas!")
                    token = CreateUserToken()  # This is for the Web service
                    token.create_token()
                    return HttpResponseRedirect('/index/')
                else:
                    messages.success(request, "Registration Successful, Login Again!")
                    return HttpResponseRedirect('/login/')
            else:
                messages.info(request, "This email is registered.")
                return HttpResponseRedirect('/register/')
        else:
            messages.info(request, "Invalid form data. Fill again!")
            return HttpResponseRedirect('/register/')

    else:
        reg_form = RegistrationForm()

    context = {'form': reg_form}
    context.update(csrf(request))
    return render_to_response('account/register.html',
                              context,
                              context_instance)


# Clearly fetch and display active auctions to any user of yaas
def list_auction(request):
    context_instance = RequestContext(request)
    try:
        queryset = Auction.fetchActiveAuctions()
        context = {'auctions': queryset, }
        return render_to_response("index.html",
                                  context,
                                  context_instance)
    except Product.DoesNotExist:
        raise Http404


# Displays the detailed description of a single auction
def auction_detail(request, id):
    context_instance = RequestContext(request)
    success = None
    try:
        queryset = Auction.getAuctionByID(id)
        if queryset:
            queryset_bids = AuctionBidder.objects.filter(auc=queryset)
            if queryset_bids:
                success = True
            num_of_bids = AuctionBidder.objects.filter(auc=queryset).values_list('unique_bidder',
                                                                                 flat=True).distinct().count()
            context = {'singleauction': queryset,
                       'current_price': queryset.current_price,
                       'bidders': queryset_bids,
                       'numofbids': num_of_bids,
                       'display': success}
            return render_to_response("aucdetail.html",
                                      context,
                                      context_instance)
    except Auction.DoesNotExist:
        raise Http404


# Bidding auction happens when a user follow the following rules,
# User can not bid unless logged in, user can only bid on other items, not own
# A user can not bid in a sequence, because he/she is winning anyways
# Bidding amount must be at least 0.01+ than the initial price or highest bid
# Soft deadline: is extending of the auction duration by 5 min, if any bid happens 5 min prior to auction deadline
# Email is sent to owner and bidders, a single email is sent to bidders, even if they bid more than once
@login_required(login_url='/login/')
def bid_on_auction(request, offset):
    context_instance = RequestContext(request)
    try:
        query_auction = Auction.getAuctionByID(offset)
        seller = Auction.getOwnerByAuctionID(offset)
        placebid = AuctionBidderForm(request.POST)
        if request.user == seller:
            messages.info(request, _('You can not bid on your item.'))
            return HttpResponseRedirect('/myauction/')
        else:
            if request.method == 'POST' and request.POST.get('placebid'):
                if query_auction:
                    if placebid.is_valid():
                        new_auc_bid = placebid.save(commit=False)
                        initial_price = float(query_auction.product.initial_price)
                        current_price = float(query_auction.current_price)
                        bid_amount = float(request.POST.get('bid_amount', ''))
                        # Amount should be greater than the initial price or the current highest bid by [0.01 min]
                        if (bid_amount > initial_price + 0.01) and (bid_amount > current_price + 0.01):
                            new_auc_bid.auc = query_auction
                            current_highest = query_auction.current_price
                            email_list = []
                            try:
                                bid_counter = AuctionBidder.objects.filter(auc=query_auction).count()
                                # Check if any bidders found for this auction
                                if bid_counter > 0:
                                    last_bidder = AuctionBidder.objects.get(auc=query_auction,
                                                                            bid_amount=current_highest)
                                    if str(request.user) == str(last_bidder.unique_bidder):
                                        messages.error(request, "You do not need to bid....you are winning anyways!")
                                        redirect_url = reverse('aucdetail', args=[new_auc_bid.auc.id])
                                        return HttpResponseRedirect(redirect_url)
                                    if str(request.user) != str(last_bidder.unique_bidder):
                                        email_list = getBiddersEmail(query_auction)
                                bidder = Bidder.objects.create(contender=request.user)
                                new_auc_bid.auc = query_auction
                                new_auc_bid.bidder = bidder
                                new_auc_bid.unique_bidder = bidder

                                query_auction.current_price = bid_amount  # Update the highest bid amount
                                query_auction.save(update_fields=['current_price'])
                                new_auc_bid = placebid.save()
                                # get emails as list which are bidding on the same
                                # auction and then append the seller email to the list
                                email = request.user.email
                                if email not in email_list:
                                    email_list.append(email)
                                email_list.append(seller.email)
                                emailer(str(email_list), "mass", new_auc_bid.auc)
                                messages.success(request, "Thank you for Bidding!")

                                if soft_deadline(new_auc_bid.bid_time,
                                                 query_auction.end_time):  # extend last 5 min of the auc
                                    query_auction.end_time = query_auction.end_time + timedelta(0, 300)
                                    query_auction.save(update_fields=['end_time'])
                                redirect_url = reverse('aucdetail', args=[new_auc_bid.auc.id])
                                return HttpResponseRedirect(redirect_url)
                            except AuctionBidder.DoesNotExist:
                                raise Http404
                        else:
                            messages.error(request, "Bid amount should be at least +0.01 "
                                                    "of the initial price or highest bid amount!")
                            redirect_url = reverse('aucdetail', args=[query_auction.id])
                            return HttpResponseRedirect(redirect_url)
                    else:
                        messages.error(request, "Invalid data. Please enter the correct amount!")
                        redirect_url = reverse('aucdetail', args=[query_auction.id])
                        return HttpResponseRedirect(redirect_url)
                else:
                    messages.info(request, 'No Auction found for bidding.')
            else:
                placebid = AuctionBidderForm()

        context = {'singleauction': query_auction, 'form': placebid}
        return render_to_response("aucdetail.html",
                                  context,
                                  context_instance)
    except Auction.DoesNotExist:
        raise Http404


# Fetch all the auctions, and display in ascending order
@login_required(login_url='/login/')
def list_own_auction(request):
    context_instance = RequestContext(request)
    success = None
    queryset = Auction.getAuctionByOwner(request.user.id)
    if request.user:
        queryset = Auction.getAuctionByOwner(request.user.id)
        if queryset:
            success = True
            return render_to_response("myauction.html",
                                      {'myauctions': queryset, 'display': success},
                                      context_instance)
        else:
            messages.info(request, "No Auction found.")
    context = {'display': success}
    return render_to_response("myauction.html",
                              context,
                              context_instance)


# List products owned by the logged in user, may be used when the system gets fat
@login_required(login_url='/login/')
def list_own_product(request):
    context_instance = RequestContext(request)
    success = None
    offset = request.user.id
    if offset:
        queryset = Product.objects.filter(seller_id=offset)
        if queryset:
            success = True
            return render_to_response("listproduct.html",
                                      {'myproducts': queryset, 'display': success},
                                      context_instance)
        else:
            messages.info(request, "No Product added by you.")
    context = {'display': success}
    return render_to_response("listproduct.html",
                              context,
                              context_instance)


# Display auctions with the same category
def list_auc_category(request, offset):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    try:
        if offset is not None:
            queryset = Auction.getAuctionByCategory(offset)
            if queryset:
                context = {'auctcategory': queryset, }
                return render_to_response("listauccat.html",
                                          context,
                                          context_instance)
        raise Http404
    except Product.DoesNotExist:
        raise Http404


# User is obliged to fulfill rules of adding new item to the auction,
# minimum of 72 hours & datetime format should be satisfied
# and then the user will be redirected to confirmation template, data is saved on the session<_new_product>
@login_required(login_url='/login/')
def add_product(request):
    # Get the request context
    success = None
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('save'):
        addauc_form = AuctionAddForm(request.POST)
        if addauc_form.is_valid():
            new_product = addauc_form.cleaned_data
            new_product = addauc_form.save(commit=False)
            new_product.seller_id = request.user.id
            title = request.POST.get('title', '')
            end_time = request.POST.get('end_time', '')

            try:
                old_auc = Auction.objects.get(title=title)
            except Auction.DoesNotExist:
                old_auc = ""

            if str(title) != str(old_auc):
                min_duration = validateDateTime(end_time)
                if min_duration:
                    new_product = addauc_form.save(commit=False)
                    request.session["_new_product"] = request.POST
                    name = request.POST.get('name', '')
                    title = request.POST.get('title', '')
                    initial_price = request.POST.get('initial_price', '')
                    description = request.POST.get('description', '')
                    end_time = request.POST.get('end_time', '')
                    category_id = request.POST.get('product_category', '')
                    category = ProductCategory.objects.get(id=category_id)
                    product = (name, title, initial_price, description, end_time, category.name)
                    success = True
                    messages.success(request, "Product saved. Confirm to activate the auction.")
                    return render_to_response('saveauc.html', {'form_data': product, 'display': success},
                                              context_instance=RequestContext(request))
                else:
                    messages.success(request, "I told you...CHECK the end date. Min 72 hours auction duration!")
                    return HttpResponseRedirect('/addproduct/')

            else:
                messages.error(request, "Auction found with the same TITLE...please change it!")
                return HttpResponseRedirect('/addproduct/')
        else:
            messages.error(request, "Fill the Auction thoroughly! Incorrect data input/s found.")
            return HttpResponseRedirect('/addproduct/')

    else:
        # If the request was not a POST, display the form to enter auction details.
        addauc_form = AuctionAddForm()

    context = {'form': addauc_form, 'display': success}
    context.update(csrf(request))
    return render_to_response('addproduct.html',
                              context,
                              context_instance)


# After the seller fills the form to add new item to the auction, he/she will be
# redirected here. The confirmation is displayed as Yes/No option to the user
# If Yes, the data/values will be retrieved from its unique session key<_new_product>
# It will be added to the auction and message will be sent to the owner by email
# If No or nothing happens on the browser, then the data will be flushed from the session
@login_required(login_url='/login/')
def save_auction(request):
    if "_new_product" in request.session:
        product = request.session.get("_new_product")
        if request.method == 'POST' and request.POST.get('yes_save'):
            end_time = datetime.strptime(product['end_time'], '%Y-%m-%d %H:%M:%S')
            end_time = timezone.make_aware(end_time, timezone.get_current_timezone())
            category = ProductCategory.objects.get(id=product['product_category'])
            new_product = Product.objects.create(name=product['name'],
                                                 seller=request.user,
                                                 initial_price=product['initial_price'],
                                                 product_category=category,
                                                 description=product['description'])
            new_auc = Auction.objects.create(product_id=new_product.pk, title=product['title'],
                                             end_time=end_time, status_id=1)
            del request.session['_new_product']
            emailer(request.user.email, "single", product['title'])
            messages.success(request, "Thank you for adding new product to the Auction!")
            return HttpResponseRedirect('/index/')
        elif request.method == 'POST' and request.POST.get('no_save'):
            messages.success(request, "Auction is not created.")
        else:
            messages.info(request, "Auction is discarded.")
    return HttpResponseRedirect('/myauction/')


# Update the description of an existing auction
# and also update the 'timestamp'
@login_required(login_url='/login/')
def update_description(request, offset):
    context_instance = RequestContext(request)
    try:
        queryset_product = Product.objects.get(id=offset)
        queryset_auction = Auction.getAuctionByProductID(offset)
        if queryset_product.seller_id == request.user.pk:
            if request.method == 'POST' and request.POST.get('update'):
                product_form = ProductUpdateForm(request.POST or None)
                product_form.fields["description"].queryset = queryset_product.description
                if product_form.is_valid():
                    queryset_product.description = request.POST.get('description')
                    queryset_product.save(update_fields=['description'])
                    queryset_auction.save(update_fields=['updated_time'])
                    messages.success(request, "Product description is updated!")
                    return HttpResponseRedirect('/myauction/')
                else:
                    messages.error(request, "Description field is required!")
                    return HttpResponseRedirect('/updatedescr/%s' % offset)
            else:
                product_form = ProductUpdateForm()
        else:
            messages.error(request, "No privilege to edit/update the data!")
            return HttpResponseRedirect('/index/')

        context = {'form': product_form}
        return render_to_response('updatedescr.html',
                                  context,
                                  context_instance)
    except Auction.DoesNotExist:
        raise Http404


# Change email of the authenticated user, and email should be unique
@login_required(login_url='/login/')
def change_email(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('save'):
        email_form = EmailUpdateForm(request.POST or None)
        email = request.POST['email']
        confirm_email = request.POST['confirm_email']
        if email == confirm_email:
            user = User.objects.get(username=request.user.username)
            if email_form.is_valid():
                user.email = email_form.cleaned_data['email']
                if exists(email):
                    user.save()
                    messages.success(request, "Email is updated successfully!")
                    return HttpResponseRedirect('/index/')
                else:
                    messages.info(request, "This email is registered.")
                    return HttpResponseRedirect('/changemail/')
            else:
                messages.error(request, "Not valid email!")
                return HttpResponseRedirect('/changemail/')
        else:
            messages.error(request, " Emails does not match.")
            return HttpResponseRedirect('/changemail/')
    else:
        email_form = EmailUpdateForm()

    context = {'form': email_form}
    return render_to_response('account/changemail.html',
                              context,
                              context_instance)


# Change user password
@login_required(login_url='/login/')
def change_password(request):
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('save'):
        passwd_form = PasswordChangeForm(user=request.user, data=request.POST)
        if passwd_form.is_valid():  # All validation rules pass
            password1 = passwd_form.cleaned_data['new_password1']
            passwd_form.save()
            user = authenticate(username=request.user.username, password=password1)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, _('Your password is updated and notified via email.'))
                emailer(user.email, "change", "")
                return HttpResponseRedirect('/index/')
        else:
            messages.error(request, "Password mismatch or wrong old password!")
            return HttpResponseRedirect('/editaccount/')
    else:
        passwd_form = PasswordChangeForm(user=request.user)

    context = {'form': passwd_form, }
    return render_to_response('account/editaccount.html',
                              context,
                              context_instance)


# Admin or staff can ban an active auction that does not comply with the terms
# Change the status of the auction to ban,
# This will automatically insure that, the auction will not be searchable & will not appear to users
# Send notification to owner of the auction and bidders, if there exist
@user_passes_test(lambda u: u.is_staff, login_url='/404/')
def ban_auction(request, id):
    try:
        queryset = Auction.getAuctionByID(id)
        if request.method == 'POST' and request.POST.get('ban'):
            if queryset and queryset.status_id == 1:
                queryset_bids = AuctionBidder.objects.filter(auc=queryset).count()
                queryset.status_id = 2
                queryset.save(update_fields=['status_id'])

                email_list = []
                if queryset_bids > 0:
                    email_list = getBiddersEmail(queryset)

                email_list.append(queryset.product.seller.email)
                emailer(str(email_list), "ban", queryset.title)
                messages.info(request, "Auction banned, seller and bidder/s are notified with email.")
                return HttpResponseRedirect('/index/')
            else:
                messages.info(request, "You can not proceed.")
                return HttpResponseRedirect('/index/')
        else:
            messages.info(request, "Something is not right. Try again.")
            return HttpResponseRedirect('/index/')
    except Auction.DoesNotExist:
        raise Http404


# Search auctions, by title, or matching string & return list of auction/auctions with details
# If no auction found, redirect user to the Referrer
def search_auction(request):
    context_instance = RequestContext(request)
    success = False
    if request.method == 'POST' and request.POST.get('search'):
        keytitle = request.POST.get('keytitle')
        if len(keytitle):
            aucfound = Auction.fetchActiveAuctions().filter(title__icontains=keytitle)
            if aucfound:
                success = True
                messages.success(request, 'The following auction/s found.')
                return render_to_response('search.html',
                                          {'auc': aucfound, 'display': success}, context_instance)
            else:
                messages.info(request, 'No search result found.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'No auction title provided on the search field!')
    return render_to_response('search.html',
                              {'display': success},
                              context_instance)


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.info(request, _("You are logged out. Welcome to login again!"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def custom_404(request):
    context_instance = RequestContext(request)
    return render_to_response('404.html',
                              locals(),
                              context_instance)


def custom_500(request):
    context_instance = RequestContext(request)
    return render_to_response('500.html',
                              locals(),
                              context_instance)


# Check if the inserted date in valid
# Check if it is greater than 72 hours(Min) for a new auction to be approved for posting
def validateDateTime(input_time):
    t_format = '%Y-%m-%d %H:%M:%S'
    end_time = datetime.strptime(input_time, t_format)
    now_str = datetime.now().strftime(t_format)
    now_dt = datetime.strptime(str(now_str), t_format)

    time_delta = end_time - now_dt
    sec = time_delta.total_seconds() - 259200.0

    if sec >= 0:
        return time_delta
    else:
        return None


# If there is a bid in the last 5 minutes of the auction deadline,
# extend the auction duration by 5 minutes more, so that others can place there bid
def soft_deadline(bid_time, end_time):
    sec = (end_time - bid_time).total_seconds()
    if sec <= 300:
        return True


# Iteration is done on the bidders to find their unique emails, so that they
# must get only one email on every bid of the auction they are in! Or when
#  Admin bans an auction, bidders will get notification by email
#  Returns their emails as a list.
#  One bidder can bid as many as he/she wants on the same bid, as long as he/she is not the highest bidder
def getBiddersEmail(queryset_auction):
    if queryset_auction:
        bidders_id_list = Bidder.objects.filter(auctions=queryset_auction).values_list('contender',
                                                                                       flat=True).distinct()
        bidder_emails = []
        for b in bidders_id_list:
            bidder = User.objects.get(id=b)
            bidder_email = bidder.email
            bidder_emails.append(bidder_email)
        return bidder_emails


def getHighestBidder(auction):
    if auction:
        highest_bid = AuctionBidder.objects.filter(auc=auction). \
            aggregate(Max('bid_amount'))['bid_amount__max']
        winner = AuctionBidder.objects.get(auc=auction, bid_amount=highest_bid)
        winner = winner.unique_bidder.contender.username
        return winner, highest_bid


# Send email to new auction creator or to mail list of bidders
# It depends on the argument from the caller method
def emailer(recipient_list, email_type, title):
    if recipient_list:
        from_email = 'noreply@ya.as'
        if email_type == 'single':
            subject = "New AUCTION"
            body = "Confirmation for creating '%s' Auction, more notified when bids happen!" % title
            send_mail(subject, body, from_email, [recipient_list, ], fail_silently=False)
        elif email_type == 'mass':
            subject = "Another New BID"
            body_bidder = "Auction title '%s' has new bid." % title
            send_mail(subject, body_bidder, from_email, [recipient_list, ], fail_silently=False)
        elif email_type == 'change':
            subject = "Password Change"
            body = "Your password is changed."
            send_mail(subject, body, from_email, [recipient_list, ], fail_silently=False)
        elif email_type == 'due':
            subject = "Auction is due"
            body = "The auction '%s' has ended." % title
            send_mail(subject, body, from_email, [recipient_list, ], fail_silently=False)
        elif email_type == 'ban':
            subject = "Auction BAN"
            body = "The Auction '%s' is banned by the admin." % title
            send_mail(subject, body, from_email, [recipient_list, ], fail_silently=False)
        else:
            print 'Failed to send email'


def email_winner(recipient_list, arg=()):
    subject = "Auction is adjudicated"
    body = "Auction '%s' has ended and winner is %s, winning price of %d." % (arg[0], arg[1], arg[2])
    send_mail(subject, body, 'noreply@ya.as', [recipient_list, ], fail_silently=False)


def exists(email):
    found_email = User.objects.filter(email=email).distinct().count()
    if found_email <= 0:
        return True
    else:
        return None

