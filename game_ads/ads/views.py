from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView, DetailView
from django.core.cache import cache
from ads.filters import AdFilter
from ads.models import Ad, Person, Category
from ads.forms import AdForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .filters import MyResponsesFilter
from .models import Response, Ad


# LoginRequiredMixin

class AdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = ['-create_date']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdFilter(self.request.GET, queryset=self.get_queryset())
        context['next_sale'] = None
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    template_name = 'ad_create.html'
    form_class = AdForm

    def post(self, request, *args, **kwargs):
        author = Person.objects.get(user=request.user.id)
        new_ad = Ad(
            author=author,
            title=request.POST['title'],
            text=request.POST['text']
        )
        new_ad.save()
        category = Category.objects.get(id=request.POST['category'])
        new_ad.category.set([category])  # Используем метод set() для установки значения для поля many-to-many

        #  Запускаем задачу celery по рассылке подписчикам на данную категорию

        return redirect('/')


@login_required
def CreateResponse(request, ad_id):
    advertisement = get_object_or_404(Ad, pk=ad_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        response_person = Person.objects.get(user=request.user.id)
        response = Response(person=response_person, ad=advertisement, text=text)
        response.save()
        return redirect('ad_detail', pk=ad_id)
    return render(request, 'create_response.html', {'ad': advertisement})


class AdDetailView(LoginRequiredMixin, DetailView):
    template_name = 'ad_detail.html'
    queryset = Ad.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'ad-{self.kwargs["pk"]}',
                        None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'ad-{self.kwargs["pk"]}', obj)
        return obj


class MyResponsesListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'my_responses.html'
    context_object_name = 'my_responses'
    ordering = ['-create_date']
    paginate_by = 2

    def get_queryset(self):
        current_user = self.request.user.id
        queryset = Response.objects.filter(ad__author=current_user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MyResponsesFilter(self.request.GET, queryset=self.get_queryset())

        return context


@login_required
def accept_response(request):
    user = request.user
    response_id = int(request.GET.get('resp_id'))
    Response.objects.filter(id=response_id).update(accepted=True)
    mail_accepted_response_back()

    return redirect('/my_responses/')


@login_required
def delete_response(request):
    user = request.user
    response_id = int(request.GET.get('resp_id'))
    Response.objects.filter(id=response_id).update(deleted=True)
    mail_accepted_response_back()

    return redirect('/my_responses/')


def mail_accepted_response_back():
    print('EMAIL SENDING TO RESPONSER')
    pass
