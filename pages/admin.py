from django.contrib import admin
from .models import About,FAQ,FooterPages
# Register your models here.
class AboutPage(admin.ModelAdmin):
    list_display = ('title','content')
    

admin.site.register(About, AboutPage)

class FooterPage(admin.ModelAdmin):
    list_display = ('title','content')
    

admin.site.register(FooterPages, FooterPage)

class FAQPage(admin.ModelAdmin):
    list_display = ('question','answer')
    

admin.site.register(FAQ, FAQPage)

