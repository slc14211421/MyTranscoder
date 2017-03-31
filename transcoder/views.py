import simplejson
from django.http import HttpResponse
from transcoder.common import tools
from models import transcodertask
from ttSerializers import ttaskSerializer
from transcoder.videoFactory.videoFactory import addTranscTask,startTranscTask,getTCnum



# Create your views here.
def addTask(request):
    if request.method == 'POST':
        taskdata=simplejson.loads((request.body).decode())
        result=addTranscTask(taskdata)
        
        return HttpResponse(simplejson.dumps(result)) 



    
def startTask(request,taskid):
    if request.method=='GET':
        
        result=startTranscTask(taskid)
       
        return HttpResponse(simplejson.dumps(result))
    
def getTC(request):
    return HttpResponse(getTCnum())


 
 
def getTaskdetail(request,qstr):
    if qstr == "ALL":
        #print qstr
        tasks=transcodertask.objects.all()
        sers=ttaskSerializer(tasks,many=True)
        return tools.JSONResponse(sers.data)
    elif qstr == "LIVE":
        tasks=transcodertask.objects.filter(status=20)
        sers=ttaskSerializer(tasks,many=True)
        return tools.JSONResponse(sers.data)
    else:    
        task=transcodertask.objects.get(taskid=qstr)
        ser=ttaskSerializer(task)
        return tools.JSONResponse(ser.data)
    