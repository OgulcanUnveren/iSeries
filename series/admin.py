from django.contrib import admin
from .models import Serie,SerieCategory,Episode,ParentEpisode,SerieWatcher,EpisodeFiles,SerieDuration,SerieRating
# Register your models here.
from django.contrib.auth.models import User
class SerieSetting(admin.ModelAdmin):
    list_display = ('id','title','featured','trending','popular')

    

admin.site.register(Serie, SerieSetting)
class SerieCategorie(admin.ModelAdmin):
    list_display = ('id','title','icon')
admin.site.register(SerieCategory,SerieCategorie)

class SerieWatcheria(admin.ModelAdmin):
    list_display = ('id','user','serie_id')
admin.site.register(SerieWatcher,SerieWatcheria)
class EpisodeContext(admin.ModelAdmin):
    list_display = ('id','episode_title','episode_is_published')
admin.site.register(Episode,EpisodeContext)
class ParentEpisodes(admin.ModelAdmin):
    list_display= ('id','title')
admin.site.register(ParentEpisode,ParentEpisodes)
class EpisodeFilesAdmin(admin.ModelAdmin):
    list_display = ('id','file')
admin.site.register(EpisodeFiles,EpisodeFilesAdmin)

class SerieDurationa(admin.ModelAdmin):
    list_display = ('id','user','serie_id')
admin.site.register(SerieDuration,SerieDurationa)

class SerieRatina(admin.ModelAdmin):
    list_display = ('id','user','serie_id')
admin.site.register(SerieRating,SerieRatina)