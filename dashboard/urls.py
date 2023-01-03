from django.urls import path
from . import views

urlpatterns = [
    path('' , views.dashboard , name='dashboard'),
    path('my-series', views.myseries, name='myseries'),
  

]