from django.db 		import models
from modules.models import Modules
from exam.models 	import Exam

# Create your models here.
class Session(models.Model):
	modulesID			= models.ForeignKey(Modules, related_name='user_id', on_delete=models.CASCADE,)
	examID				= models.ForeignKey(Exam, related_name='user_id', on_delete=models.CASCADE,)
	sessionNumber 		= models.IntegerField(help_text="Number of the corresponding session")
	presentationDone 	= models.BooleanField(default=False, blank=True)
	docDone				= models.BooleanField(default=False, blank=True)
	slideReached		= models.IntegerField(default=0, help_text="Last slide reached")
	pageReached			= models.IntegerField(default=0, help_text="Last document page reached")