from rest_framework import serializers

class mtaskSerializer(serializers.Serializer):
    taskid=serializers.CharField(max_length=100)
    createtime=serializers.DateTimeField()    
    src1=serializers.CharField(max_length=100)
    src2=serializers.CharField(max_length=100)
    dst=serializers.CharField(max_length=100)   
    status=serializers.IntegerField()
   
    