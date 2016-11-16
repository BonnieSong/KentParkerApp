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
	r_type=forms.ChoiceField(choices=((1,'News Maker'),(2,'Journalist'),(3,'Media Outlet')),widget=forms.Select(attrs={'class':'form-control'}))
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
		fields=['title','content','tags']

class PublishArticleForm(forms.ModelForm):
	class Meta:
		model=Article
		fields=['title','content','newsmaker']

class EditProfileModelForm(forms.ModelForm):
	class Meta:
		model=MyUser
		fields=['first_name','last_name','bio','picture']
		widgets={	'first_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
					'last_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
					'picture':forms.FileInput(attrs={'class':'form-control'}),
					'bio':forms.Textarea(attrs={'class':'form-control','placeholder':'Bio'})}

class ChangePasswordModelForm(forms.ModelForm):
	old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old Password'}))
	new_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New Password'}))
	confirm=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))
	class Meta:
		model=MyUser
		fields=['old_password','new_password','confirm']

	def clean(self):
		cleaned_data=super(ChangePasswordModelForm,self).clean()
		if cleaned_data.get('new_password')!=cleaned_data.get('confirm'):
			raise forms.ValidationError('Passwords did not match')
		return cleaned_data

class RequestResetPasswordForm(forms.Form):
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))

class ResetPaswordForm(forms.Form):
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password'}))
	confirm=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}))

	def clean(self):
		cleaned_data=super(ResetPaswordForm,self).clean()
		if cleaned_data.get('password')!=cleaned_data.get('confirm'):
			raise forms.ValidationError('Passwords did not match')
		return cleaned_data

class register_step2_newsmaker_form(forms.ModelForm):
	class Meta:
		model=MyUser
		fields=['address','website','phone','skype_id','twitter_id','facebook_id','bio','size','industry','source']

class register_step2_mediaoutlet_form(forms.ModelForm):
	class Meta:
		model=MyUser
		fields=['address','website','phone','skype_id','twitter_id','facebook_id','bio','size','source']

class register_step2_journalist_form(forms.ModelForm):
	#tags = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False, help_text="Tag")
	class Meta:
		model=MyUser
		fields=['organization','phone','skype_id','twitter_id','facebook_id','tags','bio','source']