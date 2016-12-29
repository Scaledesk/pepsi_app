from django.contrib import admin
from core.models import *
# Register your models here.

# class PostCodesAdmin(admin.ModelAdmin):
#      exclude = ('max_videos',)

admin.site.register(UserProfile)
admin.site.register(CourseOne)
admin.site.register(CourseTwo)
admin.site.register(CourseOneVideo)
admin.site.register(CourseTwoVideo)
admin.site.register(CourseOneVideoQues)
admin.site.register(CourseTwoQues)
