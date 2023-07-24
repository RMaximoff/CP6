from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import UserCreateView, WaitActivationView, EmailVerificationView, UserPasswordResetView, ProfileView

app_name = 'users'

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('register/whait', WaitActivationView.as_view(), name='wait_activation'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
