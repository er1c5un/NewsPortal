#from django.conf.urls.i18n import i18n_patterns
from django.views.decorators.cache import cache_page

from .views import AdsListView
from django.urls import path

urlpatterns = [
    path('', cache_page(60)(AdsListView.as_view())),
    #path('search/', cache_page(300)(PostsListSearchView.as_view())),
    #path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    #path('create/', cache_page(300)(PostCreateView.as_view()), name='post_create'),
    #path('create/<int:pk>', cache_page(300)(PostUpdateView.as_view()), name='post_update'),
    #path('delete/<int:pk>', cache_page(300)(PostDeleteView.as_view()), name='post_delete'),
    #path('become_author/', become_author, name='become_author'),
    #path('subscribe/', subscribe, name='subscribe'),
]
