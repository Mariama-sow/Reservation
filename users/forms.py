from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder' : 'votre mot de passe',}), min_length=8 )
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'mot de passe de confirmation'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password','password_confirm')
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre prenom'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom_utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse email'}),
        }
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)  # Applique les règles de validation de Django
        return password
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet email existe déjà.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hacher le mot de passe
        if commit:
            user.save()
        return user
        
class CustomUserLoginForm(AuthenticationForm):
     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom_utilisateur'}),)
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder' : 'votre mot de passe',}), min_length=8 )
    