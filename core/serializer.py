from rest_framework import serializers
from core.models import*


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('updated_at',)

class CourseQuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseQuery
        fields = '__all__'

class UserQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseQuery
        fields = '__all__'
        depth = 1

