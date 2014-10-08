
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


from yaas.models import  Auction, Product


def display_auctions(request):
    # Fetch all auctions and display to users
    context_instance = RequestContext(request)
    queryset = Auction.objects.all()
    table_head = ['ID', 'Title', 'Start Date', 'End Date', 'Status']
    context = {'auctions': queryset, 'content': table_head,}

    return render_to_response("index.html",
                              context,
                              context_instance= RequestContext(request))

def user_login(request):
    # Get the request context
    context_instance = RequestContext(request)

    if request.method == 'POST' and request.POST.get('login'):
        uname = request.POST['username']
        pword = request.POST['password']
        nextTo = request.GET.get('next', '/index/')

        user = authenticate(username = uname, password = pword)
        if user is not None and  user.is_active:
            login(request, user)
            print 'User active', user
            return HttpResponseRedirect(nextTo)
        else:
            message = "Invalid username or  password.". format(uname,pword)
            return HttpResponseRedirect('/login/')
    elif request.method == 'POST' and request.POST.get('cancel'):
        message = "Login cancelled!"
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
    context_instance = RequestContext(request)
    success = False
    if request.method == 'POST' and request.POST.get('signup'):
        uname = request.POST.get('username', '')
        pword = request.POST.get('pword', '')
        email = request.POST.get('email', '')

        message = "Registration Successful!"
        success = True
        return HttpResponseRedirect('/index/')

    elif request.method == 'POST' and request.POST.get('cancel'):
        message = "Registration cancelled!"
        return HttpResponseRedirect('/index/')
    else:
        print ''
    context = {'success': success}
    context.update(csrf(request))
    resp = render_to_response('register.html',
                             context,
                             context_instance)
    return resp