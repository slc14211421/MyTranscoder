'''
Created on Aug 21, 2016

@author: root
'''
from transcoder.common import tools
from transcoder.models import mergetask
from transcoder.mtSerializers import mtaskSerializer
from datetime import datetime
import os

def addMergeTask(taskdata):
   
    confdit=tools.lodConfig()
    logdir=confdit['logdir']
    logfilename=logdir+"/myTranscoder.log"
    lf=tools.logfile(logfilename)
     
    messageDict={}
    taskid=taskdata['taskid']
    srcfile1=taskdata['srcfile1']
    srcfile2=taskdata['srcfile2']
    dstdir=taskdata['dstdir']+"/"
    print dstdir
    if os.path.exists(dstdir):
        lf.append(taskid, dstdir+" has exists")
    else:
        lf.append(taskid, dstdir+" not exists - mkdir ")
    os.makedirs(dstdir)        
 
    messageDict['action']="addMergetask"
    messageDict['taskid']=taskid
    postfix=srcfile2.split('.')[-1]
        
    if dstdir == "":
        dstfile=confdit['outdir']+taskid+"."+postfix
    else:
        dstfile=dstdir+taskid+"."+postfix
     
    print dstdir
        # Save task info to db
     
 
    lf.append(taskid, "Start DownLoad File ")
    getFileR1=tools.getFileFromWget(srcfile1,confdit['tempdir'])
    getFileR2=tools.getFileFromWget(srcfile2,confdit['tempdir'])
    #tools.mylog(taskid, "Finish DownLoad File "+getFileR[1])
     
    if  getFileR1[0] != 0 or  getFileR2[0] != 0 :      
        lf.append(taskid, srcfile1+" download Failed !!!")
        messageDict['errorMSG']= tools.timestr()+" "+taskid+" "+srcfile1+srcfile2+" download Failed !!!"
        messageDict['status']=0
        return messageDict    
     
    lf.append(taskid, "Finish DownLoad File "+getFileR1[1]+" "+getFileR2[1])
            
    try:       
        mtask=mergetask(taskid=taskid,createtime=datetime.now(),src1=srcfile1,src2=srcfile2,status=1,dst=dstfile)
        mtask.save()
         
        messageDict['status']=1
        lf.append(taskid, "MergeTask Add Success!! ")
        return messageDict
     
    except Exception,e:
        messageDict['status']=0
        messageDict['errorMSG']=str(e)
        lf.append(taskid, "MergeTask Add Faild!! ")
        return messageDict
    

def startMergeTask(taskid):
    confdit=tools.lodConfig()   
    logdir=confdit['logdir']
    logfilename=logdir+"/myTranscoder.log"
    lf=tools.logfile(logfilename)
    
    messageDict={}
    messageDict['taskid']=taskid
    messageDict['action']="startMergetask"
    messageDict['status']=1
    
    lf.append(taskid, "Start Merge")
    try:
        task=mergetask.objects.get(taskid=taskid)              
        ser=mtaskSerializer(task)
    except Exception,e:
        messageDict['status']=4
        messageDict['message']="Task Does Noe Exist"
        lf.append(taskid, "Task Does Noe Exist")
        return messageDict
    taskdata=ser.data
    if taskdata['status']==20 :
        messageDict['status']=20
        messageDict['message']="Taskid "+ taskid + "is Running , Don't start it again!!"
        lf.append(taskid, "This Task is Running , Don't start it again!!")
        return messageDict
        
    
    #check Transcoder Capbility
#     if getTCnum() < 1:
#         messageDict['status']=5
#         messageDict['message']="Transcoding ability run out, please choose other nodes or wait!"
#         lf.append(taskid, "Transcoding ability run out, please choose other nodes or wait!")
#         return messageDict  
#       
    # Save task info to db
    try:
        mergetask.objects.filter(taskid=taskid).update(status=2)      
        
        messageDict['status']=20
        return messageDict
    except Exception,e:
        #status rollback
        mergetask.objects.filter(taskid=taskid).update(status=8)
        messageDict['message']=str(e)
        messageDict['status']=8
        lf.append(taskid, "Transcoding Process exception"+str(e))
        return  messageDict   