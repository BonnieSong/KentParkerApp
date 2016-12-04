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
from django.db.models import Q

@login_required
def home(request):
	if request.user.user_type==1:
		# this is a newsmaker
		# filter related articles about the current newsmaker
		related_articles=Article.objects.filter(newsmaker=request.user)
		# newsmaker
		my_pitches=Pitch.objects.filter(author=request.user)
		context={'related_articles':related_articles, 'pitches':my_pitches}
		return render(request,'kentparker/newsMakerDashBoard.html',context)
	elif request.user.user_type==2:
		#journalist
		# all_tags=request.user.tags
		all_tags=Tag.objects.all()
		user_tags = request.user.tags.all()
		print ("journalist user_tags: ", user_tags)
		pitches = Pitch.objects.filter(tags__in=user_tags).distinct()
		validpitches = set()
		for pitch in pitches:
			if (pitch.scooped and pitch.scooppublished) or pitch.embargoMark:
				continue
			validpitches.add(pitch)
		context = {'filter_pitches': validpitches, 'tags': all_tags}
		return render(request,'kentparker/JournalistDashBoard.html',context)
	elif request.user.user_type==3:
		# media outlet
		all_journalists = MyUser.objects.filter(user_type = 2, organization=request.user)
		published_articles = set()
		for journalist in all_journalists:
			articles = journalist.author_ar.all()
			for article in articles:
				published_articles.add(article)
		context = {'journalists': all_journalists, 'articles': published_articles }
		return render(request,'kentparker/mediaoutletdashboard.html', context)

@login_required
def mediaoutlet_articles(request):
	all_journalists = MyUser.objects.filter(user_type=2, organization=request.user)
	published_articles = set()
	for journalist in all_journalists:
		articles = journalist.author_ar.all()
		for article in articles:
			published_articles.add(article)
	context = {'journalists': all_journalists, 'articles': published_articles}
	return render(request, 'kentparker/mediaoutlet_articles.html', context)

@login_required
def journalist_Articles(request):
	all_tags = Tag.objects.all()
	articles = Article.objects.filter(author = request.user)
	context = {'articles': articles, 'tags':all_tags}
	return render(request, 'kentparker/journalist_Articles.html', context)

@login_required
def favNewsMakers_pitch(request):
	all_tags = Tag.objects.all()
	newsMakers = request.user.contacts
	pitches = set()
	if (newsMakers is not None) and (len(newsMakers)>0) :
		for newsMaker in newsMakers:
			pitches.append(newsMaker.bookmarked.all())
	context = {'filter_pitches': pitches, 'tags': all_tags}
	return render(request, 'kentparker/JournalistDashBoard.html', context)

@login_required
def bookmarked_pitch(request):
	all_tags = Tag.objects.all()
	pitches = request.user.bookmarked.all()
	filter_pitches = set()
	for pitch in pitches:
		if not pitch.embargoMark:
			filter_pitches.add(pitch)
	context = {'filter_pitches': filter_pitches, 'tags': all_tags}
	return render(request, 'kentparker/bookmarked_pitches.html', context)

@login_required
def embargo_pitch(request):
	all_tags = Tag.objects.all()
	pitches = request.user.embargoed.all()
	context = {'embargo_pitches': pitches, 'tags': all_tags}
	return render(request, 'kentparker/embargo_pitches.html', context)

@login_required
def filterTags_pitch(request, tags):
	all_tags=Tag.objects.all()
	tagsSet = set()

	chosen_tags_ids = tags.split("@")
	for tag_id in chosen_tags_ids:
		if(len(tag_id)>0):
			#tag_id = tag_id[len(tag_id)-1:]
			target_tag=Tag.objects.get(pk=tag_id)
			tagsSet.add(target_tag)

	if len(tagsSet)==0:
		tagsSet = all_tags

	pitches = Pitch.objects.filter(tags__in=tagsSet).distinct()
	validpitches = set()
	for pitch in pitches:
		if (pitch.scooped and pitch.scooppublished) or pitch.embargoMark:
			continue
		validpitches.add(pitch)
	context = {'filter_pitches': validpitches, 'tags':all_tags}
	return render(request, 'kentparker/JournalistDashBoard.html', context)


@login_required
def create_pitch(request):
	all_tags=Tag.objects.all()
	context={'tags':all_tags}
	if request.method=='GET':
		return render(request,'kentparker/create_pitch.html',context)
	if 'cancel_btn' in request.POST:
		return redirect('/')
	# print ("request.POST publish: ", request.POST)
	# use the form to do validation
	publish_pitch_form=PublishPitchForm(request.POST)
	if not publish_pitch_form.is_valid():
		return render(request,'kentparker/create_pitch.html',context)

	if 'publish_btn' in request.POST:
		# publish the pitch
		if 'Scoop' in request.POST:
			print ("scoop is True")
			new_pitch=Pitch(scooped = True, title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=True)
			print ("new_pitch.scooped: ", new_pitch.scooped)
			new_pitch.save()
		else:
			new_pitch=Pitch(title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=True)
			new_pitch.save()
	if 'save_btn' in request.POST:
		# save the pitch as a drafts
		if 'Scoop' in request.POST:
			new_pitch=Pitch(scooped = True, title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=False)
			new_pitch.save()
		else:
			new_pitch=Pitch(title=publish_pitch_form.cleaned_data.get('title'),content=publish_pitch_form.cleaned_data.get('content'),author=request.user,published=False)
			new_pitch.save()


	chosen_tags_ids=request.POST.getlist("tags-list")
	for tag_id in chosen_tags_ids:
		target_tag=Tag.objects.get(pk=tag_id)
		new_pitch.tags.add(target_tag)
	if 'new_tag' in request.POST:
		new_tag_name=request.POST['new_tag']
		if len(new_tag_name.strip())>0:
			target_tag=Tag.objects.filter(name=new_tag_name)
			if len(target_tag)>0:
				target_tag=Tag.objects.get(name=new_tag_name)
				new_pitch.tags.add(target_tag)
			else:
				target_tag=Tag.objects.create(name=new_tag_name)
				new_pitch.tags.add(target_tag)
	if 'Embargo' in request.POST:
		new_pitch.embargoMark=True
		chosen_journalists = request.POST.getlist('journalist')
		for journalist in chosen_journalists:
			try:
				target_journalist = MyUser.objects.get(user_type=2, username=journalist)
				print("target_journalist: ", target_journalist)
				new_pitch.embargoed.add(target_journalist)
				print("successssss")
			except:
				pass
	# print(new_pitch.tags.all())
	# print(new_pitch.embargoed.all())

	new_pitch.save()
	return redirect(reverse('manage_pitch'))


@login_required
def create_article(request):
	all_tags=Tag.objects.all()
	context={'tags':all_tags}
	if request.method=='GET':
		return render(request,'kentparker/create_article.html',context)
	if 'cancel_btn' in request.POST:
		return redirect('/')
	# use the form to do validation
	publish_article_form=PublishArticleForm(request.POST)
	if not publish_article_form.is_valid():
		return render(request,'kentparker/create_article.html',context)

	new_article=Article(title=publish_article_form.cleaned_data.get('title'),content=publish_article_form.cleaned_data.get('content'),author=request.user)
	new_article.save()

	if 'related_pitch' in request.POST:
		related_pitch_url=request.POST['related_pitch']
		pitch_id=related_pitch_url.split('/')[-1]
		pitch_id=int(pitch_id)
		related_pitch=get_object_or_404(Pitch,pk=pitch_id)
		related_pitch.scooppublished = True
		related_pitch.save()
		new_article.related_pitch.add(related_pitch)
		new_article.save()

	chosen_news_makers=request.POST.getlist('newsmaker')
	for news_makers in chosen_news_makers:
		try:
			target_news_maker=MyUser.objects.get(user_type=1, username=news_makers)
			print ("target_news_maker, ", target_news_maker)
			new_article.newsmaker.add(target_news_maker)
		except:
			pass
	new_article.save()
	return redirect('/')


@login_required
def manage_pitch(request):
	# show all my pitches including published and drafts
	pitches=Pitch.objects.filter(author=request.user)
	tags=Tag.objects.all()
	context={'pitches':pitches,'tags':tags}
	return render(request,'kentparker/manage_pitch.html',context)

@login_required
def filter_pitch(request,tag_id):
	chosen_tag=Tag.objects.get(id=tag_id)
	pitches=chosen_tag.pitch_set.all().filter(author=request.user)
	tags=Tag.objects.all()
	context={'pitches':pitches,'tags':tags}
	return render(request,'kentparker/manage_pitch.html',context)

@login_required
def manage_journalists(request):
	print ("manage_journalists")
	# show all journalists belong to this media outlet
	journalists = MyUser.objects.filter(user_type = 2, organization = request.user)
	context={'journalists':journalists}
	return render(request,'kentparker/manage_journalists.html',context)
# 	return redirect('/')

@login_required
def profile(request,name):
	target_user=get_object_or_404(MyUser,username=name)
	pitches=Pitch.objects.filter(author=target_user)
	already=False
	if request.user.username!=name:
		temp=request.user.contacts_f.filter(username=name)
		if temp:
			already=True
	context={'target_user':target_user,'pitches':pitches,'already':already}

	if target_user.user_type==1:
		# pitches=Pitch.objects.filter(author=target_user)
		#context={'target_user':target_user,'pitches':pitches}
		return render(request,"kentparker/profile_newsmaker.html",context)
	if target_user.user_type==2:
		articles=Article.objects.filter(author=target_user)
		context['articles']=articles
		return render(request,"kentparker/profile_jounalist.html",context)
	if target_user.user_type==3:
		articles = set()
		# print ("target user is media outlet")
		journalists = MyUser.objects.filter(user_type = 2, organization = target_user)
		for i in range(len(journalists)):
			journalist = journalists[i]
			curntarticles = Article.objects.filter(author=journalist)
			for curntarticle in curntarticles:
				articles.add(curntarticle)
		# print ("articles size: ", len(articles))
		context['articles'] = articles
		return render(request,"kentparker/profile_mediaoutlet.html",context)

# add the target user to contacts by favoriting it
@login_required
def favorite(request,name):
	if request.user.username==name:
		return redirect('/profile/'+name)
	temp=request.user.contacts_f.filter(username=name)
	if temp:
		# user already in the contacts
		# delete the user from the contacts list
		request.user.contacts_f.remove(temp.get())
	else:
		# add user to the contacts
		target_user=get_object_or_404(MyUser,username=name)
		request.user.contacts_f.add(target_user)
	return redirect('/profile/'+name)

@login_required
def contacts(request):
	context={'contacts':request.user.contacts_f.all()}
	return render(request,'kentparker/contacts.html',context)

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
	""" % (request.get_host(), reverse('reset_password',args=(target_user.username,token)))

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
	# defaultpassword = "123"
	# new_user=MyUser.objects.create_user(username=newemail,email=newemail,password=defaultpassword,first_name='',last_name='',user_type=2)
	# new_user.save()
	# django.contrib.auth.login(request,new_user)
	# if no valid user exist in the database, require registration
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
	# defaultpassword = "123"
	# new_user=MyUser.objects.create_user(username=newuseremail,email=newuseremail,password=defaultpassword,first_name='',last_name='',user_type=1)
	# new_user.save()
	# django.contrib.auth.login(request,new_user)
	# if no valid user exist in the database, require registration
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
	""" % (request.get_host(), reverse('confirm_registration',args=(new_user.username,token)))

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
	step2_form=register_step2_newsmaker_form(request.POST,instance=request.user)
	if step2_form.is_valid():
		step2_form.save()
	return redirect("/")

def register_journalist(request):
	if request.method=='GET':
		all_tags = Tag.objects.all()
		organizations = MyUser.objects.filter(user_type = 3)
		context = {'tags': all_tags, 'organizations': organizations}
		return render(request, 'kentparker/Registration_Journalist.html', context)
	# update the reuqest.user with new form
	step2_form = register_step2_journalist_form(request.POST, instance=request.user)
	#print(request.POST)
	#print(step2_form.data)
	if step2_form.is_valid():
		step2_form.save()
		chosen_tags_ids = request.POST.getlist("tags")
		for tag_id in chosen_tags_ids:
			target_tag = Tag.objects.get(pk=tag_id)
			request.user.tags.add(target_tag)
		#chosen_organization = request.POST.getlist("organization")
		if "organization" in request.POST:
			organization = request.POST.get("organization")
			if len(organization)>0:
				target_org = MyUser.objects.get(username=organization)
				request.user.organization = target_org
		request.user.save()
		return redirect("/")
	else:
		all_tags = Tag.objects.all()
		organizations = MyUser.objects.filter(user_type=3)
		context = {'tags': all_tags, 'organizations': organizations}
		return render(request, 'kentparker/Registration_Journalist.html', context)


def register_mediaoutlet(request):
	if request.method=='GET':
		return render(request,"kentparker/registration_mediaoutlet.html")
	# update the reuqest.user with new form
	step2_form = register_step2_mediaoutlet_form(request.POST, instance=request.user)
	if step2_form.is_valid():
		step2_form.save()
	return redirect("/")

def confirm_registration(request,name,token):
	target_user=get_object_or_404(MyUser,username=name)
	confirm_token=default_token_generator.make_token(target_user)
	if token==confirm_token:
		target_user.email_verify=True
		target_user.save()
		django.contrib.auth.login(request,target_user)
	return redirect('/')

def pitch_detail(request,pitchId):
	if request.method == 'GET':
		cur_pitch = Pitch.objects.get(pk=pitchId)
		related_articles = cur_pitch.article_set.all()
		picked_by = set()
		for article in related_articles:
			picked_by.add(article.author)
		already= False
		if request.user in cur_pitch.bookmarked.all():
			already = True
		print(related_articles)
		context = {"cur_pitch": cur_pitch, "already": already, "related_articles": related_articles, "picked_by": picked_by}
		return render(request, "kentparker/pitch_detail.html", context)
	# bookmark the pitch
	cur_pitch = Pitch.objects.get(pk=pitchId)
	if request.user in cur_pitch.bookmarked.all():
		cur_pitch.bookmarked.remove(request.user)
	else:
		cur_pitch.bookmarked.add(request.user)
	cur_pitch.save()

	return redirect("/")

def article_detail(request, articleId):
	if request.method == 'GET':
		cur_article = Article.objects.get(pk=articleId)
		cur_article.visited_times += 1
		cur_article.save()
		related_pitches = cur_article.related_pitch
		context = {"cur_article": cur_article, "related_pitches":related_pitches}
		return render(request, "kentparker/article_detail.html", context)

@login_required
def messages(request,username):
	if not username:
		username=request.user.message_people.all()[0].username
	
	another_user=get_object_or_404(MyUser,username=username)
	all_messages=Message.objects.filter(Q(sender=request.user,receiver=another_user) | Q(sender=another_user,receiver=request.user))
	context={'message_form':MessageForm(),'username':username,'all_messages':all_messages,'people':request.user.message_people.all()}

	if request.method == 'GET':
		return render(request,'kentparker/messages.html',context)
	message_form=MessageForm(request.POST)

	if not message_form.is_valid():
		return render(request,'kentparker/messages.html',context)

	new_message=Message.objects.create(sender=request.user,receiver=another_user,content=message_form.cleaned_data['content'])
	new_message.save()
	another_user.message_people.add(request.user)
	another_user.save()
	return render(request,'kentparker/messages.html',context)

