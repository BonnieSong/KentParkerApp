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
from django.urls import reverse

@login_required
def home(request):
	if request.user.user_type==1:
		# this is a newsmaker
		# filter related articles about the current newsmaker
		related_articles=Article.objects.filter(newsmaker=request.user)
		context={'related_articles':related_articles}
		# newsmaker
		my_pitches=Pitch.objects.filter(author=request.user)
		context={'pitches':my_pitches}
		return render(request,'kentparker/newsMakerDashBoard.html',context)
	elif request.user.user_type==2:
		#journalist
		# all_tags=request.user.tags
		all_tags=Tag.objects.all()
		pitches = Pitch.objects.filter(tags__in=all_tags).distinct()
		context = {'filter_pitches': pitches, 'tags': all_tags}
		return render(request,'kentparker/JournalistDashBoard.html',context)
	elif request.user.user_type==3:
		# media outlet
		all_journalists = MyUser.objects.filter(organization=request.user)
		published_articles = set()
		for journalist in all_journalists:
			published_articles.append(journalist.article_set.all())
		context = {'journalists': all_journalists, 'articles': published_articles }
		return render(request,'kentparker/mediaoutlet_dashboard.html',context)

@login_required
def favNewsMakers_pitch(request):
	all_tags = Tag.objects.all()
	newsMakers = request.user.contacts
	pitches = set()
	if (newsMakers is not None) and (len(newsMakers)>0) :
		for newsMaker in newsMakers:
			pitches.append(newsMaker.pitch_set.all())
	context = {'filter_pitches': pitches, 'tags': all_tags}
	return render(request, 'kentparker/JournalistDashBoard.html', context)

@login_required
def filterTags_pitch(request, tags):
	all_tags=Tag.objects.all()
	tagsSet = set()

	chosen_tags_ids = tags.split("@")
	for tag_id in chosen_tags_ids:
		if(len(tag_id)>0):
			tag_id = tag_id[len(tag_id)-1:]
			target_tag=Tag.objects.get(pk=tag_id)
			tagsSet.add(target_tag)

	if len(tagsSet)==0:
		tagsSet = all_tags

	pitches = Pitch.objects.filter(tags__in=tagsSet).distinct()
	context = {'filter_pitches': pitches, 'tags':all_tags}
	return render(request, 'kentparker/JournalistDashBoard.html', context)


@login_required
def create_pitch(request):
	all_tags=Tag.objects.all()
	context={'tags':all_tags}
	if request.method=='GET':
		return render(request,'kentparker/create_pitch.html',context)
	if 'cancel_btn' in request.POST:
		return redirect('/')
	# use the form to do validation
	publish_pitch_form=PublishPitchForm(request.POST)
	if not publish_pitch_form.is_valid():
		return render(request,'kentparker/create_pitch.html',context)

	if 'publish_btn' in request.POST:
		# publish the pitch
		new_pitch=Pitch(title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=True)
		new_pitch.save()
	if 'save_btn' in request.POST:
		# save the pitch as a draft
		new_pitch=Pitch(title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=False)
		new_pitch.save()

	chosen_tags_ids=request.POST.getlist("tags-list")
	for tag_id in chosen_tags_ids:
		target_tag=Tag.objects.get(pk=tag_id)
		new_pitch.tags.add(target_tag)
	new_pitch.save()
	return redirect('/')

@login_required
def manage_pitch(request):
	# show all my pitches including published and drafts
	pitches=Pitch.objects.filter(author=request.user)
	context={'pitches':pitches}
	return render(request,'kentparker/manage_pitch.html',context)

@login_required
def profile(request,name):
	target_user=get_object_or_404(MyUser,username=name)
	pitches=Pitch.objects.filter(author=target_user)
	context={'target_user':target_user,'pitches':pitches}
	if target_user.user_type==1:
		return render(request,"kentparker/profile_newsmaker.html",context)
	if target_user.user_type==2:
		return render(request,"kentparker/profile_jounalist.html",context)
	if target_user.user_type==3:
		return render(request,"kentparker/profile_mediaoutlet.html",context)

# add the target user to contacts by favoriting it
@login_required
def favorite(request,name):
	if request.user.username==name:
		return redirect('/profile/'+name)
	temp=request.user.contacts_set.filter(username=name)
	if temp:
		# user already in the contacts
		temp.get().delete()
	else:
		# add user to the contacts
		target_user=get_object_or_404(MyUser,username=name)
		request.user.contacts_set.add(target_user)
	return redirect('/profile/'+name)

@login_required
def get_photo(request, name):
	target_user=get_object_or_404(MyUser,username=name)
	if not target_user.picture:
		raise Http404
	content_type=guess_type(target_user.picture.name)
	return HttpResponse(target_user.picture, content_type=content_type)

@login_required
def edit_profile(request, name):
	if request.user.username!=name:
		return redirect('/profile/'+name)
	context={}
	target_user=get_object_or_404(MyUser,username=name)
	if request.method=='GET':
		context['edit_profile_form']=EditProfileModelForm(instance=target_user)
		context['name']=name
		return render(request,'kentparker/edit_profile.html',context)
	edit_profile_form=EditProfileModelForm(request.POST,request.FILES,instance=target_user)
	context={'edit_profile_form':edit_profile_form,'name':name}
	if not edit_profile_form.is_valid():
		return render(request,'kentparker/edit_profile.html',context)
	edit_profile_form.save()
	return redirect('/profile/'+name)

@login_required
def change_password(request,name):
	if request.user.username!=name:
		return redirect('/profile/'+name)
	context={}
	target_user=get_object_or_404(MyUser,username=name)
	if request.method=='GET':
		context['change_password_form']=ChangePasswordModelForm()
		context['name']=name
		return render(request,'kentparker/change_password.html',context)
	change_password_form=ChangePasswordModelForm(request.POST,instance=target_user)
	context={'change_password_form':change_password_form,'name':name}
	if not change_password_form.is_valid():
		return render(request,'kentparker/change_password.html',context)

	if not target_user.check_password(change_password_form.cleaned_data.get('old_password')):
		context['wrong_old_password']=True
		return render(request,'kentparker/change_password.html',context)

	target_user.set_password(change_password_form.cleaned_data.get('new_password'))
	target_user.save()
	return redirect('/profile/'+name)

def request_reset_password(request):
	context={}
	if request.method=='GET':
		context['request_reset_password_form']=RequestResetPasswordForm()
		return render(request,'kentparker/request_reset_password.html',context)
	else:
		request_reset_password_form=RequestResetPasswordForm(request.POST)
	context['request_reset_password_form']=request_reset_password_form
	if not request_reset_password_form.is_valid():
		return render(request,'kentparker/request_reset_password.html',context)
	target_user=MyUser.objects.filter(email=request_reset_password_form.cleaned_data.get('email'))
	if target_user:
		target_user=target_user.get()
	else:
		return redirect('/')
	token=default_token_generator.make_token(target_user)
	email_body="""
	Please click the link below to reset your password:
	http://%s%s
	""" % ('localhost:8000', reverse('reset_password',args=(target_user.username,token)))

	send_mail(subject="Reset your password",
			  message=email_body,
			  from_email='yujiel1@andrew.cmu.edu',
			  recipient_list=[target_user.email])

	context['sent']=True
	return render(request,'kentparker/request_reset_password.html',context)

def reset_password(request,name,token):
	target_user=get_object_or_404(MyUser,username=name)
	confirm_token=default_token_generator.make_token(target_user)
	if token==confirm_token:
		if request.method=='GET':
			reset_password_form=ResetPaswordForm()
			context={'reset_password_form':reset_password_form,'name':name,'token':token}
			return render(request,'kentparker/reset_password.html',context)
		reset_password_form=ResetPaswordForm(request.POST)
		context={'reset_password_form':reset_password_form,'name':name,'token':token}
		if not reset_password_form.is_valid():
			return render(request,'kentparker/reset_password.html',context)
		target_user.set_password(reset_password_form.cleaned_data.get('password'))
		target_user.save()
		return redirect('/')
	else:
		return redirect('/')

@login_required
def publish_article(request):
	return HttpResponse("")

def login(request):
	context={'register_form':RegisterForm(),'from_login':True}
	return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)

def login_google(request,email):
	print ("login_google", request.user)
	print (request)
	info = email.split('+')
	newemail, newusername = info[0], info[1]
	print (newemail)
	print (newusername)

	new_user = MyUser.objects.filter(email=newemail)
	print(len(new_user))
	if len(new_user) > 0:
		django.contrib.auth.login(request, new_user[0])
		return redirect('/')
	defaultpassword = "123"
	new_user=MyUser.objects.create_user(username=newemail,email=newemail,password=defaultpassword,first_name='',last_name='',user_type=1)
	new_user.save()
	django.contrib.auth.login(request,new_user)
	return redirect('/')

def login_facebook(request,userid):
	print("userid " + userid)
	info = userid.split('+')
	newusername, newuseremail = info[0], info[1]
	print (newusername)
	print (newuseremail)
	new_user = MyUser.objects.filter(email=newuseremail)
	print (new_user)
	if len(new_user) > 0:
		django.contrib.auth.login(request, new_user[0])
		return redirect('/')
	defaultpassword = "123"
	new_user=MyUser.objects.create_user(username=newuseremail,email=newuseremail,password=defaultpassword,first_name='',last_name='',user_type=1)
	new_user.save()
	django.contrib.auth.login(request,new_user)
	return redirect('/')

def register(request):
	context={}
	if request.method=='GET':
		register_form=RegisterForm()
	else:
		register_form=RegisterForm(request.POST)
	context['register_form']=register_form
	if not register_form.is_valid():
		return django.contrib.auth.views.login(request,template_name='kentparker/login.html',extra_context=context)

	new_user=MyUser.objects.create_user(username=register_form.cleaned_data.get('r_username'),email=register_form.cleaned_data.get('r_email'),password=register_form.cleaned_data.get('r_password'),first_name=register_form.cleaned_data.get('r_first_name'),last_name=register_form.cleaned_data.get('r_last_name'),user_type=register_form.cleaned_data.get('r_type'))
	new_user.save()
	new_user=authenticate(username=register_form.cleaned_data.get('r_username'),password=register_form.cleaned_data.get('r_password'))
	django.contrib.auth.login(request,new_user)

	token=default_token_generator.make_token(new_user)
	email_body="""
	Please click the link below to confirm your email address:
	http://%s%s
	""" % ('localhost:8000', reverse('confirm_registration',args=(new_user.username,token)))

	send_mail(subject="Confirm your email address",
			  message=email_body,
			  from_email='yujiel1@andrew.cmu.edu',
			  recipient_list=[new_user.email])

	if new_user.user_type==1:
		return redirect("/register_newsmaker")
	if new_user.user_type==2:
		return redirect("/register_journalist")
	if new_user.user_type==3:
		return redirect("/register_mediaoutlet")

	return redirect('/')

def register_newsmaker(request):
	if request.method=='GET':
		return render(request,"kentparker/registration_newsmaker.html")
	# update the reuqest.user with new form
	return render(request,"kentparker/registration_newsmaker.html")

def register_journalist(request):
	if request.method=='GET':
		return render(request,"kentparker/registration_journalist.html")
	# update the request.user with new form
	return render(request,"kentparker/registration_journalist.html")

def register_mediaoutlet(request):
	if request.method=='GET':
		return render(request,"kentparker/registration_mediaoutlet.html")
	return render(request,"kentparker/registration_mediaoutlet.html")

def confirm_registration(request,name,token):
	target_user=get_object_or_404(MyUser,username=name)
	confirm_token=default_token_generator.make_token(target_user)
	if token==confirm_token:
		target_user.email_verify=True
		target_user.save()
		django.contrib.auth.login(request,target_user)
	return redirect('/')