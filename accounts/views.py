from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from series.models import Serie,SerieWatcher
# Create your views here.
from django.urls import reverse
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
@ratelimit(key='ip', rate='5/m', block=True)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request,'Kullanıcı Adı veya parola yanlış!')
            return redirect('login')
    else:

        return render(request, 'auth/login.html')

def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('index')
@ratelimit(key='ip', rate='5/m', block=True)
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.upper().translate(str.maketrans({'Ğ':'G','Ş':'S','Ç':'C','Ö':'O','İ':'I','Ü':'U'}))
        special_characters = "!@#$%^&*()-+?_=,<>/:;'\\"
        username = username.replace(" ","")
        username = username.lower()
        if any(c in special_characters for c in username):
            messages.error(request,'Kullanıcı adı sadece harf ve sayılardan oluşmalıdır')
            return redirect(reverse('signup'))

        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if username == '':
            
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        if password == '':
            
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        
        if email  == '':
            messages.error(request,'Bütün Alanların doldurulması Zorunludur')
            return redirect(reverse('signup'))
        if password != password2:            
            messages.error(request,'Parolalar eşleşmiyor')
            return redirect(reverse('signup'))
        check_if_exist_username = User.objects.filter(username=username).count()

        if check_if_exist_username > 0:
            messages.error(request,'Bu Kullanıcı adı daha önce alınmış')
            return redirect(reverse('signup'))
        check_if_exist_email = User.objects.filter(email=email).count()

        if check_if_exist_email > 0:
            messages.error(request,'Bu e-posta daha önce kullanılmış')
            return redirect(reverse('signup'))
        
        try:
            validate_email(email)
        except:
            messages.error(request,'Lütfen doğru bir e-posta girin')
            return redirect(reverse('signup'))

        else:
            email=email
        #user = User.objects.create(username=username,email=email,password=make_password(password),is_active=1,first_name=first_name,last_name=last_name)
        #user.save()
        user = User.objects.create(username=username,email=email,password=make_password(password),is_active=1)
        user.save()
        messages.info(request,'Kayıt Başarılı lütfen giriş yapın')
        return redirect(reverse('login'))
    else:
        return render(request,'auth/register.html')





        
    
    

    

