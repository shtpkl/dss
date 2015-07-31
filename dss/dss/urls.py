import os.path 

from django.views.generic import TemplateView
from django.conf.urls import  patterns, include, url
from django.conf.urls.static  import  static
from django.conf  import  settings
from django.contrib import admin
from docmgmt.views import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
site_media = os.path.join( BASE_DIR, 'site_media')

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DigitalStorage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

#Admin Interfaces
     url(r'^admin/', include(admin.site.urls)),

# Browsing
    (r'^$', main_page),
    (r'^user/(\w+)/$', user_page),

# Session Management

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', TemplateView.as_view(template_name="registration/registration_success.html") ), 
    (r'^site_media/(?P<path>.*)/$', 'django.views.static.serve', { 'document_root': site_media }),
#
##Account Management
##    (r'^save/$', bookmark_save_page),
#
##Document Management 
    (r'^home/$', home_page),
    (r'^createfolder/$', create_folder),
    (r'^deletefolder/$', delete_folder),
    (r'^movefolder/$', move_folder),
    (r'^addfile/$',addfile),
    (r'^download/$',download_file),
    (r'^listfiles/$',listfile),
    (r'^search/$', search),
    (r'^success/$', success),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
