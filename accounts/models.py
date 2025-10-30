from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.User.objects.all()


# Folio................................................................................................................
class Folio(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.CharField(max_length=100)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.guest_name


#Folio Add Items

class FolioItem(models.Model):
    folio = models.ForeignKey(Folio, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_room_charge = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description





