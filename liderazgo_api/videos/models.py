from django.db import models

# Create your models here.
class Video(models.Model):
    videoUrl = models.CharField(max_length=255, null=True, blank=True)
    