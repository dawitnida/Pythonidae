from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from yaas import views


admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Pythonidae.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   # url(r'^index/$', TemplateView.as_view(template_name='index.html')),
    url(r'^index/$', views.display_auctions, name = 'index'),

    url(r'^login/$', views.user_login, name = 'login'),
    url(r'^register/$', views.register, name = 'register'),
    url(r'^logout/$', views.user_logout, {}, name = 'logout'),
    url(r'^listproduct/$', views.list_own_product, name = 'listproduct'),
    url(r'^myauction/$', views.list_own_auction, name = 'myauction'),
    # rl(r'^myauction/(?P<offset>.*)/$', views.list_owned_auction, name='myauction'),

    url(r'^listauccat/(?P<offset>.*)/$', 'yaas.views.list_auc_with_category', name = 'listauccat'),
    url(r'^aucdetail/(?P<offset>.*)/$',  'yaas.views.auction_detail', name = 'aucdetail'),
    url(r'^editaccount/$', views.edit_account, {}, name = 'editacc'),
    url(r'^addproduct/$', views.add_product, name ='addproduct'),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), # Django Admin documentation generator
    url(r'^admin/', include(admin.site.urls)),

)


