from django.urls import path
from .views import CustomUserLogin , CustomLogoutView , CustomUserCreation


app_name ='users'

urlpatterns=[
    path('login/', CustomUserLogin.as_view(),name= 'login' ),
    path('logout/', CustomLogoutView.as_view(), name= 'logout'),
    path('creation/', CustomUserCreation.as_view(),name='creation')
]