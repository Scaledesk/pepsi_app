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
def ServeUser(request):
    up = None
    if not UserProfile.objects.filter(user=request.user).exists():
        up = UserProfile()
        up.user = request.user
        up.save()
    up = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(up)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def ServeQues(request, course_id, video_id):
    if course_id == '1':
        covq=CourseOneVideoQues.objects.filter(video=CourseOneVideo.objects.get(video_id=video_id)).order_by('ques_no')
        serializer = CourseOneVideoQuesSerializer(covq, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif course_id == '2':
        ctq=CourseTwoQues.objects.all().order_by('ques_no')
        serializer = CourseTwoQuesSerializer(ctq, many=True)
        pprint(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def SaveCurrentModule(request):
#     up = UserProfile.objects.get(user=request.user)
#     if request.data['course_id'] == '1':
#         up.c1cm = request.data['c2cm']
#         up.save()
#         return Response(data={'status': True}, status=status.HTTP_200_OK)
#     elif request.data['course_id'] == '2':
#         up.c2cm == request.data['c2cm']
#         up.save()
#         return Response(data={'status': True}, status=status.HTTP_200_OK)(


# @api_view(['POST'])
# def CheckAnswers(request):
#     up = UserProfile.objects.get(user=request.user)
#     data = request.data
#     ans_list = []
#     test_clear = True
#     ans_list=None
#     if request.data['course_id'] == '1':
#         covq=CourseOneVideoQues.objects.filter(video=CourseOneVideo.objects.get(video_id=data['video_id']))
#         serializer = CourseOneVideoAnsSerializer(covq, many=True)
#         # current_video = CourseOneVideo.objects.get(video_id = data['video_id'])
#         # pprint(data['video_id'] + "_______________________________")
#         # c1vq = CourseOneVideoQues.objects.filter(video=current_video)
#         # pprint(str(c1vq) + "____________________________")
#         # pprint('_____________aaaaaaaaaaaaaaaaa____________')
#         # ans_list = CourseOneVideoAnsSerializer(c1vq, many=True)
#         # # pprint(str(clvq))
#
#         # q_list = request.data['q']
#         # obj_list = CourseOneVideoQues.objects.filter(video=current_video)
#         # pprint(ans_list)
#         # pprint(q_list)
#         # for key in q_list:
#         #
#         #
#         #     obj = CourseOneVideoQues.objects.get(video=current_video, ques_no=key)
#         #     temp_dict[key]=obj.correct
#         #     ans_list.append(dict)
#         #     if obj.correct != q_list[key]:
#         #         test_clear = False
#         #
#             # temp_dict = {}
#             # obj = CourseOneVideoQues.objects.get(video=current_video, ques_no=key)
#             # temp_dict[key]=obj.correct
#             # ans_list.append(dict)
#             # if obj.correct != q_list[key]:
#             #     test_clear = False
#         return Response({"data":serializer.data, "test_clear":"False"},  status=status.HTTP_200_OK)
#     elif request.data['course_id'] == '2':data=
#         return Response(data={'status': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
def SaveVideoStatus(request):
    data = request.data
    # course_id = data['course_id']
    # video_id = data ['video_id']
    status = False
    up = UserProfile.objects.get(user=request.user)
    if data['course_id'] == '2':
        if up.c2cm < settings.MAX_COURSE_TWO_VIDEO:
            up.c2cm+=1
            up.save()
            status = True
            pprint('_________________________________________')
            pprint(status)
            pprint(up.c2cm)
        return Response(data={'status': status}, status=status.HTTP_200_OK)

@api_view(['POST'])
def CheckAnswers(request):
    data=request.data
    test_clear=None
    up = UserProfile.objects.get(user=request.user)
    course_completed = False
    total_correct = 0
    if data['course_id'] == '1':
        video_id = data['video_id']
        video = CourseOneVideo.objects.get(video_id=video_id)
        ques_list = request.data['q']
        cas_list = []
        pprint(str(video.id))
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
        serializer=CheckAnsSerializer(cas_list, many=True)
        if test_clear:
            if video_id == settings.MAX_COURSE_ONE_VIDEO:
                up.c1_status = True
                up.save()
                course_completed = True
            else:
                up.c1cm+=1
                up.save()
        return Response({"data":serializer.data, "total_correct":total_correct, "test_clear":test_clear, "course_completed":course_completed},  status=status.HTTP_200_OK)

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
        cas_list.sort(key=lambda x: x.ques_no.lower())
        serializer=CheckAnsSerializer(cas_list, many=True)
        return Response({"data":serializer.data, "total_correct":total_correct, "test_clear":test_clear},  status=status.HTTP_200_OK)

@api_view(['POST'])
def SaveCurrentModule(request):
    up = UserProfile.objects.get(user=request.user)
    if request.data['course_id'] == '1':
        up.c1cm = request.data['cm']
        up.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)
    elif request.data['course_id'] == '2':
        up.c2cm = request.data['cm']
        up.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)

@api_view(['POST'])
def SaveCourseStatus(request):
        up = UserProfile.objects.get(user=request.user)
        if request.data['course_id'] == '1':
            if request.data['cs'] == 'true':
                up.c1_status = True
                up.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK)
        elif request.data['course_id'] == '2':
            if request.data['cs'] == 'true':
                up.c2_status = True
                up.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK)
