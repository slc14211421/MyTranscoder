'''
Created on May 5, 2016

@author: root
'''
from transcoder.models import transcodertask
from transcoder.common import tools,ffmpeg
#from transcoder.ttSerializers import ttaskSerializer

def mytranscjob():
    tasks=transcodertask.objects.filter(status=2)
    print "test"
#     sers=ttaskSerializer(tasks,many=True)
#     print "test2"
#     print sers.data


if __name__=="__main__":
    print "test"
    mytranscjob