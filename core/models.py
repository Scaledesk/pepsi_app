from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.validators import URLValidator

# from rest_framework.views import APIView
# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class BaseModel(models.Model):
    """Base clasForegnKeyForegnKeys for all the models"""
    def serialize_data(self):
        #get the serializable keys
        current_instance_name= self.__class__.__name__
        serializable_keys=SERIALIZABLE_VALUE.get(current_instance_name)
        serialized_data={}
        for i in serializable_keys:
            #get the valjue from the class
            #handle dates specifically
            current_value=getattr(self,i)
            if isinstance(current_value, datetime.datetime):
                current_value=str(current_value)
            serialized_data[i] = current_value
            # serialized_data.update({i:current_value}) .update is very slow to execute
        return serialized_data
    class Meta:
        abstract=True

class UserProfile(BaseModel):
    """ BaseModel to save user data """
    # user = models.ForeignKey(User)
    emp_id = models.CharField(max_length = 20, unique=True)
    emp_name = models.CharField(max_length = 30)
    c1cm = models.IntegerField(default=1)
    c2cm = models.IntegerField(default=1)
    # c1cq = models.IntegerField(default=0)
    # c2cq = models.IntegerField(default=0)
    c2_status = models.BooleanField(default=False)
    c1_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    def __unicode__(self):
        return self.emp_id

class CourseOneVideo(BaseModel):
    """model to save video urls for course 1 videos"""
    video_id = models.IntegerField(unique=True)
    video_title = models.CharField(max_length=100)
    # video_file = models.FileField(upload_to='course_one_video/', max_length=200)
    video_url = models.TextField(validators=[URLValidator()])

    class Meta:
        verbose_name = "Course One Video"
        verbose_name_plural = "Course one Videos"
    def __unicode__(self):
        return str(self.video_id)

class CourseTwoVideo(BaseModel):
    """model to save url for course 2 videos"""
    video_id = models.IntegerField(unique=True)
    video_title = models.CharField(max_length=100)
    # video_file = models.FileField(upload_to='course_one_video/', max_length=200)
    video_url = models.TextField(validators=[URLValidator()])

    class Meta:
        verbose_name = "Course Two Video"
        verbose_name_plural = "Course Two Videos"
    def __unicode__(self):
        return str(self.video_id)

class CourseOneVideoQues(BaseModel):
    """model to save question for course 1 modules"""
    OPTION_CHOICES=(('a','A'),
                    ('b','B'),
                    ('c','C'),
                    ('d','D'))
    video=models.ForeignKey(CourseOneVideo, on_delete=models.CASCADE)
    ques_no = models.IntegerField()
    ques = models.CharField(max_length=200)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    correct = models.CharField(max_length=1, choices=OPTION_CHOICES)
    class Meta:
        verbose_name = "Course One Video Question"
        verbose_name_plural = "Course One Video Questions"
        unique_together = ('video', 'ques_no',)
    def __unicode__(self):
        return ("Course-1 Video-" + str(self.video.video_id) + " Question No-" + str(self.ques_no))

class CourseTwoQues(BaseModel):
    """model to save question for course 2 models"""
    OPTION_CHOICES=(('a','A'),
                    ('b','B'),
                    ('c','C'),
                    ('d','D'))
    ques_no = models.IntegerField(unique=True)
    ques = models.CharField(max_length=200)
    a = models.CharField(max_length=100)
    b = models.CharField(max_length=100)
    c = models.CharField(max_length=100)
    d = models.CharField(max_length=100)
    correct = models.CharField(max_length=1, choices=OPTION_CHOICES)

    class Meta:
        verbose_name = "Course Two Question"
        verbose_name_plural = "Course Two Questions"
    def __unicode__(self):
        return ("Course-2 Question No-" + str(self.ques_no))
