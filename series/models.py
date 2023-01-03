from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.
import os
class EpisodeFiles(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d/', blank=True,verbose_name="Dizi Dosyaları")
    class Meta:
        verbose_name ="Dizi Dosyası"
        verbose_name_plural= "Dizi Dosyaları"
    
    def filename(self):
        return os.path.basename(self.file.name)
class Episode(models.Model):
    
    episode_title = models.CharField(max_length=570,verbose_name="Bölüm Adı:")
    episode_image = models.ImageField(upload_to='episodes',blank=True,verbose_name="Bölüm Görseli")
    episode_type = models.CharField(max_length=570,default="iframe",verbose_name="Bölüm Tipi")
    episode_video = models.FileField(blank=True,verbose_name="Bölüm Videosu")
    episode_duration = models.CharField(max_length=10, default='08:42',blank=True,verbose_name="Bölüm Süresi")
    episode_shorttext = models.CharField(max_length=200,blank=True,verbose_name="Bölüm Embed(Buraya iframe tagini yapıştırın)")
    episode_is_free = models.BooleanField(default=False,verbose_name="Ücretsiz mi?")
    episode_is_published= models.BooleanField(default=False,verbose_name="Yayınlansın mı?")
    episode_slug = models.CharField(max_length=570,verbose_name="Seo Slug")
    episode_text = HTMLField(verbose_name="Bölüm Açıklama")
    episode_files = models.ManyToManyField(EpisodeFiles,blank=True,verbose_name="Bölüm Dosyaları")
    episode_position = models.IntegerField(verbose_name="Bölüm Görünüm Sırası")
    class Meta:
        verbose_name="Dizi Bölümü"
        verbose_name_plural="Dizi Bölümleri"
    def __str__(self):
        return self.episode_title

class SerieWatcher(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Kullanıcı")
    serie_id = models.IntegerField( verbose_name="Dizi ID")
    is_bought = models.BooleanField(default=False, verbose_name="Listeye eklendi mi?")
    class Meta:
        verbose_name = "İzleyici"
        verbose_name_plural = "İzleyiciler"
    
    def __str__(self):
        return self.user.username

class SerieCategory(models.Model):
    title = models.CharField(max_length=570,verbose_name="Kategori Başlık")
    icon = models.CharField(max_length=570,default="icon-cat",verbose_name="Ikon")
    class Meta:
        verbose_name = "Dizi Kategori"
        verbose_name_plural = "Dizi Kategorileri"
    def __str__(self):
        return self.title

class ParentEpisode(models.Model):
    sequence = models.IntegerField(verbose_name="Sezon Sırası")
    title= models.CharField(max_length=570,verbose_name="Sezon Başlık")
    episodes = models.ManyToManyField(Episode,blank=True,verbose_name="Sezon Bölümleri")
    class Meta:
        verbose_name = "Sezon"
        verbose_name_plural = "Sezonlar"    
    def __str__(self):
        return self.title

class Serie(models.Model):
    title = models.CharField(max_length=570,blank=True,verbose_name="Dizi Adı")
    slug = models.CharField(max_length=570,blank=True,verbose_name="Slug")
    description = models.TextField(blank=True,verbose_name="Dizi Açıklama")
    serie_image = models.ImageField(upload_to='media/series/',blank=True,verbose_name="Dizi Görsel")
    serie_category = models.ManyToManyField(SerieCategory,verbose_name="Dizi Kategorileri")
    price = models.DecimalField(max_digits=8,decimal_places=2,blank=True,verbose_name="Ücret",default=0)
    uzatmadegeri = models.DecimalField(max_digits=8,decimal_places=2,blank=True,verbose_name="Abonelik Uzatma Ücret",default=0)
    featured = models.BooleanField(default=False,verbose_name="Fırsat Ürünü")
    trending = models.BooleanField(default=False,verbose_name="Trend")
    popular = models.BooleanField(default=False,verbose_name="Popüler")
    meta_title = models.CharField(max_length=570,verbose_name="Meta Başlığı")
    meta_description = models.TextField(verbose_name="Meta Açıklaması")
    meta_keywords = models.TextField(verbose_name="Meta Anahtar Kelimler")
    is_published = models.BooleanField(default=True,verbose_name="Yayınlandı mı?")
    is_free = models.BooleanField(default=True,verbose_name="Ücretsiz mi?")
    teacher = models.ManyToManyField(User,null=True,verbose_name="Ekleyen")
    parent_episode = models.ManyToManyField(ParentEpisode,blank=True,null=True,verbose_name="Sezonlar")
    rater = models.DecimalField(max_digits=3,decimal_places=2,default=4.50,verbose_name="Rating")
    rateoran = models.IntegerField(default=90,verbose_name="Rating Oran(Yüzde)")
    class Meta:
        verbose_name = "Dizi"
        verbose_name_plural = "Diziler"
    def __str__(self):
        return self.meta_title
class SerieDuration(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,verbose_name="Kullanıcı")
    serie_id = models.IntegerField(verbose_name="Dizi ID")
    episode_id = models.IntegerField(verbose_name="Dizi Bölümü")
    class Meta:
        verbose_name = "Kullanıcılar ne izledi?"
        verbose_name_plural = "Kullanıcılar ne izledi?"
    def __str__(self):
        return self.user.username
class SerieRating(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING,verbose_name="Kullanıcı")
    rating_value= models.IntegerField(verbose_name="Oylama Puanı")
    serie_id = models.CharField(max_length=255,verbose_name="Dizi ID")
    class Meta:
        verbose_name = "Kullanıcı Yorumları"
        verbose_name_plural = "Kullanıcı Yorumları"