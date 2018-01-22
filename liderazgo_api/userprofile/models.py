from django.db 		import models
from modules.models import Modules
from company.models import Company
from django.contrib.auth.models import User

# Create your models here.
class Userprofile(models.Model):
	userID		= models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE,)
	firstname	= models.CharField(max_length=255, null=True, blank=True)
	lastname	= models.CharField(max_length=255, null=True, blank=True)
	isActive	= models.BooleanField(default=True, blank=True)
	isAdmin		= models.BooleanField(default=False, blank=True)
	modulesID	= models.ForeignKey(Modules, related_name='user_modules', on_delete=models.CASCADE,)
	companyID	= models.ForeignKey(Company, related_name='user_company', on_delete=models.CASCADE,)