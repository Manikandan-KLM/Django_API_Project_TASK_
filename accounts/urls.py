from django.urls import path
from .views import RegisterView, ProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ChangePasswordView
from .views import ForgotPasswordView
from .views import ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

#change password and reset password

    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),


]
