# from django.contrib.auth.models import User
# from django.db import models

# # Create your models here.


# class MCQ(models.Model):
#     options = (
#         (1, 1),
#         (2, 2),
#         (3, 3),
#         (4, 4),
  
#     )
#     question = models.TextField(max_length=500)
#     option1 = models.TextField(max_length=100)
#     option2 = models.TextField(max_length=100)
#     option3 = models.TextField(max_length=100)
#     option4 = models.TextField(max_length=100)
#     right_option = models.IntegerField(choices=options)


# class CapturedImage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='captured_images/')
#     def __str__(self):
#         return f'Captured Image {self.id}'