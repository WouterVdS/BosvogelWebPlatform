from django.urls import path

from . import views

app_name = 'rent'
urlpatterns = [
    path('', views.index, name='index'),
    path('beheer/', views.manage_rentals, name='manage_rentals'),
    path('fotos/', views.photos, name='photos'),
    path('gebouw_en_terrein/', views.building_and_terrain, name='building_and_terrain'),
    path('tarieven/', views.pricing, name='pricing'),
    path('tarieven_aanpassen/', views.change_pricing, name='change_pricing'),
    path('contracten/', views.contracts, name='contracts'),
    # todo make choice: contracts publicly available, or trough mail when reserved? Or via 'huishoudelijk regelement'?
    path('reserveren/', views.reserve, name='reserve'),
]
