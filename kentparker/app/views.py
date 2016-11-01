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
	context={'register_form':RegisterForm(),'from_login':True}
	return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)

def login_google(request,email):
	print(email)
	return HttpResponse("")
	
def login_facebook(request,userid):
	print("userid " + userid)
	return HttpResponse("")

def register(request):
	context={}
	if request.method=='GET':
		register_form=RegisterForm()
	else:
		register_form=RegisterForm(request.POST)
	context['register_form']=register_form
	if not register_form.is_valid():
		return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)
	new_user=User.objects.create_user(username=register_form.cleaned_data.get('r_username'),email=register_form.cleaned_data.get('r_email'),password=register_form.cleaned_data.get('r_password'),first_name=register_form.cleaned_data.get('r_first_name'),last_name=register_form.cleaned_data.get('r_last_name'))
	new_user.save()
	new_user=authenticate(username=register_form.cleaned_data.get('r_username'),password=register_form.cleaned_data.get('r_password'))
	django.contrib.auth.login(request,new_user)
	return redirect('/')