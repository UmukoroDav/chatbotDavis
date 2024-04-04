from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Chatb
from django.utils import timezone
from . import env
# Create your views here.

open_ai_key = env
openai.api_key = open_ai_key

def ask_openai(message):
    reponse = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': 'You are an helpful assistant.'},
            {'role': 'user', 'content': message },
        ]
    )
    answer = reponse.choice[0].message.content.strip()
    return answer

def appchatbox(request):
    chat = Chatb.objects.filter(user=request.user)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        # response = ask_openai(message)
        response = 'Hw are u doing'
        
        chat = Chatb(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message' : message, 'response' : response})
    return render(request, 'chatbot.html', {'chat':chat})


def applogin(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('chatbot')
            else:
                error_message = "Invalid Username or Password"
                return render(request, 'login.html', {'error_message' : error_message})
        else:
            return render(request, 'login.html')


def appregister(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                # Create a user using the create_user method
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.first_name = name  # Set the first name
                user.save()

                # Authenticate and log in the user
                authenticated_user = authenticate(request, username=username, password=password1)
                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect('chatbot')
                else:
                    error_message = 'Authentication failed'
            except Exception as e:
                error_message = 'Something Went Wrong: ' + str(e)
        else:
            error_message = "Passwords don't match"
        
        return render(request, 'register.html', {'error_message': error_message})
    
    return render(request, 'register.html')



def applogout(request):
    auth.logout(request)
    return redirect('login')