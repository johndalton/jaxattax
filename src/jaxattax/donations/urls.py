from django.urls import path

from . import views

# app_name = 'donations'
urlpatterns = [
    path('create-session/', views.CreateSession.as_view(), name='create_session'),
    path('webhook/', views.receive_webhook, name='receive-webhook'),
]
