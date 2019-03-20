from django.urls import path

from . import views

app_name = 'takken'
urlpatterns = [
    path('', views.index, name='index'),
]
