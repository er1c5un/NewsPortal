from django_filters import FilterSet, CharFilter, \
    DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category


# создаём фильтр
class PostFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains')
    create_date = DateFilter(field_name='create_date', lookup_expr='gt')
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {'author', 'create_date'}  #'create_date': ['gt'] поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)

    # создаём фильтр
class CategoryFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Category
        fields = {'name': ['icontains']}  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)