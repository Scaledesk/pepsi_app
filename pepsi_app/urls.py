"""pepsi_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from core.rest_views import *
from rest_framework.authtoken import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api/', include('api.urls', namespace='api')),

    # login and logout handlers
    url(r'login/', views.obtain_auth_token),
    url(r'user/', ServeUser), #(?P<course_id>\d+)/(?P<video_id>\d+)/
    # url(r'video/(?P<course_id>\d+)/(?P<video_id>\d+)/', ServeVideoView.as_view()),

    url(r'video/', ServeVideo), #(?P<course_id>\d+)/(?P<video_id>\d+)/
    # url(r'login/user/', LoginView.as_view({'post': 'login_user'})),
    # url(r'logout/', LogoutView.as_view({'post': 'logout_user'})),
    # url(r'^logout/', LogoutView.as_view()),
    # url(r'^logout/', Logout),
    url(r'question/(?P<course_id>\d+)/(?P<video_id>\d+)/', ServeQues), #(?P<course_id>\d+)/(?P<video_id>\d+)/
    url(r'current-module/', SaveCurrentModule),
    url(r'course-status/', SaveCourseStatus),
    url(r'check-answers/', CheckAnswers),
    url(r'save-video-status/', SaveVideoStatus),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
