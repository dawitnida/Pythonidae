""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from yaas.serializers import *
from yaas.models import *


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def apiauction_list(request):
    if request.method == 'GET':
        auc = Auction.objects.filter(status_id=1)
        serializer = AuctionSerializer(auc, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuctionSerializer(data=data)
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        else:
            return JSONResponse(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class BidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBidder.objects.all()
    serializer_class = BidSerializer
    # authentication_classes = (BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def pre_save(self, obj):
        obj.user = self.request.user


class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.filter(status_id=1)
    serializer_class = AuctionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.user = self.request.user


class SearchList(generics.ListAPIView):
    serializer_class = AuctionSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        title = self.kwargs['title']
        if title is not None:
            queryset = self.model.objects.filter(title__icontains=title).filter(status_id=1)
            if queryset is not None:
                return queryset.order_by('end_time')
        raise Http404
