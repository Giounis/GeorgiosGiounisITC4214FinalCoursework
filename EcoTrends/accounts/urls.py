# accounts/urls.py
from django.urls import path
from . import views
from .views import CustomLoginView, delete_account

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('delete_account/', views.delete_account, name='delete_account'),

]