from django.contrib import admin
from django.conf.urls import *
from rest_framework import routers

from yaas.views import *
from yaas import ws_views


admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', ws_views.UserViewSet)
router.register(r'bids', ws_views.BidViewSet)
router.register(r'aucs', ws_views.AuctionViewSet)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Pythonidae.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^api/', include(router.urls)),
                       url(r'^api/auth/$', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api/auc/$', 'yaas.ws_views.apiauction_list'),

                       url('^api/search/(?P<title>.+)/$', ws_views.SearchList.as_view()),

                       url(r'^$', home),
                       url(r'^index/$', list_auction, name='index'),
                       url(r'^login/$', user_login, name='login'),
                       url(r'^register/$', register, name='register'),
                       url(r'^logout/$', user_logout, {}, name='logout'),
                       url(r'^listproduct/$', list_own_product, name='listproduct'),
                       url(r'^myauction/$', list_own_auction, name='myauction'),
                       # url(r'^myauction/(?P<offset>.*)/$', views.list_owned_auction, name='myauction'),

                       url(r'^listauccat/(?P<offset>.*)/$', 'yaas.views.list_auc_category', name='listauccat'),
                       url(r'^aucdetail/(?P<id>[0-9]+)/$', 'yaas.views.auction_detail', name='aucdetail'),
                       url(r'^banauc/(?P<id>[0-9]+)/$', 'yaas.views.ban_auction', name='banauc'),
                       url(r'^placebid/(?P<offset>.*)/$', 'yaas.views.bid_on_auction', name='placebid'),

                       url(r'^saveauc/$', 'yaas.views.save_auction', name='saveauc'),

                       url(r'^editaccount/$', change_password, {}, name='editacc'),
                       url(r'^changemail/$', change_email, {}, name='changemail'),
                       url(r'^updatedescr/(?P<offset>.*)/$', 'yaas.views.update_description', {}, name='updatedescr'),
                       url(r'^addproduct/$', add_product, name='addproduct'),
                       url(r'^search/$', search_auction, name='search'),

                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Django Admin documentation generator

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^i18n/', include('django.conf.urls.i18n')),

)
'''
urlpatterns += i18n_patterns('',
    url(r'^index/$', list_auction, name = 'index'),

    url(r'^login/$', user_login, name = 'login'),
    url(r'^register/$', register, name = 'register'),
    url(r'^logout/$', user_logout, {}, name = 'logout'),
    url(r'^listproduct/$', list_own_product, name = 'listproduct'),
    url(r'^myauction/$', list_own_auction, name = 'myauction'),
    # rl(r'^myauction/(?P<offset>.*)/$', views.list_owned_auction, name='myauction'),

    url(r'^listauccat/(?P<offset>.*)/$', 'yaas.views.list_auc_category', name = 'listauccat'),
    url(r'^aucdetail/(?P<id>[0-9]+)/$',  'yaas.views.auction_detail', name = 'aucdetail'),

    url(r'^banauc/(?P<id>[0-9]+)/$', 'yaas.views.ban_auction', name = 'banauc'),
    url(r'^placebid/(?P<offset>.*)/$',  'yaas.views.bid_on_auction', name = 'placebid'),

    url(r'^editaccount/$', change_password, {}, name = 'editacc'),
    url(r'^changemail/$', change_email, {}, name = 'changemail'),
    url(r'^updatedescr/(?P<offset>.*)/$', 'yaas.views.update_description', {}, name = 'updatedescr'),

    url(r'^addproduct/$', add_product, name ='addproduct'),
    url(r'^saveauc/$', 'yaas.views.save_auction', name = 'saveauc'),

    url(r'^search/$', search_auction, name ='search'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), # Django Admin documentation generator
)
'''
handler404 = 'yaas.views.custom_404'
handler500 = 'yaas.views.custom_500'
