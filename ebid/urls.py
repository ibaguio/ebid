from django.conf.urls import patterns, include, url
from ebid import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ebid.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', views.login, name='login'),
    # url(r'^logout/$', views.logout, name='logout'),
    url(r'/^$', 'ebid.views.home', name='home'),
    url(r'^dashboard/$', 'ebid.views.dashboard', name='dashboard'),
    url(r'^dashboard/history/$', 'ebid.views.history', name='history'),
    url(r'^dashboard/user_profile/$', 'ebid.views.user_profile', name='user_profile'),
    url(r'^dashboard/live_bidding/$', 'ebid.views.live_bidding', name='live_bidding'),
    url(r'^dashboard/live_bidding/do_bid/$', 'ebid.views.do_bid', name='do_bid'),
    url(r'^dashboard/live_bidding/view/$', 'ebid.views.live_bidding_new', name='live_bidding_new'),
    url(r'^dashboard/new_bidding/$', 'ebid.views.new_bidding', name='new_bidding'),
    url(r'^dashboard/new_bidding/biditems/$', 'ebid.views.fetch_biditems'),
    url(r'^dashboard/new_bidding/add_bidder/$', 'ebid.views.add_bidder'),
    url(r'^dashboard/new_bidding/publish/$', 'ebid.views.publish_bid'),
    url(r'^dashboard/new_bidding/add_biditem/$', 'ebid.views.add_biditem', name='add_biditem'),
    url(r'^dashboard/new_bidding/remove_biditem/$', 'ebid.views.remove_biditem', name='remove_biditem'),
    url(r'^dashboard/live_bidding/bid_info/$', 'ebid.views.bid_info', name='bid_info'),
    url(r'^cgi/fetch_live_bids/$', 'ebid.views.fetch_live_bids', name='fetch_live_bids'),
    url(r'^cgi/fetch_bids/$', 'ebid.views.fetch_bids', name='fetch_bids'),
    url(r'^cgi/fetch_bid_history/$', 'ebid.views.fetch_bid_history', name='fetch_bid_history'),

    url(r'^admin/', include(admin.site.urls)),
)
