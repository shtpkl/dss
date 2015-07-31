from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class RegistrationForm(forms.Form) :
	username = forms.CharField(label='Username', max_length=30)
	email = forms.EmailField(label='Email')
	password1 = forms.CharField(label='Password', widget = forms.PasswordInput() )
	password2 = forms.CharField(label='Password (Again)', widget = forms.PasswordInput() )

def clean_password2(self):
	if 'password1' in self.clean_data:
		password1 = self.clean_data['password1']
		password2 = self.clean_data['password2']
		if password1 == password2:
			return password2
		raise forms.ValidationError('Passwords do not match.')

def clean_username(self):
	username = self.clean_data['username']
	if not re.search(r'^\w+$',username):
		raise  forms.ValidationError ('username can only contain alphanumeric characters')
	try:
		Users.objects.get(username=username)
	except  ObjectDoesNotExist:
		return username
	raise forms.Validation('Usrename is already taken..')

#class BookmarkSaveForm(forms.Form):
#	url = forms.URLField(label='URL', widget=forms.TextInput(attrs = { 'size': 64 } ) )
#	title = forms.CharField(label='Title', widget=forms.TextInput(attrs = { 'size': 64 } ) )
#	tags = forms.CharField(label='Tags', required=False, widget=forms.TextInput(attrs = { 'size': 64 } ) )

class DocumentForm(forms.Form):
	docfile=forms.FileField(label='Select a File', help_text='max. 42MB')

class CreateFolderForm(forms.Form):
	foldername = forms.CharField(label='Folder', widget=forms.TextInput(attrs={'size':64} ) )

class DeleteFolderForm(forms.Form):
	foldername = forms.CharField(label='Select a Folder', widget=forms.TextInput(attrs={'size':64} ) )
#	foldername = forms.FilePathField(path ='media/%s' , recursive=True,allow_files=False,allow_folders=True, widget = forms.Select (attrs = { 'size' : '10'}) )

class MoveFolderForm(forms.Form):
	orgFolder = forms.CharField(label='Folder', widget=forms.TextInput(attrs={'size':64} ) )
	destFolder = forms.CharField(label='Folder', widget=forms.TextInput(attrs={'size':64} ) )

class UploadFileForm(forms.Form):
	file  = forms.FileField()

class DownloadFileForm(forms.Form):
	file  = forms.FileField()

class SearchForm(forms.Form):
	search = forms.CharField(label='Search', widget=forms.TextInput(attrs = { 'size' : 64 } ) )
