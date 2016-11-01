from django import forms
from django.forms import ModelForm
from app.models import *

class RegisterForm(forms.Form):
	r_username=forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
	r_email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
	r_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
	r_confirm=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
	r_first_name = forms.CharField(max_length= 20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
	r_last_name = forms.CharField(max_length= 20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

	def clean(self):
		cleaned_data=super(RegisterForm,self).clean()
		if MyUser.objects.filter(username=cleaned_data.get('r_username')):
			raise forms.ValidationError('Username is already taken.')
		if MyUser.objects.filter(email=cleaned_data.get('r_email')):
			raise forms.ValidationError('Email is already taken.')
		if cleaned_data.get('r_password')!=cleaned_data.get('r_confirm'):
			raise forms.ValidationError('Passwords did not match')
		return cleaned_data

class PublishPitchForm(forms.ModelForm):
	class Meta:
		model=Pitch
		fields=['title','content','location']

	def clean(self):
		cleaned_data=super(PublishPitchForm,self).clean()

		