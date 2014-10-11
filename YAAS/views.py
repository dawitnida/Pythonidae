
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


from yaas.forms import RegistrationForm

from yaas.models import  Auction, Product



def display_auctions(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    queryset = Auction.fetchLatestAuctions()
    context = {'auctions': queryset,}
    return render_to_response("index.html",
                              context,
                              context_instance)
@login_required
def display_product(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    queryset = Product.fetchOwnProducts()
    context = {'products': queryset}
    return render_to_response("loggedin.html",
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
            messages.success(request, 'Happy Auctionarying!')
            return HttpResponseRedirect('/loggedin/')
        else:
            messages.info(request, "Invalid username or  password.")
            return HttpResponseRedirect('/login/')

    elif request.method == 'POST' and request.POST.get('cancel'):
        messages.info(request, "Login cancelled.")
        return HttpResponseRedirect('/index/')
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
    success = False
    print success
    if request.method == 'POST' and request.POST.get('signup'):
        form = RegistrationForm(request.POST)
        print '??????????', form
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('pword', '')
            first_name = request.POST.get('fname', '')
            last_name = request.POST.get('lname', '')
            email = request.POST.get('email', '')

            new_user = form.save()
            messages.add_message(request, 1, "Registration Successful!")
            success = True

            return HttpResponseRedirect('/loggedin/')
    else:
        form =RegistrationForm(request.POST)

    context = {'success': success, 'form': form}
    context.update(csrf(request))
    resp = render_to_response('register.html',
                             context,
                             context_instance=RequestContext(request))
    return resp


def user_logout(request):
    logout(request)

