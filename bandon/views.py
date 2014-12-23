from menu.models import Buy, Money, Log
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class UserView(generic.ListView):
    template_name = 'users.html'
    context_object_name = 'user_list'              
    def get_queryset(self):
        """Return the last five published polls."""
        return User.objects.all()
    
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_buy_list'              
    def get_queryset(self):
        """Return the last five published polls."""
        return Buy.objects.exclude(end_date__lt = timezone.now()).order_by('end_date')[:14]
    
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

class LogView(generic.ListView):
    template_name = 'log.html'
    context_object_name = 'latest_log_list'              
    def get_queryset(self):
        money = Money.objects.get(user=self.request.user.pk)
	if self.request.user.is_staff:
		return Log.objects.order_by('-log_time')[:100]
	else:
	        return money.log_set.order_by('-log_time')[:100]
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LogView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = Money.objects.get(user=self.request.user.pk)
            context['today'] = timezone.now() #datetime.datetime.now()
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
            context['today'] = timezone.now() #datetime.datetime.now()
        return context
        
class HistoryView(generic.ListView):
    template_name = 'history.html'
    context_object_name = 'latest_buy_list'              
    def get_queryset(self):
        """Return the last five published polls."""
        return Buy.objects.order_by('-end_date')[:100]
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HistoryView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        try:
            context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
            context['today'] = timezone.now() #datetime.datetime.now()
        except Money.DoesNotExist:
            money = self.request.user.money_set.create()
            money.total = 0
            money.save()
            context['money'] = money
            context['today'] = timezone.now() #datetime.datetime.now()
        return context


class RegisterView(generic.TemplateView):
    template_name = 'registration/register.html'
    
class RechargeView(generic.ListView):
    template_name = 'recharge.html'
    context_object_name = 'all_money_list'
    def get_queryset(self):
        return Money.objects.all()

    def get_context_data(self, **kwargs):
        total = 0
        # Call the base implementation first to get a context
        context = super(RechargeView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
	for money in Money.objects.all():
	    total = total + money.total
	context['total'] = total
        return context
        
def logout_view(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def adduser(request):
    user_name = request.POST['name']
    mail = request.POST['mail']
    pwd1 = request.POST['pwd1']
    pwd2 = request.POST['pwd2']
        
    if pwd1 == pwd2:        
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = User.objects.create_user(user_name, mail, pwd1)
            money = user.money_set.create()
            money.total = 0
            money.save()
    return HttpResponseRedirect(reverse('index'))
