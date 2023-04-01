from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
#otp verification import
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random

# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Invalid username or Password")
            return redirect('account/login')
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

#random otp generator
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

#email otp
def send_otp(request):
     email=request.POST.get("email")
     o=generateOTP()
     htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
     send_mail('OTP request',o,'todoslists@outlook.com',[email], fail_silently=False, html_message=htmlgen)
     return HttpResponse(o)

def signup(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        confirm_password = request.POST['confirm-password']
        email = request.POST['email']
        if password != confirm_password:
            messages.info(request,'Password does not match')
            return redirect('account:signup')
        elif User.objects.filter(username=user_name).exists():
            messages.info(request,'Username already used')
            return redirect('account:signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email already used')
            return redirect('account:signup')
        else:
            user = User.objects.create_user(username=user_name,password=password,email=email,first_name=first_name,last_name=last_name)
            user.save()
            return redirect('account:login')
    else:    
        return render(request,'signup.html')