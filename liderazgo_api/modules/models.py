from django.db import models

# Create your models here.
class Modules(models.Model):	
    sessionReached 		= models.IntegerField(default=1, help_text="Max session reached")


