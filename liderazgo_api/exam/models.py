from django.db import models

# Create your models here.
class Exam(models.Model):
    examScore = models.IntegerField(default=0, help_text="Total score of the exam")
    attempts = models.IntegerField(default=0, help_text="Total of exam trials")
    