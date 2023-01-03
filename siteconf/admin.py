from django.contrib import admin

# Register your models here.
from .models import TopSiteConf
class TopConf(admin.ModelAdmin):
    list_display = ('id','telephone','work_time','twitter','facebook')
    
admin.site.register(TopSiteConf, TopConf)

