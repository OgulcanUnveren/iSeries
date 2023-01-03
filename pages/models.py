from django.db import models
from tinymce.models import HTMLField

class About(models.Model):
    title = models.CharField(max_length=270,verbose_name="Başlık",default="Hakkımızda")
    content = HTMLField(verbose_name="İçerik")
    class Meta:
        verbose_name="Hakkında"
        verbose_name_plural="Hakkında"
    def __str__(self):
        return self.title
class FAQ(models.Model):
    question = models.CharField(max_length=700,verbose_name="Soru")
    answer = models.TextField(verbose_name="Cevap")
    class Meta:
        verbose_name="SSS"
        verbose_name_plural="SSS"
    
    def __str__(self):
        return self.question
class FooterPages(models.Model):

    title = models.CharField(max_length=270,verbose_name="Başlık")
    slug = models.CharField(max_length=270, default='slug',verbose_name="Slug")
    content = HTMLField(verbose_name="İçerik")
    class Meta:
        verbose_name="Footer Sayfaları"
        verbose_name_plural="Footer Sayfaları"
    
    def __str__(self):
        return self.title