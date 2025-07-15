from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='start'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),

]