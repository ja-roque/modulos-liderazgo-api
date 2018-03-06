from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Exam(models.Model):
	user		= models.ForeignKey(User, related_name='user_exam', on_delete=models.CASCADE)
	examScore 	= models.IntegerField(default=0, help_text="Total score of the exam")
	attempts 	= models.IntegerField(default=0, help_text="Total of exam trials")