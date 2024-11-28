from django.shortcuts import render , redirect ,get_object_or_404
from django.urls import reverse , reverse_lazy
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import ListView , CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Amenities, Contact , Reservation ,Services
from .forms import ContactForm , ReservationForm

import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request,'profils/home.html')


class AmenitiesListview(ListView):
    model = Amenities
    template_name = 'profils/amenitie.html'
    context_object_name = 'amenities'

class ServicesListview(ListView):
    model = Services
    template_name = 'profils/service.html'
    context_object_name = 'services'


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class =  ReservationForm
    template_name = 'profils/reservation.html'
    success_url = reverse_lazy('home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = get_object_or_404(Services, id=self.kwargs['service_id'])
        context['service'] = service
        return context


    def form_valid(self, form):
        try:
            # Associer l'utilisateur connecté à la réservation
            form.instance.user = self.request.user
            logger.info("Tentative de sauvegarde de la réservation pour l'utilisateur : %s", self.request.user.email)
            # Associer le service  à la réservation
            form.instance.service = get_object_or_404(Services, id=self.kwargs['service_id'])
            
            # Sauvegarde du formulaire
            response = super().form_valid(form)
            logger.info("Réservation sauvegardée avec succès pour l'utilisateur : %s", self.request.user.email)

            # Envoyer un email de confirmation
            self.send_confirmation_email()

            return response
        except Exception as e:
            logger.error("Erreur lors de la sauvegarde de la réservation : %s", e)
            return self.form_invalid(form)

    def send_confirmation_email(self):  
        try:
            # Récupérer l'email de l'utilisateur
            user_email = self.request.user.email
            subject = 'Confirmation de réservation'
            message = f"Bonjour {self.request.user.first_name},\n\nVotre réservation du {self.object.check_in} au {self.object.check_out} a été confirmée."
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user_email]

            send_mail(subject, message, from_email, recipient_list)
            logger.info("Email de confirmation envoyé avec succès à : %s", user_email)
        except Exception as e:
            logger.error("Erreur lors de l'envoi de l'email de confirmation : %s", e)


    def form_invalid(self, form):
        logger.error("Le formulaire est invalide : %s", form.errors)  # Log les erreurs de validation
        return super().form_invalid(form)


class ContactCreateview(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'profils/contact.html'

    def post(self, request, *args, **kwargs):
        """Gérer la soumission du formulaire de contact."""
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()  # Sauvegarder les informations du contact dans la base de données

            # Envoi d'un email de notification
            send_mail(
                subject=f'Nouveau message de contact: {contact.subject}',
                message=f'Nom: {contact.your_name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}',
                from_email='tonemail@gmail.com',
                recipient_list=['sowmariama2385@gmail.com'],  # Remplace par ton email
                fail_silently=False,
            )

            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('home')  # Rediriger vers la page d'accueil après soumission
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form  # Réinjecter le formulaire avec les erreurs
            return self.render_to_response(context)



 