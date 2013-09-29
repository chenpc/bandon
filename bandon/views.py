from menu.models import Buy
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
    
def logout_view(request):    
    logout(request)
    return HttpResponseRedirect(reverse('index'))
