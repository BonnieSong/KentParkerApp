from django import forms
from django.forms import ModelForm
from app.models import *

class RegisterModelForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput())
	confirm=forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model=User
		fields=['username','email','password','confirm','first_name','last_name']

	def clean(self):
		cleaned_data=super(RegisterModelForm,self).clean()
		if User.objects.filter(username=cleaned_data.get('username')):
			raise forms.ValidationError('Username is already taken.')
		if User.objects.filter(email=cleaned_data.get('email')):
			raise forms.ValidationError('Email is already taken.')
		if cleaned_data.get('password')!=cleaned_data.get('confirm'):
			raise forms.ValidationError('Passwords did not match')
		return cleaned_data