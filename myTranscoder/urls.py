"""myTranscoder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from transcoder import views as transc_views
from transcoder import myjob 
from transcoder import mergeviews as merge_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #For TanscoderTask
    url(r'^addTask/$',transc_views.addTask),
    url(r'^startTask/(\w+)$',transc_views.startTask),
    url(r'^getTC/$',transc_views.getTC),
    url(r'^getTaskDetail/(\w+)$',transc_views.getTaskdetail),
    url(r'^mycronjob/$',myjob.mytranscjob),
    #For MergeTask
    url(r'^addMTask/$',merge_views.addMTask),
    url(r'^startMTask/(\w+)$',merge_views.startMTask),
    url(r'^myMergejob/$',myjob.mergejob),
    
]
