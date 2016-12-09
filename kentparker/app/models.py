from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
# Create your models here.

class Tag(models.Model):
	name=models.CharField(max_length=50)
	def __str__(self):
		return self.name

class MyUser(AbstractUser):
	picture=models.ImageField(upload_to="profile_photos",null=True,blank=True)
	email_verify=models.BooleanField(default=False)
	tags=models.ManyToManyField(Tag,blank=True)
	location=models.CharField(max_length=50,blank=True)
	website=models.URLField(max_length=200,blank=True)
	contacts=models.ForeignKey('self',null=True,blank=True,related_name='contacts_f')
	user_type=models.IntegerField()
	# newsmaker 1
	# journalist 2
	# mediaoutlet 3
	category=models.CharField(max_length=50,blank=True)
	bio=models.CharField(max_length=420, blank=True)
	organization=models.ForeignKey('self',null=True,blank=True,related_name='organization_f')
	address=models.CharField(max_length=50,blank=True)
	skype_id=models.CharField(max_length=20,blank=True)
	twitter_id=models.CharField(max_length=20,blank=True)
	facebook_id=models.CharField(max_length=20,blank=True)
	phone=models.CharField(max_length=12,blank=True)
	website=models.URLField(blank=True)
	source=models.CharField(max_length=20,blank=True)
	size=models.CharField(max_length=20,blank=True)
	related_url = models.URLField(blank=True)
	message_people=models.ManyToManyField('self',blank=True,related_name='message_people')
	media_contact = models.CharField(max_length=50, null=True, blank=True)


	def __str__(self):
		return self.username

class Pitch(models.Model):
	title=models.CharField(max_length=200)
	content=models.TextField()
	author=models.ForeignKey(MyUser,related_name='author_pr') # newsmaker
	tags=models.ManyToManyField(Tag,blank=True)
	pub_time=models.DateTimeField(auto_now_add=True)
	last_modified_time=models.DateTimeField(auto_now=True)
	attachment=models.URLField(max_length=200)
	special=models.CharField(max_length=1)
	location=models.CharField(max_length=50,default="")
	published=models.BooleanField(default=False)
	embargoMark=models.BooleanField(default=False)
	bookmarked = models.ManyToManyField(MyUser,blank=True,related_name='bookmarked')
	embargoed = models.ManyToManyField(MyUser,blank=True,related_name='embargoed')
	scooped = models.BooleanField(default=False)
	scooppublished = models.BooleanField(default=False)
	rating_responsiveness = models.DecimalField(blank=True, max_digits=9, decimal_places=2, null=True, default=0)
	rating_worthiness = models.DecimalField(blank=True, max_digits=9, decimal_places=2, null=True, default=0)
	rating_count = models.IntegerField(blank=True, null=True, default=0)
	rated_by=models.ManyToManyField(MyUser,blank=True,related_name='rated_by')

	class Meta:
		ordering=['-pub_time']

class Embargo(Pitch):
	embargo_date=models.DateTimeField()
	selected_journalists=models.ForeignKey(MyUser,null=True,blank=True) # Journalist

class Scoop(Pitch):
	selected_journalist=models.ForeignKey(MyUser) # Journalist
	status=models.BooleanField()

class Article(models.Model):
	title=models.CharField(max_length=200)
	related_pitch=models.ManyToManyField(Pitch,blank=True)
	content=models.TextField()
	author=models.ManyToManyField(MyUser,blank=True, related_name='author_ar') #Journalist
	newsmaker=models.ManyToManyField(MyUser,related_name='newsmaker_am', blank=True)
	pub_time=models.DateTimeField(auto_now_add=True)
	last_modified_time=models.DateTimeField(auto_now=True)
	visited_times = models.IntegerField(default = 0)
	published=models.BooleanField(default=False)
	rating_responsiveness = models.DecimalField(blank=True, max_digits=9, decimal_places=2, null=True, default=0)
	rating_count = models.IntegerField(blank=True, null=True, default=0)
	rated_by=models.ManyToManyField(MyUser,blank=True,related_name='article_rated_by')

	class Meta:
		ordering=['-pub_time']

class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sender')
    receiver = models.ForeignKey(MyUser, related_name='receiver')
    content = models.CharField(max_length=100)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['pub_time']
