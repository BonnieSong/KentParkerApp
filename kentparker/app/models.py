from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Tag(models.Model):
	name=models.CharField(max_length=10)
	def __str__(self):
		return self.name

class Pitch(models.Model):
	title=models.CharField(max_length=30)
	content=models.CharField()
	author=models.ForeignKey(Newsmaker)
	tags=models.ForeignKey(Tag)

class Article(models.Model):
	title=models.CharField(max_length=30)
	content=models.CharField()
	author=models.ForeignKey(Journalist)
	tags=models.ForeignKey(Tag)

class BaseUser(AbstractUser):
	# The base user models inherits from the Django built-in modeel 
	# which already has username, email, First/Last name. We don't need to 
	# define them again
	picture=models.ImageField(upload_to="profile_photos",null=True,blank=True)
	email_verify=models.BooleanField(default=False)
	tags=models.ForeignKey(Tag)

	def __str__(self):
		return self.username

class Journalist(BaseUser):
	bio=models.CharField(max_length=420, blank=True, default="")
	organization=models.ForeignKey(MediaOutlet)

class NewsMaker(BaseUser):
	# any additional fields for NewsMaker?

class MediaOutlet(BaseUser):
	# any additional fields for MedaiOutlet?

class Message(models.Model):
	sender=models.ForeignKey(BaseUser,related_name='sender')
	receiver=models.ForeignKey(BaseUser,related_name='receiver')
	content=models.CharField(max_length=40)
	send_time=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.content

	# sort the message based on send time in reverse order
	class Meta:
		ordering=['-send_time']

# we maintain a relation table which keeps tracking of the folower/followee relationship
# between any two types of users
class Relation(models.Model):
	follower=models.ForeignKey(BaseUser,related_name='follower')
	followee=models.ForeignKey(BaseUser,related_name='followee')

	def __str__(self):
		return self.follower+" -> "+self.followee