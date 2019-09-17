from django.urls import path

from . import views

app_name = 'takken'
urlpatterns = [
    path('', views.index, name='index'),
    path('wat-na-leiding/', views.afterleaderview, name='afterleader'),
    path('<slug:tak>/', views.takview, name='tak'),
]
