from django.contrib import admin

from .models import Person, Ad, Category, Response, AdCategory

admin.site.register(Person)
admin.site.register(Ad)
admin.site.register(Category)
admin.site.register(Response)
admin.site.register(AdCategory)
