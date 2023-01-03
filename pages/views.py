from django.shortcuts import render,get_object_or_404,redirect
from .models import About, FAQ, FooterPages
from series.models import Serie
from django.contrib.auth.models import User,Group


import datetime
import locale
from django.db import connection
from django.conf import settings
from series.models import Serie,Episode
from django.core.paginator import Paginator
from django_ratelimit.decorators import ratelimit
@ratelimit(key='ip', rate='10/m', block=True)
def index(request):
    
    # localetr = 'tr'
    # locale.setlocale(locale.LC_ALL, localetr)
    
    series = Episode.objects.all().order_by('-id')
    paginator = Paginator(series, 30) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    series = paginator.get_page(page_number)
    
    
    # series = Serie.objects.all().order_by('-id')
    #group = Group.objects.get(id=group_id)
    #users = group.user_set.all()
    
    ids = []
    
    # if teachers_define:
    #     for teacher in teachers_define:
    #         ids.append(teacher.teacher.id)
    #     ids = list(ids)
    # teachers = User.objects.all().filter(id__in=ids)   # group = Group.objects.all()
    num_user = User.objects.all().count()
   
    num_serie = Serie.objects.all().count()
    context = {
        
        'num_user':num_user,
        
        'num_serie':num_serie,
        'series':series,
       
    #    'groups':group,
    }
    return render(request,'pages/index.html', context)
@ratelimit(key='ip', rate='10/m', block=True)
def custompage(request,slug):
    page = get_object_or_404(FooterPages,slug=slug)
    context = {
        'page':page,
    }
    return render(request,'pages/footerpage.html', context)
@ratelimit(key='ip', rate='10/m', block=True)
def about(request):
    about_content = About.objects.first()
    if about_content:
        context= {
        'about':about_content,
    }
        return render(request, 'pages/about.html', context)
    else:
        get_object_or_404(About,id=1)
 
