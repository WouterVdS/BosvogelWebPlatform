from django.urls import path

from . import views

app_name = 'profile'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>', views.index, name='index_year'),
    path('<slug:name>', views.profile, name='profile'),
]
