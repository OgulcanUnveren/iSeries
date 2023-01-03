from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth


from django.db import connection
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from series.models import SerieWatcher,Serie



@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='10/m', block=True)
def dashboard(request):
    

    
    
        bought = SerieWatcher.objects.all().filter(user_id=request.user.id)
    
        
        context = {
        
            'bought':bought.count(),
        
           #.user.groups.all(),
        }
        return render(request,'dashboard/watcher/main.html',context)
    
@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='10/m', block=True)
def myseries(request):
    
 
    purchased_series = SerieWatcher.objects.filter(user=request.user)
    
    if purchased_series.count() > 0:
        ids=[]
        
        for serie_id in purchased_series:
            dizi = serie_id.serie_id   
    
            
            ids.append(serie_id.serie_id)
        

        purchased = Serie.objects.filter(id__in=ids)
        context = {
            
            'series':purchased,
        }  
        return render(request,'dashboard/watcher/series/purchased_serie.html',context)
    else:
        return render(request,'dashboard/watcher/series/purchased_serie.html')
