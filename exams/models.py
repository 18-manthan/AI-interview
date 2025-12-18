from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice Question'),
        ('LongDescriptive', 'Long Descriptive Answer Question'),
    )

    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    question_text = models.TextField(max_length=500)
    option1 = models.TextField(max_length=100, blank=True, null=True)
    option2 = models.TextField(max_length=100, blank=True, null=True)
    option3 = models.TextField(max_length=100, blank=True, null=True)
    option4 = models.TextField(max_length=100, blank=True, null=True)
    correct_option = models.IntegerField(blank=True, null=True)


    def __str__(self) -> str:
        return f'{self.question_text}'



class CapturedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='captured_images/')
    def __str__(self):
        return f'Captured Image {self.id}'

class ExamResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_percent = models.TextField(max_length=100)
    more_than_one_person = models.IntegerField()
    no_person = models.IntegerField()
    head_left_right = models.IntegerField()
    phone_detected = models.IntegerField()
    examination_at = models.DateTimeField(default=datetime.now())

    def __str__(self) -> str:
        return f'{self.user.username}'
    
class UserAnswer(models.Model):
    exam = models.ForeignKey(ExamResult, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self) -> str:
        return f'{self.exam.user.username}'
