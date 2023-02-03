from django.urls import path
from . import views

urlpatterns = [
    path('verify', views.BotUpdateView.as_view()),
]
