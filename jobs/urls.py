from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('new/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/edit/', views.job_update, name='job_update'),
]