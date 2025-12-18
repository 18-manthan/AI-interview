from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from .models import *

class ExamView(View):
	def get(self, request, *args, **kwargs):		
		if(request.user.is_authenticated):
			captured_image = CapturedImage.objects.filter(user=request.user.id).exists()
			if(captured_image):	
				questions = Question.objects.all()

				return render(request=request, template_name='exams/exam.html',context={"questions":questions})
			else:
				return redirect("imageai:home")
		else:			
			return redirect("users:login")

class QuestionView(View):   
	def get(self,request,*args,**kwargs):
		is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
		questions = Question.objects.all()
		if is_ajax:
			question_index = request.GET.get('index')
			try:
				question_index = int(question_index)
				question = questions[question_index]
				if question.question_type == 'MCQ':
					data = {
                	    "question_text": question.question_text, 
                	    "options": [question.option1,question.option2,question.option3,question.option4],
						"size":len(questions)
                	}
				else:
					data = {
						"question_text": question.question_text,
						"size":len(questions)
					}
				return JsonResponse(data)
			except (ValueError, Question.DoesNotExist):
				return JsonResponse({"error": "Question not found"}, status=404)
				
		return JsonResponse({"message": "No data available"})

class CheckAnswer(View):   
	def post(self,request,*args,**kwargs):
		is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
		questions = Question.objects.all()
		right_answer = []
		exam = ExamResult.objects.get(id=request.POST.get('exam_id'))
		if is_ajax:
			
			options = request.POST.getlist('choosen_option[]')			
			try:
				for i,data in enumerate(options):
					if questions[i].question_type == 'MCQ':
						if questions[i].correct_option == int(data):
							right_answer.append(1)
						else:
							right_answer.append(0)
					else:
						if data != '0':
							user_answer = UserAnswer(exam=exam, question=questions[i], answer_text=data)
							user_answer.save()

				count_of_ones = right_answer.count(1)

				print("-----------------------------------------------")
				print(exam)
				total_elements = len(questions)
				percentage_of_ones = (count_of_ones / total_elements) * 100
				exam.exam_percent = str(percentage_of_ones)
				
				data = {
					"percentage_of_ones": percentage_of_ones,
					"right_answer":right_answer,
					"phone_detected":exam.phone_detected,
					"more_than_one_person":exam.more_than_one_person,
					"no_person":exam.no_person,
					"head_left_right":exam.head_left_right,					
                }
				exam.save()
				return JsonResponse(data)
			except (ValueError, Question.DoesNotExist):
				return JsonResponse({"error": "Question not found"}, status=404)
				
		return JsonResponse({"message": "No data available"})

class ExamResultView(View):
	def get(self,request,*args,**kwargs):
		print("Exam generated -------------------------------------------------")
		is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
		if is_ajax:
			exam = ExamResult.objects.create(user=request.user,exam_percent=0,more_than_one_person=0,no_person=0,head_left_right=0,phone_detected=0)
			return JsonResponse({"exam_id": exam.id})

			



