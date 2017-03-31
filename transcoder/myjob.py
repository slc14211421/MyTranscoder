'''
Created on May 5, 2016

@author: root
'''
from common import dbfactory,ffmpeg,tools
from django.http.response import HttpResponse
from transcoder.models import transcodertask
from transcoder.models import mergetask
import threading 

def mytranscjob(request):
    confdit=tools.lodConfig()
    callback=confdit['callback']
    ffmpegBin=confdit['ffmpegBin']

    
    print "+++++++++CRONJOB STARTING Transcoder Job++++++++++"

    
    mydb=dbfactory.SQLObj()
    res=mydb.dquery("select * from transcoder_transcodertask where status=2;")
    threads = []
    
    for taskdata in res:
        #print r['taskid']
        taskid=taskdata['taskid']
        bit_rate=taskdata['bitrate']
        size=taskdata['size']
        dformat=taskdata['dformat']
        audiobitrate=taskdata['abitrate']
        downloadurl=taskdata['downloadURL']
        dstfile=taskdata['dst']
        srcfile=taskdata['src']
        tfile=confdit['tempdir']+srcfile.split('/')[-1]
        print "CALL FFMPEG for TASKID "+ taskid
        #ffmpeg.transcoder(taskid,callback,ffmpegBin,tfile, bit_rate,audiobitrate ,size, dformat,dstfile,downloadurl)
        transcodertask.objects.filter(taskid=taskid).update(status=20)
        thread = threading.Thread(target=ffmpeg.transcoder,args=(taskid,callback,ffmpegBin,tfile, bit_rate,audiobitrate ,size, dformat,dstfile,downloadurl))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
            thread.join()
        
    print "+++++++++CRONJOB END++++++++++"
    return HttpResponse("HELLO")

def mergejob(request):
    confdit=tools.lodConfig()
    callback=confdit['callback']
    ffmpegBin=confdit['ffmpegBin']

    
    print "+++++++++CRONJOB STARTING Merge JOB++++++++++"
    mydb=dbfactory.SQLObj()
    res=mydb.dquery("select * from transcoder_mergetask where status=2 order by createtime asc limit 3;")
    threads = []
    for taskdata in res:
        #print r['taskid']
        taskid=taskdata['taskid']
        dstfile=taskdata['dst']
        srcfile1=taskdata['src1']
        srcfile2=taskdata['src2']
        tfile1=confdit['tempdir']+srcfile1.split('/')[-1]
        tfile2=confdit['tempdir']+srcfile2.split('/')[-1]
        print "CALL FFMPEG for TASKID "+ taskid
        #ffmpeg.transcoder(taskid,callback,ffmpegBin,tfile, bit_rate,audiobitrate ,size, dformat,dstfile,downloadurl)
        mergetask.objects.filter(taskid=taskid).update(status=20)
        thread = threading.Thread(target=ffmpeg.merge,args=(taskid,callback,ffmpegBin,tfile1,tfile2,dstfile))
        threads.append(thread)
        thread.start()
        
    for thread in threads:
            thread.join()
    print "+++++++++CRONJOB Merge JOB END++++++++++"
    return HttpResponse("HELLO")
            

    
if __name__=='__main__':
    print "main"
