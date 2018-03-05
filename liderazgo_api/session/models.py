from django.db 		import models
from modules.models import Modules
from exam.models 	import Exam
from django.contrib.auth.models import User

# Create your models here.
class Session(models.Model):
	modulesID			= models.ForeignKey(Modules, related_name='modules_id', on_delete=models.CASCADE)
	examID				= models.ForeignKey(Exam, related_name='exam_id', on_delete=models.CASCADE)
	user				= models.ForeignKey(User, related_name='user_session', on_delete=models.CASCADE)
	sessionNumber 		= models.IntegerField(help_text="Number of the corresponding session")
	startDate			= models.DateField(null=True, blank=True)
	endDate				= models.DateField(null=True, blank=True)
	presentationDone 	= models.BooleanField(default=False, blank=True)
	docDone				= models.BooleanField(default=False, blank=True)
	videoDone			= models.BooleanField(default=False, blank=True)
	slideReached		= models.IntegerField(default=0, help_text="Last slide reached")
	pageReached			= models.IntegerField(default=0, help_text="Last document page reached")