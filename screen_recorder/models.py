import asyncio
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExamMediaRecordings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate the media file with a user
    file_data = models.BinaryField()
    file_type = models.CharField(max_length=50)  # Store the file type
    file_name = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    
    async def save_async(self, *args, **kwargs):
        # Example asynchronous save method for ExamMediaRecordings
        await asyncio.sleep(1)  # Simulating an asynchronous operation
        return await super().save(*args, **kwargs)