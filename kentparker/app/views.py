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
from app.models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

@login_required
def home(request):
	if request.user.user_type==1:
		# newsmaker
		my_pitches=Pitch.objects.filter(author=request.user)
		context={'pitches':my_pitches}
		return render(request,'kentparker/newsMakerDashBoard.html',context)
	elif request.user.user_type==2:
		# journalist
		
		return render(request,'kentparker/journalistDashBoard.html',context)
	else:
		# media outlet

		return render(request,'kentparker/mediaOutletDashBoard.html',context)

@login_required
def publish_pitch(request):
	if request.method=='GET':
		publish_pitch_form=PublishPitchForm()
		context={'publish_pitch_form':publish_pitch_form}
		return render(request,'kentparker/publishNewPitch.html',context)
	publish_pitch_form=PublishPitchForm(request.POST)
	context={'publish_pitch_form':publish_pitch_form}
	if not publish_pitch_form.is_valid():
		return render(request,'kentparker/publishNewPitch.html',context)
	new_pitch=Pitch(title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user)
	new_pitch.save()
	return redirect('/')

@login_required
def show_pitches(request):
	my_pitches=Pitch.objects.filter(author=request.user)
	context={'pitches':my_pitches}
	return render(request,'kentparker/allPitches.html',context)

@login_required
def favorite(request):
	return HttpResponse("")

@login_required
def publish_article(request):
	return HttpResponse("")

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
	new_tag=Tag.objects.create(name='test')
	new_tag.save()
	new_user=MyUser.objects.create_user(username=register_form.cleaned_data.get('r_username'),email=register_form.cleaned_data.get('r_email'),password=register_form.cleaned_data.get('r_password'),first_name=register_form.cleaned_data.get('r_first_name'),last_name=register_form.cleaned_data.get('r_last_name'),user_type=1)
	new_user.save()
	new_user=authenticate(username=register_form.cleaned_data.get('r_username'),password=register_form.cleaned_data.get('r_password'))
	django.contrib.auth.login(request,new_user)
	return redirect('/')