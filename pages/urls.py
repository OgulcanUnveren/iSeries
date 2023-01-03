from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    
    path('about' , views.about , name='about'),
    
    path('pages/<str:slug>',views.custompage,name='pages'),
  
]