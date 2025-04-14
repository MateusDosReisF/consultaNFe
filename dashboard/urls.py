from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from .views import dashboard_view
from . import views

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('acompanhar_op/', views.acompanhar_op, name='acompanhar_op'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
