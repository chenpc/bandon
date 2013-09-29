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
    def get_menu(self):
        return Menu.objects.get(pk=self.menu_id)
    def get_issuer(self):
        return User.objects.get(pk=self.issue_user).username

    
class Order(models.Model):
    buy = models.ForeignKey(Buy)
    buyer = models.IntegerField(default=0)
    dish_id = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    comment =  models.CharField(max_length=200)
    cost = models.IntegerField(default=0)