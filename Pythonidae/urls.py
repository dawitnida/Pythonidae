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
   url(r'^index/$', views.display_auctions, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^loggedin/$', views.display_product, name='loggedin'),


    url(r'^admin/', include(admin.site.urls)),
)


