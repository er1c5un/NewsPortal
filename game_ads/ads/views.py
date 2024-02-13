from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from ads.models import Ad


#LoginRequiredMixin

class AdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = ['-create_date']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        #models = Ad.objects.all()
        context = super().get_context_data(**kwargs)
        #context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        #context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
