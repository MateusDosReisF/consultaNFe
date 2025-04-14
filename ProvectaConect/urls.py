from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('nfe/', include('nfe.urls')), 
    path('financeiro/', include('financeiro.urls')),
]
