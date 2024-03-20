from django_filters import FilterSet, CharFilter, \
    DateFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Ad, Category, Response


# создаём фильтр
class AdFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains')
    create_date = DateFilter(field_name='create_date', lookup_expr='gt')
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Ad
        fields = {'author', 'create_date'}  #'create_date': ['gt'] поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)


class MyResponsesFilter(FilterSet):
    ad = CharFilter(field_name='ad__title', lookup_expr='icontains')
    create_date = DateFilter(field_name='create_date', lookup_expr='gt')
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Response
        fields = {'ad', 'create_date'}  #'create_date': ['gt'] поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
