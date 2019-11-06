from django.urls import path

from . import views

app_name = 'agenda'
urlpatterns = [
    path('', views.index, name='index'),
    path('alle-vergaderingen', views.index, {'all_vergaderingen': 'True'}, name='index_all_vergaderingen')
]
