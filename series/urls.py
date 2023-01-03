from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',views.index, name='series'),
    path('search/' , views.search , name='seriesearch'),
    path('category/<int:category_id>' , views.categoryview , name='categoryview'),
    path('<str:slug>' ,views.seriedetail, name='seriedetail'),
    path('episode/<str:slug>' ,views.episode, name='episode'),
    path('episode/<str:slug>/<str:episodeslug>' ,views.episodefromclick, name='episodefromclick'),
    path('addrating/',views.addrating,name='addrating'),
    path('addtowatchers/<str:slug>/',views.addtowatchers,name='addtowatchers'),
    path('bulkadd/',views.bulk_add_serie,name='bulk_add_serie'),
    path('bulkcatadd/',csrf_exempt(views.bulk_catadd),name='addcatbulk'),
    path('seasonadd/',csrf_exempt(views.parent_episode),name='parent_episode'),
    path('addepisode/',csrf_exempt(views.episodes),name='episodes'),
]