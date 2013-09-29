# coding=utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from menu.models import Menu, Dish, Buy, Order
import datetime
from django import forms
class Buy_Form(forms.Form):
    start_time = forms.DateTimeField(initial=datetime.datetime.now())
    end_time = forms.DateTimeField(initial=datetime.datetime.now())


class IndexView(generic.ListView):
    template_name = 'menu/index.html'
    context_object_name = 'latest_menu_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Menu.objects.all()
    
class DetailView(generic.DetailView):
    model = Menu
    template_name = 'menu/detail.html'
 
class BuyView(generic.DetailView):
    model = Buy
    template_name = 'menu/buy.html'

    
def add_menu(request):    
    menu_text = request.POST['menu_text']    
    menu_list = menu_text.splitlines()
    store_name = menu_list[0].split(": ")[1]
    tele_num = menu_list[3].split(": ")[1]
    
    item_list = menu_text[menu_text.index(u"產品:")+3:menu_text.index(u"訂購說明:")]
    
    
    menu_set = Menu.objects.filter(store_name=store_name).distinct()
    
    if menu_set.count() == 0:
        menu = Menu.objects.create()
    else:
        menu = menu_set[0]        
    
    menu.store_name = store_name
    menu.tele_num = tele_num
    for item in item_list.splitlines():
        item_name = item.split(", ")
        if len(item_name) == 2:
            menu.dish_set.create(dish_name=item_name[0], price=int(item_name[1]))            
    menu.save()
    return HttpResponseRedirect(reverse('menu:index'))


def start_buy(request):
    buy = Buy.objects.create(start_date=datetime.datetime.strptime(request.POST['start_time'], "%Y-%m-%d %H:%M"),
                              end_date=datetime.datetime.strptime(request.POST['end_time'], "%Y-%m-%d %H:%M"))
    buy.menu_id = int(request.POST['menu_pk'])
    buy.issue_user = User.objects.get(username__exact=request.user.username).pk
    print buy.issue_user
    buy.save()
    
    return HttpResponseRedirect(reverse('index'))

def start_order(request):
    print request.POST['menu_pk']
    print request.POST['dish']
    print request.POST['issue_user']
    return HttpResponseRedirect(reverse('index'))