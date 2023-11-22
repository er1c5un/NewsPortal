from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import ListView, UpdateView, CreateView, DetailView, \
    DeleteView

from .models import Post, CategorySubscribers, Category, Author
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_email_to_subscribers_of_new_post


class PostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-create_date']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostsListSearchView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts_search.html'
    context_object_name = 'posts'
    ordering = ['-create_date']
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', 'news.change_post')
    template_name = 'post_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        #user = request.POST['user']
        author = Author.objects.get(user=request.user.id)
        new_post = Post(
            author=author,# получить автора по айдишнику из запроса Category.objects.get(id=category_id)
            #category=Category.objects.get(id=request.POST['category']),
            title=request.POST['title'],
            text=request.POST['text']
        )
        new_post.save()
        category = Category.objects.get(id=request.POST['category'])
        new_post.category.set([category])  # Используем метод set() для установки значения для поля many-to-many

        #  Запускаем задачу celery по рассылке подписчикам на данную категорию
        send_email_to_subscribers_of_new_post.delay(category_id=request.POST['category'], post_id=new_post.id)

        return redirect('/')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    if not Author.objects.filter(user=user).exists():
        # Если экземпляр модели Author не существует, создаем его
        Author.objects.create(user=user, rate=0)

    return redirect('/')


@login_required
def subscribe(request):
    user = request.user
    category_id = int(request.GET.get('category_id'))
    category = Category.objects.get(id=category_id)
    category_user = CategorySubscribers.objects.filter(category=category, user=user)
    if not category_user:
        new_item = CategorySubscribers(category=category, user=user)
        new_item.save()
    red = request.META.get('HTTP_REFERER', '/')
    return redirect(red)
