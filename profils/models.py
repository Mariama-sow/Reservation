from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from djmoney.models.fields import MoneyField



class Services(models.Model):
    name = models.CharField(max_length= 100)
    image = models.ImageField(upload_to='services/')
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    description = models.TextField()
   


    def __str__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = [
    ('pending', 'En attente'),
    ('confirmed', 'Confirmée'),
    ('cancelled', 'Annulée'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    check_in = models.DateTimeField(verbose_name='Début de réservation')
    check_out = models.DateTimeField(verbose_name='Fin de réservation')
    special_request = models.TextField(verbose_name='Demande spéciale', blank=True, null=True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)


    def clean(self):
        if self.check_out <= self.check_in:
            raise ValidationError("La date de fin de réservation doit être postérieure à la date de début.")
        if self.check_in < timezone.now():
            raise ValidationError("La date de début ne peut pas être dans le passé.")
        

    def __str__(self):
        return f"Réservation de {self.user.first_name} {self.user.last_name} du {self.check_in} au {self.check_out}"


class Contact(models.Model):
    your_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)  # Enregistre automatiquement la date d'envoi

    def __str__(self):
        return self.subject


class Amenities(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    description = models.TextField()
    services = models.ManyToManyField(Services) 

    
    def __str__(self):
        return self.name

