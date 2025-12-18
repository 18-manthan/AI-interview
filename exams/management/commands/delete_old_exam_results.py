# exams/management/commands/delete_old_exam_results.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from exams.models import ExamResult
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete ExamResult records older than 6 months'

    def handle(self, *args, **options):
        # Calculate the date 6 months ago
        six_months_ago = timezone.now() - timedelta(days=180)

        # Delete ExamResult records older than 6 months
        deleted_count, _ = ExamResult.objects.filter(examination_at__lt=six_months_ago).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} ExamResult records older than 6 months'))
