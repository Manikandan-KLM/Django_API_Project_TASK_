from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

#change password and reset password

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse


#Forgot password

from django.utils.http import urlsafe_base64_decode

#Reservatins.....

from .models import Reservation, FolioItem

#Folio............
from .models import Folio,FolioItem


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


#change password and reset password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

#Forgot password


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Build password reset link
        reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
        send_mail(
            subject="Password Reset",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[email],
        )


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError("Invalid or expired token")

        return attrs

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()



#Reservations......................................................................................................................

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['reservation', 'reservation_date']


#Folio.................................................................................................................

class FolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folio
        fields = '__all__'

#Folio Add Items.......................................................................................................

class FolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolioItem
        fields = '__all__'























