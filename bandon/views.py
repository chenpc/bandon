from menu.models import Buy, Money
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_buy_list'              
    def get_queryset(self):
        """Return the last five published polls."""
        return Buy.objects.order_by('-end_date')
    
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

class RegisterView(generic.TemplateView):
    template_name = 'registration/register.html'               
        
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