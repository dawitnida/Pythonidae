from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf

from yaas.forms import RegistrationForm, AuctionAddForm
from yaas.models import  Auction, Product, AuctionBidder, Bidder



def display_auctions(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    queryset = Auction.fetchLatestAuctions()
    context = {'auctions': queryset,}
    return render_to_response("index.html",
                              context,
                              context_instance)

def list_auc_with_category(request, offset):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    queryset = Auction.getAuctionByCategory(offset)
    if queryset:
        context = {'auctcategory': queryset,}
        response = render_to_response("listauccat.html",
                              context,
                              context_instance)
        return response

def auction_detail(request, offset):
    """
    # Fetch all auctions and display to users
    :param request:
    :param offset:
    :return:
    """

    context_instance = RequestContext(request)
    queryset = Auction.getAuctionByID(offset)
    if queryset:
        context = {'singleauction': queryset,}
        response = render_to_response("aucdetail.html",
                              context,
                              context_instance)
        return response

@login_required(login_url='/login/')
def list_own_auction(request):
    context_instance = RequestContext(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        offset = request.user.id
        if offset:
            queryset = Auction.getAuctionByOwner(offset)
            if queryset:
                messages.info(request, "List of my auctions.")
                return render_to_response("myauction.html",
                                          {'myauctions' : queryset},
                                          context_instance)
            else:
                messages.info(request, "No Auction found.")
        context = {}
        return render_to_response("myauction.html",
                              context,
                              context_instance)

@login_required(login_url='/login/')
def list_own_product(request):
    context_instance = RequestContext(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    else:
        offset = request.user.id
        if offset:
            queryset = Product.objects.filter(seller_id = offset)
            if queryset:
                messages.info(request, "List of my products.")
                return render_to_response("listproduct.html",
                                          {'myproducts' : queryset},
                                          context_instance)
            else:
                messages.info(request, "No Product added by you.")
        context = {}
        return render_to_response("listproduct.html",
                              context,
                              context_instance)

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
            username =  request.user
            messages.success(request, 'Happy Auctionarying! %s' %unique )
            return HttpResponseRedirect('/index/')
        else:
            messages.info(request, "Invalid username or  password.")
            return HttpResponseRedirect('/login/')
    else:
        message = "Login interrupted!"
    context = {}
    context.update(csrf(request))
    resp = render_to_response('login.html',
                     context,
                     context_instance)
    return resp

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
            new_user = form.save()

            messages.success(request, "Thank You. Registration Successful!")
            return HttpResponseRedirect('/index/')
        else:
            messages.info(request, "Invalid form data. Fill again!")
            return HttpResponseRedirect('/register/')

    else:
        form =RegistrationForm(request.POST)

    context = {'form': form}
    context.update(csrf(request))
    resp = render_to_response('register.html',
                             context,
                             context_instance)
    return resp

@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.info(request, "You are logged out. Please Login again!")
    return HttpResponseRedirect("/index/")

#TODO
@login_required(login_url='/login/')
def add_product(request):
    # Get the request context
    context_instance=RequestContext(request)
    if request.method == 'POST' and request.POST.get('save'):
        form = AuctionAddForm(request.POST)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller_id = request.user.id

            title = request.POST.get('title', '')
            end_time = request.POST.get('end_time', '')
            #TODO CHECK the date and minimum 72 hours auction duration
            #TODO Email to the seller that auction is created

            new_product = form.save()
            new_auc = Auction.objects.create(product_id = new_product.pk, title = title,
                                             end_time = end_time,
                                             status_id = 1)

            messages.success(request, "Thank you for adding new product!")
            return HttpResponseRedirect('/listproduct/')
        else:
            messages.error(request, " Fill the Auction form thoroughly!")
            return HttpResponseRedirect('/addproduct/')

    else:
        form =AuctionAddForm(request.POST)

    context = {'form': form}
    context.update(csrf(request))
    resp = render_to_response('addproduct.html',
                             context,
                             context_instance)
    return resp

#TODO
@login_required(login_url='/login/')
def edit_account(request, instance):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    instance = request.user
    if instance and instance.id:
        context = {'account': instance}
        return render_to_response("editaccount.html",
                              context,
                              context_instance)