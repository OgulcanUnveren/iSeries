from django.db import models
from django.contrib.auth.models import User
class WatcherSociallink(models.Model):
    platform = models.CharField(max_length=30)
    social_link = models.CharField(max_length=100)
    user_profile = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'watcher_sociallink'
