from gc import get_objects
from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, ResetPasswordSerializer, FolioItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

#Forget password APIVIEW......................

from .serializers import ForgotPasswordSerializer

#Reservations.............................
from rest_framework.permissions import IsAuthenticated
from .models import Reservation, FolioItem
from .serializers import ReservationSerializer
from rest_framework.exceptions import PermissionDenied

# Swagger........................
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

#Folio...........................
from .models import Folio
from .serializers import FolioSerializer,FolioItemSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
#.......................................................................................................................

  #Profile Update
class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


    # def get_object(self):
    #     return self.request.user


    def put(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

#Profile Delete
class ProfileDeleteView(generics.DestroyAPIView):
      permission_classes = [permissions.AllowAny]
      serializer_class = UserSerializer

      def delete(self, request, pk):
       obj = User.objects.get(pk=pk)
       obj.delete()
       return Response("Deleted successfully")


    # def get_object(self):
    #     return self.request.user


#.......................................................................................................................

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



#change password and reset password


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"detail": "Old password is incorrect"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password updated successfully"}, status=200)


#Forget password APIVIEW
#generics add pannanum swagger la use aga
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password reset link sent to email."})
        return Response(serializer.errors, status=400)


#Reset password

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been reset."})
        return Response(serializer.errors, status=400)


#Reservation.............................................................................

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ReservationSerializer

    # def perform_create(self, serializer):
    #     serializer.save(Reservation=self.request.user)


#Folio..................................................................................


class FolioCreateView(generics.CreateAPIView):
    queryset = Folio.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = FolioSerializer


    def post(self, request):
        serializer = FolioSerializer(data=request.data)
        if serializer.is_valid():
            folio = serializer.save()
            return Response(FolioSerializer(folio).data, status=201)
        return Response(serializer.errors, status=400)


#Folio Detail create
class FolioDetailView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = FolioSerializer

    def get(self, request, pk):
        details = Folio.objects.get(pk=pk)
        serializer = FolioSerializer(details).data
        return Response(serializer)



#Folio Add Items................................................................................................

class FolioItemCreateView(generics.CreateAPIView):
    serializer_class = FolioItemSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        try:
            folio = Folio.objects.get(id=pk)
        except Folio.DoesNotExist:
            return Response({"error": "Folio not found"}, status=404)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(folio=folio)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#Folio update.......
class FolioItemUpdateView(generics.UpdateAPIView):
    queryset = FolioItem.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = FolioItemSerializer

    def put(self, request, pk):
        obj = get_object_or_404(FolioItem, pk=pk)
        serializer = FolioItemSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

