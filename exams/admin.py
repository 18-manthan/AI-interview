from django.contrib import admin
from .models import ExamResult, CapturedImage, Question, UserAnswer
from django.utils.html import format_html
# Register your models here.


class ExamResultAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email']

admin.site.register(ExamResult, ExamResultAdmin)
# admin.site.register(CapturedImage)

class CapturedImageAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_preview']

    def image_preview(self, obj):
        return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.image.url))
    image_preview.short_description = 'Image Preview'

admin.site.register(CapturedImage, CapturedImageAdmin)
admin.site.register(Question)

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'answer_text')
    list_filter = ('exam__user__username',)
    search_fields = ['exam__user__username', 'exam__user__email']

admin.site.register(UserAnswer, UserAnswerAdmin)