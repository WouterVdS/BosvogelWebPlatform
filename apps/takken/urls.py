from django.urls import path

from . import views

app_name = 'takken'
urlpatterns = [
    path('', views.index, name='index'),
    path('wat-na-leiding/', views.afterleader, name='afterleader'),
    path('<slug:tak>/', views.tak, name='tak'),
]
