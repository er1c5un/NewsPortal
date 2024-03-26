from django_filters import FilterSet, CharFilter, \
    DateFilter
from .models import Ad, Category, Response


class AdFilter(FilterSet):
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains')
    create_date = DateFilter(field_name='create_date', lookup_expr='gt')

    class Meta:
        model = Ad
        fields = {'author', 'create_date'}


class MyResponsesFilter(FilterSet):
    ad = CharFilter(field_name='ad__title', lookup_expr='icontains')
    create_date = DateFilter(field_name='create_date', lookup_expr='gt')
    class Meta:
        model = Response
        fields = {'ad', 'create_date'}
