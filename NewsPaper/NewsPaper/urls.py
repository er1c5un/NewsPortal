from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path(r'admin/', admin.site.urls),
    path(r'', include('news.urls')),
    path('accounts/', include('allauth.urls')),
    # url(r'^categories/', include('news.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
