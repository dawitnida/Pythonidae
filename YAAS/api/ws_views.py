""" Development of Web Applications and Web Services

"""

__author__ = "Dawit Nida (dawit.nida@abo.fi)"
__date__ = "Date: 24.10.2014"
__version__ = "Version: "

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.renderers import JSONRenderer

from yaas.api.serializers import *
from yaas.models import *


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


'''
WS1. A user should be able to send a GET request for either browsing
the auctions or for searching a specific auction. A auction or list of
auctions should be sent back in the json format.
<title> or <str> is send via the request header
No authentication required and Class based view is good practice.
'''


class SearchList(generics.ListAPIView):
    serializer_class = AuctionSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        title = self.kwargs['title']
        if title is not None:
            queryset = self.model.objects.filter(title__icontains=title).filter(status_id=1)
            if queryset is not None:
                return queryset.order_by('end_time')
        return JSONResponse({"detail": "Auction not found."}, status=status.HTTP_404_NOT_FOUND)


'''
WS2 A web service which allows an authenticated user to bid on a
given auction by sending a POST request (with the necessary information
attached in the json format). The web service should be able to
verify the bidder's credentials and bid validity, and respond depending
on the result of the bidding with a message containing the description
of the new bid or a description of the error also in json format.
It uses Token Authentication
'''


@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def bid_auction_detail(request, pk):
    content = {
        'user': unicode(request.user),
        'auth': unicode(request.auth)
    }
    if content:
        try:
            auc = Auction.getAuctionByID(pk)
            seller = Auction.getOwnerByAuctionID(pk)
            bids = AuctionBidder.objects.filter(auc=auc)
        except Auction.DoesNotExist:
            return JSONResponse({"non_auction_error": "Auction is not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = AuctionBidderModelSerializer(auc, many=False)
            return JSONResponse(serializer.data)
        elif request.method == 'POST':
            user = User.objects.get(username=content['user'])
            bidder = Bidder.objects.create(contender=user)
            data = {'unique_bidder': bidder.pk, 'auc': auc.pk,
                    'bid_amount': request.DATA.get('bid_amount'), 'bid_time': timezone.now()}

            if user.pk == seller.pk:
                return JSONResponse({"same_user_error": "You can not bid on your item."},
                                    status=status.HTTP_400_BAD_REQUEST)
            if bids.count() > 0:
                last_bidder = AuctionBidder.objects.get(auc=auc, bid_amount=auc.current_price)
                if str(user.username) == str(last_bidder.unique_bidder):
                    return JSONResponse({"duplicate_bidder_error": "No need to bid. You are winning."},
                                        status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = AuctionBidderSerializer(data=data)
                if serializer.is_valid():
                    auc.bidder = bidder
                    auc.unique_bidder = bidder
                    serializer.save()
                    return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
                return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':  # Remove bids and bidders from that specific auction and
            auc.current_price = 0  # Update the current highest price and may be in the future delete the auction itself
            auc.save(update_fields=['current_price'])
            bids.delete()
            # auc.delete() Remove the auction itself, and related product should be removed too!
            # Lets check. It needs query the related product and delete it
            return JSONResponse({"non_auction_error": "Auction is deleted"}, status=status.HTTP_204_NO_CONTENT)
    return JSONResponse(content)


# Another class based view:
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


# Awesome class based view
@permission_classes((IsAuthenticated,))
class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.filter(status_id=1)
    serializer_class = AuctionSerializer


# Bidder class view
class BidderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuctionBidder.objects.all()
    serializer_class = AuctionBidderSerializer
    model = serializer_class.Meta.model
    authentication_classes = (BasicAuthentication,)
    permission_classes = (permissions.IsAdminUser,)


# Auction API: Only available without any authentications
# Users can only view detail of an auction. nothing else
@api_view(['GET'])
def auction_detail(request, pk):
    try:
        auction = Auction.objects.get(pk=pk)
        bid = AuctionBidder.objects.filter(auc=auction)
    except Auction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuctionSerializer(auction)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AuctionSerializer(auction, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = AuctionSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        auction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = AuctionBidderModelSerializer(bid, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
