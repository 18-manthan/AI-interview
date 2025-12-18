from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from .models import ExamMediaRecordings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now


def serve_video(request, media_id):
    recording = get_object_or_404(ExamMediaRecordings, id=media_id)
    response = HttpResponse(recording.file_data, content_type=recording.file_type)
    return response

@method_decorator(csrf_exempt, name='dispatch')
class ChunkRecorder(View):

    def post(self, request):
        print("chunk start_____________________________")
        if 'recording_chunk' in request.FILES:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file_name = f'recording_{timestamp}.webm'
            file = request.FILES['recording_chunk']

            file_name = request.POST.get('name', '') + 'recording_vid.webm'
            file_path = 'media/chunk_vid/' + file_name
            with open(file_path, 'ab+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            with open(file_path, 'rb') as file_obj:
                file_data = file_obj.read()
            existing_entry = ExamMediaRecordings.objects.filter(file_name=file_name).exists()
            if existing_entry:
                recording = ExamMediaRecordings.objects.get(file_name=file_name)
                recording.file_data = file_data
                recording.save()
            else:
                user = None
                if request.user.is_authenticated:
                    user = request.user
                print(user, '-------------------------------------------------------------------')
                recording = ExamMediaRecordings(
                    user=user,
                    file_data=file_data,
                    file_type='video/webm',
                    file_name=file_name,
                    date=now()
                )
            recording.save()
            print("chunk save_____________________________")

            return JsonResponse({'message': 'Recording chunk saved successfully'})
        else:
            return JsonResponse({'error': 'No recording chunk found in request'}, status=400)
