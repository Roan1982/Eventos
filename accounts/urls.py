from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('profile/', views.profile, name='profile'),
    path('blob/<int:pk>/', views.blob_serve, name='blob_serve'),
    path('', include('django.contrib.auth.urls')),  # login/logout/password reset
]
