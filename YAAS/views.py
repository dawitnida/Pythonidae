from django.views.generic.base import TemplateView
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.utils.translation import ugettext as _

from yaas.forms import RegistrationForm, AuctionAddForm, ProductUpdateForm, AuctionBidderForm
from yaas.models import  Auction, Product, AuctionBidder, Bidder


#TODO
class HomeView(TemplateView):
    template_name = 'index.html'
home = HomeView.as_view()

def user_login(request):
    # Get the request context
    context_instance = RequestContext(request)
    if request.method == 'POST' and request.POST.get('login'):
        uname = request.POST.get('username', '')
        pword = request.POST.get('password', '')
        nextTo = request.GET.get('next', '/index/')

        user = authenticate(username = uname, password = pword)
        if user is not None and  user.is_active:
            login(request, user)
            unique = request.user.username
            messages.success(request, _('Happy Auctionarying! %s') %unique )
            return HttpResponseRedirect('/index/')
        else:
            messages.info(request, _("Invalid username or  password."))
            return HttpResponseRedirect('/login/')
    else:
        message = "Login interrupted!"
    context = {}
    context.update(csrf(request))
    return render_to_response('login.html',
                     context,
                     context_instance)

def register(request):
    # Get the request context
    context_instance=RequestContext(request)
    if request.method == 'POST' and request.POST.get('signup'):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('pword', '')
            email = request.POST.get('email', '')
            first_name = request.POST.get('fname', '')
            last_name = request.POST.get('lname', '')
            new_user = form.save(commit=False)
            new_user = form.save()

            messages.success(request, "Thank You. Registration Successful!")
            return HttpResponseRedirect('/index/')
        else:
            messages.info(request, "Invalid form data. Fill again!")
            return HttpResponseRedirect('/register/')

    else:
        form =RegistrationForm()

    context = {'form': form}
    context.update(csrf(request))
    return render_to_response('register.html',
                             context,
                             context_instance)


def display_auctions(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    try:
        queryset = Auction.fetchActiveAuctions()
    except Product.DoesNotExist:
        raise Http404

    context = {'auctions': queryset,}
    return render_to_response("index.html",
                              context,
                              context_instance)

def auction_detail(request, offset):
    context_instance = RequestContext(request)
    success = False
    try:
        queryset = Auction.getAuctionByID(offset)
    except Auction.DoesNotExist:
        raise Http404

    if queryset:
        queryset_bids = AuctionBidder.objects.filter(auc = queryset)
        if queryset_bids:
            success = True
        context = {'singleauction': queryset,
                   'current_price': queryset.current_price,
                   'bidders' : queryset_bids,
                   'display': success}
        return render_to_response("aucdetail.html",
                              context,
                              context_instance)


@login_required(login_url='/login/')
def bid_on_auction(request, offset):
    context_instance = RequestContext(request)
    try:
        queryset_auction = Auction.getAuctionByID(offset)
        seller = Auction.getOwnerByAuctionID(offset)
    except Auction.DoesNotExist:
        raise Http404

    if seller == request.user:
        messages.info(request, _('Know your rights!...You can not bid on your item.'))
    else:
        form = AuctionBidderForm(request.POST)
        if request.method == 'POST' and request.POST.get('placebid'):
            if queryset_auction:
                if form.is_valid():
                    new_auc_bid = form.save(commit=False)
                    initial_price = float(queryset_auction.product.initial_price)
                    current_price = float(queryset_auction.current_price)
                    bid_amount = float(request.POST.get('bid_amount', ''))

                    # Amount should be greater than the initial price or the current highest bid by [0.01 min]
                    if (bid_amount > initial_price+0.01) and (bid_amount > current_price+0.01):
                        new_auc_bid.auc = queryset_auction
                        current_highest_price = queryset_auction.current_price
                        try:
                           any_bids = AuctionBidder.objects.filter(auc = queryset_auction)
                           # Check if any bidders found for this auction
                           if any_bids.count() > 0:
                               last_bidder = AuctionBidder.objects.get(auc = new_auc_bid.auc, bid_amount = current_highest_price)
                               if str(last_bidder.unique_bidder) != str(request.user):
                                    new_auc_bid.auc = queryset_auction
                                    bidder = Bidder.objects.create(contender = request.user)
                                    new_auc_bid.bidder = bidder
                                    new_auc_bid.unique_bidder = bidder

                                    queryset_auction.current_price = bid_amount    # Update the highest bid amount
                                    queryset_auction.save(update_fields=['current_price'])
                                    new_auc_bid = form.save()
                                    messages.success(request, "Thank you for Bidding!")

                                    email_list = getBiddersEmail(queryset_auction)
                                    # get emails as list which are bidding on the same
                                    # auction and then append the seller email to the list
                                    email_list.append(seller.email)
                                    emailer(str(email_list), "mass", new_auc_bid.auc)
                                    redirect_url = reverse('aucdetail', args=[new_auc_bid.auc.id])
                                    return HttpResponseRedirect(redirect_url)
                               else:
                                    messages.error(request, "You do not need to bid....you are winning anyways!")
                                    redirect_url = reverse('aucdetail', args=[queryset_auction.id])
                                    return HttpResponseRedirect(redirect_url)
                           else:
                                new_auc_bid.auc = queryset_auction
                                bidder = Bidder.objects.create(contender = request.user)
                                new_auc_bid.bidder = bidder
                                new_auc_bid.unique_bidder = bidder

                                queryset_auction.current_price = bid_amount    # Update the highest bid amount
                                queryset_auction.save(update_fields=['current_price'])
                                new_auc_bid = form.save()
                                messages.success(request, "YES You are the first to bid!")

                                email_list = (request.user.email, seller.email)
                                emailer(str(email_list), "new", new_auc_bid.auc)
                                redirect_url = reverse('aucdetail', args=[new_auc_bid.auc.id])
                                return HttpResponseRedirect(redirect_url)
                        except AuctionBidder.DoesNotExist:
                                raise Http404
                    else:
                        messages.error(request, "Invalid data. Bid amount should be at least +0.01 "
                                                "of the initial price or highest bid amount!")
                        redirect_url = reverse('aucdetail', args=[queryset_auction.id])
                        return HttpResponseRedirect(redirect_url)
                else:
                    messages.error(request, "Invalid data. Please enter the correct amount!")
                    redirect_url = reverse('aucdetail', args=[queryset_auction.id])
                    return HttpResponseRedirect(redirect_url)
            else:
                messages.info(request, 'No Auction found for bidding.')
    form = AuctionBidderForm()
    context = {'singleauction': queryset_auction,  'form': form }
    return render_to_response("aucdetail.html",
                          context,
                          context_instance)


@login_required(login_url='/login/')
def list_own_auction(request):
    context_instance = RequestContext(request)
    success = False
    offset = request.user.id
    if offset:
        queryset = Auction.getAuctionByOwner(offset)
        if queryset:
            success = True
            return render_to_response("myauction.html",
                                      {'myauctions' : queryset, 'display' : success},
                                      context_instance)
        else:
            messages.info(request, "No Auction found.")
    context = {'display' : success}
    return render_to_response("myauction.html",
                              context,
                              context_instance)

@login_required(login_url='/login/')
def list_own_product(request):
    context_instance = RequestContext(request)
    success = False
    offset = request.user.id
    if offset:
        queryset = Product.objects.filter(seller_id = offset)
        if queryset:
            success = True
            return render_to_response("listproduct.html",
                                      {'myproducts' : queryset, 'display' : success},
                                      context_instance)
        else:
            messages.info(request, "No Product added by you.")
    context = {'display' : success}
    return render_to_response("listproduct.html",
                          context,
                          context_instance)

# Display auctions with the same catagory
def list_auc_with_category(request, offset):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    try:
        queryset = Auction.getAuctionByCategory(offset)
    except Product.DoesNotExist:
        raise Http404
    if queryset:
        context = {'auctcategory': queryset,}
        return render_to_response("listauccat.html",
                              context,
                              context_instance)
    else:
        raise Http404

#FIXME Confirmation to be done
@login_required(login_url='/login/')
def add_product(request):
    # Get the request context
    context_instance=RequestContext(request)
    if request.method == 'POST' and request.POST.get('save'):
        form = AuctionAddForm(request.POST)
        if form.is_valid():
            new_product = form.cleaned_data
            new_product = form.save(commit=False)
            new_product.seller_id = request.user.id
            title = request.POST.get('title', '')
            end_time = request.POST.get('end_time', '')

            try:
               old_auc = Auction.objects.get(title = title)
            except Auction.DoesNotExist:
                old_auc = ""

            if str(title) != str(old_auc):
                min_duration =  validateDateTime(end_time)
                if min_duration:
                    new_product = form.save()
                    new_auc = Auction.objects.create(product_id = new_product.pk, title = title,
                                                     end_time = end_time,
                                                     status_id = 1)

                    emailer(request.user.email, "single", title)
                    messages.success(request, "Thank you for adding new product to the Auction!")
                    return HttpResponseRedirect('/myauction/')
                else:
                    messages.success(request, "I told you...CHECK the end date. Min 72 hours auction duration!")
                    return HttpResponseRedirect('/myauction/')

            else:
                messages.error(request, "Auction found with the same TITLE...please change it!")
                return HttpResponseRedirect('/addproduct/')
        else:
            messages.error(request, " Fill the Auction thoroughly! Incorrect data input/s found.")
            return HttpResponseRedirect('/addproduct/')

    else:
        # If the request was not a POST, display the form to enter auction details.
        form =AuctionAddForm()

    context = {'form': form}
    context.update(csrf(request))
    return render_to_response('addproduct.html',
                             context,
                             context_instance)

@login_required(login_url='/login/')
def confirm_new_auction(request, product_name):
    context_instance = RequestContext(request)




@login_required(login_url='/login/')
def update_description(request, offset):
    context_instance = RequestContext(request)
    try:
        queryset_product = Product.objects.get(id=offset)
        queryset_auction = Auction.getAuctionByProductID(offset)
    except Auction.DoesNotExist:
        raise Http404

    if queryset_product.seller_id == request.user.pk:

        if request.method == 'POST' and request.POST.get('update'):
            product_form = ProductUpdateForm(request.POST or None)
            product_form.fields["description"].queryset = queryset_product.description
            if product_form.is_valid():
                queryset_product.description = request.POST.get('description')
                queryset_product.save(update_fields=['description'])
                queryset_auction.save(update_fields = ['updated_time'])
                messages.success(request, "Product description is updated!")
                return HttpResponseRedirect('/myauction/')
            else:
                messages.error(request, "Description field is required!")
                return HttpResponseRedirect('/updatedescr/%s' %offset)
        else:
            product_form = ProductUpdateForm()
    else:
        messages.error(request, "No privilege to edit/update the data!")
        return HttpResponseRedirect('/index/')

    context = {'form': product_form}
    return render_to_response('updatedescr.html',
                              context,
                              context_instance)

#TODO PasswordChangeForm
@login_required(login_url='/login/')
def edit_account(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    user_passwd_form = PasswordChangeForm(request.POST, request.user)
    if request.method == 'POST' and request.POST.get('save'):
        if user_passwd_form.is_valid():
            user_passwd_form.save()
            messages.success(request, "Profile updated!")
            return HttpResponseRedirect('/index/')
        else:
            messages.error(request, " Incorrect username or password!")
            return HttpResponseRedirect('/editaccount/')

    else:
        user_passwd_form = PasswordChangeForm()

    context = {'form': user_passwd_form}
    return render_to_response('editaccount.html',
                              context,
                              context_instance)


def search_auction(request):
    context_instance = RequestContext(request)
    success = False
    if request.method == 'POST' and request.POST.get('search'):
        keytitle = request.POST.get('keytitle')
        if len(keytitle):
            aucfound = Auction.fetchActiveAuctions().filter(title__icontains = keytitle)
            if aucfound:
                success = True
                messages.success(request, 'The following auction/s found.')
                return render_to_response('search.html',
                                          {'auc': aucfound, 'display': success}, context_instance)
            else:
                messages.info(request, 'No search result found.')
        else:
            messages.error(request, 'No auction title provided on the search field!')
    return render_to_response('search.html',{'display': success}, context_instance)


@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.info(request, _("You are logged out. Welcome to login again!"))
    return HttpResponseRedirect("/index/")


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

#  Iteration is done on the bidders to find their unique emails, so that they
#  must get only one email on every bid of the auction they are in!
#  Returns their emails as a list.
#  One bidder can bid as many as he/she wants on the same bid, as long as he/she is not the highest bidder
def getBiddersEmail(queryset_auction):
    if queryset_auction:
        bidders_id_list = Bidder.objects.filter(auctions = queryset_auction).values_list('contender', flat=True).distinct()
        # num_of_bids = AuctionBidder.objects.filter(auc = queryset).values('unique_bidder_id').distinct().count()
        bidder_emails = []
        for b in bidders_id_list:
            bidder = User.objects.get(id = b)
            bidder_email = bidder.email
            bidder_emails.append(bidder_email)
        return bidder_emails

# Send email to new auction creator or to mail list of bidders
def emailer(recipient_list, email_type, title):

    if (recipient_list):
        from_email = 'noreply@ya.as'
        if email_type == 'single':
            subject = "Thank you for creating a new Auction."
            body = "Confirmation for creating '%s' Auction.\
                    You will be notified whenever someone bids on your auction!"%title
            send_mail(subject, body, from_email, [recipient_list,], fail_silently=False)
        elif email_type == 'new':
            subject = "New BID"
            body_bidder = "Auction title '%s' has the first bid." %title
            send_mail(subject, body_bidder, from_email, [recipient_list,], fail_silently=False)
        elif email_type == 'mass':
            subject = "Another new BID"
            body_bidder = "Auction title '%s' has new bid." %title
            send_mail(subject, body_bidder, from_email, [recipient_list,], fail_silently=False)
        else:
            print 'Failed to send email'