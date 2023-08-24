from .views import PostsListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostsListSearchView
from django.urls import path
urlpatterns = [
    path('', PostsListView.as_view()),
    path('search/', PostsListSearchView.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
