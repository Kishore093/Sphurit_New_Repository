from .models import Message
from rest_framework import serializers
from django.utils import timezone, dateformat

class MessageSerializer(serializers.ModelSerializer):
    time_stamp = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = '__all__'

    def get_time_stamp(self, obj):
        return dateformat.format(obj.time_stamp, 'd-m-Y H:i A')