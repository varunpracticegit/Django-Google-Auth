from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from . import models
from .models import LoginLogoutHistory
from django.utils import timezone
from django.contrib.auth import logout as auth_logout  # Rename to avoid conflicts



# Create your views here.
def index(request):
	return render(request, 'index.html')

def signup(request):
	if request.method == 'GET':
		return render(request,'signup.html')
	else:
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['pass']
		password1 = request.POST['pass1']
		if password==password1:
			if User.objects.filter(username=username).exists():
				messages.info(request,"Username is taken")
				return redirect('signup')
			elif User.objects.filter(email=email).exists():
				messages.error(request,"Email id is already registered")
				return redirect('signup')
			else:
				user = User.objects.create_user(password=password,username=username,email=email)
				user.save()
				return redirect('login')
		else:
			messages.warning(request,"Password not match")
			return redirect('signup')
				
	#return render(request, 'signup.html')

def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	else:
		username = request.POST['username']
		password = request.POST['pass']
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')
		else:
			messages.warning(request,"Check your Username or Password.")
			return redirect('login')
			
	
def logout(request):
    if request.user.is_authenticated:
        user = request.user

        # Find the latest login record for the user with no logout_time
        latest_login = LoginLogoutHistory.objects.filter(user=user, logout_time__isnull=True).order_by('-login_time').first()

        if latest_login:
            # Record the logout time as the current time
            latest_login.logout_time = timezone.now()
            latest_login.save()

    # Use auth_logout to perform the logout action
    auth_logout(request)

    return redirect('/')