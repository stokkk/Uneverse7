from django.urls import path
from django.contrib.auth import views as auth_views # джанговские вьюхи авторизации и т.д

from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LogInView, name='login'),
    path('logout/', views.LogOutView, name='logout'),
#    path('change-password/', auth_views.PasswordChangeView.as_view()), # пример использования стандартных вьюх django
]