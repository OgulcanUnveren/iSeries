from django.db import models
import datetime
from django.contrib.auth.models import User

class ReportUser(models.Model):
    reporter = models.ForeignKey(User,models.DO_NOTHING,verbose_name="Şikayet eden Kullanıcı")
    contact_email = models.EmailField(verbose_name="İletişim E-postası")
    subject = models.TextField(verbose_name="Konu")
    screenshot = models.ImageField(verbose_name="Ekran Görüntüsü")
    class Meta:
        verbose_name="Kullanıcı Şikayetleri"
        verbose_name_plural ="Kullanıcı Şikayetleri"
    def __str__(self):
        return self.reporter.username