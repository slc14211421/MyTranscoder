import simplejson
from django.http import HttpResponse
from transcoder.videoFactory.mergeFactory import addMergeTask,startMergeTask


# Create your views here.  

def addMTask(request):
    taskdata=simplejson.loads((request.body).decode())
    print taskdata
    #messageDict={}
    #messageDict['test']="test"
    result=addMergeTask(taskdata)        
    return HttpResponse(simplejson.dumps(result))

def startMTask(request,taskid):
    if request.method=='GET':
        
        result=startMergeTask(taskid)
       
        return HttpResponse(simplejson.dumps(result))   

    
