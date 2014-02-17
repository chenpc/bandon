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
from django.conf import settings
from django.core.mail import send_mail

def mail_buy(buy):
    msg = "開團訂購 http://10.77.150.1:8000/menu/%d/buy" % buy.pk
    
    menu = Menu.objects.get(pk=buy.menu_id)    
    you = ""
    for user in User.objects.all():
        if user.email and user.email != "admin@qnap.com":
            you = you + user.email +  ", "

    me = "admin@qnap.com"
    Subject = u"[開團] %s %s" % (menu.store_name, buy.end_date.strftime("%Y-%m-%d  %H:%M"))
    From = me
    To = you

    send_mail(Subject, msg, settings.EMAIL_HOST_USER, [To], fail_silently=True)
    
def mail_cancel(buy):
    msg = "訂購流標 http://10.77.150.1:8000/menu/%d/buy" % buy.pk
    
    menu = Menu.objects.get(pk=buy.menu_id)    
    you = ""
    for order in buy.order_set.all():
        user = User.objects.get(pk=order.buyer)
        if user.email:
            you = you + user.email +  ", "

    me = "admin@qnap.com"
    Subject = u"[流標] %s %s" % (menu.store_name, buy.end_date.strftime("%Y-%m-%d  %H:%M"))
    From = me
    To = you

    send_mail(Subject, msg, settings.EMAIL_HOST_USER, [To], fail_silently=True)
      
    
    

class Buy_Form(forms.Form):
    start_time = forms.DateTimeField(initial=timezone.now())
    end_time = forms.DateTimeField(initial=timezone.now())

class AddMenuView(generic.ListView):
    template_name = 'menu/add_menu.html'
    context_object_name = 'latest_menu_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Menu.objects.all()    
    
class IndexView(generic.ListView):
    template_name = 'menu/index.html'
    context_object_name = 'latest_menu_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Menu.objects.all()
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(IndexView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
        return context
        
class OrderView(generic.ListView):
    template_name = 'menu/order.html'
    context_object_name = 'latest_order_list'
                
    def get_queryset(self):
        """Return the last five published polls."""
        return Order.objects.all()
      
class DetailView(generic.DetailView):
    model = Menu
    template_name = 'menu/detail.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
        return context

 
class BuyView(generic.DetailView):
    model = Buy
    template_name = 'menu/buy.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BuyView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
        return context

class BuyListView(generic.DetailView):
    model = Buy
    template_name = 'menu/buy_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BuyListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
        return context

    
def add_menu(request):    
    menu_text = request.POST['menu_text']    
    menu_list = menu_text.splitlines()
    store_name = menu_list[0].split(": ")[1]
    misc = menu_list[1].split(": ")[1]
    tele_num = menu_list[3].split(": ")[1]
    
    item_list = menu_text[menu_text.index(u"產品:")+3:menu_text.index(u"訂購說明:")]
    
    
    menu_set = Menu.objects.filter(store_name=store_name).distinct()
    
    if menu_set.count() == 0:
        menu = Menu.objects.create()
    else:
        menu = menu_set[0]        
    
    menu.store_name = store_name
    menu.tele_num = tele_num
    menu.misc = misc
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
    mail_buy(buy)
    return HttpResponseRedirect(reverse('index'))

def del_buy(request, buy_pk):
    buy = Buy.objects.get(pk=buy_pk)
    return_list = dict()
    for entry in buy.order_set.all():
        tmp_dish = Dish.objects.get(pk=entry.dish_id)
        if entry.buyer in return_list:
            return_list[entry.buyer] = return_list[entry.buyer] + entry.count * tmp_dish.price            
        else:
            return_list[entry.buyer] = entry.count * tmp_dish.price        
        
    for k,v in return_list.items():
        money = Money.objects.get(user=k)
        if v - buy.discount >= 0:
            money.total = money.total + (v - buy.discount)
        money.save()
        
    buy.status = 1
    buy.save()
    mail_cancel(buy)
    return HttpResponseRedirect(reverse('history'))
    
def change_money(request):
    money = Money.objects.get(user=int(request.POST['userid']))
    money.total = money.total + int(request.POST['change_money'])
    money.save()
    return HttpResponseRedirect(reverse('recharge'))
    
def start_order(request):    
    buy = Buy.objects.get(pk=int(request.POST['buy_pk']))
    
    if buy.status !=0 and buy.end_date > timezone.now():
        return HttpResponseRedirect(reverse('index'))        
    
    count = int(request.POST['count'])
    order = buy.order_set.create()
    order.buyer = request.user.pk
    order.dish_id = int(request.POST['dish'])
    order.count = count
    dish = Dish.objects.get(pk=order.dish_id)
    try:
        money = Money.objects.get(user=request.user.pk)
    except Money.DoesNotExist:
        money = request.user.money_set.create()
        money.total = 0
        money.save()
        
    order_list = buy.order_set.filter(buyer=order.buyer)
    total_cost = 0    
    for entry in order_list:
        tmp_dish = Dish.objects.get(pk=entry.dish_id) 
        total_cost = total_cost + tmp_dish.price * entry.count
    
    if total_cost - buy.discount >= 0:
        cost = dish.price * order.count
    else:
        cost = dish.price * order.count - (buy.discount - total_cost)
    
    if cost < 0:
        cost = 0  
    money.total = money.total - cost
    
    money.save()
    order.save()
    return HttpResponseRedirect(reverse('index'))

def del_order(request, order_pk):    
    order = Order.objects.get(pk=order_pk)
    buy = order.buy
    dish = Dish.objects.get(pk=order.dish_id)
    
    money = Money.objects.get(user=order.buyer)  
    
    if request.user.pk == order.buyer and order.buy.end_date > timezone.now():        
        #money.total = money.total + order.count * tmp_dish.price
        
        order_list = buy.order_set.filter(buyer=order.buyer)
        total_cost = 0
        for entry in order_list:
            tmp_dish = Dish.objects.get(pk=entry.dish_id)
            total_cost = total_cost + tmp_dish.price * entry.count
        
        if total_cost > buy.discount:
            if (total_cost - order.count * tmp_dish.price) <= buy.discount:
                money.total = money.total + total_cost - buy.discount
            else:
                money.total = money.total + order.count * dish.price
                            
        order.delete()
        money.save()           
    return HttpResponseRedirect(reverse('index'))
