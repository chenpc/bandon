# coding=utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from menu.models import Menu, Dish, Buy, Order, Money
import datetime
from django.utils import timezone
from django import forms
class Buy_Form(forms.Form):
    start_time = forms.DateTimeField(initial=timezone.now())
    end_time = forms.DateTimeField(initial=timezone.now())


class IndexView(generic.ListView):
    template_name = 'menu/index.html'
    context_object_name = 'latest_menu_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Menu.objects.all()
        
class OrderView(generic.ListView):
    template_name = 'menu/order.html'
    context_object_name = 'latest_order_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Order.objects.all()
      
class DetailView(generic.DetailView):
    model = Menu
    template_name = 'menu/detail.html'
 
class BuyView(generic.DetailView):
    model = Buy
    template_name = 'menu/buy.html'

class BuyListView(generic.DetailView):
    model = Buy
    template_name = 'menu/buy_list.html'

    
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
    type = request.POST['type']
    if type == "launch":
        df = datetime.timedelta(hours=10)
    else:
        df = datetime.timedelta(hours=15)       
    buy = Buy.objects.create(start_date=timezone.now(),
        end_date=timezone.make_aware(datetime.datetime.strptime(request.POST['end_time'], "%m/%d/%Y")+df, timezone.get_current_timezone()))
    
    if type == "dinner":  
        buy.discount = 80 # by QNAP
           
    buy.menu_id = int(request.POST['menu_pk'])
    buy.issue_user = User.objects.get(username__exact=request.user.username).pk
    buy.save()    
    return HttpResponseRedirect(reverse('index'))

def change_money(request):
    money = Money.objects.get(user=request.user.pk)
    print request.POST['change_money']
    money.total = money.total + int(request.POST['change_money'])
    money.save()
    return HttpResponseRedirect(reverse('recharge'))
    
def start_order(request):    
    buy = Buy.objects.get(pk=int(request.POST['buy_pk']))
    order = buy.order_set.create()
    order.buyer = request.user.pk
    order.dish_id = int(request.POST['dish'])
    dish = Dish.objects.get(pk=order.dish_id)
    try:
        money = Money.objects.get(user=request.user.pk)
    except Money.DoesNotExist:
        money = request.user.money_set.create()
        money.total = 0
        money.save()
        
    order_list = Order.objects.filter(buyer=order.buyer)
    total_cost = 0    
    for entry in order_list:
        tmp_dish = Dish.objects.get(pk=entry.dish_id) 
        total_cost = total_cost + tmp_dish.price    
    
    if total_cost - buy.discount >= 0:
        cost = dish.price
    else:
        cost = dish.price - buy.discount + total_cost        
    
    if cost < 0:
        cost = 0  
    money.total = money.total - cost
    order.cost = cost
    money.save()
    order.save()
    return HttpResponseRedirect(reverse('index'))

def del_order(request, order_pk):    
    order = Order.objects.get(pk=order_pk)
    tmp_dish = Dish.objects.get(pk=order.dish_id)
    return_cost = tmp_dish.price - order.cost
    money = Money.objects.get(user=order.buyer)  
    if request.user.pk == order.buyer and order.buy.end_date > timezone.now():
        tmp_buyer = order.buyer
        money.total = money.total + order.cost
        order.delete()
        order_list = Order.objects.filter(buyer=tmp_buyer)
        
        for entry in order_list:
            if entry.cost < return_cost:
                return_cost = return_cost - entry.cost
                money.total = money.total + entry.cost
                entry.cost = 0
                
            else:
                entry.cost = entry.cost - return_cost
                money.total = money.total + return_cost
                return_cost = 0
            entry.save()            
        
        money.save()           
    return HttpResponseRedirect(reverse('index'))