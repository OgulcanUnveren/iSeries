from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="Kullanıcı")
    twitter = models.CharField(max_length=270, blank=True,verbose_name="Twitter Adresi")
    facebook = models.CharField(max_length=270, blank=True,verbose_name="Facebook Adresi")
    instagram = models.CharField(max_length=270, blank=True,verbose_name="Instagram Adresi")
    bio = models.TextField(max_length=500, blank=True,verbose_name="Bio")
    
    avatar = models.ImageField(upload_to=f'{get_random_string(length=32)}/%Y/%m/%d/')
   
    location = models.CharField(max_length=30, blank=True,verbose_name="Konum")
    birth_date = models.DateField(null=True, blank=True,verbose_name="Doğum Tarihi")
    class Meta:
        verbose_name="Profil"
        verbose_name_plural = 'Kullanıcı Profilleri'
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()