from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Tag(models.Model):
	name=models.CharField(max_length=10)
	def __str__(self):
		return self.name

class BaseUser(AbstractUser):
	picture=models.ImageField(upload_to="profile_photos",null=True,blank=True)
	email_verify=models.BooleanField(default=False)
	tags=models.ForeignKey(Tag)
	location=models.CharField(max_length=50)
	website=models.URLField(max_length=200)
	contacts=models.ForeignKey('self')

	def __str__(self):
		return self.username

class NewsMaker(BaseUser):
	category=models.CharField(max_length=50)

class MediaOutlet(BaseUser):
	category=models.CharField(max_length=50)

class Journalist(BaseUser):
	bio=models.CharField(max_length=420, blank=True, default="")
	organization=models.ForeignKey(MediaOutlet)

class Pitch(models.Model):
	title=models.CharField(max_length=30)
	content=models.TextField()
	author=models.ForeignKey(NewsMaker)
	tags=models.ForeignKey(Tag)
	pub_time=models.DateTimeField(auto_now_add=True)
	last_modified_time=models.DateTimeField(auto_now=True)
	attachment=models.URLField(max_length=200)
	special=models.CharField(max_length=1)
	location=models.CharField(max_length=50)

	class Meta:
		ordering=['-pub_time']

class Embargo(Pitch):
	embargo_date=models.DateTimeField()
	selected_journalists=models.ForeignKey(Journalist)

class Scoop(Pitch):
	selected_journalist=models.ForeignKey(Journalist)
	status=models.BooleanField()	


class Article(models.Model):
	title=models.CharField(max_length=30)
	content=models.TextField()
	author=models.ForeignKey(Journalist)
	tags=models.ForeignKey(Tag)
	pub_time=models.DateTimeField(auto_now_add=True)
	last_modified_time=models.DateTimeField(auto_now=True)
	related_pitch=models.ForeignKey(Pitch)
	attachment=models.URLField(max_length=200)

	class Meta:
		ordering=['-pub_time']


class Message(models.Model):
	sender=models.ForeignKey(BaseUser,related_name='sender')
	receiver=models.ForeignKey(BaseUser,related_name='receiver')
	content=models.TextField()
	send_time=models.DateTimeField(auto_now_add=True)
	attachment=models.URLField(max_length=200)

	def __str__(self):
		return self.content

	# sort the message based on send time in reverse order
	class Meta:
		ordering=['-send_time']

# we maintain a relation table which keeps tracking of the folower/followee relationship
# between any two types of users
# class Relation(models.Model):
# 	follower=models.ForeignKey(BaseUser,related_name='follower')
# 	followee=models.ForeignKey(BaseUser,related_name='followee')

# 	def __str__(self):
# 		return self.follower+" -> "+self.followee