# from rest_framework import viewsets
from rest_framework import status
# from rest_framework.authtoken.models import Token
from core.models import *
from core.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from pprint import pprint
import json
from django.conf import settings
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def LoginRegister(request):
    """
    view to match the user to its profile if profile exist,
    if not, user profile is created and than user is matched to its user profile
    """
    emp_id = request.data['emp_id']
    emp_name = request.data['emp_name']
    data = {}
    if not UserProfile.objects.filter(emp_id=emp_id).exists():
        up = UserProfile()
        up.emp_id = emp_id
        up.emp_name = emp_name
        up.save()
    up = UserProfile.objects.get(emp_id=emp_id)
    serializer = UserProfileSerializer(up)
    return Response(data={'status': True, 'data':serializer.data}, status=status.HTTP_200_OK)

class ServeVideoView(APIView):
    """
    View to serve course video to frontend
    """
    authentication_classes = (authentication.TokenAuthentication,)
    renderer_classes = (JSONRenderer)
    permission_classes = (permissions.IsAuthenticated)
    def post(self, request, course_id, video_id):
        return Response(data={'status': True, 'data': data_dict}, status=status.HTTP_200_OK)

@api_view(['POST'])
def ServeVideo(request):
    """
    view to serve the video url on request.
    """
    cv=None
    data=request.data
    if data['course_id']=='1':
        cv=CourseOneVideo.objects.get(video_id=data['video_id'])
    elif data['course_id']=='2':
        cv=CourseTwoVideo.objects.get(video_id=1)
    video_title=cv.video_title
    video_url=cv.video_url
    return Response(data={'video_title':video_title, 'video_url':video_url}, status=status.HTTP_200_OK )

@api_view(['POST'])
def ServeQues(request):
    """
    view to serve question on request
    """
    course_id = request.data['course_id']
    if course_id == '1':
        video_id = request.data['video_id']
        covq=CourseOneVideoQues.objects.filter(video=CourseOneVideo.objects.get(video_id=video_id)).order_by('ques_no')
        serializer = CourseOneVideoQuesSerializer(covq, many=True)
        return Response(data={'data':serializer.data}, status=status.HTTP_200_OK)
    elif course_id == '2':
        ctq=CourseTwoQues.objects.all().order_by('ques_no')
        serializer = CourseTwoQuesSerializer(ctq, many=True)
        return Response(data={'data': serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
def SaveVideoStatus(request):
    """
    view to save video status for course 2.
    """
    data = request.data
    task_status = False
    up = UserProfile.objects.get(emp_id=request.data['emp_id'])
    if data['course_id'] == '2':
        if (up.c2cm < 4) and (int(data['video_id']) == up.c2cm):
            up.c2cm+=1
            up.save()
            task_status = True
        return Response(data={'status': task_status}, status=status.HTTP_200_OK)

@api_view(['POST'])
def CheckAnswers(request):
    """
    view to check the answer of modules, if found all correct, databases is updated
    """
    data=request.data
    test_clear=True
    up = UserProfile.objects.get(emp_id=request.data['emp_id'])
    course_completed = False
    total_correct = 0
    if data['course_id'] == '1':
        video_id = data['video_id']
        video = CourseOneVideo.objects.get(video_id=video_id)
        ques_list = request.data['q']
        cas_list = []
        for key in ques_list:
            cas= CheckAnsSerializer()
            cas.ques_no = key
            if CourseOneVideoQues.objects.get(video=video, ques_no=int(key)).correct == ques_list[key]:
                cas.is_correct = True
                total_correct+=1
            else:
                cas.is_correct = False
                test_clear = False
            cas_list.append(cas)
        cas_list.sort(key=lambda x: x.ques_no.lower())
        serializer=CheckAnsSerializer(cas_list, many=True)
        if test_clear:
            if video_id == settings.MAX_COURSE_ONE_VIDEO:
                up.c1_status = True
                up.save()
            else:
                if up.c1cm == int(video_id):
                    up.c1cm+=1
                    up.save()
        return Response(data={"data":serializer.data, "total_correct":total_correct, "test_clear":test_clear, "course_completed":up.c1_status},  status=status.HTTP_200_OK)

    if data['course_id'] == '2':
        ques_list = request.data['q']
        cas_list = []
        for key in ques_list:
            cas= CheckAnsSerializer()
            cas.ques_no = key
            if CourseTwoQues.objects.get(ques_no=int(key)).correct == ques_list[key]:
                cas.is_correct = True
                total_correct+=1
            else:
                cas.is_correct = False
                test_clear = False
            cas_list.append(cas)
        if test_clear:
            up.c2_status = True
            up.save()
        # cas_list.order_by('ques_no')
        cas_list.sort(key=lambda x: int(x.ques_no))
        serializer=CheckAnsSerializer(cas_list, many=True)
        return Response(data={"data":serializer.data, "total_correct":total_correct, "test_clear":test_clear,  "course_completed":up.c2_status},  status=status.HTTP_200_OK)

# @api_view(['POST'])
# def SaveCourseStatus(request):
#         up = UserProfile.objects.get(emp_id=request.data['emp_id'])
#         if request.data['course_id'] == '1':
#             if request.data['cs'] == 'true':
#                 up.c1_status = True
#                 up.save()
#                 return Response(data={'status': True}, status=status.HTTP_200_OK)
#         elif request.data['course_id'] == '2':
#             if request.data['cs'] == 'true':
#                 up.c2_status = True
#                 up.save()
#                 return Response(data={'status': True}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def SaveCurrentModule(request):
#     up = UserProfile.objects.get(emp_id=request.data['emp_id'])
#     if request.data['course_id'] == '1':
#         up.c1cm = request.data['cm']
#         up.save()
#         return Response(data={'status': True}, status=status.HTTP_200_OK)
#     elif request.data['course_id'] == '2':
#         up.c2cm = request.data['cm']
#         up.save()
#         return Response(data={'status': True}, status=status.HTTP_200_OK)
