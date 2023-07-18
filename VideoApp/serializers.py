from rest_framework import serializers

class EnterTextAndDurationSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    video_duration_seconds = serializers.IntegerField()






    