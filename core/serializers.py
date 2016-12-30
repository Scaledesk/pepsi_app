from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ("user", "c1cm", "c2cm", "c2_status", "c1_status")

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
    # video = CourseOneVideoSerializer()
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


# class OrderSerializer(serializers.ModelSerializer)
#     class Meta:
#         model = Order
#
# class UserSerializer(serializers.ModelSerializer)
#     orders = OrderSerializer(many = True)
#     class Meta:
#         model = user
#         fields = ('city', 'firstName', 'zip', 'taxNumber', 'lastName', 'street', 'country', 'email', 'orders')

# class LocationsSerializer(serializers.ModelSerializer):
#     country_id = serializers.Field(source='country.id')
#
#     class Meta:
#         model = Location
#         fields = (
#             'id',
#             'location',
#             'country_id',
#         )
#

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
