from django.shortcuts import render, redirect
from .models import ReportUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django_ratelimit.decorators import ratelimit
# Create your views here.


@login_required(login_url="/accounts/login")
@ratelimit(key='ip', rate='5/m', block=True)
def sendreport(request):
    if request.method == 'POST':
        if request.FILES.get('send_screenshot') != None:
            reporter = request.user
            email = request.POST.get('email')
            try:
                validate_email(email)
            except ValidationError as e:
                messages.info(request,'Hatalı email formatı! Konu sistem yöneticilerimiz tarafından incelenecek')
                return redirect('/contact/dashboard/reports')
            else:
                
                subject = request.POST.get('subject')
                extensions = ['jpg','jpeg','png']
                screenshot = request.FILES.get('send_screenshot')
                
                for extension in extensions:
                    if screenshot.name.endswith(extension):
                        report = ReportUser.objects.create(reporter=reporter,contact_email=email,subject=subject,screenshot=screenshot)
                        report.save()
                        messages.info(request,'Şikayetiniz başarıyla gönderildi! Konu sistem yöneticilerimiz tarafından incelenecek')
                        return redirect('/contact/dashboard/reports')
                    
                messages.info(request,'Hatalı dosya formatı! Konu sistem yöneticilerimiz tarafından incelenecek')
                return redirect('/contact/dashboard/reports')
    else:
        return render(request,'dashboard/watcher/report/sendreports.html')
def validateEmail(email):
    if len(email) > 6:
        if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return 1
    return 0