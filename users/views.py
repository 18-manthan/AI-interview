from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def user_login(request):
    if request.method == 'POST':  
        try:
            user = authenticate(username=request.POST['username'], password=request.POST['password'])        
            if user is not None:
                login(request,user)                     
                return JsonResponse({ 'status': 'success', 'message': 'You have successfully logged in.'})
            else:
                return JsonResponse({ 'status': 'error', 'message': 'Invalid credentials' })
        except User.DoesNotExist:
                return JsonResponse({ 'status': 'error', 'message': "User doesn't exist"})
    return render(request, 'users/login.html')



def user_registration(request):
    if request.method == 'POST':
        if request.POST.get('email'):
            if User.objects.filter(email = request.POST.get('email')).exists():
                return JsonResponse({ 'status': 'error', 'message': 'User already exists with the given email. Try another' })
            else:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.first_name = request.POST['firstname']
                user.last_name = request.POST['lastname']        
                user.save()
                return JsonResponse({ 'status' : 'success', 'message':'Registration successful. Please login using your credentials' })     
    return render(request, 'users/register.html')



def user_logout(request):
    logout(request)
    return redirect ('users:login')
