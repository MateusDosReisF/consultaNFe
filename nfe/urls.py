from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views 

app_name = 'nfe'

urlpatterns = [
    path('empresas/list/', views.EmpresaListView.as_view(), name = 'empresa_list'),
    path('empresas/create/', views.EmpresaCreateView.as_view(), name = 'empresa_create'),
    path('empresas/<int:pk>/detail', views.EmpresaDetailView.as_view(), name = 'empresa_detail'),
    path('empresas/<int:pk>/update/', views.EmpresaUpdateView.as_view(), name = 'empresa_update'),
    path('empresas/<int:pk>/delete/', views.EmpresaDeleteView.as_view(), name = 'empresa_delete'),

    path('etiqueta/list/', views.EtiquetaListView.as_view(), name = 'etiqueta_list'),
    path('etiqueta/create/', views.EtiquetaCreateView.as_view(), name = 'etiqueta_create'),
    path('etiqueta/<int:pk>/update/', views.EtiquetaUpdateView.as_view(), name = 'etiqueta_update'),
    path('etiqueta/<int:pk>/delete/', views.EtiquetaDeleteView.as_view(), name = 'etiqueta_delete'),

    path('consultar_notas/', views.consulta_notas, name='consultar_notas'),
    path('listar_xmls/', views.listar_xmls, name='listar_xmls'), 
    path('adicionar-etiqueta/', views.adicionar_etiqueta, name='adicionar_etiqueta'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)