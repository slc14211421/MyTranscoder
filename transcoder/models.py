#!/usr/bin/env python
#coding=UTF-8

from __future__ import unicode_literals

from django.db import models
from django.db.models.fields import CharField, DateTimeField, IntegerField


# Create your models here.

class transcodertask(models.Model):
    taskid=CharField(max_length=100,primary_key=True)
    createtime=DateTimeField()
    size=CharField(max_length=50)
    src=CharField(max_length=100)
    dst=CharField(max_length=100)
    dformat=CharField(max_length=30)
    downloadURL=CharField(max_length=100)
    transnode=CharField(max_length=60)
    # 1 Not transcoding, 2 transcoding ,3 transcoding sucess , 8 transcoding Failed
    status=IntegerField()
    bitrate=IntegerField()
    abitrate=IntegerField()
    starttime=DateTimeField(null=True)
    endtime=DateTimeField(null=True)
    def __unicode__(self):
    # 在Python3中使用 def __str__(self)
        return self.taskid
    
    def getTask(self):
        
        return self.src
    
class mergetask(models.Model):
    taskid=CharField(max_length=100,primary_key=True)
    createtime=DateTimeField()
    src1=CharField(max_length=100)
    src2=CharField(max_length=100)
    dst=CharField(max_length=100)
    # 1 Not transcoding, 2 transcoding ,3 transcoding sucess , 8 transcoding Failed
    status=IntegerField()
    def __unicode__(self):
    # 在Python3中使用 def __str__(self)
        return self.taskid
    
    def getTask(self):
        
        return self.src1
    
