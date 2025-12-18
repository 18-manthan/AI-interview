from django.urls import path
from exams.views import ExamView,QuestionView,CheckAnswer,ExamResultView

app_name = "exam_app"

urlpatterns = [
    path('', ExamView.as_view(),name="exam"),
    path('question', QuestionView.as_view(),name="question"),
    path('check_answer', CheckAnswer.as_view(),name="check_answer"),
    path('create_exam', ExamResultView.as_view(),name="create_exam"),  
]

