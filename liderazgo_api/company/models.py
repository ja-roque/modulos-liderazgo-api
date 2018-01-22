from django.db import models

# Create your models here.
# Create your models here.
class Company(models.Model):
	companyName	= models.CharField(max_length=255, null=True, blank=True)
	package		= models.CharField(max_length=255, null=True, blank=True)
	isActive		= models.BooleanField(default=True, blank=True)
	suscriptionStart= models.DateTimeField(null=True, blank=True)
	suscriptionEnd	= models.DateTimeField(null=True, blank=True)
	created 		= models.DateTimeField(auto_now_add=True)