from django import template 

import hashlib
from six import text_type
from django.conf import settings
from django.contrib.auth.models import User
from series.models import Serie,ParentEpisode,Episode
register = template.Library()

@register.filter(name='getname')
def getname(self):
    
    episode = Serie.objects.filter(parent_episode__episodes__id=self).first()    
    epsmin  = Episode.objects.filter(id=self).first()
    if episode is not None:
        sezon_bas = ParentEpisode.objects.filter(episodes__id=self).first()
                
        episode =  episode.title + " | " + sezon_bas.title + " | " + epsmin.episode_title
        return episode
    else:
            
        return "HATA"
@register.filter(name='getserieimage')
def getserieimage(self):
    episode = Serie.objects.filter(parent_episode__episodes__id=self).first()
    return episode.serie_image.url 
@register.filter(name='getserieslug')
def getserieslug(self):
    episode = Serie.objects.filter(parent_episode__episodes__id=self).first()
    return episode.slug     