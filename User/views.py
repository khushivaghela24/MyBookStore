from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db import IntegrityError

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'Username already exists!'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Form is invalid. Please check your input.'
            })
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'form': form,
                'error': 'Invalid username or password.'
            })
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')