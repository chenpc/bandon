# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):    
    store_name = models.CharField(max_length=200)
    tele_num = models.CharField(max_length=200)
    type = models.IntegerField(default=0)
    misc = models.CharField(max_length=200)
    tickets = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.store_name
    def vote_list(self):
        user_list = []        
        for vote in self.vote_set.all():            
            user_list.append(vote.user)
        return user_list

class Vote(models.Model):
    menu = models.ForeignKey(Menu)
    user = models.ForeignKey(User)
    
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
    type = models.IntegerField(default=0)
    def get_order(self):
        return self.order_set.filter(vaild=1)
    def get_menu(self):
        return Menu.objects.get(pk=self.menu_id)
    def get_issuer(self):
        return User.objects.get(pk=self.issue_user).username
    def orderlist(self):
        olist = dict()
        total = 0
        total_count = 0        
        for order in self.order_set.filter(vaild=1):            
            if order.get_dish() in olist:
                (p1, p2) = olist[order.get_dish()]                                
                p1.append(order)                
                olist[order.get_dish()] = (p1, p2 + order.count)                                
            else:
                olist[order.get_dish()] = ([order, ], order.count)
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
    vaild = models.IntegerField(default=1)    
    def get_cost(self):
        return self.get_dish().price * self.count
    def get_dish(self):
        return Dish.objects.get(pk=self.dish_id)
    def get_buyer(self):
        return User.objects.get(pk=self.buyer)
    def __unicode__(self):
        return User.objects.get(pk=self.buyer).username + " " + self.buy.__unicode__()+ " " + Dish.objects.get(pk=self.dish_id).dish_name



class Money(models.Model):
    user = models.ForeignKey(User)
    total = models.IntegerField(default=0)
    def cost(self, order, cost, reason):
        log = self.log_set.create()
        log.money = self
        log.order = order
        log.cost = -cost
        self.total = self.total - cost
        log.left = self.total
        log.reason = reason
        self.save()        
        log.save()
        
    def __unicode__(self):
        return self.user.username
    
class Log(models.Model):
    money = models.ForeignKey(Money)
    order = models.ForeignKey(Order, null=True)
    cost = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    log_time = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=20)
    def __unicode__(self):
        return str(self.pk) + " " + unicode(self.order) + str(self.cost)