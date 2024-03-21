#from django.conf.urls.i18n import i18n_patterns
from django.views.decorators.cache import cache_page

from .views import AdsListView, AdCreateView, CreateResponse, AdDetailView, MyResponsesListView, \
    accept_response, delete_response
from django.urls import path

urlpatterns = [
    path('', cache_page(60)(AdsListView.as_view()), name='ads'),
    #path('search/', cache_page(300)(PostsListSearchView.as_view())),
    path('<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('create/', cache_page(300)(AdCreateView.as_view()), name='ad_create'),
    #path('create/<int:pk>', cache_page(300)(PostUpdateView.as_view()), name='post_update'),
    #path('delete/<int:pk>', cache_page(300)(PostDeleteView.as_view()), name='post_delete'),
    path('accept_response/', accept_response, name='accept_response'),
    path('delete_response/', delete_response, name='delete_response'),
    #path('subscribe/', subscribe, name='subscribe'),
    path('response/<int:ad_id>/', CreateResponse, name='create_response'),
    path('my_responses/', MyResponsesListView.as_view(), name='my_responses'),
]
