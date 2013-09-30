from menu.models import Buy, Money
from django.views import generic
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


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
        context['money'] = self.request.user.money_set.get(user=self.request.user.pk)
        
        
        return context
    
def logout_view(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))
