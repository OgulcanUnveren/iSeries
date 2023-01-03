from django.db import models

# Create your models here.
class TopSiteConf(models.Model):
    
    logo_white = models.ImageField(upload_to='media/logos',blank=True,verbose_name="Logo Beyaz")
    logo_normal = models.ImageField(upload_to='media/logos',blank=True,verbose_name="Logo Normal")
    telephone = models.CharField(default=555-9999999,blank=True,max_length=20,verbose_name="Telefon")
    work_time = models.CharField(default="Mon-Sun 07:00-19:00",max_length=270,blank=True,verbose_name="Çalışma Saatleri")

    twitter = models.CharField(default="https://twitter.com/th3d1gger",max_length=270,blank=True)
    facebook = models.CharField(default="https://facebook.com",max_length=270,blank=True)
    linkedin = models.CharField(default="https://linkedin.com", max_length=270,blank=True)
    instagram = models.CharField(default="https://instagram.com",max_length=270,blank=True)
    class Meta:
        verbose_name="Sağlayıcı Bilgileri"
        verbose_name_plural="Sağlayıcı Bilgileri"
    def __str__(self):
        return self.telephone

