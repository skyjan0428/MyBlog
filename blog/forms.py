from django import forms
from .models import User

class SignUpForm(forms.Form):
	name = forms.CharField(label='name', min_length=1, max_length=10)
	email = forms.CharField(label='email', min_length=1, max_length=30)
	password = forms.CharField(label='password', widget=forms.PasswordInput(), min_length=1, max_length=20)

	# class Meta:
	# 	model = User
	# 	fields = ['name', 'email', 'password']


class LoginForm(forms.Form):
	email = forms.CharField(label='email', min_length=1, max_length=30)
	password = forms.CharField(label='password', widget=forms.PasswordInput(), min_length=1, max_length=20)