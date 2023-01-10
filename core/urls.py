from django.urls import path
from core import views

urlpatterns = [
    path('core/signup', views.UserCreateView.as_view(), name='create_user'),
    path('core/login', views.UserLoginView.as_view(), name='login_user'),
    path('core/profile', views.UserProfile.as_view(), name='user_profile'),
    path('core/update_password', views.ChangePasswordView.as_view(), name='change_password'),
]
