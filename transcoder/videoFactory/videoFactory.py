'''
Created on Apr 24, 2016

@author: root
'''
from transcoder.common import tools
from transcoder.models import transcodertask
from datetime import datetime
from transcoder.ttSerializers import ttaskSerializer
import os





def addTranscTask(taskdata):
    confdit=tools.lodConfig()
    logdir=confdit['logdir']
    logfilename=logdir+"/myTranscoder.log"
    lf=tools.logfile(logfilename)
    
    messageDict={}
    taskid=taskdata['taskid']
    srcfile=taskdata['srcfile']
    templatename=taskdata['templatename']
    dstdir=taskdata['dstdir']+"/"
    if os.path.exists(dstdir):
        lf.append(taskid, dstdir+" has exists")
    else:
        lf.append(taskid, dstdir+" not exists - mkdir ")
        os.makedirs(dstdir)	    

    messageDict['action']="addtask"
    messageDict['taskid']=taskid
    
    try:
        tempdit=tools.loadTemplate(templatename)
    except Exception,e:
        messageDict['status']=0
        messageDict['errorMSG']=str(e)
        lf.append(taskid, "Task Add Faild!! ")
        return  messageDict
       
    bit_rate=tempdit['bitrate']
    audiobitrate=tempdit['abitrate']
    size=tempdit['size']
    dformat=tempdit['format']
    transnode=confdit['transNode']
    
    postfix=eval(confdit['formate'])[dformat]
    
    if dstdir == "":
        dstfile=confdit['outdir']+taskid+postfix
    else:
        dstfile=dstdir+taskid+postfix
    
    if dformat == 'hls':
        if dstdir == "":
            dstfile=confdit['outdir']+taskid
        else:
            dstfile=dstdir+taskid
    
        # Save task info to db
    

    lf.append(taskid, "Start DownLoad File ")
    getFileR=tools.getFileFromWget(srcfile,confdit['tempdir'])
    #tools.mylog(taskid, "Finish DownLoad File "+getFileR[1])
    
    if  getFileR[0] != 0 :      
        lf.append(taskid, srcfile+" download Failed !!!")
        messageDict['errorMSG']= tools.timestr()+" "+taskid+" "+srcfile+" download Failed !!!"
        messageDict['status']=0
        return messageDict    
    
    lf.append(taskid, "Finish DownLoad File "+getFileR[1])
           
    try:       
        ttask=transcodertask(taskid=taskid,createtime=datetime.now(),transnode=transnode,src=srcfile,size=size,dformat=dformat,status=1,bitrate=bit_rate,dst=dstfile,abitrate=audiobitrate)
        ttask.save()
        
        messageDict['status']=1
        lf.append(taskid, "Task Add Success!! ")
        return messageDict
    
    except Exception,e:
        messageDict['status']=0
        messageDict['errorMSG']=str(e)
        lf.append(taskid, "Task Add Faild!! ")
        return messageDict
    
def startTranscTask(taskid):
    confdit=tools.lodConfig()   
    logdir=confdit['logdir']
    logfilename=logdir+"/myTranscoder.log"
    lf=tools.logfile(logfilename)
    
    messageDict={}
    messageDict['taskid']=taskid
    messageDict['action']="starttask"
    messageDict['status']=1
    
    lf.append(taskid, "Start Transcoding")
    try:
        task=transcodertask.objects.get(taskid=taskid)              
        ser=ttaskSerializer(task)
    except Exception,e:
        messageDict['status']=4
        messageDict['message']="Task Does Noe Exist"
        lf.append(taskid, "Task Does Noe Exist")
        return messageDict
    taskdata=ser.data
#     if taskdata['status']==3 :
#         messageDict['status']=6
#         messageDict['message']="Don't repeat transcoding"
#         lf.append(taskid, "Don't repeat transcoding")
#         return messageDict
    
    if taskdata['status']==20 :
        messageDict['status']=20
        messageDict['message']="Taskid "+ taskid + "is Running , Don't start it again!!"
        lf.append(taskid, "This Task is Running , Don't start it again!!")
        return messageDict
        
    taskid=taskdata['taskid']
    dformat=taskdata['dformat']
    postfix=eval(confdit['formate'])[dformat]
    downloadurl=confdit['outftp']+taskid+postfix
    
    #check Transcoder Capbility
    if getTCnum() < 1:
        messageDict['status']=5
        messageDict['message']="Transcoding ability run out, please choose other nodes or wait!"
        lf.append(taskid, "Transcoding ability run out, please choose other nodes or wait!")
        return messageDict  
      
    # Save task info to db
    try:
        transcodertask.objects.filter(taskid=taskid).update(status=2)
        transcodertask.objects.filter(taskid=taskid).update(starttime=datetime.now())
        transcodertask.objects.filter(taskid=taskid).update(downloadURL=downloadurl)
        #ffmpeg.transcoder(taskid,callback,ffmpegBin,tfile, bit_rate,audiobitrate ,size, dformat,dstfile,downloadurl)
        messageDict['status']=20
        return messageDict
    except Exception,e:
        #status rollback
        transcodertask.objects.filter(taskid=taskid).update(status=8)
        messageDict['message']=str(e)
        messageDict['status']=8
        lf.append(taskid, "Transcoding Process exception"+str(e))
        return  messageDict
    
    
        
    #print tools.timestr()+" Now CallBack :",tools.httpPost2(callback,messageDict)
        

def getTCnum():
    confdit=tools.lodConfig()
    maxthreads=confdit['maxthreads']
    tasks=transcodertask.objects.filter(status=20)
    sers=ttaskSerializer(tasks,many=True)
    livenum=sers.data.__len__()
    return int(maxthreads)-livenum
        



        

if __name__=='__main__':
    print "Just For Testing"        
