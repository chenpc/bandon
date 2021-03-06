from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from bandon import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bandon.views.home', name='home'),
    # url(r'^bandon/', include('bandon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^$', @login_required(login_url='/accounts/login/') (views.IndexView.as_view()), name="index"),
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    url(r'^history/$', login_required(views.HistoryView.as_view()), name='history'),
    url(r'^log/$', login_required(views.LogView.as_view()), name='log'),
    url(r'^admin/', include(admin.site.urls), name="admin"),   
    url(r'^menu/', include('menu.urls', namespace="menu")),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/out/$', views.logout_view, name = "logout"),
    url(r'^accounts/register/$', views.RegisterView.as_view(), name = "register"),
    url(r'^accounts/adduser/$', views.adduser, name = "adduser"),
    url(r'^accounts/admin/$', views.adduser, name = "manage_user"),
    url(r'^recharge/$', views.RechargeView.as_view(), name = "recharge"),
)
