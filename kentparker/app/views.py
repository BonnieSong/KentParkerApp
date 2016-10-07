from django.shortcuts import render, redirect
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.shortcuts import get_object_or_404
import django.contrib.auth.views
from app.forms import *

@login_required
def home(request):
	return render(request,'kentparker/index.html')

def login(request):
	context={'register_form':RegisterModelForm(),'from_login':True}
	return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)

def register(request):
	context={}
	if request.method=='GET':
		register_form=RegisterModelForm()
	else:
		register_form=RegisterModelForm(request.POST)
	context['register_form']=register_form
	if not register_form.is_valid():
		return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)
	new_user=User.objects.create_user(username=register_form.cleaned_data.get('username'),email=register_form.cleaned_data.get('email'),password=register_form.cleaned_data.get('password'),first_name=register_form.cleaned_data.get('first_name'),last_name=register_form.cleaned_data.get('last_name'))
	new_user.save()
	new_user=authenticate(username=register_form.cleaned_data.get('username'),password=register_form.cleaned_data.get('password'))
	django.contrib.auth.login(request,new_user)
	return redirect('/')