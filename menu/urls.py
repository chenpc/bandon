from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from menu import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^(?P<order_pk>\d+)/order$', login_required(views.OrderView.as_view()), name='order'),
    url(r'^(?P<order_pk>\d+)/del_order', login_required(views.del_order), name='del_order'),
    url(r'^add_menu$', login_required(views.add_menu), name='add_menu'),
    url(r'^start_buy$', login_required(views.start_buy), name='start_buy'),
    url(r'^(?P<buy_pk>\d+)/del_buy', login_required(views.del_buy), name='del_buy'),
    url(r'^(?P<pk>\d+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+)/buy$', login_required(views.BuyView.as_view()), name='buy'),
    url(r'^(?P<pk>\d+)/buy_list$', login_required(views.BuyListView.as_view()), name='buy_list'),
    url(r'^add_order$', login_required(views.start_order), name='start_order'),
    url(r'^change_money$', login_required(views.change_money), name='change_money'),
)