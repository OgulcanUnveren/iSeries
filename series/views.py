from django.shortcuts import get_object_or_404, render, redirect
from .models import Serie,SerieCategory,Episode,SerieWatcher,SerieDuration,SerieRating,ParentEpisode
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.db import connection
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django_ratelimit.decorators import ratelimit


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]
@ratelimit(key='ip', rate='10/m', block=True)
def index(request):
    
    
    series = Episode.objects.all().order_by('-id')    
    paginator = Paginator(series , 12)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    categories = SerieCategory.objects.all()
    sayi = []
    categories_left = []
    for category in categories:
        cat_sayi = Serie.objects.all().filter(serie_category__id=category.id)
        if cat_sayi.count() > 0:
            categor = '<li><a href="/series/category/'+str(category.id)+'">'+category.title+'<span>'+'('+str(cat_sayi.count())+')'+'</span></a></li>'
            
            categories_left.append(categor)
            
    toplamcat = len(categories_left)
    try:
        lasts = Serie.objects.all().filter(trending=True).order_by('-id')[:3]
    except:
        lasts = None

        
    context = {
        'edx_host':settings.EDX_HOST,
        'toplamcat':toplamcat,
        'cate':categories_left,
        'lasts':lasts,
        'series':paged_listings,
    }
    return render(request,'series/serie.html', context)

@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='10/m', block=True)
def addtowatchers(request,slug):
    if request.method == 'GET':
        user = request.user
        serie = get_object_or_404(Serie,slug=slug)
        is_bought = True
        if_exist = SerieWatcher.objects.filter(user__id=user.id,serie_id=serie.id).first()
        if if_exist is not None:
            return redirect('/dashboard/my-series')
        else:
            yeni = SerieWatcher(user=user,serie_id=serie.id,is_bought=is_bought)
            yeni.save()
            return redirect('/dashboard/my-series')



@ratelimit(key='ip', rate='5/m', block=True)
def search(request):
    
    if request.method == "GET":
        return redirect("/")
    
    last_three = Serie.objects.all().filter(trending=True).order_by('-id')[:3]
    #Keywords
    categories = SerieCategory.objects.all()
    sayi = []
    categories_left = []
    for category in categories:
        cat_sayi = Serie.objects.all().filter(serie_category__id=category.id).order_by('-id')
        if cat_sayi.count() > 0:
            categor = '<li><a href="/series/category/'+str(category.id)+'">'+category.title+'<span>'+'('+str(cat_sayi.count())+')'+'</span></a></li>'
            
            categories_left.append(categor)
            
    toplamcat = len(categories_left)
    

    
    
    if 'keywords' in request.POST:
        keywords = request.POST['keywords']
        if keywords != '':
            series = Serie.objects.all().filter(Q(title__icontains=keywords) | Q(description__icontains=keywords)).order_by('-id')
            paginator = Paginator(series , 12)
            page = request.GET.get('page')
            paged_listings = paginator.get_page(page)
    context = {
        'edx_host':settings.EDX_HOST,
        'toplamcat':toplamcat,
        'cate':categories_left,
        'searchparam':request.POST['keywords'],
        'lasts':last_three,
        'series':series,
        'seriescount':series.count(),
    }
    return render(request, 'series/serie.html',context)
@ratelimit(key='ip', rate='5/m', block=True)
def categoryview(request, category_id):
    maincat = get_object_or_404(SerieCategory,id=category_id)
    last_three = Serie.objects.all().filter(serie_category__id=category_id)
    categories = SerieCategory.objects.all()
    sayi = []
    categories_left = []
    for category in categories:
        cat_sayi = Serie.objects.all().filter(serie_category__id=category.id).order_by('-id')
        if cat_sayi.count() > 0:
            categor = '<li><a href="/series/category/'+str(category.id)+'">'+category.title+'<span>'+'('+str(cat_sayi.count())+')'+'</span></a></li>'
            
            categories_left.append(categor)
            
    toplamcat = len(categories_left)
       
    

        
    context = {
        'edx_host':settings.EDX_HOST,
        'toplamcat':toplamcat,
        'cate':categories_left,
        'maincat':maincat,
        'series':last_three,
        'seriescount':last_three.count(),
    }
    return render(request,'series/serie.html', context)
@ratelimit(key='ip', rate='5/m', block=True)
def seriedetail(request,slug):
    
    #teachers =dictfetchall(cursor3) 
    #teachers = WatcherSerieaccessrole.objects.all().filter(serie_id=serie_id,role='instructor')
    #print(teachers)
    serie = get_object_or_404(Serie,slug=slug)
    rate_count = SerieRating.objects.filter(serie_id=serie.id).all()
    rate_count = rate_count.count()
    rater = 0
    varmi = SerieRating.objects.filter(serie_id=serie.id,user__id=request.user.id).first()
    if varmi:
        kullanmis = True
    else:
        kullanmis = False
    teacher = []
    if request.user.is_authenticated:
        bought = SerieWatcher.objects.filter(serie_id=serie.id,user_id=request.user.id).count()
    #bought  = bought.count()
        print(bought)
        if bought == 1:
            bought = True
        else:
            bought = False
    else:
        bought = False 
   # counter = episodes.count()
    i = 0
    context = {
        'varmi':varmi,
        'kullanmis':kullanmis,
        'counter':rate_count,
       # 'serie_detail':serie_detail,
        'edx_host':settings.EDX_HOST,
        'teacher':teacher,
        'bought':bought,
        'serie':serie,
       # 'episodes':episodes,
    }
    return render(request,'series/seriedetail.html',context)
@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='5/m', block=True)
def episode(request,serie_id):

    duration = SerieDuration.objects.all().filter(serie_id=serie_id,user__id=request.user.id)
    print(duration.count())
    if duration.count() > 0:
        episode_id = duration[0].episode_id
       
        serie = get_object_or_404(Serie,id=serie_id)
        episode = Episode.objects.get(id=episode_id)

        context = {
        'episode_id':episode_id,
        'first':episode,
        'serie':serie,
    }
        return render(request,'series/episode.html',context)
    
    
    else:
        serie = get_object_or_404(Serie,id=serie_id)
    
        i = 0;
        for parent in serie.parent_episode.all():
            if i >= 1:
                pass
            else:
            
                first = parent.episodes.all()[0]
                i+=1    
     
        context = {
        'episode_id':first.id,
        'first':first,
        'serie':serie,
    }
        return render(request,'series/episode.html',context)
@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='5/m', block=True)      
def episodefromclick(request,slug,episodeslug):
    serie = get_object_or_404(Serie,slug=slug)
    episode = Episode.objects.get(episode_slug=episodeslug)
    if episode.episode_type =='video':
        context = {
        'episode_id':episode.id,
        'first':episode,
        'serie':serie,
    }
        return render(request,'series/episode.html',context)
    else:
        return render(request,'series/episodequiz/quizview.html')
@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='1/m', block=True)        
def addrating(request):
    if request.method == 'POST':
        serie_id = request.POST.get('serie_id')
        rating_value = request.POST.get('rating')
        if int(rating_value) > 5:
            messages.info(request, ' En fazla 5 yıldızla oy kullanabilirsiniz')
            return redirect(f'/series/{serie_id}')
        varmi = SerieRating.objects.all().filter(user__id=request.user.id,serie_id=serie_id)
        if varmi:
            messages.info(request, ' Zaten Kurs Değerlendirilmiş')
            return redirect(f'/series/{serie_id}')
        else:
            yenioy = SerieRating(user=request.user,rating_value=rating_value,serie_id=serie_id)
            yenioy.save()
            serie_rating = SerieRating.objects.all().filter(serie_id=serie_id)
            rater = 0
            if serie_rating:
                for rate in serie_rating:
                    rater+=int(rate.rating_value)
                rater = rater / int(serie_rating.count())
                rateoran = rater * 100 / 5

            else:
                rater = 0
                rateoran= 0
            serier = Serie.objects.get(serie__id=serie_id)    
            serier.rater = rater
            serier.rateoran = rateoran
            serier.save()
            messages.info(request, ' Kurs Değerlendirme oyunuz Eklendi')
            return redirect(f'/series/{serie_id}')

def get_current_serie(titler):
    return get_object_or_404(Serie, title=titler)

@csrf_exempt 
def bulk_add_serie(request):
    if request.method == "POST":
        title = request.POST.get("title")
        slug = request.POST.get("slug")
        desc = request.POST.get("desc")
        
        serie_image = request.FILES.get('serie_image')
        print(serie_image)
        #return
        price = 0
        uzatmadegeri = 0
        featured = True
        trending = True
        popular = True
        meta_title = title
        meta_description = desc
        meta_keywords = desc
        is_published = True
        is_free = True
        yeni = Serie(title=title,slug=slug,description=desc,price=price,uzatmadegeri=uzatmadegeri,serie_image=serie_image,featured=featured,trending=trending,popular=popular,meta_title=meta_title,meta_description=meta_description,meta_keywords=meta_keywords,is_published=is_published,is_free=is_free)
        yeni.save()
        cater = str(request.POST.get("cat_title"))
        cat_array = []
        my_list = cater.split(",")
        for element in my_list:
            element = element.replace("\t","")
            element = element.replace("\n","")
            element = element.replace(" ","")
            cat = SerieCategory.objects.filter(title=element).first()
            #print("cat:"+str(cat.count()))
            
            
            
            
            current_serie = get_current_serie(request.POST['title'])
            current_serie.serie_category.add(cat)
            current_serie.save()
          
        
        
        
        from django.http import JsonResponse
        return JsonResponse({'oldu':'oldu'})



@csrf_exempt
def bulk_catadd(request):
    if request.method == "POST":
        title = request.POST.get("cat_title")
        icon = "icon"+str(title)
        cate = SerieCategory.objects.create(title=title,icon=icon)
        cate.save()
        from django.http import JsonResponse
        return JsonResponse({'olducat':'olducat'})


@csrf_exempt
def parent_episode(request):
    if request.method == "POST":
        title =str(request.POST.get('seasondata'))
        ccounter = ParentEpisode.objects.filter(title=title)
        if ccounter.count() > 0:
            pass
        else:
            yeni = ParentEpisode(sequence=request.POST.get('sequence'),title=title)
            yeni.save()

        peps = ParentEpisode.objects.filter(title=request.POST.get('seasondata')).first()

        current_serie = get_current_serie(request.POST.get('title'))
        current_serie.parent_episode.add(peps)
        current_serie.save()
        from django.http import JsonResponse
        return JsonResponse({'sezon oldu':'sezon eklendi'})
@csrf_exempt
def episodes(request):
    if request.method == "POST":
        episode_title = str(request.POST.get('episode_title'))
        counter = Episode.objects.filter(episode_title=episode_title)
        if counter.count()> 0:
            pass
        else:
            yeni = Episode(episode_title=episode_title,episode_type="video",episode_slug=request.POST.get('episode_slug'),episode_position=request.POST.get('episode_position'),episode_text='<iframe width="560" height="315" src="https://www.youtube.com/embed/CoXOilsdBcs" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
            yeni.save()

        peps = Episode.objects.filter(episode_title=episode_title).first()

        current_serie = get_object_or_404(ParentEpisode,title=request.POST.get('seasondata'))
        current_serie.episodes.add(peps)
        current_serie.save()
        from django.http import JsonResponse
        return JsonResponse({'Bölüm '+str(request.POST.get('episode_position'))+":"+episode_title+" oldu" :'sezon eklendi'})