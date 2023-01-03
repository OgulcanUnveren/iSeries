from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/reports/',views.sendreport,name='sendreport'),
]