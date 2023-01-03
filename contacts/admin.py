from django.contrib import admin

# Register your models here.
from .models import ReportUser


class ReportUseradmin(admin.ModelAdmin):
    list_display = ('contact_email','subject')
    

admin.site.register(ReportUser, ReportUseradmin)