from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import ListView, CreateView

from ads.filters import AdFilter
from ads.models import Ad, Person, Category
from ads.forms import AdForm


# LoginRequiredMixin

class AdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = ['-create_date']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        context['filter'] = AdFilter(self.request.GET, queryset=self.get_queryset())
        # К словарю добавим текущую дату в ключ 'time_now'.
        #context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_sale'] = None
        return context


class AdCreateView(LoginRequiredMixin, CreateView):
    # permission_required = ('news.add_post', 'news.change_post')
    template_name = 'ad_create.html'
    form_class = AdForm

    def post(self, request, *args, **kwargs):
        # user = request.POST['user']
        author = Person.objects.get(user=request.user.id)
        new_ad = Ad(
            author=author,  # получить автора по айдишнику из запроса Category.objects.get(id=category_id)
            # category=Category.objects.get(id=request.POST['category']),
            title=request.POST['title'],
            text=request.POST['text']
        )
        new_ad.save()
        category = Category.objects.get(id=request.POST['category'])
        new_ad.category.set([category])  # Используем метод set() для установки значения для поля many-to-many

        #  Запускаем задачу celery по рассылке подписчикам на данную категорию
        # send_email_to_subscribers_of_new_post.delay(category_id=request.POST['category'], post_id=new_post.id)

        return redirect('/')
