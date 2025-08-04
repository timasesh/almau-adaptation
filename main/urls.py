from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('about/', views.about_view, name='about'),
    path('documents/', views.documents_view, name='documents'),
    path('api/documents/search/', views.documents_api_search, name='documents_api_search'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
    path('logout/', views.logout_view, name='logout'),
    path('processes_instructions/', views.processes_instructions_view, name='processes_instructions'),
    path('api/processes_instructions/search/', views.processes_instructions_api_search, name='processes_instructions_api_search'),
    path('map/', views.map_view, name='map'),
]
