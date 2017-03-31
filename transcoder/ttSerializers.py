from rest_framework import serializers

class ttaskSerializer(serializers.Serializer):
    taskid=serializers.CharField(max_length=100)
    createtime=serializers.DateTimeField()
    size=serializers.CharField(max_length=50)
    src=serializers.CharField(max_length=100)
    dst=serializers.CharField(max_length=100)
    dformat=serializers.CharField(max_length=30)
    downloadURL=serializers.CharField(max_length=100)
    transnode=serializers.CharField(max_length=60)
    status=serializers.IntegerField()
    bitrate=serializers.IntegerField()
    abitrate=serializers.IntegerField()
    starttime=serializers.DateTimeField()
    endtime=serializers.DateTimeField()
    