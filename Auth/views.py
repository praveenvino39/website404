from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# Create your views here.

def signupuser(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                messages.success(request, 'Your Account created successfully, Now you can Login')
                return redirect('homepage')
            except IntegrityError:
                messages.error(request, 'Username already taken, Try different!')
                return redirect('signup')
        else:
            messages.success(request, 'Password not match')
            return redirect('signup')
    else:
        return render(request, 'Auth/signupuser.html', {'form': UserCreationForm()})

def loginuser(request):
    if request.method=='POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully signed in as {}.'.format(request.user))
            return redirect('homepage')
        else:
            print('user doesn\'t exist')
            messages.error(request, 'User doesn\'t exits')
            return redirect('login')
    else:
        return render(request, 'Auth/login.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')
