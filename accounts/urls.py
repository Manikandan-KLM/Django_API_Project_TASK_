from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, ReservationListCreateView, FolioItemUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ChangePasswordView
from .views import ForgotPasswordView
from .views import ResetPasswordView
from .views import ProfileUpdateView,ProfileDeleteView

#Reservation................................
from .views import ReservationListCreateView

#Folio..........................................

from .views import FolioCreateView,FolioDetailView,FolioItemCreateView,FolioItemUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
#UPdate and delete urls..................................................................................................
    path('update/', ProfileUpdateView.as_view()),
    path('api/profile/<int:pk>)',ProfileUpdateView.as_view()),

    # path('delete/', ProfileDeleteView.as_view()),
   path('api/delete/<int:pk>/', ProfileDeleteView.as_view()),

#.....................................................................................................................
    path('token/refresh/', TokenRefreshView.as_view()),

#change password and reset password

    path('change-password/', ChangePasswordView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

#Reservation............................................................................................................

    path('reservation/', ReservationListCreateView.as_view()),

#Folio.................................................................................................................

    path('folio-create/', FolioCreateView.as_view()),
    path('folio-detail/<int:pk>/', FolioDetailView.as_view()),
    path('folios-add-items/<int:pk>/items/', FolioItemCreateView.as_view()),
    path('folio-update-items/<int:pk>/', FolioItemUpdateView.as_view()),
]
