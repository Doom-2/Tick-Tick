from django.urls import path
from core import views
from core.views import VkApiErrorPage, VkLoginErrorPage

urlpatterns = [
    path('core/signup', views.UserCreateView.as_view(), name='create-user'),
    path('core/login', views.UserLoginView.as_view(), name='login-user'),
    path('core/profile', views.UserProfile.as_view(), name='user-profile'),
    path('core/update_password', views.ChangePasswordView.as_view(), name='user-update-password'),
    path('core/vk_api_error/', VkApiErrorPage.as_view(), name='vk-api-error-page'),
    path('core/vk_login_error/', VkLoginErrorPage.as_view(), name='vk-login-error-page'),
]
