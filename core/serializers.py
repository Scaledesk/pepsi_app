from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("emp_id", "emp_name", "c1cm", "c2cm", "c2_status", "c1_status")

class CourseOneVideoQuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOneVideoQues
        fields = ('id', 'video', 'ques_no', 'ques', 'a', 'b', 'c', 'd' )

class CourseTwoQuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTwoQues
        fields = ('id', 'ques', 'ques_no', 'a', 'b', 'c', 'd' )
        order_by = ('ques_no')

class CourseOneVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOneVideo
        fields = ('id')

class CourseOneVideoAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOneVideoQues
        fields = ('video', 'ques_no', 'correct' )

class CourseTwoAnsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTwoQues
        fields = ('id', 'ques', 'correct' )

class CheckAnsSerializer(serializers.Serializer):
    ques_no = serializers.IntegerField()
    is_correct=serializers.BooleanField(default=False)
