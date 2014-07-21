from rango.models import UserProfil
from django.contrib.auth.models import User
from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length = 128, help_text = 'Please enter category name')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

	class Meta:
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length = 128, help_text = 'Please enter title of the page')		
	url = forms.CharField(max_length=200, help_text="Please enter the URL of the page.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page

		fields = ('title', 'url', 'views')

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfilForm(forms.ModelForm):
	class Meta:
		model = UserProfil
		fields = ('website', 'picture')		