from django.contrib import admin
from django.urls import path, include
from events.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('events.api_urls')),
    path('eventos/', include('events.urls')),
    path('', HomeView.as_view(), name='home'),
]
