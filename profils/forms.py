from django import forms

from .models import Contact, Reservation

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['your_name', 'email', 'subject', 'message']
        widgets = {
            'your_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message'}),
        }

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'special_request',]
        widgets = {
            'check_in': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'check_out': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'special_request': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Demande spéciale'}),
            # 'service': forms.Select(attrs={'class': 'form-control'}),
        }

