# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):    
    store_name = models.CharField(max_length=200)
    tele_num = models.CharField(max_length=200)
    type = models.IntegerField(default=0)
    misc = models.CharField(max_length=200)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.store_name

class Dish(models.Model):
    menu = models.ForeignKey(Menu)
    dish_name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    commet = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.dish_name
    
class Buy(models.Model):
    issue_user = models.IntegerField(default=0)
    start_date = models.DateTimeField('start order')
    end_date = models.DateTimeField('end order')
    menu_id = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    def get_menu(self):
        return Menu.objects.get(pk=self.menu_id)
    def get_issuer(self):
        return User.objects.get(pk=self.issue_user).username
    def orderlist(self):
        olist = dict()
        total = 0
        total_count = 0        
        for order in self.order_set.all():            
            if order.get_dish() in olist:
                (count, name) = olist[order.get_dish()]                
                olist[order.get_dish()] = (count+order.count, name + ", " + order.get_buyer().username, order.get_dish().price)
            else:
                olist[order.get_dish()] = (order.count, order.get_buyer().username +"*"+ str(order.count), order.get_dish().price)
            total = total + order.get_dish().price * order.count
            total_count = total_count + order.count
        olist["Total"] = (total_count, "", total)
        

            
        return olist
    def __unicode__(self):
        return Menu.objects.get(pk=self.menu_id).store_name + " End Time " +self.end_date.__str__()

    
class Order(models.Model):
    buy = models.ForeignKey(Buy)
    buyer = models.IntegerField(default=0)
    dish_id = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    comment =  models.CharField(max_length=200)
    cost = models.IntegerField(default=0)
    def get_dish(self):
        return Dish.objects.get(pk=self.dish_id)
    def get_buyer(self):
        return User.objects.get(pk=self.buyer)
    def __unicode__(self):
        return str(self.pk) + " " + User.objects.get(pk=self.buyer).username + " " + self.buy.__unicode__()+ " " + Dish.objects.get(pk=self.dish_id).dish_name

class Money(models.Model):
    user = models.ForeignKey(User)
    total = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.user.pk) + " " + self.user.username