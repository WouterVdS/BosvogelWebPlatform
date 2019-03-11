from django.urls import path

from . import views

urlpatterns = [
    path('', views.rent_home, name='rent'),
    path('fotos/', views.photos, name='photos'),
    path('tarieven/', views.pricing, name='pricing'),
    path('contracten/', views.contracts, name='contracts'),
    path('reserveren/', views.reserve, name='reserve'),
    path('reservering_bekijken/', views.check_reservation, name='check_reservation'),
]
