from django.urls import path

from home.views import HomeView


urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
]
