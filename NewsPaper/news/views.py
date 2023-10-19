from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, \
    DeleteView

from .models import Post
from .filters import PostFilter
from .forms import PostForm


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


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'


@login_required
def become_author(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts/')
