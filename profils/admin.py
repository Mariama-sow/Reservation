from django.contrib import admin
from .models import Amenities, Services , Reservation

admin.site.register(Amenities)
admin.site.register(Services)
admin.site.register(Reservation)