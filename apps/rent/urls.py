from django.urls import path

from . import views

app_name = 'rent'
urlpatterns = [
    path('', views.index, name='index'),
    path('beheer/', views.manage_rentals, name='manage_rentals'),
    path('fotos/', views.photos, name='photos'),
    path('tarieven/', views.pricing, name='pricing'),
    path('contracten/', views.contracts, name='contracts'),
    path('reserveren/', views.reserve, name='reserve'),
    path('reservering_bekijken/', views.check_reservation, name='check_reservation'),
]
