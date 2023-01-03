from django.contrib import admin
from .models import Profile
# Register your models here.
class UserProfile(admin.ModelAdmin):
    
    list_display = ('id','user','twitter','instagram')
    list_display_links = ('id','user')
    
    
    search_fields = ('user.username',)
    

admin.site.register(Profile, UserProfile)
