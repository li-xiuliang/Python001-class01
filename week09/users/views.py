'''
Author: your name
Date: 2020-08-22 19:09:13
LastEditTime: 2020-08-23 09:14:21
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /auth_learn/users/views.py
'''
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/index/')
    else:
        form = UserCreationForm()
    print(form)
    return render(request, 'users/register.html', context = {'form': form, 'next': redirect_to})

