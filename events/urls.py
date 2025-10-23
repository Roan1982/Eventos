from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('crear/', views.EventCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    path('<slug:slug>/editar/', views.EventUpdateView.as_view(), name='edit'),
    path('<slug:slug>/eliminar/', views.EventDeleteView.as_view(), name='delete'),
    path('<slug:slug>/contactar/', views.contact_creator, name='contact_creator'),
    path('review/<slug:slug>/add/', views.add_review, name='add_review'),
    path('review/delete/<int:pk>/', views.delete_review, name='delete_review'),
    path('media/<int:pk>/', views.media_blob_serve, name='media_blob'),
]
