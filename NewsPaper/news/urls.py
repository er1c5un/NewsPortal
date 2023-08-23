#from django.urls import path
# Импортируем созданное нами представление
#from django.urls import path, include
#from django.urls import path
from django.template.defaulttags import url

#from django.urls import path
#from django.conf.urls import url, include
from .views import PostsListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from django.urls import path
urlpatterns = [
    path('', PostsListView.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Ссылка на детали новости
    path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание новости
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
