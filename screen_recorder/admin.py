from django.contrib import admin
from .models import ExamMediaRecordings
from django.utils.html import format_html
from django.urls import reverse

class MediaRecordingAdmin(admin.ModelAdmin):
	list_display = ('user', 'file_type', 'file_name', 'date', 'display_video')

	def display_video(self, obj):
		return format_html('<video width="320" height="240" controls><source src="{}" type="{}"></video>',
			reverse('screen_recorder_app:serve_video', args=[obj.id]), obj.file_type)

	display_video.short_description = 'Video Player'

admin.site.register(ExamMediaRecordings, MediaRecordingAdmin)