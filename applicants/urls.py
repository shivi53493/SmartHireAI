from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    path('', views.applicant_list, name='applicant_list'),
    path('new/', views.applicant_create, name='applicant_create'),
    path('<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('<int:pk>/edit/', views.applicant_update, name='applicant_update'),
    path('parse-resume/', views.parse_resume, name='parse_resume'),
]
