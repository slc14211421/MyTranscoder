'''
Created on Apr 23, 2016

@author: root
'''
import subprocess,os
from transcoder.common import tools
from transcoder.models import transcodertask,mergetask
from datetime import datetime
import shutil


    

def transcoder(taskid,callback,ffmpegbin,tfile,bit_rate,abitrate,size,dformat,dstfile,downloadurl):
    print tools.timestr()+" "+ taskid + "transcoder String "
    confdit=tools.lodConfig()
    messageDict={}
    messageDict['taskid']=taskid
    messageDict['action']="transcodeResult"
    filename=downloadurl.split('/')[4]
    
    
    if dformat == "mp4" or dformat == "mpegts":
        if abitrate == -1:
            cmmd="%s -y -i %s -b:v %s -maxrate %s -minrate %s -f %s -acodec libvo_aacenc -ar 48000 -ac 2 -r 25 -vcodec libx264  -s %s %s" % (ffmpegbin,tfile,bit_rate,bit_rate,bit_rate,dformat,size,dstfile)
        else:
            cmmd="%s -y -i %s -b:v %s -maxrate %s -minrate %s -f %s -acodec libvo_aacenc -ar 48000 -b:a %s -ac 2 -r 25 -vcodec libx264  -s %s %s" % (ffmpegbin,tfile,bit_rate,bit_rate,bit_rate,dformat,abitrate,size,dstfile)
    
    if dformat == "flv":
        if abitrate == -1:
            cmmd="%s -y -i %s -c:v h264 -strict -2  -ar 48000 -r 25 -c:a aac -b:v %s  -s %s %s" % (ffmpegbin,tfile,bit_rate,size,dstfile)
        else:
            cmmd="%s -y -i %s -c:v h264 -strict -2  -ar 48000 -r 25 -c:a aac -b:v %s -b:a %s -s %s %s" % (ffmpegbin,tfile,bit_rate,abitrate,size,dstfile)
    
        
    if dformat == 'hls':
        postfix=eval(confdit['formate'])[dformat]
        hlsdstdir=dstfile
        if os.path.exists(hlsdstdir):
            print hlsdstdir+" has exists!"
        else:
            os.mkdir(hlsdstdir)
        m3u8dstfile=dstfile+"/"+taskid+postfix
        tsfiles=dstfile+"/"+taskid+"%03d.ts"
        downloadurl=confdit['outftp']+taskid
        
        if abitrate == -1:
            cmmd="%s -re -i %s -map 0 -c:v h264 -strict -2 -c:a aac  -segment_list_type hls -f ssegment -b:v %s  -s %s -segment_list %s  -segment_time 10  %s" % (ffmpegbin,tfile,bit_rate,size,m3u8dstfile,tsfiles)            
        else:                
            cmmd="%s -re -i %s -map 0 -c:v h264 -strict -2 -c:a aac  -segment_list_type hls -f ssegment -b:v %s -b:a %s -s %s -segment_list %s   -segment_time 10  %s" % (ffmpegbin,tfile,bit_rate,abitrate,size,m3u8dstfile,tsfiles)     
        
    print   tools.timestr()+" "+ taskid + " "+cmmd
    try:
        result=subprocess.call(cmmd,shell=True)
        if result == 0:
            messageDict['status']=3
            messageDict['downloadURL']=downloadurl
            #messageDict['dstfile']=dstfile
            if dformat == 'hls':
                
                shutil.copytree(dstfile, confdit['outdir']+taskid)
            else:
                shutil.copyfile(dstfile,confdit['outdir']+filename)
            print tools.timestr()+" "+taskid+" Transcoder-Sucess"
            transcodertask.objects.filter(taskid=taskid).update(status=3)
            transcodertask.objects.filter(taskid=taskid).update(downloadURL=downloadurl)
            transcodertask.objects.filter(taskid=taskid).update(endtime=datetime.now())
        else:
            messageDict['status']=8
            transcodertask.objects.filter(taskid=taskid).update(status=8)
            print  tools.timestr()+" "+taskid+" Transcoder-Failed"    
         
    except Exception as e:
        print e
        messageDict['status']=8
        transcodertask.objects.filter(taskid=taskid).update(status=8)
        print tools.timestr()+" "+taskid+" Transcoder-Failed"
         
    tools.httpPost2(callback, messageDict)
    
def merge(taskid,callback,ffmpegbin,tfile1,tfile2,dstfile):
    print tools.timestr()+" "+ taskid + "Merge String "
    confdit=tools.lodConfig()
    messageDict={}
    messageDict['taskid']=taskid
    messageDict['action']="MergeResult"
    sourcedir=confdit['tempdir']
    mergetdir=confdit['mergetdir']
    sourcefile1=sourcedir+tfile1.split('/')[-1]
    sourcefile2=sourcedir+tfile2.split('/')[-1]
    mtfile1=mergetdir+taskid+"1.ts"
    mtfile2=mergetdir+taskid+"2.ts"
    dfomat1=tfile1.split('.')[-1]
    dfomat2=tfile2.split('.')[-1]
    
    if dfomat1 == dfomat2 and dfomat1 == 'ts' :
        print "TS Merge "
        cmmd1="%s -i 'concat:%s|%s' -acodec copy -vcodec copy %s" % (ffmpegbin,sourcefile1,sourcefile2,dstfile)
        
        try:
            result1=subprocess.call(cmmd1,shell=True)
            if result1 == 0 :
                messageDict['status']=3           
                print tools.timestr()+" "+taskid+" Merge-Sucess"
                mergetask.objects.filter(taskid=taskid).update(status=3)
            else:
                messageDict['status']=8
                mergetask.objects.filter(taskid=taskid).update(status=8)
                print  tools.timestr()+" "+taskid+" Merge-Failed"    
        
            
        except Exception as e:
            print e
            messageDict['status']=8
            mergetask.objects.filter(taskid=taskid).update(status=8)
            print tools.timestr()+" "+taskid+" Merge-Failed"           
                
    
    
    if dfomat1 == dfomat2 and dfomat1 == 'mp4' :
        cmmd1="%s -i  %s -c copy -bsf:v h264_mp4toannexb -strict -2 -c:a aac  -f mpegts %s" % (ffmpegbin,sourcefile1,mtfile1)
        cmmd2="%s -i  %s -c copy -bsf:v h264_mp4toannexb -strict -2 -c:a aac  -f mpegts %s" % (ffmpegbin,sourcefile2,mtfile2)
        cmmd3="%s -i 'concat:%s|%s' -c copy -bsf:a aac_adtstoasc  -movflags +faststart %s" % (ffmpegbin,mtfile1,mtfile2,dstfile)
    
        try:
            result1=subprocess.call(cmmd1,shell=True)
            result2=subprocess.call(cmmd2,shell=True)
            result3=subprocess.call(cmmd3,shell=True)
            if result1 == 0 and result2 == 0 and result3 == 0:
                messageDict['status']=3           
                print tools.timestr()+" "+taskid+" Merge-Sucess"
                mergetask.objects.filter(taskid=taskid).update(status=3)
            else:
                messageDict['status']=8
                mergetask.objects.filter(taskid=taskid).update(status=8)
                print  tools.timestr()+" "+taskid+" Merge-Failed"    
        
        except Exception as e:
            print e
            messageDict['status']=8
            mergetask.objects.filter(taskid=taskid).update(status=8)
            print tools.timestr()+" "+taskid+" Merge-Failed"
        
    tools.httpPost2(callback, messageDict)    
    
        
        

if __name__=="__main__":
    print "This is Testing"
    #print transcoder('/opt/ffmpeg/bin/ffmpeg','/home/vision/transcTemp/gqss.ts','2500','800*600','mpegts','/home/vision/out/10000000.ts')
    transcoder('vod0000000111','http://192.168.150.100:8088/transcResult','/opt/ffmpeg/bin/ffmpeg','/home/vision/transcTemp/gqss.ts','800000',-1,'720x576','hls','/home/vision/out/10000000.m3u8','downloadtest')
