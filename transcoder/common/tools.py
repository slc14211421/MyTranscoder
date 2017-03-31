'''
Created on Apr 23, 2016

@author: root
'''
import subprocess
import ConfigParser
import os
import time
import httplib
import simplejson
from django.http.response import StreamingHttpResponse
from rest_framework.renderers import JSONRenderer





   
def getFileFromWget(url,tdir):
    commd="wget -t 2 -P "+tdir+" "+url
    tfile=tdir+url.split('/')[-1]
    result=subprocess.call(commd,shell=True)
    return [result,tfile]

def lodConfig():
    basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print basedir
    confdit={}
    conf=ConfigParser.ConfigParser()
    conf.read(basedir+"/config/transcoder.conf")
    confdit['ffmpegBin']=conf.get('transc','ffmpegBin')
    confdit['outdir']=conf.get('transc','outdir')
    confdit['tempdir']=conf.get('transc','tempdir')
    confdit['mergetdir']=conf.get('transc','mergetdir')
    confdit['outftp']=conf.get('transc','outftp')
    confdit['callback']=conf.get('transc','callback')
    confdit['formate']=conf.get('transc','formate')
    confdit['transNode']=conf.get('transc','transNode')
    confdit['maxthreads']=conf.get('transc','maxthreads')
    confdit['logdir']=conf.get('transc','logdir')
    return confdit

def loadTemplate(templateName):
    basedir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tempdit={}
    temp=ConfigParser.ConfigParser()
    temp.read(basedir+"/template/template.conf")
    tempdit['bitrate']=temp.get(templateName,'bitrate')
    tempdit['abitrate']=temp.get(templateName,'abitrate')
    tempdit['size']=temp.get(templateName,'size')
    tempdit['format']=temp.get(templateName,'format')
    return tempdit

def timestr():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def httpPostB(url,messageDict):
    msgJSON=simplejson.dumps(messageDict,indent=4)
    requrl = "/"+url.split('/')[-1]+"/"
    headerdata = {"Host":url.split('/')[2]}
    #print url.split('/')
    #print requrl,headerdata
    conn = httplib.HTTPConnection(url.split('/')[2])
    conn.request(method="POST",url=requrl,body=msgJSON,headers = headerdata) 
    return conn.getresponse().status

def httpPost2(url,messageDict):
    msgJSON=simplejson.dumps(messageDict,indent=4)
    ml=len(url.split('/'))
    #requrl = "/"+str(url.split('/')[3:])+"/"
    requrl = "/"
    i=3
    while (i<ml):
        print url.split('/')[i]
        if (i+1) == ml:
            requrl = requrl+str(url.split('/')[i])
        else:     
            requrl = requrl+str(url.split('/')[i])+"/"
        i=i+1
        
         
    headerdata = {"Host":url.split('/')[2]}
    #print url.split('/')
    print requrl,headerdata
    conn = httplib.HTTPConnection(url.split('/')[2])
    conn.request(method="POST",url=requrl,body=msgJSON,headers = headerdata)
    response=conn.getresponse()
    print msgJSON
    print response.status
    print response.read()
    return response.status


class JSONResponse(StreamingHttpResponse):
    def __init__(self,data,**kwargs):
        content=JSONRenderer().render(data)
        kwargs['content_type']='application/json;charset=utf-8'
        super(JSONResponse,self).__init__(content,**kwargs)
        
class logfile:
    def __init__(self,filename):
        self.filename = filename
    def append(self,taskid,tstr):
        self.logstr = "["+timestr()+"]"+" "+taskid+" "+tstr+"\n"
        f = open(self.filename,'a')
        print>>f,self.logstr
        f.close()  

if __name__=='__main__':
    print "This is Testing ....."
    #print getFileFromWget("ftp://vision:vision@192.168.150.120/vod/gqss.ts", "/home/vision/transcTemp/")
    confdit=lodConfig()
    for i in confdit:
        print i,confdit[i]
    
    print  timestr()
    print httpPost2("http://192.168.150.100:8088/transcResult", '{"111":111}')
      
