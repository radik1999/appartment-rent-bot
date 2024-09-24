from django.urls import path
from appartment_bot import views


urlpatterns = [
    path('webhook/', views.telegram_webhook, name='telegram-webhook'),
]
