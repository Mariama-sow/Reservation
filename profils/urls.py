from django.urls import path
from .views import home , AmenitiesListview , ContactCreateview , ReservationCreateView , ServicesListview


urlpatterns = [
   path('service/',ServicesListview.as_view() ,name='service' ),
   path('reservation/<int:service_id>/',ReservationCreateView .as_view() ,name='reservation' ),
   path('contact/',ContactCreateview.as_view() ,name='contact' ),
   path('amenitie/',AmenitiesListview.as_view() ,name='amenitie' ),
   path('home/',home ,name= 'home' ),

]