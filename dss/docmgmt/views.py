from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User,Group
from django.contrib.auth import logout
from docmgmt.forms import *
#from bookmarks.models import *

# Create your views here.
def main_page(request) :
#	output='''
#		<html>
#			<head><title>%s</title></head>
#			<body><h1>%s</h1><p>%s</p></body>
#		</html>
#	''' % ( 'Django Bookmarks', 'Welecome to Django Bookmarks',
#		'Where you can store and share bookmarks!' )
#        template = get_template('main_page.html')
#	variables = Context ( {
#		'head_title': 'Django Bookmarks',
#		'user': request.user
#		})
#	output=template.render(variables)
	return render_to_response('main_page.html', RequestContext(request))


def user_page(request,username):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('Requested User not found.')
	bookmarks = user.bookmark_set.all()
	variables = RequestContext( request, {
		'username': username,
		'bookmarks': bookmarks
		} )
	return render_to_response('user_page.html',variables)

def logout_page (request) :
	logout(request)
	return HttpResponseRedirect('/')

@csrf_exempt
def register_page(request) :
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user( username= form.cleaned_data['username'],
						password = form.cleaned_data['password1'],
						email= form.cleaned_data['email']
						)
			user.groups.add(Group.objects.get(name='user') )
		return HttpResponseRedirect('/register/success')
	else :
		form = RegistrationForm()
		variables = RequestContext(request, { 'form' : form } )
		str (variables['csrf_token'] )
		return render_to_response( 'registration/register.html', variables )

@csrf_exempt
def bookmark_save_page(request):
	if request.method == 'POST':
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'] )
			bookmark,created = Bookmark.objects.get_or_create(user=request.user, link=link)
			bookmark.title=form.cleaned_data['title']
			if not created :
				bookmark.tag_set.clear()
			tag_names = form.cleaned_data['tags'].split()
			for tag_name in tag_names :
				tag,dummy = Tag.objects.get_or_create(name=tag_name)
				bookmark.tag_set.add(tag)
			bookmark.save()
			return HttpResponseRedirect('user/%s/' % request.user.username)
	else:
		form=BookmarkSaveForm()
		variables = RequestContext(request, {'form': form } )
		return render_to_response('bookmark_save.html', variables)

from docmgmt.models import Document
from docmgmt.forms  import DocumentForm

def list_file(request):
	if request.method == 'POST':
		form = DocumentForm(request.POST,request.FILES)
		if form.is_valid():
			newdoc = Document(docfile = request.FILES['docfile'] )
			newdoc.save()
			return HttpResponseRedirect(reverse('dss.docmgmt.views.listfile')) 
	else:
		form=DocumentForm()
	documents = Document.objects.all()
	return render_to_response('list.html', { 'documents' : documents, 'form' : form } , context_instance = RequestContext(request) )

def home_page(request):
	return render_to_response('home_page.html', RequestContext(request))

def success(request):
	return render_to_response('success.html', RequestContext(request) )

from docmgmt.forms  import CreateFolderForm
import os
import shutil

@csrf_exempt
def create_folder(request):
	if request.method == 'POST':
		form=CreateFolderForm(request.POST) 
		if form.is_valid() :  
			foldername= form.cleaned_data['foldername']
			print (settings.MEDIA_ROOT + request.user.username +'/'+ foldername)
			os.makedirs(settings.MEDIA_ROOT + request.user.username + '/' +  foldername)
			return HttpResponseRedirect('/success')
	else:
		form=CreateFolderForm()
		return render_to_response('createfolder.html', { 'form' : form },  context_instance = RequestContext(request))

@csrf_exempt
def delete_folder(request):
	if request.method == 'POST':
		form=DeleteFolderForm(request.POST) 
		if form.is_valid() :  
			foldername= "media/" + request.user.username + "/" + form.cleaned_data['foldername']
			if os.path.isdir(foldername):
				print foldername
				shutil.rmtree(foldername)
				return HttpResponseRedirect('/success')
	else:
		form=DeleteFolderForm()
		return render_to_response('deletefolder.html', { 'form' : form },  context_instance = RequestContext(request))

@csrf_exempt
def move_folder(request):
	basedir = "media/"
	if request.method == 'POST':
		form=MoveFolderForm(request.POST) 
		if form.is_valid() :  
			src= basedir + request.user.username + "/" + form.cleaned_data['orgFolder']
			dest= basedir + request.user.username + "/" + form.cleaned_data['destFolder']
			print src, os.path.isdir(src)
			if os.path.isdir(src) :
				shutil.move(src, dest)
				print src, dest
				return HttpResponseRedirect('/success')
	else:
		form=MoveFolderForm()
		return render_to_response('movefolder.html', { 'form' : form },  context_instance = RequestContext(request))

from django.conf import settings
@csrf_exempt
def addfile(request):
	if request.method == 'POST':
		form=UploadFileForm(request.POST, request.FILES) 
		if form.is_valid() :  
			file = request.FILES['file']
			fpath=settings.MEDIA_ROOT + request.user.username +'/' + file.name
			with open(fpath,'wb+') as destination:
				for chunk in file.chunks():
					destination.write(chunk)
			return HttpResponseRedirect('/success')
	else:
		form=UploadFileForm()
		return render_to_response('addfile.html', { 'form' : form },  context_instance = RequestContext(request))

from django.core.servers.basehttp import FileWrapper
from django.utils.encoding import smart_str
import mimetypes

@csrf_exempt
def download_file(request):
	if request.method == 'POST':
		form=DownloadFileForm(request.POST, request.FILES) 
		if form.is_valid() :  
			file = request.FILES['file']
			file_path ="".join(settings.MEDIA_ROOT) + "".join(file.name)
			file_wrapper = FileWrapper(file,'rb')
			fp = open(file.name,'rb')
			file_mimetype,encoding = mimetypes.guess_type(file.name)
			print file_wrapper, file_mimetype
			response = HttpResponse(fp.read(), content_type = file_mimetype)
			response['X-Sendfile'] = file_path
			response['Content-Length'] = os.stat(file_path).st_size
			response['Content-Disposition'] ='attachment; filename=%s' % smart_str(file.name)
			return response
	else:
		form=UploadFileForm()
		return render_to_response('download.html', { 'form' : form },  context_instance = RequestContext(request))

from os.path import abspath, dirname
from pathlib import Path
from filebrowser.base import FileListing, FileObject

def filter_filelisting(item) :
	return item.filetype != "Folder"

@csrf_exempt
def listfile(request):
	filelist ={} 
	if request.method == 'GET':
		filelisting = FileListing(settings.MEDIA_ROOT ,filter_func = filter_filelisting)
		for file in filelisting.files_walk_filtered():
			rel_file_path = file.url[len(settings.MEDIA_ROOT):]
			filelist[rel_file_path]= file.filename
			print file.url.find(settings.MEDIA_ROOT) + len(settings.MEDIA_ROOT)
	else : 
		delfile= request.POST.get('Delete')
		os.remove(delfile)
		filelisting = FileListing(settings.MEDIA_ROOT ,filter_func = filter_filelisting)
		for file in filelisting.files_walk_filtered():
			filelist[file.url]= file.filename
	return render_to_response('listfiles.html', { 'filelist' : filelist },  context_instance = RequestContext(request))


@csrf_exempt
def search(request):
	if request.method == 'POST':
		filelist = {}
		form=SearchForm(request.POST) 
		if form.is_valid() :  
			txtSearch= form.cleaned_data['search']
			for dirpath,dirs,files in os.walk(settings.MEDIA_ROOT):
				for filename in files:
					fname = os.path.join(dirpath, filename)
					ext =filename[ filename.rindex(".") + 1: ]
					print ext
					if ext =='docx':
						fstr = open((dirpath+"/"+filename),'rb').read()
						pattern = re.compile(txtSearch)	
						pattern.findall(fstr)
					else :
						with open(fname ,'rb') as inpfile:
							for line in inpfile :
								if re.search(txtSearch,line):
									rel_file_path = dirpath[len(settings.MEDIA_ROOT):]
									filelist[rel_file_path] = filename
		return render_to_response('search.html', { 'filelist' : filelist , 'form' : form },  context_instance = RequestContext(request))
	else:
		form=SearchForm()
		return render_to_response('search.html', { 'form' : form },  context_instance = RequestContext(request))
