from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AdvertModel(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    img_link = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    tg_link = models.CharField(max_length=255, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    web_link = models.CharField(max_length=100, blank=True, null=True)
    other_links= models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title}"